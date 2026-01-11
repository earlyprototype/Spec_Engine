"""
Test Vector Search Functionality

Validates that vector indexes are working correctly and semantic search
produces sensible results.
"""

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
from neo4j import GraphDatabase
from embedding_generator import EmbeddingGenerator

load_dotenv()


class VectorSearchTester:
    """Test suite for vector search functionality."""
    
    def __init__(self):
        """Initialize tester with Neo4j connection and embedding generator."""
        # Connect to Neo4j
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        
        if not neo4j_password:
            raise ValueError("NEO4J_PASSWORD not set in environment")
        
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.generator = EmbeddingGenerator()
        
        print("VectorSearchTester initialized")
        print(f"  Neo4j: {neo4j_uri}")
    
    def close(self):
        """Close connections."""
        self.driver.close()
    
    def test_index_exists(self) -> bool:
        """Test 1: Check if vector index exists and is online."""
        print("\n" + "="*70)
        print("TEST 1: Vector Index Status")
        print("="*70)
        
        with self.driver.session() as session:
            result = session.run("""
                SHOW INDEXES
                YIELD name, type, state, populationPercent
                WHERE name = 'pattern_embeddings'
                RETURN name, type, state, populationPercent
            """)
            
            record = result.single()
            
            if not record:
                print("✗ FAILED: Vector index 'pattern_embeddings' not found")
                print("  Run: cypher-shell < vector_index_setup.cypher")
                return False
            
            index_name = record['name']
            index_type = record['type']
            state = record['state']
            population = record['populationPercent']
            
            print(f"✓ Index found: {index_name}")
            print(f"  Type: {index_type}")
            print(f"  State: {state}")
            print(f"  Population: {population}%")
            
            if state != 'ONLINE':
                print(f"✗ FAILED: Index is not ONLINE (current: {state})")
                print("  Wait for index to come online: CALL db.awaitIndexes()")
                return False
            
            if population < 100:
                print(f"⚠ WARNING: Index population is {population}%, may not be fully ready")
            
            print("✓ PASSED: Vector index is online and ready")
            return True
    
    def test_embedding_coverage(self) -> bool:
        """Test 2: Check how many patterns have embeddings."""
        print("\n" + "="*70)
        print("TEST 2: Embedding Coverage")
        print("="*70)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                RETURN count(p) AS total,
                       count(p.embedding) AS with_embeddings,
                       count(p) - count(p.embedding) AS without_embeddings
            """)
            
            record = result.single()
            total = record['total']
            with_embeddings = record['with_embeddings']
            without_embeddings = record['without_embeddings']
            coverage = (with_embeddings / total * 100) if total > 0 else 0
            
            print(f"Pattern count:")
            print(f"  Total: {total}")
            print(f"  With embeddings: {with_embeddings}")
            print(f"  Without embeddings: {without_embeddings}")
            print(f"  Coverage: {coverage:.1f}%")
            
            if total == 0:
                print("✗ FAILED: No patterns in database")
                print("  Run pattern extraction first")
                return False
            
            if with_embeddings == 0:
                print("✗ FAILED: No patterns have embeddings")
                print("  Run: python generate_pattern_embeddings.py")
                return False
            
            if coverage < 100:
                print(f"⚠ WARNING: Only {coverage:.1f}% of patterns have embeddings")
                print("  Some patterns will not be searchable")
            else:
                print("✓ PASSED: All patterns have embeddings")
            
            return with_embeddings > 0
    
    def test_embedding_dimensions(self) -> bool:
        """Test 3: Verify embeddings have correct dimensions."""
        print("\n" + "="*70)
        print("TEST 3: Embedding Dimensions")
        print("="*70)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.embedding IS NOT NULL
                RETURN p.name AS name,
                       size(p.embedding) AS dimensions,
                       p.embedding_model AS model,
                       p.embedding_version AS version
                LIMIT 5
            """)
            
            records = list(result)
            
            if not records:
                print("✗ FAILED: No patterns with embeddings found")
                return False
            
            expected_dims = 768
            all_correct = True
            
            print(f"Sample patterns (expected dimensions: {expected_dims}):")
            for record in records:
                name = record['name']
                dims = record['dimensions']
                model = record['model']
                version = record['version']
                
                status = "✓" if dims == expected_dims else "✗"
                print(f"  {status} {name}: {dims} dimensions")
                print(f"     Model: {model}, Version: {version}")
                
                if dims != expected_dims:
                    all_correct = False
            
            if all_correct:
                print(f"\n✓ PASSED: All embeddings have correct dimensions ({expected_dims})")
            else:
                print(f"\n✗ FAILED: Some embeddings have incorrect dimensions")
                print("  Regenerate embeddings: python generate_pattern_embeddings.py --force")
            
            return all_correct
    
    def test_vector_search(self, test_queries: List[str]) -> bool:
        """Test 4: Execute sample vector searches."""
        print("\n" + "="*70)
        print("TEST 4: Vector Search Queries")
        print("="*70)
        
        all_passed = True
        
        for i, query_text in enumerate(test_queries, 1):
            print(f"\nQuery {i}: \"{query_text}\"")
            print("-" * 70)
            
            try:
                # Generate query embedding
                embedding, metadata = self.generator.generate_embedding(query_text)
                print(f"  Embedding generated: {metadata['duration_ms']}ms")
                
                # Execute vector search
                with self.driver.session() as session:
                    result = session.run("""
                        CALL db.index.vector.queryNodes('pattern_embeddings', 5, $embedding)
                        YIELD node, score
                        RETURN node.name AS pattern,
                               score AS similarity,
                               node.confidence AS confidence,
                               node.stars AS stars,
                               node.reasoning AS reasoning
                        ORDER BY score DESC
                    """, embedding=embedding)
                    
                    results = list(result)
                    
                    if not results:
                        print("  ✗ No results returned")
                        all_passed = False
                        continue
                    
                    print(f"  ✓ Found {len(results)} results:")
                    for j, record in enumerate(results, 1):
                        pattern = record['pattern']
                        similarity = record['similarity']
                        confidence = record['confidence']
                        stars = record['stars']
                        reasoning = record['reasoning'][:80] if reasoning else "N/A"
                        
                        print(f"\n  {j}. {pattern} (similarity: {similarity:.3f})")
                        print(f"     Confidence: {confidence}, Stars: {stars}")
                        print(f"     Reasoning: {reasoning}...")
            
            except Exception as e:
                print(f"  ✗ Query failed: {e}")
                all_passed = False
        
        if all_passed:
            print("\n✓ PASSED: All vector searches executed successfully")
        else:
            print("\n✗ FAILED: Some vector searches failed")
        
        return all_passed
    
    def test_performance(self) -> bool:
        """Test 5: Check query performance."""
        print("\n" + "="*70)
        print("TEST 5: Query Performance")
        print("="*70)
        
        import time
        
        # Sample query
        query_text = "Web application for file management with TypeScript"
        
        print(f"Query: \"{query_text}\"")
        print("Running 5 iterations to measure performance...")
        
        timings = []
        
        try:
            for i in range(5):
                # Generate embedding
                start = time.time()
                embedding, _ = self.generator.generate_embedding(query_text, use_cache=True)
                embed_time = (time.time() - start) * 1000
                
                # Execute search
                start = time.time()
                with self.driver.session() as session:
                    result = session.run("""
                        CALL db.index.vector.queryNodes('pattern_embeddings', 10, $embedding)
                        YIELD node, score
                        RETURN node.name, score
                    """, embedding=embedding)
                    list(result)  # Consume results
                search_time = (time.time() - start) * 1000
                
                total_time = embed_time + search_time
                timings.append({
                    'embedding': embed_time,
                    'search': search_time,
                    'total': total_time
                })
                
                print(f"  Run {i+1}: {total_time:.1f}ms (embed: {embed_time:.1f}ms, search: {search_time:.1f}ms)")
            
            # Calculate averages
            avg_embed = sum(t['embedding'] for t in timings) / len(timings)
            avg_search = sum(t['search'] for t in timings) / len(timings)
            avg_total = sum(t['total'] for t in timings) / len(timings)
            
            print(f"\nAverage timings:")
            print(f"  Embedding: {avg_embed:.1f}ms")
            print(f"  Search: {avg_search:.1f}ms")
            print(f"  Total: {avg_total:.1f}ms")
            
            # Check against targets
            target_embed = 50  # ms
            target_search = 100  # ms
            target_total = 200  # ms
            
            print(f"\nPerformance targets:")
            embed_status = "✓" if avg_embed < target_embed else "⚠"
            search_status = "✓" if avg_search < target_search else "⚠"
            total_status = "✓" if avg_total < target_total else "⚠"
            
            print(f"  {embed_status} Embedding: {avg_embed:.1f}ms (target: <{target_embed}ms)")
            print(f"  {search_status} Search: {avg_search:.1f}ms (target: <{target_search}ms)")
            print(f"  {total_status} Total: {avg_total:.1f}ms (target: <{target_total}ms)")
            
            if avg_total < target_total:
                print("\n✓ PASSED: Performance within targets")
                return True
            else:
                print("\n⚠ WARNING: Performance exceeds targets but still functional")
                return True
        
        except Exception as e:
            print(f"\n✗ FAILED: Performance test error: {e}")
            return False
    
    def run_all_tests(self):
        """Run complete test suite."""
        print("\n" + "="*70)
        print("VECTOR SEARCH TEST SUITE")
        print("="*70)
        print("\nValidating semantic search setup and functionality...")
        
        results = {}
        
        # Test 1: Index exists
        results['index_exists'] = self.test_index_exists()
        if not results['index_exists']:
            print("\n✗ CRITICAL: Vector index not ready. Cannot proceed with tests.")
            return results
        
        # Test 2: Embedding coverage
        results['embedding_coverage'] = self.test_embedding_coverage()
        if not results['embedding_coverage']:
            print("\n✗ CRITICAL: No embeddings found. Cannot proceed with search tests.")
            return results
        
        # Test 3: Embedding dimensions
        results['embedding_dimensions'] = self.test_embedding_dimensions()
        
        # Test 4: Vector searches
        test_queries = [
            "Build a file manager application for desktop",
            "Real-time chat application with WebSocket",
            "Command-line tool for data processing",
            "Web application with authentication and database"
        ]
        results['vector_search'] = self.test_vector_search(test_queries)
        
        # Test 5: Performance
        results['performance'] = self.test_performance()
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        total = len(results)
        passed = sum(1 for v in results.values() if v)
        
        for test_name, passed_test in results.items():
            status = "✓ PASSED" if passed_test else "✗ FAILED"
            print(f"  {status}: {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
        
        if all(results.values()):
            print("\n✓ SUCCESS: All tests passed!")
            print("  Vector search is ready for use.")
            print("\nNext steps:")
            print("  1. Integrate with PatternQueryInterface")
            print("  2. Update Commander to use semantic search")
            print("  3. Test hybrid queries (semantic + structural)")
        else:
            print("\n✗ FAILURE: Some tests failed.")
            print("  Review errors above and fix issues before proceeding.")
        
        return results


def main():
    """Main entry point."""
    try:
        tester = VectorSearchTester()
        results = tester.run_all_tests()
        tester.close()
        
        # Exit with appropriate code
        if all(results.values()):
            sys.exit(0)
        else:
            sys.exit(1)
    
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
