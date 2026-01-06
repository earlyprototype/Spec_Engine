# quality_judge.py
# LLM-as-a-Judge Quality Evaluation
# Advanced multi-dimensional quality scoring using reasoning-capable LLM

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


class QualityJudge:
    """
    LLM-as-a-Judge for comprehensive pattern quality evaluation.
    
    Uses reasoning-capable LLM (gemini-2.5-pro) to evaluate patterns across
    multiple dimensions:
    - Architectural soundness (0-1)
    - Completeness (0-1)
    - Clarity and usefulness (0-1)
    - Technical accuracy (0-1)
    
    Compares patterns against:
    - Repository description and README
    - Industry best practices
    - Similar patterns in knowledge graph
    """
    
    # Quality thresholds
    EXCELLENT_THRESHOLD = 0.85
    GOOD_THRESHOLD = 0.70
    ACCEPTABLE_THRESHOLD = 0.55
    
    def __init__(self):
        """Initialise judge with Gemini Pro model."""
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Unset Google Cloud auth env vars
        for var in ['GOOGLE_APPLICATION_CREDENTIALS', 'GCLOUD_PROJECT']:
            os.environ.pop(var, None)
        
        genai.configure(api_key=api_key)
        # Use Pro for reasoning capability
        self.llm = genai.GenerativeModel('gemini-2.5-pro')
        
        logger.info("QualityJudge initialised with gemini-2.5-pro")
    
    @llm_retry
    def evaluate_pattern(self, pattern: Dict, repo_context: Dict = None) -> Tuple[float, str]:
        """
        Evaluate pattern quality using LLM-as-Judge.
        
        Args:
            pattern: Extracted pattern dictionary
            repo_context: Optional repository context (README, description, etc.)
        
        Returns:
            Tuple of (judge_score, judge_feedback)
            - judge_score: 0.0-1.0 composite quality score
            - judge_feedback: Detailed evaluation feedback
        """
        logger.info(f"Evaluating pattern: {pattern.get('pattern_name', 'unknown')}")
        
        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(pattern, repo_context)
        
        try:
            response = self.llm.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            evaluation_result = json.loads(response_text)
            
            # Extract scores
            judge_score = float(evaluation_result.get('composite_score', 0.5))
            
            # Build feedback
            judge_feedback = self._format_judge_feedback(evaluation_result)
            
            logger.info(f"Evaluation complete: score={judge_score:.2f}")
            
            return judge_score, judge_feedback
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse judge response: {e}")
            logger.debug(f"Response text: {response_text[:500]}")
            return 0.5, f"Judge parsing error: {str(e)}"
        
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return 0.5, f"Evaluation error: {str(e)}"
    
    def _build_evaluation_prompt(self, pattern: Dict, repo_context: Dict = None) -> str:
        """Build evaluation prompt with pattern and context."""
        
        context_section = ""
        if repo_context:
            context_section = f"""
REPOSITORY CONTEXT:
- Description: {repo_context.get('description', 'N/A')}
- README excerpt: {repo_context.get('readme', 'N/A')[:1000]}
- Stars: {repo_context.get('stars', 0)}
- Language: {repo_context.get('language', 'N/A')}
"""
        
        return f"""You are an expert software architect and pattern evaluator. Evaluate this extracted architectural pattern for quality and usefulness.

PATTERN TO EVALUATE:
{json.dumps(pattern, indent=2)}

{context_section}

EVALUATION CRITERIA (score each 0.0-1.0):

1. ARCHITECTURAL SOUNDNESS (weight: 0.30)
   - Is the pattern architecturally sound and well-structured?
   - Does it follow established architectural principles?
   - Are the constraints logically consistent with the pattern?
   - Would this pattern scale and be maintainable?
   
   Score Guidelines:
   - 0.9-1.0: Excellent architecture, industry best practices
   - 0.7-0.89: Good architecture, minor improvements possible
   - 0.5-0.69: Acceptable but has architectural concerns
   - 0.0-0.49: Significant architectural issues

2. COMPLETENESS (weight: 0.25)
   - Are all necessary components identified?
   - Are requirements comprehensive and specific?
   - Are constraints complete and well-defined?
   - Are technologies and their roles clearly specified?
   
   Score Guidelines:
   - 0.9-1.0: Comprehensive, nothing missing
   - 0.7-0.89: Mostly complete, minor gaps
   - 0.5-0.69: Some important elements missing
   - 0.0-0.49: Significant gaps in completeness

3. CLARITY AND USEFULNESS (weight: 0.25)
   - Is the pattern clearly described and understandable?
   - Would this be useful for developers implementing similar systems?
   - Are the constraints actionable and practical?
   - Is the reasoning clear and helpful?
   
   Score Guidelines:
   - 0.9-1.0: Crystal clear, highly useful
   - 0.7-0.89: Clear and useful, minor ambiguities
   - 0.5-0.69: Somewhat unclear or limited usefulness
   - 0.0-0.49: Confusing or not useful

4. TECHNICAL ACCURACY (weight: 0.20)
   - Are technologies correctly identified and described?
   - Are criticality scores realistic?
   - Are technology roles accurate?
   - Are suggested substitutes appropriate?
   
   Score Guidelines:
   - 0.9-1.0: Technically accurate throughout
   - 0.7-0.89: Mostly accurate, minor errors
   - 0.5-0.69: Some technical inaccuracies
   - 0.0-0.49: Significant technical errors

RESPOND IN JSON FORMAT:
{{
    "architectural_soundness": {{
        "score": 0.85,
        "reasoning": "Pattern follows clean architecture principles with clear separation of concerns...",
        "strengths": ["Clear layering", "Good separation of concerns"],
        "weaknesses": ["Could benefit from more specific error handling patterns"]
    }},
    "completeness": {{
        "score": 0.80,
        "reasoning": "Most components identified, but missing some edge cases...",
        "strengths": ["Comprehensive technology stack", "Well-defined constraints"],
        "weaknesses": ["Missing authentication patterns", "No mention of testing strategy"]
    }},
    "clarity_usefulness": {{
        "score": 0.90,
        "reasoning": "Very clear description with actionable constraints...",
        "strengths": ["Clear naming", "Actionable constraints", "Good examples"],
        "weaknesses": ["Could use more context about when to apply"]
    }},
    "technical_accuracy": {{
        "score": 0.88,
        "reasoning": "Technologies correctly identified with appropriate roles...",
        "strengths": ["Accurate tech stack", "Realistic criticality scores"],
        "weaknesses": ["One substitute suggestion seems questionable"]
    }},
    "composite_score": 0.85,
    "overall_assessment": "Excellent pattern with strong architectural foundation. Clear, complete, and technically accurate. Minor improvements possible in edge case handling and authentication patterns.",
    "key_strengths": [
        "Strong architectural foundation",
        "Clear and actionable constraints",
        "Comprehensive technology identification"
    ],
    "improvement_areas": [
        "Add authentication and authorization patterns",
        "Include testing strategy",
        "Expand error handling patterns"
    ],
    "recommendation": "APPROVED - Ready for production use with minor enhancements"
}}

Be thorough and critical. Consider industry best practices and real-world applicability.
The composite score should be the weighted average: (0.30 * arch + 0.25 * complete + 0.25 * clarity + 0.20 * accuracy).
"""
    
    def _format_judge_feedback(self, evaluation_result: Dict) -> str:
        """Format evaluation result into readable feedback."""
        feedback = []
        
        # Overall assessment
        composite = evaluation_result.get('composite_score', 0.0)
        assessment = evaluation_result.get('overall_assessment', 'No assessment provided')
        recommendation = evaluation_result.get('recommendation', 'N/A')
        
        feedback.append(f"COMPOSITE SCORE: {composite:.2f}/1.0")
        feedback.append(f"RECOMMENDATION: {recommendation}")
        feedback.append(f"\n{assessment}")
        feedback.append("")
        
        # Dimensional scores
        feedback.append("DIMENSIONAL SCORES:")
        
        dimensions = [
            ('architectural_soundness', 'Architectural Soundness'),
            ('completeness', 'Completeness'),
            ('clarity_usefulness', 'Clarity & Usefulness'),
            ('technical_accuracy', 'Technical Accuracy')
        ]
        
        for key, label in dimensions:
            dim_data = evaluation_result.get(key, {})
            score = dim_data.get('score', 0.0)
            reasoning = dim_data.get('reasoning', 'N/A')
            
            feedback.append(f"\n{label}: {score:.2f}")
            feedback.append(f"  {reasoning}")
            
            strengths = dim_data.get('strengths', [])
            if strengths:
                feedback.append(f"  Strengths: {', '.join(strengths)}")
            
            weaknesses = dim_data.get('weaknesses', [])
            if weaknesses:
                feedback.append(f"  Weaknesses: {', '.join(weaknesses)}")
        
        # Key strengths
        key_strengths = evaluation_result.get('key_strengths', [])
        if key_strengths:
            feedback.append("\nKEY STRENGTHS:")
            for strength in key_strengths:
                feedback.append(f"  + {strength}")
        
        # Improvement areas
        improvement_areas = evaluation_result.get('improvement_areas', [])
        if improvement_areas:
            feedback.append("\nIMPROVEMENT AREAS:")
            for area in improvement_areas:
                feedback.append(f"  - {area}")
        
        return "\n".join(feedback)
    
    def get_quality_tier(self, score: float) -> str:
        """Get quality tier label for a judge score."""
        if score >= self.EXCELLENT_THRESHOLD:
            return "EXCELLENT"
        elif score >= self.GOOD_THRESHOLD:
            return "GOOD"
        elif score >= self.ACCEPTABLE_THRESHOLD:
            return "ACCEPTABLE"
        else:
            return "NEEDS_IMPROVEMENT"


