# issue_miner.py
# Mine GitHub Issues for troubleshooting knowledge and anti-pattern detection
# Part of Issue Mining Extension (see ISSUE_MINING_EXTENSION.md)

import os
import json
from github import Github
import google.generativeai as genai
from neo4j import GraphDatabase

class IssueMiner:
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        
        # Configure Google Gemini with direct API key (disable Cloud SDK auth)
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Unset Google Cloud auth env vars to force API key usage
        for var in ['GOOGLE_APPLICATION_CREDENTIALS', 'GCLOUD_PROJECT']:
            os.environ.pop(var, None)
        
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel('gemini-2.5-flash')
        
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), 
                  os.getenv("NEO4J_PASSWORD", "password"))
        )
    
    def mine_issues(self, repo_name, pattern_name, limit=50):
        """
        Mine issues for a specific repository and pattern.
        
        Args:
            repo_name: Full repo name (e.g., "microsoft/vscode")
            pattern_name: Pattern to validate (e.g., "filesystem_browser")
            limit: Max issues to analyze (default: 50)
        
        Returns:
            Dict with issues, solutions, anti-patterns, validations
        """
        print(f"\nMining issues for: {repo_name}")
        print(f"Pattern: {pattern_name}")
        print(f"Limit: {limit}")
        
        try:
            repo = self.github.get_repo(repo_name)
        except Exception as e:
            print(f"Error fetching repo: {e}")
            return {'anti_patterns': [], 'solutions': [], 'validations': []}
        
        # Get closed issues (they have resolutions)
        print(f"\nFetching closed issues...")
        issues = repo.get_issues(
            state='closed',
            labels=['bug', 'architecture', 'design']
        )
        
        results = {
            'anti_patterns': [],
            'solutions': [],
            'validations': [],
            'irrelevant': 0
        }
        
        count = 0
        for issue in issues:
            if count >= limit:
                break
            
            count += 1
            print(f"[{count}/{limit}] Analyzing issue #{issue.number}...")
            
            try:
                # Analyze with LLM
                analysis = self._analyze_issue(
                    issue=issue,
                    pattern_name=pattern_name,
                    repo_name=repo_name
                )
                
                if analysis:
                    # Categorize
                    if analysis['type'] == 'anti_pattern':
                        results['anti_patterns'].append(analysis)
                        print(f"  → Anti-pattern detected: {analysis['problem']}")
                    elif analysis['type'] == 'solution':
                        results['solutions'].append(analysis)
                        print(f"  → Solution found: {analysis['solution'][:50]}...")
                    elif analysis['type'] == 'validation':
                        results['validations'].append(analysis)
                        print(f"  → Pattern validation")
                    
                    # Store in graph
                    self._store_issue(analysis)
                else:
                    results['irrelevant'] += 1
                    print(f"  → Irrelevant to architecture")
                    
            except Exception as e:
                print(f"  → Error: {e}")
                continue
        
        # Summary
        print(f"\n=== Mining Complete ===")
        print(f"Analyzed: {count} issues")
        print(f"Anti-patterns: {len(results['anti_patterns'])}")
        print(f"Solutions: {len(results['solutions'])}")
        print(f"Validations: {len(results['validations'])}")
        print(f"Irrelevant: {results['irrelevant']}")
        print(f"Cost: ~${count * 0.01:.2f}")
        
        return results
    
    def _analyze_issue(self, issue, pattern_name, repo_name):
        """Use LLM to analyze issue."""
        
        # Get issue content
        title = issue.title
        body = issue.body[:2000] if issue.body else "No description"
        
        # Get first 5 comments
        try:
            comments = [c.body[:500] for c in list(issue.get_comments())[:5]]
        except:
            comments = []
        
        labels = [l.name for l in issue.labels]
        
        # LLM analysis
        prompt = f"""
Analyze this GitHub issue in context of architectural pattern.

Repository: {repo_name}
Pattern: {pattern_name}

Issue #{issue.number}: {title}
Labels: {labels}

Body:
{body}

Comments:
{' '.join(comments) if comments else 'No comments'}

Determine:
1. Does this indicate an anti-pattern? (pattern that fails in specific context)
2. Does this provide a solution to an architectural problem?
3. Does this validate or discuss the pattern architecture?

Extract in JSON format:
{{
    "type": "anti_pattern" | "solution" | "validation" | "irrelevant",
    "pattern_affected": "{pattern_name}",
    "problem": "Brief description of problem (if applicable)",
    "solution": "Brief description of solution (if applicable)",
    "why_fails": "Why pattern fails in this context (if anti-pattern)",
    "recommended_instead": "Better pattern recommendation (if applicable)",
    "confidence": "high" | "medium" | "low",
    "severity": "high" | "medium" | "low" (if anti-pattern),
    "reasoning": "Brief explanation of classification"
}}

If irrelevant to architecture/pattern, return {{"type": "irrelevant"}}.
Be conservative - only classify as anti-pattern if clear evidence of pattern failure.
"""
        
        try:
            # Use Gemini to generate response
            response = self.llm.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to extract JSON (Gemini might wrap it in markdown code blocks)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(response_text)
            
            if analysis.get('type') == 'irrelevant':
                return None
            
            # Add metadata
            analysis['issue_id'] = f"{repo_name}/issues/{issue.number}"
            analysis['issue_url'] = issue.html_url
            analysis['issue_title'] = title
            analysis['created'] = str(issue.created_at)
            analysis['closed'] = str(issue.closed_at) if issue.closed_at else None
            analysis['repo'] = repo_name
            
            return analysis
            
        except Exception as e:
            print(f"    LLM analysis error: {e}")
            return None
    
    def _store_issue(self, analysis):
        """Store issue analysis in Neo4j."""
        
        try:
            with self.neo4j.session() as session:
                if analysis['type'] == 'anti_pattern':
                    # Create or update anti-pattern
                    session.run("""
                        MERGE (ap:AntiPattern {name: $name})
                        ON CREATE SET
                            ap.why_fails = $why_fails,
                            ap.severity = $severity,
                            ap.frequency = 1,
                            ap.evidence = [$issue_url],
                            ap.alternative = $alternative
                        ON MATCH SET
                            ap.frequency = ap.frequency + 1,
                            ap.evidence = CASE 
                                WHEN NOT $issue_url IN ap.evidence 
                                THEN ap.evidence + $issue_url 
                                ELSE ap.evidence 
                            END
                        
                        // Link to pattern it affects
                        WITH ap
                        MATCH (p:Pattern {name: $pattern})
                        MERGE (p)-[:HAS_ANTI_PATTERN]->(ap)
                        
                        // Create issue node
                        CREATE (i:Issue {
                            id: $issue_id,
                            title: $title,
                            url: $issue_url,
                            repo: $repo,
                            type: 'anti_pattern',
                            problem: $problem,
                            severity: $severity,
                            reasoning: $reasoning
                        })
                        
                        CREATE (i)-[:INDICATES]->(ap)
                    """,
                        name=analysis['pattern_affected'] + "_anti",
                        why_fails=analysis.get('why_fails', 'Unknown'),
                        severity=analysis.get('severity', 'medium'),
                        issue_url=analysis['issue_url'],
                        pattern=analysis['pattern_affected'],
                        issue_id=analysis['issue_id'],
                        title=analysis['issue_title'],
                        problem=analysis.get('problem', ''),
                        repo=analysis['repo'],
                        reasoning=analysis.get('reasoning', ''),
                        alternative=analysis.get('recommended_instead', '')
                    )
                
                elif analysis['type'] == 'solution':
                    # Create solution node
                    session.run("""
                        CREATE (s:Solution {
                            id: $issue_id + '_solution',
                            approach: $solution,
                            problem: $problem,
                            source: $issue_url,
                            repo: $repo,
                            confidence: $confidence,
                            reasoning: $reasoning
                        })
                        
                        // Link to pattern
                        WITH s
                        MATCH (p:Pattern {name: $pattern})
                        MERGE (s)-[:SOLVES_ISSUE_WITH]->(p)
                        
                        // Create issue node
                        CREATE (i:Issue {
                            id: $issue_id,
                            title: $title,
                            url: $issue_url,
                            repo: $repo,
                            type: 'solution',
                            problem: $problem
                        })
                        
                        CREATE (i)-[:SOLVED_BY]->(s)
                    """,
                        issue_id=analysis['issue_id'],
                        solution=analysis.get('solution', ''),
                        problem=analysis.get('problem', ''),
                        issue_url=analysis['issue_url'],
                        repo=analysis['repo'],
                        confidence=analysis.get('confidence', 'medium'),
                        reasoning=analysis.get('reasoning', ''),
                        pattern=analysis.get('recommended_instead', analysis['pattern_affected']),
                        title=analysis['issue_title']
                    )
                
                elif analysis['type'] == 'validation':
                    # Create validation link
                    session.run("""
                        CREATE (i:Issue {
                            id: $issue_id,
                            title: $title,
                            url: $issue_url,
                            repo: $repo,
                            type: 'validation',
                            reasoning: $reasoning
                        })
                        
                        // Link to pattern
                        WITH i
                        MATCH (p:Pattern {name: $pattern})
                        MERGE (i)-[:VALIDATES]->(p)
                    """,
                        issue_id=analysis['issue_id'],
                        title=analysis['issue_title'],
                        issue_url=analysis['issue_url'],
                        repo=analysis['repo'],
                        reasoning=analysis.get('reasoning', ''),
                        pattern=analysis['pattern_affected']
                    )
                    
        except Exception as e:
            print(f"    Graph storage error: {e}")

    def mine_for_low_confidence_patterns(self, confidence_threshold=0.7):
        """
        Mine issues for all low-confidence patterns to validate them.
        
        Args:
            confidence_threshold: Patterns below this are considered low confidence
        
        Returns:
            Summary of validation results
        """
        print(f"\n=== Mining Issues for Low-Confidence Patterns ===")
        print(f"Threshold: <{confidence_threshold}")
        
        # Get low-confidence patterns from graph
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.confidence = 'low' 
                   OR (p.confidence = 'medium' AND rand() < 0.3)
                RETURN p.name AS pattern_name, 
                       p.source_repo AS repo,
                       p.confidence AS confidence
                LIMIT 20
            """)
            
            patterns = [dict(r) for r in result]
        
        print(f"Found {len(patterns)} patterns to validate\n")
        
        results = []
        for i, p in enumerate(patterns, 1):
            print(f"\n[{i}/{len(patterns)}] Pattern: {p['pattern_name']}")
            print(f"  Current confidence: {p['confidence']}")
            print(f"  Source: {p['repo']}")
            
            # Mine issues
            mining_result = self.mine_issues(
                repo_name=p['repo'],
                pattern_name=p['pattern_name'],
                limit=20  # Smaller limit for validation
            )
            
            results.append({
                'pattern': p['pattern_name'],
                'repo': p['repo'],
                'validations': len(mining_result['validations']),
                'anti_patterns': len(mining_result['anti_patterns']),
                'solutions': len(mining_result['solutions'])
            })
        
        # Summary
        print(f"\n=== Validation Mining Complete ===")
        total_validations = sum(r['validations'] for r in results)
        total_anti = sum(r['anti_patterns'] for r in results)
        print(f"Total validations found: {total_validations}")
        print(f"Total anti-patterns found: {total_anti}")
        print(f"Total cost: ~${len(patterns) * 20 * 0.01:.2f}")
        
        return results

# Usage
if __name__ == "__main__":
    import sys
    
    print("Issue Mining for Pattern Validation")
    print("====================================")
    print("\nOptions:")
    print("1. Mine issues for specific repo/pattern")
    print("2. Validate all low-confidence patterns")
    print("3. Test single issue analysis")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    miner = IssueMiner()
    
    if choice == "1":
        repo_name = input("Repository (e.g., microsoft/vscode): ").strip()
        pattern_name = input("Pattern name (e.g., filesystem_browser): ").strip()
        limit = int(input("Max issues to analyze (default 50): ").strip() or "50")
        
        results = miner.mine_issues(
            repo_name=repo_name,
            pattern_name=pattern_name,
            limit=limit
        )
        
        print(f"\n=== Results ===")
        print(f"Anti-patterns: {len(results['anti_patterns'])}")
        print(f"Solutions: {len(results['solutions'])}")
        print(f"Validations: {len(results['validations'])}")
        
        if results['anti_patterns']:
            print(f"\nAnti-patterns detected:")
            for ap in results['anti_patterns']:
                print(f"  • {ap['problem']}")
                print(f"    Severity: {ap['severity']}")
                print(f"    Source: {ap['issue_url']}")
    
    elif choice == "2":
        results = miner.mine_for_low_confidence_patterns()
        
        print(f"\nValidation summary:")
        for r in results:
            print(f"\n{r['pattern']}")
            print(f"  Validations: {r['validations']}")
            print(f"  Anti-patterns: {r['anti_patterns']}")
            print(f"  Solutions: {r['solutions']}")
    
    elif choice == "3":
        print("\nTest mode: Analyze single repo for pattern")
        print("Example: microsoft/vscode, filesystem_browser, limit 10")
        
        results = miner.mine_issues(
            repo_name="microsoft/vscode",
            pattern_name="filesystem_browser",
            limit=10
        )
        
        print(f"\n✓ Test complete")
        print(f"Cost: ~$0.10")
    
    else:
        print("Invalid choice.")
