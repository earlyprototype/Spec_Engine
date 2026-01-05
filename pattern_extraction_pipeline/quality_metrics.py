# quality_metrics.py
# Calculate quality scores for GitHub repositories

from datetime import datetime, timezone
from typing import Dict


class QualityMetricsCalculator:
    """
    Calculate multi-dimensional quality scores for GitHub repositories.
    Goes beyond just star counts to measure actual quality.
    """
    
    def calculate_quality_score(self, repo) -> Dict[str, float]:
        """
        Calculate composite quality score from multiple signals.
        
        Args:
            repo: PyGithub Repository object
        
        Returns:
            {
                'composite_score': 0.85,  # Overall quality (0-1)
                'popularity_score': 0.9,
                'maintenance_score': 0.85,
                'maturity_score': 0.8,
                'community_score': 0.9,
                'freshness_score': 0.95
            }
        """
        
        popularity = self._calculate_popularity(repo)
        maintenance = self._calculate_maintenance(repo)
        maturity = self._calculate_maturity(repo)
        community = self._calculate_community(repo)
        freshness = self._calculate_freshness(repo)
        
        # Weighted composite score
        composite = (
            popularity * 0.30 +
            maintenance * 0.25 +
            maturity * 0.20 +
            community * 0.15 +
            freshness * 0.10
        )
        
        return {
            'composite_score': round(composite, 3),
            'popularity_score': round(popularity, 3),
            'maintenance_score': round(maintenance, 3),
            'maturity_score': round(maturity, 3),
            'community_score': round(community, 3),
            'freshness_score': round(freshness, 3),
            
            # Raw metrics for storage
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'watchers': repo.watchers_count,
            'open_issues': repo.open_issues_count,
            'contributors': repo.get_contributors().totalCount if hasattr(repo, 'get_contributors') else 0,
            'repo_age_months': self._get_repo_age_months(repo),
            'days_since_update': self._get_days_since_update(repo)
        }
    
    def _calculate_popularity(self, repo) -> float:
        """
        Popularity score based on stars, forks, watchers.
        
        Scoring:
        - Stars: logarithmic scale (1K = 0.5, 10K = 0.75, 100K = 1.0)
        - Forks: indicates people actually use it
        - Watchers: indicates ongoing interest
        """
        stars = repo.stargazers_count
        forks = repo.forks_count
        watchers = repo.watchers_count
        
        # Logarithmic star scoring
        if stars >= 100000:
            star_score = 1.0
        elif stars >= 50000:
            star_score = 0.95
        elif stars >= 20000:
            star_score = 0.9
        elif stars >= 10000:
            star_score = 0.85
        elif stars >= 5000:
            star_score = 0.75
        elif stars >= 2000:
            star_score = 0.65
        elif stars >= 1000:
            star_score = 0.5
        elif stars >= 500:
            star_score = 0.35
        else:
            star_score = 0.2
        
        # Fork ratio (indicates active use)
        fork_ratio = min(forks / max(stars, 1), 1.0)  # Cap at 1.0
        fork_score = fork_ratio * 0.5 + 0.5  # Scale to 0.5-1.0
        
        # Watcher ratio
        watcher_ratio = min(watchers / max(stars, 1), 1.0)
        watcher_score = watcher_ratio * 0.5 + 0.5
        
        # Weighted average
        popularity = (star_score * 0.6 + fork_score * 0.25 + watcher_score * 0.15)
        
        return min(popularity, 1.0)
    
    def _calculate_maintenance(self, repo) -> float:
        """
        Maintenance score based on activity and responsiveness.
        
        Signals:
        - Recent commits (is it actively maintained?)
        - Issue resolution (how responsive are maintainers?)
        - Issue ratio (healthy balance of open vs closed)
        """
        days_since_update = self._get_days_since_update(repo)
        
        # Recency scoring
        if days_since_update <= 7:
            recency_score = 1.0  # Updated this week
        elif days_since_update <= 30:
            recency_score = 0.9  # Updated this month
        elif days_since_update <= 90:
            recency_score = 0.75  # Updated this quarter
        elif days_since_update <= 180:
            recency_score = 0.6  # Updated this half-year
        elif days_since_update <= 365:
            recency_score = 0.4  # Updated this year
        else:
            recency_score = 0.2  # Potentially abandoned
        
        # Issue health (prefer repos with some but not too many open issues)
        open_issues = repo.open_issues_count
        
        if open_issues == 0:
            issue_score = 0.7  # Either no issues or not tracked
        elif open_issues <= 10:
            issue_score = 1.0  # Healthy
        elif open_issues <= 50:
            issue_score = 0.85  # Active but manageable
        elif open_issues <= 200:
            issue_score = 0.6  # Busy but might be ok
        else:
            issue_score = 0.4  # Potentially overwhelmed
        
        maintenance = (recency_score * 0.7 + issue_score * 0.3)
        
        return min(maintenance, 1.0)
    
    def _calculate_maturity(self, repo) -> float:
        """
        Maturity score based on age and stability.
        
        Sweet spot: 1-3 years old (proven but not ancient)
        """
        age_months = self._get_repo_age_months(repo)
        
        if age_months < 3:
            maturity_score = 0.4  # Too new, unproven
        elif age_months < 6:
            maturity_score = 0.6  # Young but showing promise
        elif age_months < 12:
            maturity_score = 0.8  # Established
        elif age_months < 24:
            maturity_score = 1.0  # Sweet spot: proven
        elif age_months < 36:
            maturity_score = 0.95  # Mature
        elif age_months < 48:
            maturity_score = 0.85  # Older but still relevant
        else:
            # Decay over time (may be outdated)
            years = age_months / 12
            maturity_score = max(0.5 - (years - 4) * 0.05, 0.3)
        
        return min(maturity_score, 1.0)
    
    def _calculate_community(self, repo) -> float:
        """
        Community score based on contributor activity and documentation.
        
        Signals:
        - Has description
        - Has README
        - Has license
        - Multiple contributors (not a one-person project)
        """
        score = 0.5  # Base score
        
        # Has description
        if repo.description:
            score += 0.1
        
        # Has README (most repos do)
        try:
            repo.get_readme()
            score += 0.1
        except:
            pass
        
        # Has license
        if repo.license:
            score += 0.15
        
        # Contributors (indicates community involvement)
        try:
            contributor_count = repo.get_contributors().totalCount
            if contributor_count >= 50:
                score += 0.15  # Large community
            elif contributor_count >= 20:
                score += 0.1  # Active community
            elif contributor_count >= 5:
                score += 0.05  # Small team
            # else: single maintainer or very small
        except:
            pass
        
        return min(score, 1.0)
    
    def _calculate_freshness(self, repo) -> float:
        """
        How fresh/current is this pattern?
        
        Same as maintenance recency but scaled differently.
        """
        days_since_update = self._get_days_since_update(repo)
        
        if days_since_update <= 30:
            return 1.0
        elif days_since_update <= 90:
            return 0.95
        elif days_since_update <= 180:
            return 0.85
        elif days_since_update <= 365:
            return 0.7
        elif days_since_update <= 730:
            return 0.5
        else:
            return 0.3
    
    def _get_repo_age_months(self, repo) -> int:
        """Calculate repo age in months."""
        created_at = repo.created_at
        now = datetime.now(timezone.utc)
        delta = now - created_at
        return int(delta.days / 30)
    
    def _get_days_since_update(self, repo) -> int:
        """Calculate days since last update."""
        updated_at = repo.updated_at
        now = datetime.now(timezone.utc)
        delta = now - updated_at
        return delta.days
    
    def get_quality_tier(self, composite_score: float) -> str:
        """
        Convert composite score to human-readable tier.
        
        Returns: 'excellent' | 'high' | 'good' | 'moderate' | 'low'
        """
        if composite_score >= 0.85:
            return 'excellent'
        elif composite_score >= 0.75:
            return 'high'
        elif composite_score >= 0.65:
            return 'good'
        elif composite_score >= 0.5:
            return 'moderate'
        else:
            return 'low'
    
    def get_maintenance_status(self, maintenance_score: float, days_since_update: int) -> str:
        """
        Get maintenance status label.
        
        Returns: 'active' | 'maintained' | 'stale' | 'abandoned'
        """
        if days_since_update <= 30 and maintenance_score >= 0.8:
            return 'active'
        elif days_since_update <= 180 and maintenance_score >= 0.6:
            return 'maintained'
        elif days_since_update <= 365:
            return 'stale'
        else:
            return 'abandoned'


