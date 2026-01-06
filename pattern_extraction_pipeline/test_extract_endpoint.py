"""
Test the extract endpoint
"""
import requests
import json

# Test if server is running
try:
    response = requests.get('http://localhost:8000/health', timeout=2)
    print(f"Server health check: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"ERROR: Server not responding - {e}")
    print("Is the domain_selector_server.py running?")
    exit(1)

# Test extract endpoint with sample data
test_queries = [
    {
        "query": "topic:microservices stars:>5000",
        "purpose": "Test query",
        "limit": 5
    }
]

print("\nTesting /extract endpoint...")
try:
    response = requests.post(
        'http://localhost:8000/extract',
        headers={'Content-Type': 'application/json'},
        json={'queries': test_queries},
        timeout=5
    )
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\nSUCCESS: Extract endpoint is working!")
        print("\nNow checking status endpoint...")
        
        import time
        time.sleep(1)
        
        status_response = requests.get('http://localhost:8000/extract/status')
        print(f"Status: {status_response.json()}")
    else:
        print(f"\nERROR: Unexpected status code: {response.status_code}")
        
except Exception as e:
    print(f"ERROR: {e}")
