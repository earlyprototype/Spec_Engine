# test_extraction.py
# Test single repository extraction

from pattern_extractor import PatternExtractor

def test_single_extraction():
    """Test extracting pattern from a single repository."""
    
    # Initialize
    extractor = PatternExtractor()
    
    # Extract from ONE repo (test)
    print("\n=== Testing Single Repository Extraction ===")
    print("Repository: microsoft/vscode")
    print("Domain: file_management")
    
    pattern = extractor.analyze_single_repo(
        "microsoft/vscode",  # Example: VS Code file explorer
        domain="file_management"
    )
    
    print(f"\n✓ Extracted pattern: {pattern['pattern_name']}")
    print(f"✓ Confidence: {pattern['confidence']}")
    print(f"✓ Requirements type: {pattern['requirements']['type']}")
    print(f"✓ Requirements domain: {pattern['requirements']['domain']}")
    print(f"✓ Constraints: {pattern['constraints']}")
    print(f"✓ Technologies: {[t['name'] for t in pattern['technologies']]}")
    print(f"✓ Reasoning: {pattern['reasoning']}")
    
    # Store in graph
    print("\n=== Storing Pattern in Neo4j ===")
    extractor.store_pattern(pattern)
    
    print("\n✓ First pattern extracted and stored")
    print("✓ Cost: ~$0.01")
    print("✓ Time: ~10 seconds")
    
    return pattern

def test_multiple_extraction():
    """Test extracting patterns from multiple repositories."""
    
    extractor = PatternExtractor()
    
    print("\n=== Testing Multiple Repository Extraction ===")
    
    # Extract 5 file managers
    print("\n--- File Managers (limit: 5) ---")
    file_managers = extractor.extract_patterns(
        "topic:file-manager stars:>5000",
        limit=5
    )
    
    print(f"\n✓ Extracted {len(file_managers)} file manager patterns")
    for pattern in file_managers:
        print(f"  - {pattern['pattern_name']} ({pattern['stars']} stars)")
    
    # Calculate cost
    total_cost = len(file_managers) * 0.01
    print(f"\n✓ Total cost: ~${total_cost:.2f}")
    
    return file_managers

if __name__ == "__main__":
    import sys
    
    print("Choose test:")
    print("1. Single repository extraction (microsoft/vscode)")
    print("2. Multiple repositories extraction (5 file managers)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_single_extraction()
    elif choice == "2":
        test_multiple_extraction()
    else:
        print("Invalid choice. Running single extraction test...")
        test_single_extraction()
