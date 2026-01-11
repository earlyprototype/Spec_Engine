# batch_extract.py
# Extract 400+ patterns across multiple domains

from pattern_extractor import PatternExtractor
import time

def batch_extract_all():
    """Extract patterns from multiple domains."""
    
    extractor = PatternExtractor()
    
    # Define extraction targets
    extraction_targets = [
        # File Management (100 repos)
        {
            "name": "File Managers",
            "query": "topic:file-manager stars:>5000",
            "limit": 100
        },
        # Dashboards (100 repos)
        {
            "name": "Dashboards",
            "query": "topic:dashboard stars:>10000",
            "limit": 100
        },
        # APIs (100 repos)
        {
            "name": "API Gateways",
            "query": "topic:api-gateway stars:>5000",
            "limit": 100
        },
        # Data Management (100 repos)
        {
            "name": "Data Management",
            "query": "topic:database topic:management stars:>5000",
            "limit": 100
        }
    ]
    
    total_patterns = []
    total_cost = 0
    
    print("=== Batch Pattern Extraction ===")
    print(f"Total targets: {len(extraction_targets)}")
    print(f"Expected patterns: {sum(t['limit'] for t in extraction_targets)}")
    print(f"Estimated cost: ${sum(t['limit'] for t in extraction_targets) * 0.01:.2f}")
    print("\nThis will take approximately 30-60 minutes.")
    
    proceed = input("\nProceed? (yes/no): ").strip().lower()
    if proceed != "yes":
        print("Cancelled.")
        return
    
    start_time = time.time()
    
    for i, target in enumerate(extraction_targets, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(extraction_targets)}] Extracting: {target['name']}")
        print(f"Query: {target['query']}")
        print(f"Limit: {target['limit']}")
        print(f"{'='*60}\n")
        
        try:
            patterns = extractor.extract_patterns(
                search_query=target['query'],
                limit=target['limit']
            )
            
            total_patterns.extend(patterns)
            cost = len(patterns) * 0.01
            total_cost += cost
            
            print(f"\n✓ Extracted {len(patterns)} patterns from {target['name']}")
            print(f"✓ Cost: ${cost:.2f}")
            
            # Rate limiting pause
            if i < len(extraction_targets):
                print("\nPausing for 10 seconds (rate limiting)...")
                time.sleep(10)
                
        except Exception as e:
            print(f"\n✗ Error extracting {target['name']}: {e}")
            continue
    
    end_time = time.time()
    duration = (end_time - start_time) / 60  # minutes
    
    # Summary
    print(f"\n{'='*60}")
    print("=== Extraction Complete ===")
    print(f"{'='*60}")
    print(f"Total patterns extracted: {len(total_patterns)}")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"Duration: {duration:.1f} minutes")
    print(f"Average cost per pattern: ${total_cost / len(total_patterns):.4f}")
    
    # Breakdown by domain
    print("\nBreakdown by domain:")
    for i, target in enumerate(extraction_targets):
        # Count patterns for this target
        # (In real implementation, would track which patterns came from which query)
        expected = target['limit']
        print(f"  {target['name']}: ~{expected} patterns")
    
    print("\n✓ All patterns stored in Neo4j")
    print("✓ Run test_query.py to test recommendations")

def extract_specific_domain(domain_name, query, limit=50):
    """Extract patterns from a specific domain."""
    
    extractor = PatternExtractor()
    
    print(f"\n=== Extracting: {domain_name} ===")
    print(f"Query: {query}")
    print(f"Limit: {limit}")
    print(f"Estimated cost: ${limit * 0.01:.2f}\n")
    
    patterns = extractor.extract_patterns(
        search_query=query,
        limit=limit
    )
    
    print(f"\n✓ Extracted {len(patterns)} patterns")
    print(f"✓ Cost: ${len(patterns) * 0.01:.2f}")
    
    return patterns

if __name__ == "__main__":
    import sys
    
    print("Batch Pattern Extraction")
    print("========================")
    print("\nOptions:")
    print("1. Extract all domains (400 patterns, ~$4, 30-60 min)")
    print("2. Extract specific domain (custom)")
    print("3. Quick test (10 patterns per domain, ~$0.40)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        batch_extract_all()
    
    elif choice == "2":
        print("\nExamples:")
        print("  - topic:authentication stars:>5000")
        print("  - language:python topic:web-framework stars:>10000")
        print("  - topic:monitoring stars:>5000")
        
        domain_name = input("\nDomain name: ").strip()
        query = input("GitHub query: ").strip()
        limit = int(input("Limit (default 50): ").strip() or "50")
        
        extract_specific_domain(domain_name, query, limit)
    
    elif choice == "3":
        print("\nRunning quick test (10 patterns per domain)...")
        
        extractor = PatternExtractor()
        
        domains = [
            ("File Managers", "topic:file-manager stars:>5000", 10),
            ("Dashboards", "topic:dashboard stars:>10000", 10),
            ("APIs", "topic:api-gateway stars:>5000", 10),
            ("Data Tools", "topic:database topic:management stars:>5000", 10)
        ]
        
        total = 0
        for name, query, limit in domains:
            print(f"\nExtracting {name}...")
            patterns = extractor.extract_patterns(query, limit)
            print(f"✓ {len(patterns)} patterns")
            total += len(patterns)
        
        print(f"\n✓ Total: {total} patterns")
        print(f"✓ Cost: ${total * 0.01:.2f}")
    
    else:
        print("Invalid choice.")
