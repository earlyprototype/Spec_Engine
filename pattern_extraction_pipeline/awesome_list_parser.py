#!/usr/bin/env python3
"""
Awesome List Parser - Extract GitHub repos from awesome lists

This script parses awesome lists (like awesome-nlp) to extract high-quality
GitHub repository URLs, which can then be fed to the pattern extraction pipeline.

Usage:
    python awesome_list_parser.py --list keon/awesome-nlp --min-stars 1000
    python awesome_list_parser.py --list awesome-python --output repos.txt
"""

import re
import os
import argparse
import json
from typing import List, Dict, Set
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
from github import Github

load_dotenv()


class AwesomeListParser:
    """Parse GitHub URLs from awesome lists"""
    
    def __init__(self):
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in .env file")
        
        self.github = Github(github_token)
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        })
    
    def fetch_readme(self, repo_full_name: str) -> str:
        """
        Fetch README content from a GitHub repository
        
        Args:
            repo_full_name: Repository in format "owner/repo"
        
        Returns:
            README content as string
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            readme = repo.get_readme()
            content = readme.decoded_content.decode('utf-8')
            print(f"[OK] Fetched README from {repo_full_name}")
            return content
        except Exception as e:
            print(f"[ERROR] Failed to fetch README from {repo_full_name}: {e}")
            return ""
    
    def extract_github_urls(self, markdown_content: str) -> Set[str]:
        """
        Extract GitHub repository URLs from markdown content
        
        Args:
            markdown_content: Markdown text containing GitHub URLs
        
        Returns:
            Set of unique GitHub repository URLs (owner/repo format)
        """
        # Pattern to match GitHub URLs in various formats
        patterns = [
            r'https?://github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)',  # Full URLs
            r'\[.*?\]\(https?://github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)\)',  # Markdown links
        ]
        
        repos = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, markdown_content)
            for match in matches:
                # Clean up the repo name
                repo = match.strip('/')
                
                # Remove URL fragments and query parameters
                repo = repo.split('#')[0].split('?')[0]
                
                # Skip non-repo URLs (like /issues, /pulls, /blob)
                if any(x in repo for x in ['/issues', '/pulls', '/blob', '/tree', '/wiki', '/releases']):
                    continue
                
                # Ensure it's a valid owner/repo format
                parts = repo.split('/')
                if len(parts) == 2 and parts[0] and parts[1]:
                    repos.add(repo)
        
        return repos
    
    def get_repo_metadata(self, repo_full_name: str) -> Dict:
        """
        Fetch metadata for a GitHub repository
        
        Args:
            repo_full_name: Repository in format "owner/repo"
        
        Returns:
            Dictionary with repo metadata
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            
            metadata = {
                'full_name': repo.full_name,
                'name': repo.name,
                'owner': repo.owner.login,
                'html_url': repo.html_url,
                'description': repo.description or '',
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'language': repo.language or 'Unknown',
                'topics': repo.get_topics(),
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat(),
                'archived': repo.archived,
                'fork': repo.fork
            }
            
            return metadata
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch metadata for {repo_full_name}: {e}")
            return None
    
    def filter_repos(
        self,
        repos: List[Dict],
        min_stars: int = 0,
        max_stars: int = None,
        languages: List[str] = None,
        exclude_forks: bool = True,
        exclude_archived: bool = True,
        required_topics: List[str] = None
    ) -> List[Dict]:
        """
        Filter repositories based on criteria
        
        Args:
            repos: List of repository metadata dictionaries
            min_stars: Minimum star count
            max_stars: Maximum star count (None = no limit)
            languages: List of allowed languages (None = all)
            exclude_forks: Exclude forked repositories
            exclude_archived: Exclude archived repositories
            required_topics: List of required topics (None = no requirement)
        
        Returns:
            Filtered list of repositories
        """
        filtered = []
        
        for repo in repos:
            # Skip if metadata fetch failed
            if not repo:
                continue
            
            # Star count filter
            if repo['stars'] < min_stars:
                continue
            
            if max_stars and repo['stars'] > max_stars:
                continue
            
            # Fork filter
            if exclude_forks and repo['fork']:
                continue
            
            # Archived filter
            if exclude_archived and repo['archived']:
                continue
            
            # Language filter
            if languages and repo['language'] not in languages:
                continue
            
            # Topics filter
            if required_topics:
                repo_topics = set(repo['topics'])
                if not any(topic in repo_topics for topic in required_topics):
                    continue
            
            filtered.append(repo)
        
        return filtered
    
    def parse_awesome_list(
        self,
        awesome_list_repo: str,
        min_stars: int = 0,
        output_format: str = 'json'
    ) -> List[Dict]:
        """
        Parse an awesome list and extract high-quality repositories
        
        Args:
            awesome_list_repo: Awesome list repository (e.g., "keon/awesome-nlp")
            min_stars: Minimum stars for included repos
            output_format: 'json' or 'urls'
        
        Returns:
            List of repository metadata or URLs
        """
        print(f"\n[START] Parsing awesome list: {awesome_list_repo}")
        print(f"[CONFIG] Min stars: {min_stars}")
        
        # Fetch README
        readme_content = self.fetch_readme(awesome_list_repo)
        if not readme_content:
            return []
        
        # Extract GitHub URLs
        repo_urls = self.extract_github_urls(readme_content)
        print(f"[FOUND] {len(repo_urls)} unique GitHub repositories")
        
        # Fetch metadata for each repo
        repos_with_metadata = []
        print(f"\n[FETCHING] Repository metadata...")
        
        for i, repo_url in enumerate(repo_urls, 1):
            print(f"  [{i}/{len(repo_urls)}] Fetching {repo_url}...", end=' ')
            metadata = self.get_repo_metadata(repo_url)
            
            if metadata:
                print(f"({metadata['stars']} stars)")
                repos_with_metadata.append(metadata)
            else:
                print("(failed)")
        
        # Filter repos
        filtered_repos = self.filter_repos(
            repos_with_metadata,
            min_stars=min_stars,
            exclude_forks=True,
            exclude_archived=True
        )
        
        print(f"\n[FILTERED] {len(filtered_repos)} repositories meet criteria")
        
        # Sort by stars
        filtered_repos.sort(key=lambda x: x['stars'], reverse=True)
        
        return filtered_repos


