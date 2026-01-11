#!/usr/bin/env python3
"""
Example: Integrating Awesome List repos with Pattern Extractor

This script demonstrates how to use repositories extracted from awesome lists
with the pattern extraction pipeline.
"""

import json
from awesome_list_parser import AwesomeListParser


def example_1_basic_extraction():
    """
    Example 1: Extract top NLP libraries from awesome-nlp
    """
    print("\n=== Example 1: Basic Extraction ===\n")
    
    parser = AwesomeListParser()
    
    # Parse awesome-nlp and get top repos
    repos = parser.parse_awesome_list(
        awesome_list_repo='keon/awesome-nlp',
        min_stars=1000
    )
    
    print(f"\nExtracted {len(repos)} high-quality NLP repositories")
    print("\nTop 10:")
    for i, repo in enumerate(repos[:10], 1):
        print(f"  {i}. {repo['full_name']}: {repo['stars']} stars")
    
    # Save for later use
    with open('awesome_nlp_top_repos.json', 'w') as f:
        json.dump(repos, f, indent=2)
    
    print("\n[SAVED] awesome_nlp_top_repos.json")


def example_2_generate_domain_queries():
    """
    Example 2: Generate domain queries for pattern extractor
    """
    print("\n=== Example 2: Generate Domain Queries ===\n")
    
    # Load previously extracted repos
    with open('awesome_nlp_top_repos.json') as f:
        repos = json.load(f)
    
    # Create domain queries (for adding to domain_selector_server.py)
    domains = []
    
    for repo in repos[:20]:  # Top 20 repos
        domain = {
            'name': f"awesome_{repo['name'].lower()}",
            'query': f"repo:{repo['full_name']}",
            'max_repos': 1,
            'metadata': {
                'source': 'awesome-nlp',
                'stars': repo['stars'],
                'language': repo['language'],
                'topics': repo['topics']
            }
        }
        domains.append(domain)
    
    # Print sample queries
    print("Sample domain queries for pattern extractor:")
    print("=" * 60)
    for domain in domains[:5]:
        print(f"\n{domain['name']}:")
        print(f"  Query: {domain['query']}")
        print(f"  Stars: {domain['metadata']['stars']}")
        print(f"  Language: {domain['metadata']['language']}")
    
    # Save
    with open('awesome_domain_queries.json', 'w') as f:
        json.dump(domains, f, indent=2)
    
    print(f"\n\n[SAVED] awesome_domain_queries.json ({len(domains)} queries)")


def example_3_filter_by_language():
    """
    Example 3: Filter repos by programming language
    """
    print("\n=== Example 3: Filter by Language ===\n")
    
    # Load repos
    with open('awesome_nlp_top_repos.json') as f:
        repos = json.load(f)
    
    # Group by language
    by_language = {}
    for repo in repos:
        lang = repo['language'] or 'Unknown'
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(repo)
    
    # Print summary
    print("Repositories by language:")
    print("=" * 60)
    for lang, lang_repos in sorted(by_language.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{lang}: {len(lang_repos)} repositories")
        for repo in lang_repos[:3]:  # Top 3 per language
            print(f"  - {repo['full_name']} ({repo['stars']} stars)")
        if len(lang_repos) > 3:
            print(f"  ... and {len(lang_repos) - 3} more")
    
    # Save Python repos separately (most relevant for your pipeline)
    python_repos = by_language.get('Python', [])
    with open('awesome_nlp_python_only.json', 'w') as f:
        json.dump(python_repos, f, indent=2)
    
    print(f"\n[SAVED] awesome_nlp_python_only.json ({len(python_repos)} Python repos)")


def example_4_topic_analysis():
    """
    Example 4: Analyze repository topics
    """
    print("\n=== Example 4: Topic Analysis ===\n")
    
    # Load repos
    with open('awesome_nlp_top_repos.json') as f:
        repos = json.load(f)
    
    # Count topics
    topic_counts = {}
    for repo in repos:
        for topic in repo['topics']:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    # Sort by frequency
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("Most common topics in awesome-nlp repos:")
    print("=" * 60)
    for topic, count in sorted_topics[:20]:
        print(f"  {topic}: {count} repos")
    
    # Find repos with specific topics
    target_topics = ['knowledge-graph', 'graph', 'semantic', 'rag']
    
    print(f"\n\nRepos matching topics {target_topics}:")
    print("=" * 60)
    
    matching_repos = []
    for repo in repos:
        if any(topic in repo['topics'] for topic in target_topics):
            matching_repos.append(repo)
            print(f"  - {repo['full_name']}")
            print(f"    Topics: {', '.join(repo['topics'])}")
            print(f"    Stars: {repo['stars']}\n")
    
    if matching_repos:
        with open('awesome_nlp_graph_repos.json', 'w') as f:
            json.dump(matching_repos, f, indent=2)
        print(f"[SAVED] awesome_nlp_graph_repos.json ({len(matching_repos)} repos)")
    else:
        print("No repos found with graph/knowledge-graph topics")


def example_5_combine_multiple_lists():
    """
    Example 5: Combine multiple awesome lists
    """
    print("\n=== Example 5: Combine Multiple Lists ===\n")
    
    parser = AwesomeListParser()
    
    awesome_lists = [
        'keon/awesome-nlp',
        # Add more awesome lists here:
        # 'josephmisiti/awesome-machine-learning',
        # 'academic/awesome-datascience',
    ]
    
    all_repos = {}  # Use dict to deduplicate by full_name
    
    for awesome_list in awesome_lists:
        print(f"\nParsing {awesome_list}...")
        repos = parser.parse_awesome_list(
            awesome_list_repo=awesome_list,
            min_stars=1000
        )
        
        # Add to combined dict (deduplicates automatically)
        for repo in repos:
            if repo['full_name'] not in all_repos:
                all_repos[repo['full_name']] = repo
                all_repos[repo['full_name']]['sources'] = []
            
            all_repos[repo['full_name']]['sources'].append(awesome_list)
    
    # Convert back to list and sort
    combined_repos = sorted(
        all_repos.values(),
        key=lambda x: x['stars'],
        reverse=True
    )
    
    print(f"\n\n[COMBINED] {len(combined_repos)} unique repositories from {len(awesome_lists)} lists")
    
    # Find repos that appear in multiple lists (high quality signal!)
    multi_list_repos = [r for r in combined_repos if len(r['sources']) > 1]
    print(f"[HIGH QUALITY] {len(multi_list_repos)} repos appear in multiple lists")
    
    # Save
    with open('awesome_combined_repos.json', 'w') as f:
        json.dump(combined_repos, f, indent=2)
    
    print("[SAVED] awesome_combined_repos.json")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Awesome List Integration Examples")
    print("=" * 60)
    
    # Run examples
    # Uncomment the ones you want to try:
    
    example_1_basic_extraction()
    # example_2_generate_domain_queries()
    # example_3_filter_by_language()
    # example_4_topic_analysis()
    # example_5_combine_multiple_lists()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60 + "\n")
    
    print("Next steps:")
    print("  1. Review the generated JSON files")
    print("  2. Add repos to your domain_selector_server.py")
    print("  3. Run pattern extraction on discovered repos")
    print("  4. Compare patterns from awesome-list repos vs GitHub search\n")
