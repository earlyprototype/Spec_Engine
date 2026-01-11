#!/usr/bin/env python3
"""
System validation and health check script.

Verifies that all components are working correctly before production use.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import yaml
from dotenv import load_dotenv
from neo4j import GraphDatabase
import google.generativeai as genai

from ide_rule_library.logger import StructuredLogger

load_dotenv(override=True)


class SystemValidator:
    """Validate IDE Rule Library system health"""
    
    def __init__(self, logger):
        self.logger = logger
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
    
    def check_environment_variables(self) -> Tuple[bool, str]:
        """Check required environment variables"""
        required_vars = [
            'NEO4J_URI',
            'NEO4J_USER',
            'NEO4J_PASSWORD',
            'GEMINI_API_KEY'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            return False, f"Missing environment variables: {', '.join(missing)}"
        
        return True, "All required environment variables present"
    
    def check_config_file(self) -> Tuple[bool, str]:
        """Check config.yaml exists and is valid"""
        config_path = Path(__file__).parent / 'config.yaml'
        
        if not config_path.exists():
            return False, f"Config file not found: {config_path}"
        
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
            
            required_sections = ['gemini', 'neo4j', 'logging']
            missing = [s for s in required_sections if s not in config]
            
            if missing:
                return False, f"Missing config sections: {', '.join(missing)}"
            
            return True, "Config file valid"
            
        except Exception as e:
            return False, f"Config file error: {e}"
    
    def check_neo4j_connection(self) -> Tuple[bool, str]:
        """Check Neo4j connection"""
        try:
            uri = os.getenv('NEO4J_URI')
            user = os.getenv('NEO4J_USER')
            password = os.getenv('NEO4J_PASSWORD')
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            
            with driver.session() as session:
                result = session.run("RETURN 1 AS test")
                record = result.single()
                
                if record['test'] != 1:
                    return False, "Neo4j query returned unexpected result"
            
            driver.close()
            return True, f"Neo4j connection successful ({uri})"
            
        except Exception as e:
            return False, f"Neo4j connection failed: {e}"
    
    def check_neo4j_indexes(self) -> Tuple[bool, str]:
        """Check required Neo4j indexes exist"""
        try:
            uri = os.getenv('NEO4J_URI')
            user = os.getenv('NEO4J_USER')
            password = os.getenv('NEO4J_PASSWORD')
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            
            with driver.session() as session:
                result = session.run("SHOW INDEXES")
                indexes = [dict(record) for record in result]
                
                # Check for vector index
                vector_indexes = [idx for idx in indexes if 'ide_rule_embeddings' in str(idx)]
                
                if not vector_indexes:
                    driver.close()
                    return False, "Vector index 'ide_rule_embeddings' not found"
            
            driver.close()
            return True, f"Found {len(indexes)} indexes including vector index"
            
        except Exception as e:
            return False, f"Index check failed: {e}"
    
    def check_database_content(self) -> Tuple[bool, str]:
        """Check database has rules"""
        try:
            uri = os.getenv('NEO4J_URI')
            user = os.getenv('NEO4J_USER')
            password = os.getenv('NEO4J_PASSWORD')
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            
            with driver.session() as session:
                result = session.run("""
                    MATCH (r:IDERule)
                    RETURN count(r) AS total,
                           sum(CASE WHEN r.quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_quality
                """)
                
                record = result.single()
                total = record['total']
                with_quality = record['with_quality']
            
            driver.close()
            
            if total == 0:
                return False, "Database is empty (no IDERule nodes)"
            
            if with_quality == 0:
                self.warnings.append(f"No rules have quality scores (run migrate_quality_scores.py)")
                return True, f"Found {total} rules (0 with quality scores)"
            
            if with_quality < total:
                self.warnings.append(f"{total - with_quality} rules missing quality scores")
            
            return True, f"Found {total} rules ({with_quality} with quality scores)"
            
        except Exception as e:
            return False, f"Database content check failed: {e}"
    
    def check_gemini_api(self) -> Tuple[bool, str]:
        """Check Gemini API access"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            
            # Test with a simple query
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content("Say 'test' if you can read this.")
            
            if not response or not response.text:
                return False, "Gemini API returned empty response"
            
            return True, "Gemini API working"
            
        except Exception as e:
            return False, f"Gemini API check failed: {e}"
    
    def check_quality_distribution(self) -> Tuple[bool, str]:
        """Check quality score distribution is reasonable"""
        try:
            uri = os.getenv('NEO4J_URI')
            user = os.getenv('NEO4J_USER')
            password = os.getenv('NEO4J_PASSWORD')
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            
            with driver.session() as session:
                result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.quality_score IS NOT NULL
                    RETURN min(r.quality_score) AS min,
                           max(r.quality_score) AS max,
                           avg(r.quality_score) AS avg,
                           count(r) AS total
                """)
                
                record = result.single()
                
                if not record or record['total'] == 0:
                    driver.close()
                    return True, "No quality scores to analyze (run migration first)"
                
                min_score = record['min']
                max_score = record['max']
                avg_score = record['avg']
                total = record['total']
            
            driver.close()
            
            # Check for reasonable distribution
            if min_score == max_score:
                self.warnings.append(f"All quality scores are identical ({min_score:.1f})")
            
            if avg_score < 20 or avg_score > 90:
                self.warnings.append(f"Average quality score unusual: {avg_score:.1f}")
            
            return True, f"Quality range: {min_score:.1f}-{max_score:.1f}, avg: {avg_score:.1f} ({total} rules)"
            
        except Exception as e:
            return False, f"Quality distribution check failed: {e}"
    
    def check_required_files(self) -> Tuple[bool, str]:
        """Check required Python files exist"""
        base_path = Path(__file__).parent
        
        required_files = [
            'quality_scorer.py',
            'enhanced_rule_extractor.py',
            'enhanced_query_engine.py',
            'generate_cursorrules_v2.py',
            'logger.py',
            'exceptions.py',
            'retry_handler.py',
            'migrate_quality_scores.py',
            'quality_analysis.py',
            'estimate_costs.py'
        ]
        
        missing = [f for f in required_files if not (base_path / f).exists()]
        
        if missing:
            return False, f"Missing files: {', '.join(missing)}"
        
        return True, f"All {len(required_files)} required files present"
    
    def run_checks(self) -> bool:
        """Run all validation checks"""
        checks = [
            ("Environment Variables", self.check_environment_variables),
            ("Config File", self.check_config_file),
            ("Required Files", self.check_required_files),
            ("Neo4j Connection", self.check_neo4j_connection),
            ("Neo4j Indexes", self.check_neo4j_indexes),
            ("Database Content", self.check_database_content),
            ("Quality Distribution", self.check_quality_distribution),
            ("Gemini API", self.check_gemini_api),
        ]
        
        print("\n" + "="*70)
        print("SYSTEM VALIDATION")
        print("="*70)
        
        for check_name, check_func in checks:
            try:
                passed, message = check_func()
                
                if passed:
                    print(f"[OK] {check_name}: {message}")
                    self.checks_passed += 1
                else:
                    print(f"[FAIL] {check_name}: {message}")
                    self.checks_failed += 1
                    
            except Exception as e:
                print(f"[ERROR] {check_name}: {e}")
                self.checks_failed += 1
        
        # Print warnings
        if self.warnings:
            print("\n" + "="*70)
            print("WARNINGS")
            print("="*70)
            for warning in self.warnings:
                print(f"[WARNING] {warning}")
        
        # Print summary
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        print(f"Checks passed: {self.checks_passed}")
        print(f"Checks failed: {self.checks_failed}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.checks_failed == 0:
            print("\nSTATUS: System is ready for production use")
            print("="*70)
            return True
        else:
            print("\nSTATUS: System has issues that need to be resolved")
            print("="*70)
            return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate IDE Rule Library system')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Load config
    config_path = Path(__file__).parent / 'config.yaml'
    
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        logger = StructuredLogger("validator", config.get('logging', {}))
    else:
        # Fallback if config doesn't exist
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("validator")
    
    validator = SystemValidator(logger)
    success = validator.run_checks()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
