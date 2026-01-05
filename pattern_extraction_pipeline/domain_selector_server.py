# domain_selector_server.py
# Simple Flask server for domain/topic selector UI

from flask import Flask, request, jsonify
from flask_cors import CORS
from domain_topic_selector import DomainTopicSelector
from pattern_extractor import PatternExtractor
import threading

app = Flask(__name__)
CORS(app)

selector = DomainTopicSelector()
extractor = PatternExtractor()

# Store extraction status
extraction_status = {
    'running': False,
    'current_domain': None,
    'progress': 0,
    'total': 0,
    'completed': 0,
    'logs': [],
    'domain_results': {}
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
        
        if not queries:
            return jsonify({'error': 'No queries provided'}), 400
        
        # Reset status
        extraction_status = {
            'running': True,
            'current_domain': None,
            'progress': 0,
            'total': len(queries),
            'completed': 0,
            'logs': [],
            'domain_results': {}
        }
        
        # Start extraction in background thread
        thread = threading.Thread(target=run_extraction, args=(queries,))
        thread.start()
        
        return jsonify({'status': 'started', 'total': len(queries)})
        
    except Exception as e:
        extraction_status['running'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/extract/status', methods=['GET'])
def extract_status():
    """Get current extraction status."""
    return jsonify(extraction_status)

def run_extraction(queries):
    """Run pattern extraction in background."""
    global extraction_status
    
    try:
        for i, query_obj in enumerate(queries):
            query = query_obj['query']
            limit = query_obj['limit']
            domain_name = f"domain_{i+1}"
            
            extraction_status['current_domain'] = domain_name
            extraction_status['progress'] = i + 1
            extraction_status['logs'].append(f"Extracting {domain_name}: {query}")
            extraction_status['domain_results'][domain_name] = {
                'status': 'running',
                'patterns': 0,
                'query': query
            }
            
            try:
                patterns = extractor.extract_patterns(query, limit=limit)
                extraction_status['completed'] += len(patterns)
                extraction_status['domain_results'][domain_name] = {
                    'status': 'complete',
                    'patterns': len(patterns),
                    'query': query
                }
                extraction_status['logs'].append(f"[OK] {len(patterns)} patterns extracted for {domain_name}")
            except Exception as e:
                extraction_status['domain_results'][domain_name] = {
                    'status': 'error',
                    'patterns': 0,
                    'query': query,
                    'error': str(e)
                }
                extraction_status['logs'].append(f"[ERROR] {domain_name}: {str(e)}")
        
        extraction_status['logs'].append(f"[COMPLETE] Total patterns: {extraction_status['completed']}")
        
    except Exception as e:
        extraction_status['logs'].append(f"[FATAL] {str(e)}")
    finally:
        extraction_status['running'] = False
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
    print("\nPress Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=8000, debug=True)