def main():
    parser = argparse.ArgumentParser(
        description='Extract GitHub repositories from awesome lists'
    )
    
    parser.add_argument(
        '--list',
        required=True,
        help='Awesome list repository (e.g., keon/awesome-nlp)'
    )
    
    parser.add_argument(
        '--min-stars',
        type=int,
        default=100,
        help='Minimum star count (default: 100)'
    )
    
    parser.add_argument(
        '--max-stars',
        type=int,
        default=None,
        help='Maximum star count (default: unlimited)'
    )
    
    parser.add_argument(
        '--output',
        default='awesome_repos.json',
        help='Output file path (default: awesome_repos.json)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'urls', 'domains'],
        default='json',
        help='Output format: json (full metadata), urls (list of URLs), domains (for pattern extractor)'
    )
    
    args = parser.parse_args()
    
    # Parse awesome list
    parser_instance = AwesomeListParser()
    repos = parser_instance.parse_awesome_list(
        awesome_list_repo=args.list,
        min_stars=args.min_stars
    )
    
    # Generate output based on format
    if args.format == 'json':
        output_data = repos
    elif args.format == 'urls':
        output_data = [repo['html_url'] for repo in repos]
    elif args.format == 'domains':
        # Format for pattern extractor: query string per repo
        output_data = [
            f"repo:{repo['owner']}/{repo['name']}"
            for repo in repos
        ]
    
    # Save output
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.format == 'json':
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        else:
            f.write('\n'.join(output_data))
    
    print(f"\n[SAVED] Output written to {args.output}")
    
    # Print summary
    print(f"\n[SUMMARY]")
    print(f"  Total repos extracted: {len(repos)}")
    if repos:
        print(f"  Star range: {repos[-1]['stars']} - {repos[0]['stars']}")
        print(f"  Top 5 repos:")
        for repo in repos[:5]:
            print(f"    - {repo['full_name']}: {repo['stars']} stars ({repo['language']})")


if __name__ == '__main__':
    main()
