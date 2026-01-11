"""
Generate Pattern Embeddings for Knowledge Graph

Batch processes all Pattern nodes in Neo4j, generates embeddings using Gemini,
and stores them back in the graph with metadata.
"""

import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
import argparse
from dotenv import load_dotenv
from neo4j import GraphDatabase
from embedding_generator import EmbeddingGenerator

load_dotenv()


class PatternEmbeddingPipeline:
    """
    Pipeline for generating and storing pattern embeddings in Neo4j.
    """
    
    def __init__(self, batch_size: int = 50, force_regenerate: bool = False):
        """
        Initialize the embedding pipeline.
        
        Args:
            batch_size: Number of patterns to process per batch
            force_regenerate: If True, regenerate embeddings even if they exist
        """
        # Initialize embedding generator
        self.generator = EmbeddingGenerator()
        
        # Connect to Neo4j
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        
        if not neo4j_password:
            raise ValueError("NEO4J_PASSWORD not set in environment")
        
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        self.batch_size = batch_size
        self.force_regenerate = force_regenerate
        
        print("PatternEmbeddingPipeline initialized:")
        print(f"  Neo4j: {neo4j_uri}")
        print(f"  Batch size: {batch_size}")
        print(f"  Force regenerate: {force_regenerate}")
    
    def close(self):
        """Close database connection."""
        self.driver.close()
    
    def get_pattern_count(self) -> Dict[str, int]:
        """Get count of patterns with and without embeddings."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                RETURN count(p) AS total,
                       count(p.embedding) AS with_embeddings,
                       count(p) - count(p.embedding) AS without_embeddings
            """)
            record = result.single()
            return dict(record)
    
    def get_patterns_batch(self, skip: int, limit: int) -> List[Dict]:
        """
        Fetch a batch of patterns from Neo4j.
        
        Args:
            skip: Number of patterns to skip
            limit: Number of patterns to fetch
        
        Returns:
            List of pattern dictionaries
        """
        with self.driver.session() as session:
            if self.force_regenerate:
                # Get all patterns regardless of embedding status
                query = """
                    MATCH (p:Pattern)
                    RETURN p.name AS name,
                           p.reasoning AS reasoning,
                           p.description AS description,
                           p.stars AS stars,
                           p.confidence AS confidence,
                           p.source_repo AS source_repo,
                           elementId(p) AS element_id
                    ORDER BY p.name
                    SKIP $skip
                    LIMIT $limit
                """
            else:
                # Only get patterns without embeddings
                query = """
                    MATCH (p:Pattern)
                    WHERE p.embedding IS NULL
                    RETURN p.name AS name,
                           p.reasoning AS reasoning,
                           p.description AS description,
                           p.stars AS stars,
                           p.confidence AS confidence,
                           p.source_repo AS source_repo,
                           elementId(p) AS element_id
                    ORDER BY p.name
                    SKIP $skip
                    LIMIT $limit
                """
            
            result = session.run(query, skip=skip, limit=limit)
            return [dict(record) for record in result]
    
    def update_pattern_embedding(
        self,
        element_id: str,
        embedding: List[float],
        metadata: Dict
    ):
        """
        Update pattern node with embedding and metadata.
        
        Args:
            element_id: Neo4j element ID of pattern node
            embedding: Embedding vector (768 dimensions)
            metadata: Embedding metadata (model, version, date)
        """
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Pattern)
                WHERE elementId(p) = $element_id
                SET p.embedding = $embedding,
                    p.embedding_model = $model,
                    p.embedding_version = $version,
                    p.embedding_date = datetime($date)
            """,
                element_id=element_id,
                embedding=embedding,
                model=metadata['model'],
                version=metadata['model_version'],
                date=metadata['timestamp']
            )
    
    def process_batch(self, patterns: List[Dict]) -> Dict[str, int]:
        """
        Process a batch of patterns: generate embeddings and update Neo4j.
        
        Args:
            patterns: List of pattern dictionaries
        
        Returns:
            Statistics dictionary (success, failed counts)
        """
        if not patterns:
            return {'success': 0, 'failed': 0, 'skipped': 0}
        
        stats = {'success': 0, 'failed': 0, 'skipped': 0}
        
        # Prepare texts for embedding
        texts = []
        for pattern in patterns:
            text = self.generator.prepare_pattern_text(pattern)
            texts.append(text)
        
        # Generate embeddings (batch)
        results = self.generator.generate_batch(texts, use_cache=True, show_progress=False)
        
        # Update Neo4j with embeddings
        for pattern, (embedding, metadata) in zip(patterns, results):
            if embedding is None:
                print(f"  ✗ Failed: {pattern['name']} - {metadata.get('error', 'Unknown error')}")
                stats['failed'] += 1
                continue
            
            try:
                self.update_pattern_embedding(
                    element_id=pattern['element_id'],
                    embedding=embedding,
                    metadata=metadata
                )
                
                cache_indicator = "📦" if metadata.get('cache_hit') else "🔄"
                print(f"  ✓ {cache_indicator} {pattern['name']} ({metadata['duration_ms']}ms)")
                stats['success'] += 1
            
            except Exception as e:
                print(f"  ✗ Failed to update Neo4j: {pattern['name']} - {e}")
                stats['failed'] += 1
        
        return stats
    
    def run(self):
        """
        Run the complete embedding generation pipeline.
        """
        print("\n" + "="*70)
        print("PATTERN EMBEDDING GENERATION PIPELINE")
        print("="*70)
        
        # Get initial counts
        counts = self.get_pattern_count()
        total_patterns = counts['total']
        with_embeddings = counts['with_embeddings']
        without_embeddings = counts['without_embeddings']
        
        print(f"\nInitial Status:")
        print(f"  Total patterns: {total_patterns}")
        print(f"  With embeddings: {with_embeddings}")
        print(f"  Without embeddings: {without_embeddings}")
        
        if without_embeddings == 0 and not self.force_regenerate:
            print("\n✓ All patterns already have embeddings!")
            print("  Use --force to regenerate all embeddings.")
            return
        
        # Determine how many to process
        to_process = total_patterns if self.force_regenerate else without_embeddings
        
        print(f"\nProcessing {to_process} patterns...")
        print(f"Batch size: {self.batch_size}")
        print("="*70 + "\n")
        
        # Process in batches
        total_stats = {'success': 0, 'failed': 0, 'skipped': 0}
        processed = 0
        
        while processed < to_process:
            batch_num = (processed // self.batch_size) + 1
            print(f"Batch {batch_num}: Processing patterns {processed+1}-{min(processed+self.batch_size, to_process)}...")
            
            # Fetch batch
            patterns = self.get_patterns_batch(processed, self.batch_size)
            
            if not patterns:
                break
            
            # Process batch
            batch_stats = self.process_batch(patterns)
            
            # Update totals
            for key in total_stats:
                total_stats[key] += batch_stats[key]
            
            processed += len(patterns)
            
            print(f"  Batch complete: {batch_stats['success']} success, {batch_stats['failed']} failed\n")
        
        # Final report
        print("="*70)
        print("GENERATION COMPLETE")
        print("="*70)
        print(f"\nResults:")
        print(f"  Success: {total_stats['success']}")
        print(f"  Failed: {total_stats['failed']}")
        print(f"  Total processed: {processed}")
        
        # Final counts
        final_counts = self.get_pattern_count()
        print(f"\nFinal Status:")
        print(f"  Total patterns: {final_counts['total']}")
        print(f"  With embeddings: {final_counts['with_embeddings']}")
        print(f"  Without embeddings: {final_counts['without_embeddings']}")
        
        # Generator stats
        print(f"\nEmbedding Generator Statistics:")
        gen_stats = self.generator.get_stats()
        for key, value in gen_stats.items():
            print(f"  {key}: {value}")
        
        print("\n✓ Pipeline complete!")
        
        if final_counts['without_embeddings'] == 0:
            print("\n✓ All patterns now have embeddings!")
            print("  Next step: Run test_vector_search.py to validate")
        else:
            print(f"\n⚠ Warning: {final_counts['without_embeddings']} patterns still missing embeddings")
            print("  Review errors above and re-run if needed")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate embeddings for patterns in Neo4j knowledge graph"
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Number of patterns to process per batch (default: 50)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force regenerate embeddings even if they exist'
    )
    
    args = parser.parse_args()
    
    try:
        pipeline = PatternEmbeddingPipeline(
            batch_size=args.batch_size,
            force_regenerate=args.force
        )
        
        pipeline.run()
        pipeline.close()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
