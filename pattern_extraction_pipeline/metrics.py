"""
Metrics Collection

Lightweight metrics collection for tracking extraction pipeline performance.
Provides counters and timers for monitoring operation success/failure rates and durations.
"""

from collections import defaultdict
import time
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Metrics:
    """
    Simple metrics collector for tracking counters and timers.
    
    Features:
    - Increment counters for events (e.g., 'rules_extracted', 'errors')
    - Start/stop timers for operations
    - Generate summary reports
    
    Example:
        >>> metrics = Metrics()
        >>> metrics.increment('rules_extracted')
        >>> metrics.start_timer('rule_extraction')
        >>> # ... do work ...
        >>> metrics.end_timer('rule_extraction')
        >>> print(metrics.get_report())
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize metrics collector.
        
        Args:
            name: Optional name for this metrics instance
        """
        self.name = name or "metrics"
        self.counters = defaultdict(int)
        self.timers = {}
        self._timer_history = defaultdict(list)
        self._start_time = time.time()
    
    def increment(self, metric_name: str, value: int = 1):
        """
        Increment a counter metric.
        
        Args:
            metric_name: Name of the metric (e.g., 'rules_extracted')
            value: Amount to increment (default: 1)
        """
        self.counters[metric_name] += value
        logger.debug(f"Metric '{metric_name}' incremented by {value} (now: {self.counters[metric_name]})")
    
    def set(self, metric_name: str, value: int):
        """
        Set a counter to a specific value.
        
        Args:
            metric_name: Name of the metric
            value: Value to set
        """
        self.counters[metric_name] = value
        logger.debug(f"Metric '{metric_name}' set to {value}")
    
    def start_timer(self, timer_name: str):
        """
        Start a timer for an operation.
        
        Args:
            timer_name: Name of the operation
        """
        self.timers[timer_name] = time.time()
        logger.debug(f"Timer '{timer_name}' started")
    
    def end_timer(self, timer_name: str) -> Optional[float]:
        """
        End a timer and record the duration.
        
        Args:
            timer_name: Name of the operation
        
        Returns:
            float: Duration in seconds, or None if timer not found
        """
        if timer_name not in self.timers:
            logger.warning(f"Timer '{timer_name}' not found (not started?)")
            return None
        
        duration = time.time() - self.timers[timer_name]
        del self.timers[timer_name]
        
        # Store duration in history for averaging
        self._timer_history[timer_name].append(duration)
        
        # Also store as a counter for the latest duration
        self.counters[f"{timer_name}.duration_ms"] = int(duration * 1000)
        
        logger.debug(f"Timer '{timer_name}' ended: {duration:.3f}s")
        return duration
    
    def get_timer_stats(self, timer_name: str) -> Dict[str, float]:
        """
        Get statistics for a timer.
        
        Args:
            timer_name: Name of the timer
        
        Returns:
            dict: Statistics including count, total, avg, min, max
        """
        if timer_name not in self._timer_history:
            return {}
        
        durations = self._timer_history[timer_name]
        
        return {
            'count': len(durations),
            'total_seconds': sum(durations),
            'avg_seconds': sum(durations) / len(durations),
            'min_seconds': min(durations),
            'max_seconds': max(durations)
        }
    
    def get_report(self) -> Dict:
        """
        Get a summary report of all metrics.
        
        Returns:
            dict: Complete metrics report
        """
        elapsed = time.time() - self._start_time
        
        report = {
            'name': self.name,
            'elapsed_seconds': round(elapsed, 2),
            'counters': dict(self.counters),
            'timers': {
                name: self.get_timer_stats(name)
                for name in self._timer_history.keys()
            }
        }
        
        return report
    
    def print_report(self):
        """Print a human-readable metrics report."""
        report = self.get_report()
        
        print(f"\n{'='*60}")
        print(f"METRICS REPORT: {report['name']}")
        print(f"{'='*60}")
        print(f"Elapsed time: {report['elapsed_seconds']:.2f}s")
        
        if report['counters']:
            print(f"\nCounters:")
            for name, value in sorted(report['counters'].items()):
                if not name.endswith('_ms'):  # Skip duration counters (shown in timers)
                    print(f"  {name}: {value}")
        
        if report['timers']:
            print(f"\nTimers:")
            for name, stats in sorted(report['timers'].items()):
                if stats:
                    print(f"  {name}:")
                    print(f"    Count: {stats['count']}")
                    print(f"    Total: {stats['total_seconds']:.2f}s")
                    print(f"    Average: {stats['avg_seconds']:.3f}s")
                    print(f"    Min: {stats['min_seconds']:.3f}s")
                    print(f"    Max: {stats['max_seconds']:.3f}s")
        
        print(f"{'='*60}\n")
    
    def reset(self):
        """Reset all metrics."""
        self.counters.clear()
        self.timers.clear()
        self._timer_history.clear()
        self._start_time = time.time()
        logger.info(f"Metrics '{self.name}' reset")


class MetricsRegistry:
    """
    Registry for managing multiple Metrics instances.
    
    Useful when you want separate metrics for different components
    (e.g., 'pattern_extraction', 'rule_extraction', 'database').
    
    Example:
        >>> registry = MetricsRegistry()
        >>> registry.get('pattern_extraction').increment('extracted')
        >>> registry.get('rule_extraction').increment('extracted')
        >>> registry.print_all_reports()
    """
    
    def __init__(self):
        self._metrics = {}
    
    def get(self, name: str) -> Metrics:
        """
        Get or create a metrics instance.
        
        Args:
            name: Name of the metrics instance
        
        Returns:
            Metrics instance
        """
        if name not in self._metrics:
            self._metrics[name] = Metrics(name=name)
        return self._metrics[name]
    
    def get_all_reports(self) -> Dict[str, Dict]:
        """Get reports for all metrics instances."""
        return {name: metrics.get_report() for name, metrics in self._metrics.items()}
    
    def print_all_reports(self):
        """Print reports for all metrics instances."""
        for metrics in self._metrics.values():
            metrics.print_report()
    
    def reset_all(self):
        """Reset all metrics instances."""
        for metrics in self._metrics.values():
            metrics.reset()
