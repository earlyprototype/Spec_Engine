#!/usr/bin/env python3
"""
Quality scoring system for repository assessment.

Replaces simple star count with multi-dimensional quality metrics
to prevent cargo culting from popular but unvalidated sources.
"""

from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any
import re


class RepoQualityScorer:
    """Calculate composite quality scores for repositories"""
    
    # Production signal patterns
    PRODUCTION_SIGNALS = {
        'deployment': [
            'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
            'kubernetes/', 'k8s/', '.dockerignore', 'helm/',
            'terraform/', 'ansible/', 'Makefile', 'Chart.yaml',
            'skaffold.yaml', 'tilt', 'docker-compose.yaml'
        ],
        'ci_cd': [
            '.github/workflows/', '.gitlab-ci.yml', '.circleci/',
            'Jenkinsfile', '.travis.yml', 'azure-pipelines.yml',
            '.drone.yml', 'bitbucket-pipelines.yml', 'codecov.yml',
            'sonar-project.properties'
        ],
        'monitoring': [
            'prometheus.yml', 'grafana/', 'datadog.yaml',
            'newrelic.ini', 'sentry.properties', '.sentry-release',
            'otel-config.yaml', 'opentelemetry'
        ],
        'testing': [
            'pytest.ini', '.coveragerc', 'tox.ini', 'tests/',
            'test/', 'conftest.py', '.pytest_cache',
            'coverage.xml', 'htmlcov/', 'jest.config'
        ],
        'security': [
            '.snyk', 'dependabot.yml', 'SECURITY.md',
            'bandit.yml', 'safety.json', '.github/dependabot.yml',
            'renovate.json', 'trivy.yaml'
        ],
        'documentation': [
            'docs/', 'CHANGELOG.md', 'CONTRIBUTING.md',
            'CODE_OF_CONDUCT.md', 'LICENSE', 'README.md',
            'ARCHITECTURE.md', 'ADR/', 'DESIGN.md'
        ],
        'quality_tools': [
            'ruff.toml', '.ruff.toml', 'pyproject.toml',
            '.pre-commit-config.yaml', '.editorconfig',
            'mypy.ini', '.mypy.ini', 'pylint.rc'
        ]
    }
    
    def __init__(self):
        pass
    
    def calculate_quality_score(self, repo_data: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate composite quality score (0-100) based on multiple factors.
        
        Args:
            repo_data: Dictionary containing:
                - stars: int
                - forks: int
                - created_at: datetime
                - updated_at: datetime
                - open_issues: int
                - closed_issues: int (optional)
                - contributors: list (optional)
                - files: list of file paths
                - readme_length: int (optional)
                
        Returns:
            Tuple of (total_score, breakdown_dict)
        """
        weights = {}
        
        # 1. Star velocity (not just count) - Max 20 points
        weights['star_velocity'] = self._calculate_star_velocity(repo_data)
        
        # 2. Freshness/maintenance - Max 20 points
        weights['freshness'] = self._calculate_freshness(repo_data)
        
        # 3. Issue health - Max 15 points
        weights['issue_health'] = self._calculate_issue_health(repo_data)
        
        # 4. Contributor diversity - Max 15 points
        weights['diversity'] = self._calculate_diversity(repo_data)
        
        # 5. Production readiness - Max 20 points
        weights['production_ready'] = self._calculate_production_readiness(repo_data)
        
        # 6. Documentation quality - Max 5 points
        weights['documentation'] = self._calculate_documentation(repo_data)
        
        # 7. Usage signal (fork ratio) - Max 5 points
        weights['usage_signal'] = self._calculate_usage_signal(repo_data)
        
        total_score = sum(weights.values())
        
        return round(total_score, 2), weights
    
    def _calculate_star_velocity(self, repo_data: Dict) -> float:
        """Calculate stars per year, normalized"""
        created = repo_data.get('created_at')
        if not created:
            return 0.0
            
        # Handle string dates (convert to datetime)
        if isinstance(created, str):
            try:
                created = datetime.fromisoformat(created.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return 0.0
        
        # Validate datetime object
        if not isinstance(created, datetime):
            return 0.0
            
        age_years = (datetime.now(timezone.utc) - created).days / 365.25
        age_years = max(age_years, 0.5)  # Minimum 6 months
        
        stars = repo_data.get('stars', 0)
        stars_per_year = stars / age_years
        
        # Normalize: 1000 stars/year = full score
        score = min(stars_per_year / 1000, 1.0) * 20
        
        return round(score, 2)
    
    def _calculate_freshness(self, repo_data: Dict) -> float:
        """Calculate maintenance/activity score"""
        updated = repo_data.get('updated_at')
        if not updated:
            return 0.0
        
        # Handle string dates (convert to datetime)
        if isinstance(updated, str):
            try:
                updated = datetime.fromisoformat(updated.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return 0.0
        
        # Validate datetime object
        if not isinstance(updated, datetime):
            return 0.0
            
        days_since_update = (datetime.now(timezone.utc) - updated).days
        
        if days_since_update < 30:
            return 20.0
        elif days_since_update < 90:
            return 15.0
        elif days_since_update < 180:
            return 10.0
        elif days_since_update < 365:
            return 5.0
        else:
            return 0.0
    
    def _calculate_issue_health(self, repo_data: Dict) -> float:
        """Calculate issue management quality"""
        open_issues = repo_data.get('open_issues', 0)
        closed_issues = repo_data.get('closed_issues', 0)
        
        if open_issues == 0 and closed_issues == 0:
            # No issues at all - might be new or unused
            return 7.5  # Neutral score
        
        total_issues = open_issues + closed_issues
        if total_issues == 0:
            return 7.5
            
        # Low open/total ratio = good issue management
        open_ratio = open_issues / total_issues
        score = (1 - min(open_ratio, 1.0)) * 15
        
        return round(score, 2)
    
    def _calculate_diversity(self, repo_data: Dict) -> float:
        """Calculate contributor diversity (not single person's opinion)"""
        contributors = repo_data.get('contributors', [])
        
        # Validate contributors is a list
        if not isinstance(contributors, list):
            contributors = []
        
        contributor_count = len(contributors) if contributors else 1
        
        # Normalize: 20 contributors = full score
        score = min(contributor_count / 20, 1.0) * 15
        
        return round(score, 2)
    
    def _calculate_production_readiness(self, repo_data: Dict) -> float:
        """Check for production indicators in repo files"""
        files = repo_data.get('files', [])
        if not files:
            return 0.0
        
        production_score, signals = self.assess_production_maturity(files)
        
        # Store found signals for later reference
        repo_data['production_signals'] = signals
        
        # Scale to 20 points max
        return round(production_score * 0.20, 2)
    
    def _calculate_documentation(self, repo_data: Dict) -> float:
        """Calculate documentation quality"""
        files = repo_data.get('files', [])
        
        # Validate files is a list
        if not isinstance(files, list):
            files = []
        
        score = 0.0
        
        # Key documentation files
        if 'CHANGELOG.md' in files or 'CHANGELOG' in files:
            score += 2.0
        if 'CONTRIBUTING.md' in files or 'CONTRIBUTING' in files:
            score += 1.5
        
        # README quality (length as proxy)
        readme_length = repo_data.get('readme_length', 0)
        if not isinstance(readme_length, (int, float)) or readme_length < 0:
            readme_length = 0
        
        if readme_length > 3000:
            score += 1.5
        elif readme_length > 1000:
            score += 0.5
        
        return min(score, 5.0)
    
    def _calculate_usage_signal(self, repo_data: Dict) -> float:
        """Calculate fork ratio as usage indicator"""
        stars = repo_data.get('stars', 1)
        forks = repo_data.get('forks', 0)
        
        # Validate inputs
        if not isinstance(stars, (int, float)) or stars < 1:
            stars = 1
        if not isinstance(forks, (int, float)) or forks < 0:
            forks = 0
        
        # High fork ratio = people actually USE it
        fork_ratio = forks / max(stars, 1)
        
        # Normalize: 10% fork ratio = full score
        score = min(fork_ratio * 100, 1.0) * 5
        
        return round(score, 2)
    
    def assess_production_maturity(self, files: List[str]) -> Tuple[float, Dict[str, List[str]]]:
        """
        Assess production maturity based on file patterns.
        
        Returns:
            Tuple of (score 0-100, found_signals dict)
        """
        score = 0.0
        found_signals = {}
        total_possible = sum(len(patterns) for patterns in self.PRODUCTION_SIGNALS.values())
        
        for category, patterns in self.PRODUCTION_SIGNALS.items():
            category_hits = []
            for pattern in patterns:
                # Check if pattern matches any file
                if self._pattern_matches_files(pattern, files):
                    category_hits.append(pattern)
                    score += (100.0 / total_possible)
            
            if category_hits:
                found_signals[category] = category_hits
        
        return min(score, 100.0), found_signals
    
    def _pattern_matches_files(self, pattern: str, files: List[str]) -> bool:
        """
        Check if a pattern matches any file in the list.
        
        Uses case-insensitive matching to catch variations like 'Dockerfile' vs 'dockerfile'.
        For directory patterns (ending with /), checks if path starts with or contains the directory.
        """
        pattern_lower = pattern.lower()
        
        for file in files:
            file_lower = file.lower()
            
            if pattern.endswith('/'):
                # Directory pattern - check if file path starts with directory
                # or contains it as a path component
                if file_lower.startswith(pattern_lower):
                    return True
                # Also check for directory anywhere in path (e.g., '/tests/' in 'src/tests/test_main.py')
                if f'/{pattern_lower}' in f'/{file_lower}':
                    return True
            else:
                # File pattern - check if pattern appears in filename or path
                if pattern_lower in file_lower:
                    return True
        
        return False
    
    def calculate_confidence_level(self, repo_data: Dict, quality_score: float) -> int:
        """
        Calculate confidence level (1-5) based on production signals.
        
        5 = Strong production signals, active maintenance, comprehensive testing
        3 = Some signals, decent activity
        1 = Tutorial/example code, no production indicators
        """
        signals = repo_data.get('production_signals', {})
        
        # Count categories with signals
        categories_covered = len(signals)
        
        # Check for critical production indicators
        has_deployment = 'deployment' in signals
        has_ci_cd = 'ci_cd' in signals
        has_tests = 'testing' in signals
        has_monitoring = 'monitoring' in signals
        
        # Recent activity
        days_since_update = repo_data.get('days_since_update', 999)
        is_active = days_since_update < 90
        
        # Quality threshold
        high_quality = quality_score >= 70
        medium_quality = quality_score >= 50
        
        if (categories_covered >= 5 and has_deployment and has_ci_cd and 
            has_tests and is_active and high_quality):
            return 5
        elif (categories_covered >= 4 and has_ci_cd and has_tests and 
              is_active and medium_quality):
            return 4
        elif (categories_covered >= 3 and (has_ci_cd or has_tests) and 
              medium_quality):
            return 3
        elif categories_covered >= 2:
            return 2
        else:
            return 1


def enhance_repo_metadata(repo_data: Dict) -> Dict:
    """
    Enhance repository data with quality scores and metadata.
    
    This function should be called after fetching basic repo data
    to add quality assessment fields.
    """
    scorer = RepoQualityScorer()
    
    # Calculate derived fields
    created = repo_data.get('created_at')
    updated = repo_data.get('updated_at')
    
    if created:
        repo_data['repo_age_days'] = (datetime.now(timezone.utc) - created).days
    
    if updated:
        repo_data['days_since_update'] = (datetime.now(timezone.utc) - updated).days
    
    # Calculate quality score
    quality_score, breakdown = scorer.calculate_quality_score(repo_data)
    repo_data['repo_quality_score'] = quality_score
    repo_data['quality_breakdown'] = breakdown
    
    # Add production signal flags
    signals = repo_data.get('production_signals', {})
    repo_data['has_ci_cd'] = 'ci_cd' in signals
    repo_data['has_deployment'] = 'deployment' in signals
    repo_data['has_tests'] = 'testing' in signals
    repo_data['has_monitoring'] = 'monitoring' in signals
    repo_data['has_security'] = 'security' in signals
    
    # Calculate confidence level
    repo_data['confidence_level'] = scorer.calculate_confidence_level(
        repo_data, quality_score
    )
    
    return repo_data


if __name__ == '__main__':
    # Test with sample data
    test_repo = {
        'stars': 10000,
        'forks': 1200,
        'created_at': datetime(2022, 1, 1, tzinfo=timezone.utc),
        'updated_at': datetime(2025, 12, 15, tzinfo=timezone.utc),
        'open_issues': 45,
        'closed_issues': 380,
        'contributors': ['user1', 'user2', 'user3', 'user4', 'user5'],
        'files': [
            'Dockerfile',
            '.github/workflows/ci.yml',
            'tests/test_main.py',
            'pytest.ini',
            'CHANGELOG.md',
            'README.md',
            'kubernetes/deployment.yaml',
            'prometheus.yml'
        ],
        'readme_length': 4500
    }
    
    enhanced = enhance_repo_metadata(test_repo)
    
    print("\n" + "="*60)
    print("QUALITY SCORING TEST")
    print("="*60)
    print(f"\nRepo Quality Score: {enhanced['repo_quality_score']}/100")
    print(f"Confidence Level: {enhanced['confidence_level']}/5")
    print(f"\nBreakdown:")
    for factor, score in enhanced['quality_breakdown'].items():
        print(f"  {factor:20s}: {score:5.2f}")
    print(f"\nProduction Signals:")
    for category, signals in enhanced.get('production_signals', {}).items():
        print(f"  {category:15s}: {', '.join(signals[:3])}")
