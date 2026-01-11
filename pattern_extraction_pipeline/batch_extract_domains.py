# batch_extract_domains.py
# Batch extract patterns across multiple domains

from pattern_extractor import PatternExtractor
import time

def main():
    extractor = PatternExtractor()

    # Define domains to extract
    domains = [
        ("topic:file-manager stars:>5000", 20, "file_management"),
        ("topic:dashboard stars:>5000", 30, "dashboards"),
        ("topic:cli stars:>5000", 20, "cli_tools"),
        ("topic:api OR topic:backend stars:>5000", 50, "backend_api"),
        ("topic:websocket OR topic:realtime stars:>5000", 20, "realtime"),
        ("topic:database stars:>5000", 30, "databases"),
        ("topic:authentication stars:>5000", 20, "auth"),
        ("topic:monitoring stars:>5000", 20, "monitoring"),
        ("topic:testing stars:>5000", 20, "testing"),
        ("topic:devops stars:>5000", 30, "devops"),
    ]

    total_extracted = 0
    start_time = time.time()

    print("\n" + "="*70)
    print("BATCH PATTERN EXTRACTION")
    print("="*70)
    print(f"\nExtracting patterns from {len(domains)} domains")
    print(f"Expected total: ~{sum(d[1] for d in domains)} patterns")
    print(f"Using: Google Gemini API (FREE)")
    print("="*70 + "\n")

    for i, (query, limit, domain_name) in enumerate(domains, 1):
        print(f"\n[{i}/{len(domains)}] {'='*60}")
        print(f"Domain: {domain_name}")
        print(f"Query: {query}")
        print(f"Target: {limit} patterns")
        print("="*60)
        
        try:
            patterns = extractor.extract_patterns(query, limit=limit)
            total_extracted += len(patterns)
            
            print(f"[OK] {len(patterns)} patterns extracted for {domain_name}")
            
            # Brief pause between domains to avoid rate limits
            if i < len(domains):
                print("\nWaiting 10 seconds before next domain...")
                time.sleep(10)
        
        except Exception as e:
            print(f"[ERROR] Failed to extract {domain_name}: {e}")
            continue

    elapsed = time.time() - start_time
    
    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print(f"Total patterns extracted: {total_extracted}")
    print(f"Time elapsed: {elapsed/60:.1f} minutes")
    print(f"Average: {elapsed/total_extracted:.1f} seconds per pattern")
    print("="*70)
    
    print("\nNext steps:")
    print("1. Run: python verify_data_quality.py")
    print("2. Run: python pattern_query.py")
    print("3. View graph: http://localhost:7474")

if __name__ == "__main__":
    main()