# ============================================================================
# Convenience functions
# ============================================================================

def calculate_repo_quality(repo) -> Dict:
    """Quick function to calculate repo quality."""
    calculator = QualityMetricsCalculator()
    return calculator.calculate_quality_score(repo)


def get_quality_summary(repo) -> str:
    """Get human-readable quality summary."""
    calculator = QualityMetricsCalculator()
    metrics = calculator.calculate_quality_score(repo)
    
    tier = calculator.get_quality_tier(metrics['composite_score'])
    status = calculator.get_maintenance_status(
        metrics['maintenance_score'],
        metrics['days_since_update']
    )
    
    return f"{tier.capitalize()} quality, {status} ({metrics['stars']} stars, updated {metrics['days_since_update']} days ago)"


if __name__ == "__main__":
    # Example usage
    from github import Github
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    g = Github(os.getenv("GITHUB_TOKEN"))
    
    # Test with a well-known repo
    repo = g.get_repo("facebook/react")
    
    calculator = QualityMetricsCalculator()
    metrics = calculator.calculate_quality_score(repo)
    
    print(f"Repository: {repo.full_name}")
    print(f"Composite Score: {metrics['composite_score']}")
    print(f"  Popularity: {metrics['popularity_score']}")
    print(f"  Maintenance: {metrics['maintenance_score']}")
    print(f"  Maturity: {metrics['maturity_score']}")
    print(f"  Community: {metrics['community_score']}")
    print(f"  Freshness: {metrics['freshness_score']}")
    print(f"\nQuality Tier: {calculator.get_quality_tier(metrics['composite_score'])}")
    print(f"Status: {calculator.get_maintenance_status(metrics['maintenance_score'], metrics['days_since_update'])}")
