# domain_selector_server.py
# Simple Flask server for domain/topic selector UI

import os
from dotenv import load_dotenv

# Load environment variables FIRST before importing other modules
# Use override=True to ensure .env file takes precedence over system variables
load_dotenv(override=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from domain_topic_selector import DomainTopicSelector
from pattern_extractor import PatternExtractor
import threading
import sys
from datetime import datetime

app = Flask(__name__)
CORS(app)

selector = DomainTopicSelector()

# Callback for real-time pattern updates
def on_pattern_extracted(pattern):
    """Called when a pattern is successfully extracted."""
    global extraction_status
    extraction_status['completed'] += 1

extractor = PatternExtractor(progress_callback=on_pattern_extracted)

# Store extraction status
extraction_status = {
    'running': False,
    'phase': None,  # 'validating' or 'extracting'
    'current_domain': None,
    'progress': 0,
    'total': 0,
    'completed': 0,
    'logs': [],
    'domain_results': {},
    'validation_results': {}  # Track query validation
}

@app.route('/analyse', methods=['POST'])
def analyse():
    """Analyse project requirements and return recommendations."""
    try:
        data = request.json
        description = data.get('description')
        technologies = data.get('technologies')
        
        if not description:
            return jsonify({'error': 'Description is required'}), 400
        
        result = selector.analyse_requirements(description, technologies)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract', methods=['POST'])
def extract():
    """Start pattern extraction based on queries."""
    global extraction_status
    
    if extraction_status['running']:
        return jsonify({'error': 'Extraction already running'}), 400
    
    try:
        data = request.json
        queries = data.get('queries', [])
        min_validation_results = data.get('min_validation_results', 5)
        
        if not queries:
            return jsonify({'error': 'No queries provided'}), 400
        
        print("\n" + "="*70)
        print(f"EXTRACTION REQUEST: {len(queries)} queries")
        print("="*70)
        for i, q in enumerate(queries, 1):
            print(f"  {i}. {q['query']} (limit: {q['limit']})")
        print("="*70 + "\n")
        sys.stdout.flush()
        
        # Reset status
        extraction_status = {
            'running': True,
            'phase': 'validating',
            'current_domain': None,
            'progress': 0,
            'total': len(queries),
            'completed': 0,
            'logs': [],
            'domain_results': {},
            'validation_results': {}
        }
        
        # Start extraction in background thread
        thread = threading.Thread(target=run_extraction, args=(queries, min_validation_results))
        thread.start()
        
        return jsonify({'status': 'started', 'total': len(queries)})
        
    except Exception as e:
        extraction_status['running'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/extract/status', methods=['GET'])
def extract_status():
    """Get current extraction status."""
    return jsonify(extraction_status)

@app.route('/metrics/quality', methods=['GET'])
def quality_metrics():
    """Get quality and validation metrics from Neo4j."""
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        )
        
        with driver.session() as session:
            # Get overall statistics
            stats_result = session.run("""
                MATCH (p:Pattern)
                RETURN 
                    count(p) as total_patterns,
                    avg(p.quality_score) as avg_quality,
                    avg(p.validation_score) as avg_validation,
                    avg(p.judge_score) as avg_judge,
                    sum(CASE WHEN p.needs_review = true THEN 1 ELSE 0 END) as needs_review_count,
                    sum(CASE WHEN p.extraction_status = 'complete' THEN 1 ELSE 0 END) as complete_count,
                    sum(CASE WHEN p.extraction_status = 'partial' THEN 1 ELSE 0 END) as partial_count
            """)
            stats = stats_result.single()
            
            # Get patterns needing review
            review_result = session.run("""
                MATCH (p:Pattern)
                WHERE p.needs_review = true
                RETURN p.name as name, p.validation_score as score, p.source_repo as repo
                ORDER BY p.validation_score ASC
                LIMIT 10
            """)
            needs_review = [dict(record) for record in review_result]
            
            # Get top quality patterns
            top_result = session.run("""
                MATCH (p:Pattern)
                WHERE p.judge_score > 0
                RETURN p.name as name, p.judge_score as score, p.source_repo as repo
                ORDER BY p.judge_score DESC
                LIMIT 10
            """)
            top_patterns = [dict(record) for record in top_result]
            
            # Get extraction completeness
            completeness_result = session.run("""
                MATCH (p:Pattern)
                RETURN 
                    sum(CASE WHEN p.has_readme = true THEN 1 ELSE 0 END) as with_readme,
                    sum(CASE WHEN p.has_structure = true THEN 1 ELSE 0 END) as with_structure,
                    sum(CASE WHEN p.has_dependencies = true THEN 1 ELSE 0 END) as with_dependencies,
                    count(p) as total
            """)
            completeness = completeness_result.single()
            
            driver.close()
            
            return jsonify({
                'statistics': {
                    'total_patterns': stats['total_patterns'],
                    'avg_quality_score': round(stats['avg_quality'] or 0, 2),
                    'avg_validation_score': round(stats['avg_validation'] or 0, 2),
                    'avg_judge_score': round(stats['avg_judge'] or 0, 2),
                    'needs_review_count': stats['needs_review_count'],
                    'complete_extractions': stats['complete_count'],
                    'partial_extractions': stats['partial_count']
                },
                'completeness': {
                    'readme_percent': round((completeness['with_readme'] / completeness['total'] * 100) if completeness['total'] > 0 else 0, 1),
                    'structure_percent': round((completeness['with_structure'] / completeness['total'] * 100) if completeness['total'] > 0 else 0, 1),
                    'dependencies_percent': round((completeness['with_dependencies'] / completeness['total'] * 100) if completeness['total'] > 0 else 0, 1)
                },
                'needs_review': needs_review,
                'top_patterns': top_patterns
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def log_console(message):
    """Log to both console and status logs."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    console_msg = f"[{timestamp}] {message}"
    print(console_msg, flush=True)
    extraction_status['logs'].append(message)

def run_extraction(queries, min_validation_results=5):
    """Run pattern extraction in background."""
    global extraction_status
    
    try:
        # Phase 1: Validate all queries first
        extraction_status['phase'] = 'validating'
        log_console(f"[PHASE 1] Validating queries (min results: {min_validation_results})...")
        
        validated_queries = []
        failed_queries = []
        
        for i, query_obj in enumerate(queries):
            query = query_obj['query']
            limit = query_obj['limit']
            domain_name = f"domain_{i+1}"
            
            extraction_status['current_domain'] = domain_name
            extraction_status['progress'] = i + 1
            log_console(f"Query {i+1}/{len(queries)}: {query}")
            
            try:
                # Validate and refine query using user's min threshold
                status, refined_query, result_count = extractor.validate_and_refine_query(query, min_results=min_validation_results)
                
                extraction_status['validation_results'][domain_name] = {
                    'original_query': query,
                    'refined_query': refined_query,
                    'result_count': result_count,
                    'status': status
                }
                
                if status == 'ok':
                    log_console(f"  [OK] {result_count} results")
                    validated_queries.append({
                        'query': refined_query,
                        'limit': limit,
                        'domain_name': domain_name
                    })
                elif status == 'refined':
                    log_console(f"  [REFINED] {refined_query}")
                    log_console(f"  {result_count} results (was: {query})")
                    validated_queries.append({
                        'query': refined_query,
                        'limit': limit,
                        'domain_name': domain_name
                    })
                elif status == 'failed':
                    log_console(f"  [FAILED] Query returned 0 results, skipping extraction")
                    failed_queries.append(domain_name)
                    extraction_status['domain_results'][domain_name] = {
                        'status': 'skipped',
                        'patterns': 0,
                        'query': query,
                        'reason': 'No results after refinement'
                    }
                
            except Exception as e:
                log_console(f"  [ERROR] Validation failed: {str(e)}")
                extraction_status['validation_results'][domain_name] = {
                    'original_query': query,
                    'refined_query': query,
                    'result_count': 0,
                    'status': 'error',
                    'error': str(e)
                }
                failed_queries.append(domain_name)
        
        log_console(f"[PHASE 1 COMPLETE] {len(validated_queries)} queries ready, {len(failed_queries)} skipped")
        
        # Phase 2: Extract patterns
        extraction_status['phase'] = 'extracting'
        extraction_status['progress'] = 0
        log_console("[PHASE 2] Extracting patterns...")
        
        for i, validated in enumerate(validated_queries):
            query = validated['query']
            limit = validated['limit']
            domain_name = validated['domain_name']
            
            extraction_status['current_domain'] = domain_name
            extraction_status['progress'] = i + 1
            log_console(f"Extracting {domain_name}: {query}")
            extraction_status['domain_results'][domain_name] = {
                'status': 'running',
                'patterns': 0,
                'query': query
            }
            
            try:
                # Extract patterns (validation already done, so skip it)
                log_console(f"  Searching GitHub for {limit} repos...")
                patterns = extractor.extract_patterns(query, limit=limit, validate=False)
                # Note: extraction_status['completed'] is updated in real-time via callback
                extraction_status['domain_results'][domain_name] = {
                    'status': 'complete',
                    'patterns': len(patterns),
                    'query': query
                }
                log_console(f"[OK] {len(patterns)} patterns extracted for {domain_name}")
            except Exception as e:
                extraction_status['domain_results'][domain_name] = {
                    'status': 'error',
                    'patterns': 0,
                    'query': query,
                    'error': str(e)
                }
                log_console(f"[ERROR] {domain_name}: {str(e)}")
        
        log_console(f"[COMPLETE] Total patterns: {extraction_status['completed']}")
        
    except Exception as e:
        log_console(f"[FATAL] {str(e)}")
    finally:
        extraction_status['running'] = False
        extraction_status['phase'] = None
        extraction_status['current_domain'] = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("="*70)
    print("Domain & Topic Selector Server")
    print("="*70)
    print("\n1. Server starting on http://localhost:8000")
    print("2. Open domain_selector_ui.html in your browser")
    print("\nServer logging enabled - you'll see extraction progress here")
    print("\nPress Ctrl+C to stop\n")
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
