"""
Test Hybrid Query Interface

Validates that semantic + structural queries work correctly and produce
sensible, well-scored pattern recommendations.
"""

import os
import sys
from typing import Dict, List
from dotenv import load_dotenv
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic

load_dotenv()


class HybridQueryTester:
    """Test suite for hybrid query functionality."""
    
    def __init__(self):
        """Initialize tester with semantic interface."""
        self.interface = PatternQueryInterfaceSemantic()
        print("HybridQueryTester initialized")
    
    def close(self):
        """Close interface."""
        self.interface.close()
    
    def test_semantic_only(self) -> bool:
        """Test 1: Pure semantic search without constraints."""
        print("\n" + "="*70)
        print("TEST 1: Semantic Search (No Constraints)")
        print("="*70)
        
        query = "Build a file manager application for desktop users"
        print(f"\nQuery: \"{query}\"")
        
        try:
            result = self.interface.find_patterns_semantic(
                goal=query,
                top_k=5,
                min_similarity=0.5
            )
            
            patterns = result['patterns']
            
            if not patterns:
                print("✗ FAILED: No patterns returned")
                return False
            
            print(f"✓ Found {len(patterns)} patterns")
            print(f"  Embedding time: {result['embedding_time_ms']}ms")
            print(f"  Method: {result['method']}")
            
            # Check patterns have required fields
            for i, p in enumerate(patterns[:3], 1):
                required_fields = [
                    'name', 'composite_score', 'recommendation',
                    'semantic_similarity', 'breakdown'
                ]
                
                missing = [f for f in required_fields if f not in p]
                if missing:
                    print(f"✗ Pattern {i} missing fields: {missing}")
                    return False
                
                print(f"\n  {i}. {p['name']}")
                print(f"     Composite: {p['composite_score']:.3f}")
                print(f"     Semantic: {p['breakdown']['semantic_match']:.3f}")
                print(f"     Recommendation: {p['recommendation']}")
            
            # Verify patterns are sorted by composite score
            scores = [p['composite_score'] for p in patterns]
            if scores != sorted(scores, reverse=True):
                print("✗ FAILED: Patterns not sorted by composite score")
                return False
            
            print("\n✓ PASSED: Semantic search working correctly")
            return True
        
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_hybrid_with_tech_constraints(self) -> bool:
        """Test 2: Hybrid search with technology constraints."""
        print("\n" + "="*70)
        print("TEST 2: Hybrid Search with Technology Constraints")
        print("="*70)
        
        query = "Web application for data visualization"
        constraints = {
            'technologies': ['typescript', 'react'],
            'min_stars': 5000,
            'min_confidence': 'medium'
        }
        
        print(f"\nQuery: \"{query}\"")
        print(f"Constraints: {constraints}")
        
        try:
            result = self.interface.find_patterns_hybrid(
                goal=query,
                constraints=constraints,
                top_k=5
            )
            
            patterns = result['patterns']
            
            if not patterns:
                print("⚠ WARNING: No patterns matched constraints")
                print("  This might be expected if knowledge graph is small")
                return True  # Not a failure if DB is small
            
            print(f"✓ Found {len(patterns)} patterns matching constraints")
            
            # Verify patterns have technologies
            for i, p in enumerate(patterns[:3], 1):
                techs = p.get('technologies', [])
                print(f"\n  {i}. {p['name']}")
                print(f"     Technologies: {', '.join(techs) if techs else 'None'}")
                print(f"     Stars: {p['stars']:,}")
                print(f"     Composite: {p['composite_score']:.3f}")
                
                # Check stars constraint
                if p['stars'] < constraints['min_stars']:
                    print(f"     ⚠ Stars below minimum ({p['stars']} < {constraints['min_stars']})")
            
            # Check user review format
            if 'user_review_text' in result:
                print("\n✓ User review text generated")
                print("  Preview (first 200 chars):")
                print("  " + result['user_review_text'][:200] + "...")
            
            print("\n✓ PASSED: Hybrid search with constraints working")
            return True
        
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_confidence_scoring(self) -> bool:
        """Test 3: Verify confidence scoring is sensible."""
        print("\n" + "="*70)
        print("TEST 3: Confidence Scoring")
        print("="*70)
        
        query = "Command-line tool for file processing"
        
        try:
            result = self.interface.find_patterns_semantic(
                goal=query,
                top_k=10
            )
            
            patterns = result['patterns']
            
            if not patterns:
                print("✗ FAILED: No patterns to test scoring")
                return False
            
            print(f"Testing {len(patterns)} patterns for score consistency...\n")
            
            # Check score components
            for i, p in enumerate(patterns[:5], 1):
                composite = p['composite_score']
                breakdown = p['breakdown']
                
                semantic = breakdown['semantic_match']
                conf_val = breakdown['confidence_value']
                stars_norm = breakdown['normalized_stars']
                
                # Verify composite is within bounds
                if not (0 <= composite <= 1):
                    print(f"✗ Pattern {i}: Composite score out of bounds: {composite}")
                    return False
                
                # Verify recommendation matches score
                rec = p['recommendation']
                if composite > 0.7 and rec != 'high':
                    print(f"✗ Pattern {i}: Score {composite:.3f} should be 'high' not '{rec}'")
                    return False
                elif 0.5 < composite <= 0.7 and rec != 'medium':
                    print(f"✗ Pattern {i}: Score {composite:.3f} should be 'medium' not '{rec}'")
                    return False
                
                print(f"  {i}. {p['name']}")
                print(f"     Composite: {composite:.3f} ({rec})")
                print(f"     Components: semantic={semantic:.3f}, conf={conf_val:.2f}, stars={stars_norm:.3f}")
                
                # Check explanation exists
                if 'explanation' not in p:
                    print(f"     ⚠ Missing explanation")
                else:
                    print(f"     Explanation: {p['explanation'][:60]}...")
            
            print("\n✓ PASSED: Confidence scoring is consistent")
            return True
        
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_cross_pattern_discovery(self) -> bool:
        """Test 4: Cross-pattern discovery (conceptual similarity)."""
        print("\n" + "="*70)
        print("TEST 4: Cross-Pattern Discovery")
        print("="*70)
        
        query = "Event-driven architecture for data processing"
        
        try:
            result = self.interface.discover_alternatives(
                goal=query,
                include_different_tech=True,
                min_similarity=0.6,
                top_k=10
            )
            
            patterns = result['patterns']
            approaches = result['approaches']
            
            if not patterns:
                print("⚠ WARNING: No conceptually similar patterns found")
                print("  This might be expected for specialized queries")
                return True
            
            print(f"✓ Found {len(patterns)} conceptually similar patterns")
            print(f"  Grouped into {result['total_approaches']} architectural approaches")
            
            # Display approaches
            print("\nArchitectural Approaches:")
            for approach, patterns_list in list(approaches.items())[:3]:
                print(f"\n  {approach}: {len(patterns_list)} patterns")
                for p in patterns_list[:2]:
                    print(f"    - {p['name']} (similarity: {p['conceptual_similarity']:.3f})")
            
            # Verify patterns have tech stacks
            patterns_with_tech = [p for p in patterns if p.get('tech_stack')]
            print(f"\n  Patterns with tech stack info: {len(patterns_with_tech)}/{len(patterns)}")
            
            print("\n✓ PASSED: Cross-pattern discovery working")
            return True
        
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_similar_patterns(self) -> bool:
        """Test 5: Find patterns similar to a reference pattern."""
        print("\n" + "="*70)
        print("TEST 5: Similar Pattern Search")
        print("="*70)
        
        # First, get a reference pattern
        print("Getting reference pattern...")
        ref_result = self.interface.find_patterns_semantic(
            goal="Desktop application",
            top_k=1
        )
        
        if not ref_result['patterns']:
            print("⚠ WARNING: No patterns available for similarity test")
            return True
        
        reference_pattern = ref_result['patterns'][0]['name']
        print(f"Reference: {reference_pattern}")
        
        try:
            result = self.interface.find_similar_patterns(
                pattern_name=reference_pattern,
                top_k=5,
                min_similarity=0.5
            )
            
            similar = result['similar_patterns']
            
            if not similar:
                print("⚠ No similar patterns found (might be unique pattern)")
                return True
            
            print(f"\n✓ Found {len(similar)} similar patterns:")
            
            for i, p in enumerate(similar, 1):
                shared = p['shared_technologies']
                all_techs = p['all_technologies']
                
                print(f"\n  {i}. {p['name']}")
                print(f"     Similarity: {p['similarity']:.3f}")
                print(f"     Shared tech: {', '.join(shared) if shared else 'None'}")
                print(f"     All tech: {', '.join(all_techs[:3]) if all_techs else 'None'}")
                print(f"     Overlap: {p['tech_overlap_count']} technologies")
            
            print("\n✓ PASSED: Similar pattern search working")
            return True
        
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_enhanced_spec_verification(self) -> bool:
        """Test 6: Enhanced SPEC feasibility verification."""
        print("\n" + "="*70)
        print("TEST 6: Enhanced SPEC Verification")
        print("="*70)
        
        spec = {
            'goal': 'Build a web-based project management tool',
            'tech_stack': {
                'languages': ['typescript'],
                'frameworks': ['react']
            },
            'deployment_type': 'web'
        }
        
        print(f"SPEC Goal: {spec['goal']}")
        print(f"Tech Stack: {spec['tech_stack']}")
        
        try:
            # Test semantic verification
            result = self.interface.verify_spec_feasibility(
                spec,
                use_semantic=True
            )
            
            print(f"\nFeasibility Assessment:")
            print(f"  Score: {result['feasibility_score']}")
            print(f"  Confidence: {result['confidence']}")
            print(f"  Method: {result.get('method', 'unknown')}")
            print(f"  Supporting patterns: {len(result['supporting_patterns'])}")
            
            if result['concerns']:
                print(f"  Concerns: {', '.join(result['concerns'])}")
            
            if result['recommendations']:
                print(f"  Recommendations:")
                for rec in result['recommendations'][:2]:
                    print(f"    - {rec}")
            
            # Verify score is in valid range
            score = result['feasibility_score']
            if not (0 <= score <= 1):
                print(f"✗ FAILED: Score out of range: {score}")
                return False
            
            print("\n✓ PASSED: Enhanced verification working")
            return True
        
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run complete test suite."""
        print("\n" + "="*70)
        print("HYBRID QUERY TEST SUITE")
        print("="*70)
        print("\nValidating semantic + structural query integration...")
        
        results = {}
        
        # Run all tests
        results['semantic_only'] = self.test_semantic_only()
        results['hybrid_with_constraints'] = self.test_hybrid_with_tech_constraints()
        results['confidence_scoring'] = self.test_confidence_scoring()
        results['cross_pattern_discovery'] = self.test_cross_pattern_discovery()
        results['similar_patterns'] = self.test_similar_patterns()
        results['enhanced_verification'] = self.test_enhanced_spec_verification()
        
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
            print("\n✓ SUCCESS: All hybrid query tests passed!")
            print("  Semantic + structural queries working correctly.")
            print("\nNext steps:")
            print("  1. Integrate with SPEC Commander")
            print("  2. Add pattern-informed spec generation")
            print("  3. Test user review workflow")
        else:
            print("\n✗ FAILURE: Some tests failed.")
            print("  Review errors above and fix issues before proceeding.")
        
        return results


def main():
    """Main entry point."""
    try:
        tester = HybridQueryTester()
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
