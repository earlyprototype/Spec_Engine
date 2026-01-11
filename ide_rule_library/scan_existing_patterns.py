#!/usr/bin/env python3
"""
Scan existing Pattern repositories for IDE rule files.
Optimized with tree API, progress tracking, and proper error handling.
"""

import os
import sys
import yaml
import fnmatch
from github import Github, GithubException, UnknownObjectException
from neo4j import GraphDatabase
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from collections import defaultdict
from pathlib import Path

from ide_rule_library.logger import StructuredLogger
from rate_limiter import GitHubRateLimiter
from progress_tracker import ProgressTracker
from rule_extractor import RuleExtractor
from neo4j_writer import Neo4jRuleWriter


class ExistingPatternScanner:
    """Scan Pattern nodes for IDE rule files via GitHub API (optimized)"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize scanner with config, logging, and connections"""
        
        # Load environment variables with override (pattern_extractor pattern)
        load_dotenv(override=True)
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize logger
        self.logger = StructuredLogger('scanner', self.config['logging'])
        self.logger.info("Initializing IDE Rule Library Scanner")
        
        # Connect to Neo4j (using pattern_extractor.py's working pattern)
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        )
        self.logger.info("Connected to Neo4j")
        
        # Connect to GitHub
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            self.logger.warning("GITHUB_TOKEN not found - rate limits will be restricted (60/hour vs 5000/hour)")
            print("\nWARNING: No GitHub token found!")
            print("Set GITHUB_TOKEN in .env for 5000 requests/hour (vs 60/hour)")
            print("Get token at: https://github.com/settings/tokens\n")
        
        self.gh = Github(github_token) if github_token else Github()
        
        # Initialize rate limiter
        self.rate_limiter = GitHubRateLimiter(
            self.gh, 
            self.config['github'],
            self.logger
        )
        self.logger.info(f"GitHub API initialized ({self.rate_limiter.get_remaining_calls()} calls remaining)")
        
        # Initialize progress tracker
        self.progress_tracker = ProgressTracker()
        
        # Initialize extractor (lazy - only if extraction enabled)
        self.extractor = None
        
        # Initialize Neo4j writer (lazy - only if extraction enabled)
        self.writer = None
    
    def get_all_patterns(self) -> List[Dict]:
        """Get all Pattern nodes from Neo4j"""
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                RETURN p.name AS pattern_name,
                       p.source_repo AS repo_url,
                       p.stars AS stars,
                       p.confidence AS confidence
                ORDER BY p.stars DESC
            """)
            return [dict(record) for record in result]
    
    def _parse_repo_url(self, repo_url: str) -> Tuple[str, str]:
        """Parse GitHub repo URL into owner/repo"""
        repo_url = repo_url.replace('https://github.com/', '')
        repo_url = repo_url.replace('http://github.com/', '')
        repo_url = repo_url.rstrip('/')
        
        parts = repo_url.split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
        return None, None
    
    def _match_pattern(self, file_paths: set, pattern: str) -> List[str]:
        """Match file pattern against set of paths"""
        matches = []
        
        # Handle wildcard patterns
        if '*' in pattern:
            for path in file_paths:
                if fnmatch.fnmatch(path, pattern):
                    matches.append(path)
        # Handle directory patterns
        elif pattern.endswith('/'):
            for path in file_paths:
                if path.startswith(pattern):
                    matches.append(path)
        # Exact match
        elif pattern in file_paths:
            matches.append(pattern)
        
        return matches
    
    def check_repo_for_rules(self, repo_url: str) -> Dict:
        """Check repo for rule files using tree API (1 API call vs 20+)"""
        owner, repo_name = self._parse_repo_url(repo_url)
        
        if not owner or not repo_name:
            return {'found': [], 'error': 'Invalid repo URL'}
        
        try:
            # Get repo with rate limiting
            repo = self.rate_limiter.call_with_retry(
                self.gh.get_repo, f"{owner}/{repo_name}"
            )
            
            # Get entire tree in ONE API call
            default_branch = repo.default_branch
            tree = self.rate_limiter.call_with_retry(
                repo.get_git_tree, default_branch, recursive=True
            )
            
            # Build set of all file paths
            file_paths = {item.path for item in tree.tree if item.type == 'blob'}
            
            # Check all priority patterns against cached tree
            found_files = []
            
            for priority_num, priority_key in [(1, 'priority_1_files'), 
                                                 (2, 'priority_2_files'), 
                                                 (3, 'priority_3_files')]:
                for file_pattern in self.config.get(priority_key, []):
                    matches = self._match_pattern(file_paths, file_pattern)
                    for match in matches:
                        found_files.append({
                            'path': match,
                            'priority': priority_num,
                            'type': 'file'
                        })
            
            return {
                'found': found_files,
                'total_files': len(found_files),
                'error': None
            }
            
        except UnknownObjectException:
            return {'found': [], 'error': 'Repository not found or private'}
            
        except GithubException as e:
            if e.status == 404:
                return {'found': [], 'error': 'Repository not found or private'}
            elif e.status == 403:
                if 'rate limit' in str(e).lower():
                    return {'found': [], 'error': 'API rate limit exceeded'}
                else:
                    return {'found': [], 'error': 'Access forbidden'}
            elif e.status == 451:
                return {'found': [], 'error': 'Repository unavailable (DMCA)'}
            else:
                return {'found': [], 'error': f'GitHub API error: {e.status}'}
                
        except Exception as e:
            self.logger.error(f"Unexpected error checking {repo_url}: {e}", exc_info=True)
            return {'found': [], 'error': str(e)}
    
    def scan_all_patterns(self, dry_run: bool = True, max_repos: int = None) -> Dict:
        """Scan all patterns for IDE rule files"""
        
        print("\n" + "="*80)
        print("IDE RULE FILE SCANNER")
        print("="*80)
        
        # Get all patterns
        patterns = self.get_all_patterns()
        total = len(patterns)
        
        if max_repos:
            patterns = patterns[:max_repos]
            print(f"Scanning first {max_repos} of {total} patterns...")
        else:
            print(f"Scanning all {total} patterns...")
        
        if dry_run:
            print("DRY RUN MODE - Reporting findings only, no extraction")
        else:
            print("EXTRACTION MODE - Will extract and store rule files")
        
        print(f"\nGitHub API calls available: {self.rate_limiter.get_remaining_calls()}")
        print("="*80 + "\n")
        
        # Track results
        results = {
            'total_scanned': 0,
            'repos_with_rules': 0,
            'total_rule_files': 0,
            'by_format': defaultdict(int),
            'by_priority': defaultdict(int),
            'repos_with_errors': 0,
            'repos_found': []
        }
        
        # Scan each pattern
        for i, pattern in enumerate(patterns, 1):
            repo_url = pattern['repo_url']
            
            # Skip if already processed (from checkpoint)
            if self.progress_tracker.is_processed(repo_url):
                self.logger.info(f"Skipping {repo_url} (already processed)")
                results['total_scanned'] += 1
                continue
            
            print(f"[{i}/{len(patterns)}] {pattern['pattern_name']}")
            print(f"  Repo: {repo_url}")
            print(f"  Stars: {pattern['stars']:,}")
            
            # Check for rules
            check_result = self.check_repo_for_rules(repo_url)
            results['total_scanned'] += 1
            
            if check_result.get('error'):
                print(f"  [ERROR] {check_result['error']}")
                results['repos_with_errors'] += 1
                self.progress_tracker.mark_processed(repo_url, success=False, error=check_result['error'])
                
            elif check_result['found']:
                print(f"  [OK] Found {len(check_result['found'])} rule file(s):")
                for rule_file in check_result['found']:
                    print(f"    - {rule_file['path']} (P{rule_file['priority']})")
                    
                    # Track stats
                    file_name = rule_file['path'].split('/')[-1]
                    results['by_format'][file_name] += 1
                    results['by_priority'][f"priority_{rule_file['priority']}"] += 1
                
                results['repos_with_rules'] += 1
                results['total_rule_files'] += len(check_result['found'])
                results['repos_found'].append({
                    'pattern': pattern,
                    'rules': check_result['found']
                })
                
                self.progress_tracker.mark_processed(repo_url, success=True)
                
                # Extract rules if not dry run
                if not dry_run:
                    self._extract_rules(pattern, check_result['found'])
            else:
                print(f"  - No rule files found")
                self.progress_tracker.mark_processed(repo_url, success=True)
            
            print()
            
            # Rate limit check every 50 repos
            if (i % 50) == 0:
                remaining = self.rate_limiter.get_remaining_calls()
                print(f"--- Rate limit check: {remaining} calls remaining ---\n")
                if remaining < 100:
                    self.logger.warning("Approaching rate limit")
                    print("WARNING: Approaching rate limit. Consider pausing.\n")
        
        # Save final checkpoint
        self.progress_tracker.save_checkpoint()
        
        # Print summary
        self._print_summary(results, dry_run)
        
        return results
    
    def _extract_rules(self, pattern: Dict, rule_files: List[Dict]):
        """Extract rule files using RuleExtractor and Neo4jWriter"""
        
        # Initialize extractor and writer if not already done
        if not self.extractor:
            try:
                self.extractor = RuleExtractor(
                    self.gh,
                    self.config,
                    self.logger,
                    self.rate_limiter
                )
                self.logger.info("RuleExtractor initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize RuleExtractor: {e}")
                return
        
        if not self.writer:
            self.writer = Neo4jRuleWriter(
                self.neo4j,
                self.config,
                self.logger
            )
            self.logger.info("Neo4jWriter initialized")
        
        # Extract each rule file
        for rule_file in rule_files:
            file_path = rule_file['path']
            
            # Check if already processed
            if self.progress_tracker.is_processed(pattern['repo_url'], file_path):
                self.logger.info(f"Skipping {file_path} (already processed)")
                continue
            
            self.logger.info(f"Extracting {file_path} from {pattern['pattern_name']}")
            
            # Extract with Gemini
            result = self.extractor.extract_rule_file(
                pattern['repo_url'],
                file_path,
                pattern['stars']
            )
            
            if result['success']:
                # Write to Neo4j
                written = self.writer.write_rule(
                    result['data'],
                    pattern_name=pattern['pattern_name']
                )
                
                if written:
                    self.logger.info(f"Successfully stored {file_path}")
                    self.progress_tracker.mark_processed(
                        pattern['repo_url'],
                        file_path,
                        success=True
                    )
                else:
                    self.logger.info(f"Skipped {file_path} (duplicate)")
                    self.progress_tracker.mark_skipped(
                        pattern['repo_url'],
                        file_path
                    )
            else:
                self.logger.error(f"Failed to extract {file_path}: {result.get('error')}")
                self.progress_tracker.mark_processed(
                    pattern['repo_url'],
                    file_path,
                    success=False,
                    error=result.get('error')
                )
    
    def _print_summary(self, results: Dict, dry_run: bool):
        """Print scan summary"""
        print("\n" + "="*80)
        print("SCAN SUMMARY")
        print("="*80)
        print(f"Total patterns scanned:     {results['total_scanned']}")
        print(f"Repos with IDE rule files:  {results['repos_with_rules']}")
        
        if results['total_scanned'] > 0:
            success_rate = (results['repos_with_rules']/results['total_scanned']*100)
            print(f"Success rate:               {success_rate:.1f}%")
        
        print(f"Total rule files found:     {results['total_rule_files']}")
        print(f"Repos with errors:          {results['repos_with_errors']}")
        
        if results['by_priority']:
            print(f"\nBy Priority:")
            for priority in sorted(results['by_priority'].keys()):
                print(f"  {priority}: {results['by_priority'][priority]} files")
        
        if results['by_format']:
            print(f"\nMost Common Formats:")
            sorted_formats = sorted(results['by_format'].items(), key=lambda x: x[1], reverse=True)
            for format_name, count in sorted_formats[:10]:
                print(f"  {format_name}: {count} repos")
        
        if results['repos_found']:
            print(f"\n--- Sample Repos with Rules (first 5) ---")
            for item in results['repos_found'][:5]:
                pattern = item['pattern']
                rules = item['rules']
                print(f"\n{pattern['pattern_name']} ({pattern['stars']:,} stars)")
                for rule in rules:
                    print(f"  - {rule['path']}")
        
        print("\n" + "="*80)
        
        if dry_run:
            print("\nDRY RUN COMPLETE")
            print("\nTo extract IDE rules, run:")
            print("  python scan_existing_patterns.py --extract")
            print("\nOr to extract from specific repos:")
            print("  python scan_existing_patterns.py --extract --max 50")
        else:
            print("\nEXTRACTION COMPLETE")
            print(f"Processed {results['total_rule_files']} rule files from {results['repos_with_rules']} repositories")
        
        print("="*80 + "\n")
    
    def close(self):
        """Close connections"""
        self.neo4j.close()
        self.logger.info("Scanner closed")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scan Pattern repositories for IDE rule files')
    parser.add_argument('--extract', action='store_true', help='Extract rules (default is dry run)')
    parser.add_argument('--max', type=int, help='Maximum number of repos to scan')
    parser.add_argument('--clear-checkpoint', action='store_true', help='Clear progress checkpoint and start fresh')
    
    args = parser.parse_args()
    
    scanner = ExistingPatternScanner()
    
    try:
        # Clear checkpoint if requested
        if args.clear_checkpoint:
            scanner.progress_tracker.clear_checkpoint()
            print("Checkpoint cleared - starting fresh\n")
        
        # Run scan
        results = scanner.scan_all_patterns(
            dry_run=not args.extract,
            max_repos=args.max
        )
        
        # Save results to JSON
        import json
        output_file = 'scan_results.json'
        with open(output_file, 'w') as f:
            json_results = {
                'total_scanned': results['total_scanned'],
                'repos_with_rules': results['repos_with_rules'],
                'total_rule_files': results['total_rule_files'],
                'by_format': dict(results['by_format']),
                'by_priority': dict(results['by_priority']),
                'repos_with_errors': results['repos_with_errors'],
                'repos_found': [
                    {
                        'pattern_name': r['pattern']['pattern_name'],
                        'repo_url': r['pattern']['repo_url'],
                        'stars': r['pattern']['stars'],
                        'rules': r['rules']
                    }
                    for r in results['repos_found']
                ]
            }
            json.dump(json_results, f, indent=2)
        
        print(f"Results saved to {output_file}")
        
    finally:
        scanner.close()


if __name__ == '__main__':
    main()
