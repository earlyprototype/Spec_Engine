#!/usr/bin/env python3
"""Track scan/extraction progress with checkpoint/resume capability"""

import json
from pathlib import Path
from typing import Dict, Set, Optional
from datetime import datetime


class ProgressTracker:
    """Track scan/extraction progress with checkpoint/resume"""
    
    def __init__(self, checkpoint_file: str = 'extraction_progress.json'):
        self.checkpoint_file = Path(checkpoint_file)
        self.processed: Set[str] = set()
        self.failed: Dict[str, str] = {}
        self.stats = {
            'total_attempted': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'last_update': None
        }
        self._load_checkpoint()
    
    def _load_checkpoint(self):
        """Load progress from checkpoint file"""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'r') as f:
                    data = json.load(f)
                    self.processed = set(data.get('processed', []))
                    self.failed = data.get('failed', {})
                    self.stats = data.get('stats', self.stats)
                    print(f"Loaded checkpoint: {len(self.processed)} already processed")
            except Exception as e:
                print(f"Warning: Could not load checkpoint: {e}")
    
    def is_processed(self, repo_url: str, file_path: str = None) -> bool:
        """Check if item already processed"""
        if file_path:
            key = f"{repo_url}:{file_path}"
        else:
            key = repo_url
        return key in self.processed
    
    def mark_processed(self, repo_url: str, file_path: str = None, success: bool = True, error: str = None):
        """Mark item as processed and update stats"""
        if file_path:
            key = f"{repo_url}:{file_path}"
        else:
            key = repo_url
        
        self.processed.add(key)
        
        if success:
            self.stats['successful'] += 1
        else:
            self.stats['failed'] += 1
            if error:
                self.failed[key] = error
        
        self.stats['total_attempted'] += 1
        self.stats['last_update'] = datetime.utcnow().isoformat()
        
        # Save checkpoint every 10 items
        if self.stats['total_attempted'] % 10 == 0:
            self.save_checkpoint()
    
    def mark_skipped(self, repo_url: str, file_path: str = None):
        """Mark item as skipped (already in database)"""
        if file_path:
            key = f"{repo_url}:{file_path}"
        else:
            key = repo_url
        
        self.processed.add(key)
        self.stats['skipped'] += 1
        self.stats['total_attempted'] += 1
        self.stats['last_update'] = datetime.utcnow().isoformat()
    
    def save_checkpoint(self):
        """Save current progress to checkpoint file"""
        try:
            data = {
                'processed': list(self.processed),
                'failed': self.failed,
                'stats': self.stats,
                'saved_at': datetime.utcnow().isoformat()
            }
            
            with open(self.checkpoint_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save checkpoint: {e}")
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return self.stats.copy()
    
    def get_failed_items(self) -> Dict[str, str]:
        """Get dictionary of failed items and their errors"""
        return self.failed.copy()
    
    def clear_checkpoint(self):
        """Clear checkpoint file (for starting fresh)"""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
        self.processed = set()
        self.failed = {}
        self.stats = {
            'total_attempted': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'last_update': None
        }
