# pattern_critic.py
# Async Reflection/Critic Pattern - Validates extracted patterns for quality
# Uses LLM-as-Critic to evaluate patterns against a validation rubric

import os
import json
import logging
from typing import Dict, Tuple
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log, after_log

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retry decorator for LLM calls
llm_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((Exception,)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)


class PatternCritic:
    """
    LLM-based pattern validator using reflection/critic pattern.
    
    Evaluates extracted patterns against a validation rubric:
    - Pattern name clarity and descriptiveness
    - Requirements specificity and actionability
    - Constraints technical soundness
    - Technology accuracy
    - Logical consistency
    
    Uses gemini-2.5-flash for fast, cost-effective validation.
    """
    
    # Validation thresholds
    NEEDS_REVIEW_THRESHOLD = 0.7  # Patterns below this score need human review
    ACCEPTABLE_THRESHOLD = 0.8    # Patterns above this are considered good
    
    def __init__(self):
        """Initialise critic with Gemini Flash model."""
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Unset Google Cloud auth env vars
        for var in ['GOOGLE_APPLICATION_CREDENTIALS', 'GCLOUD_PROJECT']:
            os.environ.pop(var, None)
        
        genai.configure(api_key=api_key)
        # Use Flash for fast, cost-effective validation
        self.llm = genai.GenerativeModel('gemini-2.5-flash')
        
        logger.info("PatternCritic initialised with gemini-2.5-flash")
    
    @llm_retry
    def validate_pattern(self, pattern: Dict) -> Tuple[float, bool, str]:
        """
        Validate a pattern against quality rubric.
        
        Args:
            pattern: Extracted pattern dictionary
        
        Returns:
            Tuple of (validation_score, needs_review, critic_notes)
            - validation_score: 0.0-1.0 quality score
            - needs_review: True if score < threshold
            - critic_notes: Detailed feedback from critic
        """
        logger.info(f"Validating pattern: {pattern.get('pattern_name', 'unknown')}")
        
        # Build validation prompt
        prompt = self._build_validation_prompt(pattern)
        
        try:
            response = self.llm.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            validation_result = json.loads(response_text)
            
            # Extract scores
            overall_score = float(validation_result.get('overall_score', 0.5))
            needs_review = overall_score < self.NEEDS_REVIEW_THRESHOLD
            
            # Build critic notes
            critic_notes = self._format_critic_notes(validation_result)
            
            logger.info(f"Validation complete: score={overall_score:.2f}, needs_review={needs_review}")
            
            return overall_score, needs_review, critic_notes
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse critic response: {e}")
            logger.debug(f"Response text: {response_text[:500]}")
            # Fallback: assume needs review
            return 0.5, True, f"Critic parsing error: {str(e)}"
        
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return 0.5, True, f"Validation error: {str(e)}"
    
    def _build_validation_prompt(self, pattern: Dict) -> str:
        """Build validation prompt with rubric."""
        return f"""You are a technical pattern validation expert. Evaluate this extracted architectural pattern against the validation rubric.

PATTERN TO VALIDATE:
{json.dumps(pattern, indent=2)}

VALIDATION RUBRIC (score each 0.0-1.0):

1. PATTERN NAME CLARITY (weight: 0.2)
   - Is the name clear, descriptive, and follows naming conventions?
   - Does it accurately represent the pattern's purpose?
   - Score: 1.0 = excellent, 0.5 = acceptable, 0.0 = poor

2. REQUIREMENTS SPECIFICITY (weight: 0.25)
   - Are requirements specific and actionable?
   - Is the domain clearly identified?
   - Is the context appropriate?
   - Score: 1.0 = very specific, 0.5 = somewhat vague, 0.0 = missing/unclear

3. CONSTRAINTS TECHNICAL SOUNDNESS (weight: 0.25)
   - Are constraints technically accurate?
   - Are criticality levels appropriate (must/should/nice-to-have)?
   - Are violation impacts realistic?
   - Is reasoning provided and sound?
   - Score: 1.0 = excellent, 0.5 = acceptable, 0.0 = flawed

4. TECHNOLOGY ACCURACY (weight: 0.2)
   - Are technologies correctly identified?
   - Are roles and criticality scores reasonable?
   - Are substitutes appropriate?
   - Score: 1.0 = accurate, 0.5 = mostly correct, 0.0 = incorrect

5. LOGICAL CONSISTENCY (weight: 0.1)
   - Are there contradictions or inconsistencies?
   - Do all parts align logically?
   - Score: 1.0 = fully consistent, 0.5 = minor issues, 0.0 = major contradictions

RESPOND IN JSON FORMAT:
{{
    "name_clarity_score": 0.85,
    "name_clarity_notes": "Clear and descriptive name...",
    
    "requirements_score": 0.75,
    "requirements_notes": "Domain is clear but context could be more specific...",
    
    "constraints_score": 0.90,
    "constraints_notes": "Constraints are well-defined with appropriate criticality...",
    
    "technology_score": 0.80,
    "technology_notes": "Technologies are accurate, criticality scores reasonable...",
    
    "consistency_score": 0.95,
    "consistency_notes": "No contradictions found...",
    
    "overall_score": 0.83,
    "summary": "Good pattern with clear structure. Minor improvements needed in requirements specificity.",
    "critical_issues": [],
    "suggestions": ["Add more specific context to requirements", "Consider adding error handling constraints"]
}}

Be critical but fair. Focus on technical accuracy and completeness.
"""
    
    def _format_critic_notes(self, validation_result: Dict) -> str:
        """Format validation result into readable critic notes."""
        notes = []
        
        # Overall summary
        overall = validation_result.get('overall_score', 0.0)
        summary = validation_result.get('summary', 'No summary provided')
        notes.append(f"OVERALL SCORE: {overall:.2f}/1.0")
        notes.append(f"SUMMARY: {summary}")
        notes.append("")
        
        # Individual scores
        notes.append("DETAILED SCORES:")
        notes.append(f"  - Name Clarity: {validation_result.get('name_clarity_score', 0.0):.2f}")
        notes.append(f"    {validation_result.get('name_clarity_notes', 'N/A')}")
        notes.append(f"  - Requirements: {validation_result.get('requirements_score', 0.0):.2f}")
        notes.append(f"    {validation_result.get('requirements_notes', 'N/A')}")
        notes.append(f"  - Constraints: {validation_result.get('constraints_score', 0.0):.2f}")
        notes.append(f"    {validation_result.get('constraints_notes', 'N/A')}")
        notes.append(f"  - Technology: {validation_result.get('technology_score', 0.0):.2f}")
        notes.append(f"    {validation_result.get('technology_notes', 'N/A')}")
        notes.append(f"  - Consistency: {validation_result.get('consistency_score', 0.0):.2f}")
        notes.append(f"    {validation_result.get('consistency_notes', 'N/A')}")
        notes.append("")
        
        # Critical issues
        critical_issues = validation_result.get('critical_issues', [])
        if critical_issues:
            notes.append("CRITICAL ISSUES:")
            for issue in critical_issues:
                notes.append(f"  - {issue}")
            notes.append("")
        
        # Suggestions
        suggestions = validation_result.get('suggestions', [])
        if suggestions:
            notes.append("SUGGESTIONS FOR IMPROVEMENT:")
            for suggestion in suggestions:
                notes.append(f"  - {suggestion}")
        
        return "\n".join(notes)
    
    def get_quality_tier(self, score: float) -> str:
        """Get quality tier label for a validation score."""
        if score >= self.ACCEPTABLE_THRESHOLD:
            return "EXCELLENT"
        elif score >= self.NEEDS_REVIEW_THRESHOLD:
            return "GOOD"
        elif score >= 0.5:
            return "NEEDS_REVIEW"
        else:
            return "POOR"


# Usage example
if __name__ == "__main__":
    # Test pattern
    test_pattern = {
        "pattern_name": "filesystem_browser",
        "confidence": "high",
        "requirements": {
            "type": "data_management",
            "domain": "file_system",
            "context": ["existing_files", "web_ui"]
        },
        "constraints": [
            {
                "rule": "filesystem_is_source_of_truth",
                "criticality": "must",
                "enforcement": "architectural",
                "violation_impact": "high",
                "reasoning": "Core principle for data integrity"
            }
        ],
        "technologies": [
            {
                "name": "react",
                "role": "primary",
                "criticality": 0.95,
                "adoption_confidence": 0.9,
                "can_substitute": ["vue", "preact"]
            }
        ],
        "reasoning": "Pattern for browsing filesystem with web UI"
    }
    
    critic = PatternCritic()
    score, needs_review, notes = critic.validate_pattern(test_pattern)
    
    print(f"\nValidation Score: {score:.2f}")
    print(f"Needs Review: {needs_review}")
    print(f"Quality Tier: {critic.get_quality_tier(score)}")
    print(f"\nCritic Notes:\n{notes}")
