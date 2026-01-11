"""
Debug environment loading in domain selector server context
"""
import os
from dotenv import load_dotenv

print("="*60)
print("Environment Variable Debugging")
print("="*60)

print("\nBEFORE load_dotenv():")
print(f"  NEO4J_URI: {os.getenv('NEO4J_URI')}")
print(f"  NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD')}")

load_dotenv(override=True)

print("\nAFTER load_dotenv(override=True):")
print(f"  NEO4J_URI: {os.getenv('NEO4J_URI')}")
print(f"  NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD')}")

print("\nNow importing PatternExtractor...")
from pattern_extractor import PatternExtractor

print("\nCreating PatternExtractor instance...")
try:
    extractor = PatternExtractor()
    print("SUCCESS: Created PatternExtractor")
    print(f"Neo4j URI being used: {extractor.neo4j._pool.address}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
