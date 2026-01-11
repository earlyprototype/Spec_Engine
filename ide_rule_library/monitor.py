#!/usr/bin/env python3
"""Real-time monitor for IDE Rule extraction progress"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from collections import deque


def load_progress():
    """Load current progress stats"""
    progress_file = Path('extraction_progress.json')
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            return json.load(f)
    return None


def load_log_tail(lines=30):
    """Get last N lines from log file"""
    log_file = Path('logs/ide_rule_library.log')
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            # Read last N lines efficiently
            return deque(f, maxlen=lines)
    except:
        return []


def parse_log_line(line):
    """Parse JSON log line and extract key info"""
    try:
        log_entry = json.loads(line)
        timestamp = log_entry.get('timestamp', '')
        level = log_entry.get('level', '')
        message = log_entry.get('message', '')
        return f"[{timestamp[-8:]}] {level}: {message}"
    except:
        return line.strip()


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def calculate_eta(stats):
    """Calculate estimated time remaining"""
    if not stats or stats.get('total_attempted', 0) == 0:
        return "Unknown"
    
    total = stats['total_attempted']
    successful = stats['successful']
    failed = stats['failed']
    
    # Estimate total files (rough guess based on scan results)
    estimated_total = 800
    remaining = estimated_total - total
    
    if remaining <= 0:
        return "Complete"
    
    # Estimate rate (files per second)
    # Assuming ~2-3 files per minute = ~0.04 files/sec
    rate = 0.04  # Conservative estimate
    
    seconds_remaining = remaining / rate
    hours = int(seconds_remaining // 3600)
    minutes = int((seconds_remaining % 3600) // 60)
    
    if hours > 0:
        return f"~{hours}h {minutes}m"
    else:
        return f"~{minutes}m"


def monitor_loop(refresh_seconds=5):
    """Main monitoring loop"""
    print("Starting IDE Rule Library Monitor...")
    print("Press Ctrl+C to exit\n")
    time.sleep(2)
    
    last_total = 0
    
    try:
        while True:
            clear_screen()
            
            # Header
            print("=" * 80)
            print("IDE RULE LIBRARY - EXTRACTION MONITOR")
            print("=" * 80)
            print(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
            print()
            
            # Load current stats
            progress = load_progress()
            
            if not progress:
                print("No progress data found. Is extraction running?")
                print("\nStart extraction with:")
                print("  python scan_existing_patterns.py --extract")
            else:
                stats = progress['stats']
                
                # Progress stats
                print("EXTRACTION PROGRESS")
                print("-" * 80)
                total = stats['total_attempted']
                successful = stats['successful']
                failed = stats['failed']
                skipped = stats['skipped']
                
                success_rate = (successful / total * 100) if total > 0 else 0
                
                print(f"Total Attempts:    {total}")
                print(f"  Successfully stored:  {successful}")
                print(f"  Failed:               {failed}")
                print(f"  Skipped (duplicate):  {skipped}")
                print(f"\nSuccess Rate:      {success_rate:.1f}%")
                
                # Calculate velocity
                if last_total > 0:
                    velocity = (total - last_total) / refresh_seconds
                    print(f"Velocity:          {velocity * 60:.1f} files/minute")
                
                last_total = total
                
                # ETA
                eta = calculate_eta(stats)
                print(f"Estimated ETA:     {eta}")
                
                print()
                
                # Recent activity
                print("RECENT ACTIVITY (last 15 log entries)")
                print("-" * 80)
                
                log_lines = load_log_tail(15)
                if log_lines:
                    for line in log_lines:
                        parsed = parse_log_line(line)
                        # Color code by level
                        if 'ERROR' in parsed:
                            print(f"\033[91m{parsed}\033[0m")  # Red
                        elif 'Successfully stored' in parsed:
                            print(f"\033[92m{parsed}\033[0m")  # Green
                        elif 'Extracting' in parsed:
                            print(f"\033[94m{parsed}\033[0m")  # Blue
                        else:
                            print(parsed)
                else:
                    print("No recent log entries")
                
                print()
                print("=" * 80)
                print(f"Refreshing in {refresh_seconds}s... (Press Ctrl+C to exit)")
            
            time.sleep(refresh_seconds)
            
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "=" * 80)
        print("MONITOR STOPPED")
        print("=" * 80)
        
        # Final summary
        progress = load_progress()
        if progress:
            stats = progress['stats']
            print(f"\nFinal Statistics:")
            print(f"  Total processed:    {stats['total_attempted']}")
            print(f"  Successfully stored: {stats['successful']}")
            print(f"  Failed:             {stats['failed']}")
            print(f"  Success rate:       {stats['successful']/stats['total_attempted']*100:.1f}%")
        
        print("\nExtraction is still running in the background.")
        print("Run this monitor again anytime to check progress.\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor IDE Rule extraction progress')
    parser.add_argument('--refresh', type=int, default=5, 
                       help='Refresh interval in seconds (default: 5)')
    
    args = parser.parse_args()
    
    # Change to ide_rule_library directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    monitor_loop(args.refresh)