# Usage example
if __name__ == "__main__":
    # Test pattern
    test_pattern = {
        "pattern_name": "filesystem_browser_with_metadata_cache",
        "confidence": "high",
        "requirements": {
            "type": "data_management",
            "domain": "file_system",
            "context": ["existing_files", "web_ui", "performance"]
        },
        "constraints": [
            {
                "rule": "filesystem_is_source_of_truth",
                "criticality": "must",
                "enforcement": "architectural",
                "violation_impact": "high",
                "reasoning": "Core principle for data integrity"
            },
            {
                "rule": "database_for_metadata_only",
                "criticality": "should",
                "enforcement": "implementation",
                "violation_impact": "medium",
                "reasoning": "Improves performance without compromising integrity"
            }
        ],
        "technologies": [
            {
                "name": "react",
                "role": "primary",
                "criticality": 0.95,
                "adoption_confidence": 0.9,
                "can_substitute": ["vue", "preact"]
            },
            {
                "name": "sqlite",
                "role": "cache",
                "criticality": 0.6,
                "adoption_confidence": 0.85,
                "can_substitute": ["indexeddb", "localstorage"]
            }
        ],
        "reasoning": "Pattern for browsing filesystem with web UI and metadata caching for performance"
    }
    
    repo_context = {
        "description": "A modern file manager with web interface",
        "readme": "This project provides a fast, modern file browser...",
        "stars": 5000,
        "language": "JavaScript"
    }
    
    judge = QualityJudge()
    score, feedback = judge.evaluate_pattern(test_pattern, repo_context)
    
    print(f"\nJudge Score: {score:.2f}")
    print(f"Quality Tier: {judge.get_quality_tier(score)}")
    print(f"\nJudge Feedback:\n{feedback}")
