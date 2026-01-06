# trajectory_logger.py
# Agent Trajectory Logging - Structured logging for complete extraction paths
# Tracks all steps, decisions, and outcomes for analysis and debugging

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TrajectoryLogger:
    """
    Structured logging system for pattern extraction trajectories.
    
    Records the complete path of each extraction including:
    - Repository selection and validation
    - GitHub API calls (URLs, response times, success/failure)
    - LLM prompts and responses (truncated for privacy)
    - Quality metric calculations
    - Neo4j storage operations
    - Critic validation results
    
    Trajectories stored as JSON files for post-analysis.
    """
    
    def __init__(self, log_dir: str = "logs/trajectories"):
        """
        Initialise trajectory logger.
        
        Args:
            log_dir: Directory to store trajectory JSON files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Current trajectory being recorded
        self.current_trajectory: Optional[Dict] = None
        self.trajectory_start_time: Optional[float] = None
        
        logger.info(f"TrajectoryLogger initialised: {self.log_dir}")
    
    def start_extraction(self, domain: str, search_query: str, limit: int) -> str:
        """
        Start a new extraction trajectory.
        
        Args:
            domain: Domain being extracted
            search_query: GitHub search query
            limit: Max repositories to process
        
        Returns:
            Trajectory ID
        """
        trajectory_id = f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.trajectory_start_time = time.time()
        
        self.current_trajectory = {
            "trajectory_id": trajectory_id,
            "domain": domain,
            "search_query": search_query,
            "limit": limit,
            "started_at": datetime.now().isoformat(),
            "events": [],
            "repositories": [],
            "summary": {
                "total_repos": 0,
                "successful": 0,
                "partial": 0,
                "failed": 0,
                "total_time_seconds": 0
            }
        }
        
        self.log_event("extraction_started", {
            "domain": domain,
            "query": search_query,
            "limit": limit
        })
        
        logger.info(f"Started trajectory: {trajectory_id}")
        return trajectory_id
    
    def log_event(self, event_type: str, data: Dict[str, Any], level: str = "info"):
        """
        Log an event in the current trajectory.
        
        Args:
            event_type: Type of event (e.g., 'github_api_call', 'llm_extraction')
            data: Event data
            level: Log level (info, warning, error)
        """
        if not self.current_trajectory:
            logger.warning("No active trajectory, event not logged")
            return
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": time.time() - self.trajectory_start_time,
            "type": event_type,
            "level": level,
            "data": data
        }
        
        self.current_trajectory["events"].append(event)
    
    def start_repository(self, repo_name: str, repo_url: str, stars: int):
        """Start processing a repository."""
        repo_data = {
            "repo_name": repo_name,
            "repo_url": repo_url,
            "stars": stars,
            "started_at": datetime.now().isoformat(),
            "start_time": time.time(),
            "events": [],
            "data_fetched": {
                "readme": False,
                "structure": False,
                "dependencies": False,
                "quality_metrics": False
            },
            "extraction_result": None,
            "errors": []
        }
        
        self.current_trajectory["repositories"].append(repo_data)
        
        self.log_event("repository_started", {
            "repo": repo_name,
            "stars": stars
        })
    
    def log_github_api_call(self, operation: str, repo_name: str, 
                           success: bool, response_time: float, 
                           error: Optional[str] = None):
        """
        Log a GitHub API call.
        
        Args:
            operation: Operation type (e.g., 'fetch_readme', 'analyze_structure')
            repo_name: Repository name
            success: Whether call succeeded
            response_time: Response time in seconds
            error: Error message if failed
        """
        data = {
            "operation": operation,
            "repo": repo_name,
            "success": success,
            "response_time_seconds": round(response_time, 3)
        }
        
        if error:
            data["error"] = str(error)[:200]  # Truncate long errors
        
        # Update repository data
        if self.current_trajectory["repositories"]:
            current_repo = self.current_trajectory["repositories"][-1]
            current_repo["events"].append({
                "type": "github_api",
                "operation": operation,
                "success": success,
                "response_time": response_time
            })
            
            if success:
                if operation == "fetch_readme":
                    current_repo["data_fetched"]["readme"] = True
                elif operation == "analyze_structure":
                    current_repo["data_fetched"]["structure"] = True
                elif operation == "fetch_dependencies":
                    current_repo["data_fetched"]["dependencies"] = True
            
            if error and not success:
                current_repo["errors"].append(f"GitHub API: {error[:100]}")
        
        level = "info" if success else "warning"
        self.log_event("github_api_call", data, level)
    
    def log_llm_extraction(self, repo_name: str, success: bool, 
                          response_time: float, pattern_name: Optional[str] = None,
                          confidence: Optional[str] = None, error: Optional[str] = None):
        """
        Log LLM extraction attempt.
        
        Args:
            repo_name: Repository name
            success: Whether extraction succeeded
            response_time: LLM response time in seconds
            pattern_name: Extracted pattern name
            confidence: Extraction confidence
            error: Error message if failed
        """
        data = {
            "repo": repo_name,
            "success": success,
            "response_time_seconds": round(response_time, 3)
        }
        
        if pattern_name:
            data["pattern_name"] = pattern_name
        if confidence:
            data["confidence"] = confidence
        if error:
            data["error"] = str(error)[:200]
        
        # Update repository data
        if self.current_trajectory["repositories"]:
            current_repo = self.current_trajectory["repositories"][-1]
            current_repo["events"].append({
                "type": "llm_extraction",
                "success": success,
                "response_time": response_time,
                "pattern_name": pattern_name
            })
            
            if error and not success:
                current_repo["errors"].append(f"LLM: {error[:100]}")
        
        level = "info" if success else "error"
        self.log_event("llm_extraction", data, level)
    
    def log_quality_metrics(self, repo_name: str, quality_score: float, 
                           freshness_score: float, maintenance_score: float):
        """Log quality metrics calculation."""
        data = {
            "repo": repo_name,
            "quality_score": round(quality_score, 3),
            "freshness_score": round(freshness_score, 3),
            "maintenance_score": round(maintenance_score, 3)
        }
        
        # Update repository data
        if self.current_trajectory["repositories"]:
            current_repo = self.current_trajectory["repositories"][-1]
            current_repo["data_fetched"]["quality_metrics"] = True
            current_repo["quality_metrics"] = data
        
        self.log_event("quality_metrics_calculated", data)
    
    def log_neo4j_storage(self, pattern_name: str, success: bool, 
                         response_time: float, error: Optional[str] = None):
        """Log Neo4j storage operation."""
        data = {
            "pattern": pattern_name,
            "success": success,
            "response_time_seconds": round(response_time, 3)
        }
        
        if error:
            data["error"] = str(error)[:200]
        
        # Update repository data
        if self.current_trajectory["repositories"]:
            current_repo = self.current_trajectory["repositories"][-1]
            current_repo["events"].append({
                "type": "neo4j_storage",
                "success": success,
                "response_time": response_time
            })
            
            if error and not success:
                current_repo["errors"].append(f"Neo4j: {error[:100]}")
        
        level = "info" if success else "error"
        self.log_event("neo4j_storage", data, level)
    
    def log_critic_validation(self, pattern_name: str, validation_score: float,
                             needs_review: bool, response_time: float):
        """Log critic validation results."""
        data = {
            "pattern": pattern_name,
            "validation_score": round(validation_score, 3),
            "needs_review": needs_review,
            "response_time_seconds": round(response_time, 3)
        }
        
        # Update repository data
        if self.current_trajectory["repositories"]:
            current_repo = self.current_trajectory["repositories"][-1]
            current_repo["events"].append({
                "type": "critic_validation",
                "validation_score": validation_score,
                "needs_review": needs_review
            })
            current_repo["validation"] = data
        
        self.log_event("critic_validation", data)
    
    def finish_repository(self, extraction_status: str):
        """
        Finish processing current repository.
        
        Args:
            extraction_status: 'successful', 'partial', or 'failed'
        """
        if not self.current_trajectory["repositories"]:
            return
        
        current_repo = self.current_trajectory["repositories"][-1]
        current_repo["finished_at"] = datetime.now().isoformat()
        current_repo["total_time_seconds"] = time.time() - current_repo["start_time"]
        current_repo["extraction_result"] = extraction_status
        
        # Update summary
        self.current_trajectory["summary"]["total_repos"] += 1
        if extraction_status == "successful":
            self.current_trajectory["summary"]["successful"] += 1
        elif extraction_status == "partial":
            self.current_trajectory["summary"]["partial"] += 1
        else:
            self.current_trajectory["summary"]["failed"] += 1
        
        self.log_event("repository_finished", {
            "repo": current_repo["repo_name"],
            "status": extraction_status,
            "time_seconds": round(current_repo["total_time_seconds"], 2)
        })
    
    def finish_extraction(self) -> str:
        """
        Finish extraction trajectory and save to file.
        
        Returns:
            Path to saved trajectory file
        """
        if not self.current_trajectory:
            logger.warning("No active trajectory to finish")
            return ""
        
        # Calculate total time
        total_time = time.time() - self.trajectory_start_time
        self.current_trajectory["finished_at"] = datetime.now().isoformat()
        self.current_trajectory["summary"]["total_time_seconds"] = round(total_time, 2)
        
        # Calculate success rate
        total = self.current_trajectory["summary"]["total_repos"]
        if total > 0:
            successful = self.current_trajectory["summary"]["successful"]
            partial = self.current_trajectory["summary"]["partial"]
            success_rate = ((successful + partial) / total) * 100
            self.current_trajectory["summary"]["success_rate_percent"] = round(success_rate, 1)
        
        self.log_event("extraction_finished", {
            "total_repos": total,
            "successful": self.current_trajectory["summary"]["successful"],
            "partial": self.current_trajectory["summary"]["partial"],
            "failed": self.current_trajectory["summary"]["failed"],
            "total_time": round(total_time, 2)
        })
        
        # Save to file
        trajectory_id = self.current_trajectory["trajectory_id"]
        filename = f"{trajectory_id}.json"
        filepath = self.log_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.current_trajectory, f, indent=2)
        
        logger.info(f"Trajectory saved: {filepath}")
        
        # Reset
        self.current_trajectory = None
        self.trajectory_start_time = None
        
        return str(filepath)
    
    def get_trajectory_analysis(self, trajectory_file: str) -> Dict:
        """
        Analyse a trajectory file and generate insights.
        
        Args:
            trajectory_file: Path to trajectory JSON file
        
        Returns:
            Analysis results
        """
        with open(trajectory_file, 'r', encoding='utf-8') as f:
            trajectory = json.load(f)
        
        analysis = {
            "trajectory_id": trajectory["trajectory_id"],
            "domain": trajectory["domain"],
            "summary": trajectory["summary"],
            "timing_analysis": {},
            "error_analysis": {},
            "data_completeness": {}
        }
        
        # Timing analysis
        github_times = []
        llm_times = []
        neo4j_times = []
        
        for repo in trajectory["repositories"]:
            for event in repo["events"]:
                if event["type"] == "github_api" and "response_time" in event:
                    github_times.append(event["response_time"])
                elif event["type"] == "llm_extraction" and "response_time" in event:
                    llm_times.append(event["response_time"])
                elif event["type"] == "neo4j_storage" and "response_time" in event:
                    neo4j_times.append(event["response_time"])
        
        if github_times:
            analysis["timing_analysis"]["github_avg_seconds"] = round(sum(github_times) / len(github_times), 3)
        if llm_times:
            analysis["timing_analysis"]["llm_avg_seconds"] = round(sum(llm_times) / len(llm_times), 3)
        if neo4j_times:
            analysis["timing_analysis"]["neo4j_avg_seconds"] = round(sum(neo4j_times) / len(neo4j_times), 3)
        
        # Error analysis
        error_types = {}
        for repo in trajectory["repositories"]:
            for error in repo.get("errors", []):
                error_type = error.split(":")[0]
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        analysis["error_analysis"] = error_types
        
        # Data completeness
        readme_count = sum(1 for r in trajectory["repositories"] if r["data_fetched"]["readme"])
        structure_count = sum(1 for r in trajectory["repositories"] if r["data_fetched"]["structure"])
        deps_count = sum(1 for r in trajectory["repositories"] if r["data_fetched"]["dependencies"])
        total = len(trajectory["repositories"])
        
        if total > 0:
            analysis["data_completeness"] = {
                "readme_percent": round((readme_count / total) * 100, 1),
                "structure_percent": round((structure_count / total) * 100, 1),
                "dependencies_percent": round((deps_count / total) * 100, 1)
            }
        
        return analysis


# Usage example
if __name__ == "__main__":
    logger = TrajectoryLogger()
    
    # Start extraction
    trajectory_id = logger.start_extraction(
        domain="file_managers",
        search_query="topic:file-manager stars:>1000",
        limit=10
    )
    
    # Simulate repository processing
    logger.start_repository("owner/repo", "https://github.com/owner/repo", 5000)
    logger.log_github_api_call("fetch_readme", "owner/repo", True, 0.523)
    logger.log_github_api_call("analyze_structure", "owner/repo", True, 0.234)
    logger.log_quality_metrics("owner/repo", 0.85, 0.90, 0.80)
    logger.log_llm_extraction("owner/repo", True, 2.456, "filesystem_browser", "high")
    logger.log_neo4j_storage("filesystem_browser", True, 0.145)
    logger.log_critic_validation("filesystem_browser", 0.82, False, 1.234)
    logger.finish_repository("successful")
    
    # Finish extraction
    filepath = logger.finish_extraction()
    print(f"Trajectory saved to: {filepath}")
    
    # Analyse trajectory
    analysis = logger.get_trajectory_analysis(filepath)
    print(f"\nAnalysis:\n{json.dumps(analysis, indent=2)}")
