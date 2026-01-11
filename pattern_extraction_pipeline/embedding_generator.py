"""
Embedding Generator for Pattern Knowledge Graph

Generates semantic embeddings for patterns using Gemini text-embedding-004.
Handles batching, caching, rate limiting, and error recovery.
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
from functools import lru_cache
import hashlib

load_dotenv()


class EmbeddingGenerator:
    """
    Wrapper for Gemini embedding API with caching and rate limiting.
    """
    
    # Model configuration
    MODEL_NAME = "models/text-embedding-004"
    EMBEDDING_DIMENSIONS = 768
    MODEL_VERSION = "2026-01"
    
    # Rate limiting (free tier: 1500 requests/day ≈ 60/hour ≈ 1/minute for safety)
    REQUESTS_PER_MINUTE = 60
    MIN_DELAY_SECONDS = 60 / REQUESTS_PER_MINUTE
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY_BASE = 2  # Exponential backoff: 2s, 4s, 8s
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize embedding generator.
        
        Args:
            cache_dir: Directory for caching embeddings (default: ./embedding_cache)
        """
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        
        # Setup cache
        self.cache_dir = Path(cache_dir) if cache_dir else Path("./embedding_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Track rate limiting
        self.last_request_time = 0
        self.request_count = 0
        
        print(f"EmbeddingGenerator initialized:")
        print(f"  Model: {self.MODEL_NAME}")
        print(f"  Dimensions: {self.EMBEDDING_DIMENSIONS}")
        print(f"  Cache: {self.cache_dir}")
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text hash."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path for key."""
        return self.cache_dir / f"{cache_key}.json"
    
    def _load_from_cache(self, text: str) -> Optional[List[float]]:
        """Load embedding from cache if exists."""
        cache_key = self._get_cache_key(text)
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    return data['embedding']
            except Exception as e:
                print(f"Warning: Cache read failed: {e}")
                return None
        
        return None
    
    def _save_to_cache(self, text: str, embedding: List[float]):
        """Save embedding to cache."""
        cache_key = self._get_cache_key(text)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    'text': text[:200],  # Store truncated text for reference
                    'embedding': embedding,
                    'model': self.MODEL_NAME,
                    'dimensions': len(embedding),
                    'timestamp': datetime.now().isoformat()
                }, f)
        except Exception as e:
            print(f"Warning: Cache write failed: {e}")
    
    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.MIN_DELAY_SECONDS:
            sleep_time = self.MIN_DELAY_SECONDS - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def generate_embedding(self, text: str, use_cache: bool = True) -> Tuple[List[float], Dict]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            use_cache: Whether to use cached embeddings
        
        Returns:
            (embedding_vector, metadata)
            - embedding_vector: List of floats (768 dimensions)
            - metadata: Dict with model info, timing, cache hit status
        """
        start_time = time.time()
        
        # Check cache first
        if use_cache:
            cached = self._load_from_cache(text)
            if cached is not None:
                return cached, {
                    'model': self.MODEL_NAME,
                    'model_version': self.MODEL_VERSION,
                    'dimensions': len(cached),
                    'cache_hit': True,
                    'duration_ms': int((time.time() - start_time) * 1000),
                    'timestamp': datetime.now().isoformat()
                }
        
        # Generate new embedding with retry logic
        embedding = self._generate_with_retry(text)
        
        # Cache the result
        if use_cache:
            self._save_to_cache(text, embedding)
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        return embedding, {
            'model': self.MODEL_NAME,
            'model_version': self.MODEL_VERSION,
            'dimensions': len(embedding),
            'cache_hit': False,
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_with_retry(self, text: str) -> List[float]:
        """
        Generate embedding with exponential backoff retry.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        
        Raises:
            Exception if all retries exhausted
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                # Rate limit before request
                self._rate_limit()
                
                # Call Gemini API
                result = genai.embed_content(
                    model=self.MODEL_NAME,
                    content=text,
                    task_type="retrieval_document"
                )
                
                return result['embedding']
            
            except Exception as e:
                error_msg = str(e)
                
                # Check if rate limit error
                if "429" in error_msg or "ResourceExhausted" in error_msg:
                    wait_time = (self.RETRY_DELAY_BASE ** attempt) * 60  # Wait longer for rate limits
                    print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt+1}/{self.MAX_RETRIES}")
                    time.sleep(wait_time)
                    continue
                
                # Other errors
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAY_BASE ** attempt
                    print(f"Error generating embedding: {error_msg}")
                    print(f"Retry {attempt+1}/{self.MAX_RETRIES} after {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Failed to generate embedding after {self.MAX_RETRIES} attempts: {error_msg}")
        
        raise Exception(f"Failed to generate embedding after {self.MAX_RETRIES} attempts")
    
    def generate_batch(
        self,
        texts: List[str],
        use_cache: bool = True,
        show_progress: bool = True
    ) -> List[Tuple[List[float], Dict]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            use_cache: Whether to use cached embeddings
            show_progress: Whether to print progress
        
        Returns:
            List of (embedding, metadata) tuples
        """
        results = []
        total = len(texts)
        cache_hits = 0
        
        for i, text in enumerate(texts, 1):
            if show_progress and i % 10 == 0:
                print(f"Progress: {i}/{total} embeddings generated ({cache_hits} cache hits)")
            
            try:
                embedding, metadata = self.generate_embedding(text, use_cache)
                results.append((embedding, metadata))
                
                if metadata['cache_hit']:
                    cache_hits += 1
            
            except Exception as e:
                print(f"Error processing text {i}: {e}")
                results.append((None, {'error': str(e)}))
        
        if show_progress:
            print(f"Batch complete: {total} texts, {cache_hits} cache hits, {total - cache_hits} API calls")
        
        return results
    
    def prepare_pattern_text(self, pattern: Dict) -> str:
        """
        Prepare pattern data for embedding.
        
        Concatenates key fields: name, reasoning, description, metadata.
        
        Args:
            pattern: Pattern dictionary from Neo4j
        
        Returns:
            Concatenated text string optimized for embedding
        """
        components = []
        
        # Pattern name
        if 'name' in pattern and pattern['name']:
            components.append(f"Pattern: {pattern['name']}")
        
        # Primary reasoning
        if 'reasoning' in pattern and pattern['reasoning']:
            components.append(f"Approach: {pattern['reasoning']}")
        
        # Description
        if 'description' in pattern and pattern['description']:
            components.append(f"Description: {pattern['description']}")
        
        # Metadata for context
        if 'stars' in pattern and pattern['stars']:
            stars = pattern['stars']
            if stars > 10000:
                popularity = "highly popular"
            elif stars > 5000:
                popularity = "popular"
            else:
                popularity = "established"
            components.append(f"Popularity: {popularity} ({stars} stars)")
        
        if 'confidence' in pattern and pattern['confidence']:
            components.append(f"Confidence: {pattern['confidence']}")
        
        # Join components
        return " | ".join(components)
    
    def get_stats(self) -> Dict:
        """Get statistics about embedding generation."""
        cache_files = list(self.cache_dir.glob("*.json"))
        
        return {
            'total_requests': self.request_count,
            'cached_embeddings': len(cache_files),
            'cache_directory': str(self.cache_dir),
            'model': self.MODEL_NAME,
            'model_version': self.MODEL_VERSION,
            'dimensions': self.EMBEDDING_DIMENSIONS
        }


def test_embedding_generator():
    """Test the embedding generator with sample text."""
    print("Testing EmbeddingGenerator...")
    
    generator = EmbeddingGenerator()
    
    # Test single embedding
    test_text = "Microkernel architecture with plugin-based extensibility for desktop applications"
    print(f"\nGenerating embedding for: '{test_text[:60]}...'")
    
    embedding, metadata = generator.generate_embedding(test_text)
    
    print(f"\nResults:")
    print(f"  Dimensions: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
    print(f"  Metadata: {metadata}")
    
    # Test cache hit
    print("\nTesting cache...")
    embedding2, metadata2 = generator.generate_embedding(test_text)
    print(f"  Cache hit: {metadata2['cache_hit']}")
    print(f"  Duration: {metadata2['duration_ms']}ms (should be very fast)")
    
    # Test batch
    print("\nTesting batch generation...")
    test_texts = [
        "Web application with React and TypeScript",
        "Command-line tool for file management",
        "Real-time messaging with WebSocket support"
    ]
    
    results = generator.generate_batch(test_texts, show_progress=True)
    print(f"\nBatch results: {len(results)} embeddings generated")
    
    # Print stats
    print("\nGenerator statistics:")
    stats = generator.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nTest complete!")


if __name__ == "__main__":
    test_embedding_generator()
