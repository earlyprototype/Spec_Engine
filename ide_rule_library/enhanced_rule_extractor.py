#!/usr/bin/env python3
"""
Enhanced rule extraction with context-aware Gemini analysis.

Replaces simple extraction with multi-dimensional analysis including:
- Context and constraints
- Trade-offs
- Anti-patterns
- Confidence levels
- Production evidence
"""

import json
import hashlib
from typing import Dict, Any, Optional
import google.generativeai as genai

from ide_rule_library.exceptions import (
    ExtractionError, 
    GeminiError, 
    GeminiQuotaExceededError,
    GeminiTimeoutError,
    ValidationError,
    MalformedDataError,
    GeminiQuotaExceededError as QuotaError,  # Alias for compatibility
    GeminiTimeoutError as TimeoutError  # Alias for compatibility
)
from ide_rule_library.retry_handler import call_gemini_with_retry


class EnhancedRuleExtractor:
    """Extract rules with enhanced context-aware analysis"""
    
    def __init__(self, model_name: str, logger):
        self.model_name = model_name
        self.logger = logger
        self.model = genai.GenerativeModel(model_name)
    
    def extract_rule(self, file_content: str, file_path: str, 
                    repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract IDE rule with enhanced analysis.
        
        Args:
            file_content: Content of the rule file
            file_path: Path to the file in the repo
            repo_data: Enhanced repository metadata including quality scores
            
        Returns:
            Enhanced rule dictionary
            
        Raises:
            ExtractionError: If extraction fails
            ValidationError: If data validation fails
            GeminiError: If Gemini API fails
        """
        
        # Validate inputs
        if not file_content or not file_content.strip():
            raise ValidationError(f"Empty file content for {file_path}")
        
        if not repo_data:
            raise ValidationError(f"Missing repo_data for {file_path}")
        
        # Build enhanced prompt
        try:
            prompt = self._build_enhanced_prompt(file_content, file_path, repo_data)
        except Exception as e:
            raise ExtractionError(f"Failed to build prompt for {file_path}: {e}") from e
        
        try:
            self.logger.info(f"Analyzing {file_path} with enhanced context")
            
            # Call Gemini with retry logic
            response = call_gemini_with_retry(
                self.model,
                prompt,
                max_attempts=3,
                logger=self.logger
            )
            
            if not response or not response.text:
                raise GeminiError(f"Empty response from Gemini for {file_path}")
            
            # Parse JSON response
            analysis = self._parse_response(response.text)
            
            if not analysis:
                raise MalformedDataError(f"Failed to parse Gemini response for {file_path}")
            
            # Build enhanced rule dict
            rule = self._build_rule_dict(analysis, file_content, file_path, repo_data)
            
            self.logger.info(f"Successfully extracted enhanced rule (confidence: {rule.get('confidence_level', 0)}/5)")
            
            return rule
            
        except (GeminiQuotaExceededError, GeminiTimeoutError) as e:
            self.logger.error(f"Gemini API error for {file_path}: {e}")
            raise
            
        except ValidationError as e:
            self.logger.error(f"Validation error for {file_path}: {e}")
            raise
            
        except Exception as e:
            self.logger.error(f"Unexpected extraction error for {file_path}: {e}", exc_info=True)
            raise ExtractionError(f"Failed to extract rule from {file_path}: {e}") from e
    
    def _build_enhanced_prompt(self, content: str, file_path: str, 
                               repo_data: Dict) -> str:
        """Build context-aware analysis prompt"""
        
        # Get production signals
        prod_signals = repo_data.get('production_signals', {})
        has_ci_cd = repo_data.get('has_ci_cd', False)
        has_deployment = repo_data.get('has_deployment', False)
        has_tests = repo_data.get('has_tests', False)
        has_monitoring = repo_data.get('has_monitoring', False)
        
        repo_quality_score = repo_data.get('repo_quality_score', 0)
        
        prompt = f"""
Analyze this IDE rule file with critical thinking and context awareness.

REPOSITORY CONTEXT:
- Name: {repo_data.get('name', 'unknown')}
- Stars: {repo_data.get('stars', 0):,}
- Repo Quality Score: {repo_quality_score:.1f}/100
- Age: {repo_data.get('repo_age_days', 0)} days
- Contributors: {len(repo_data.get('contributors', []))}
- Last Updated: {repo_data.get('days_since_update', 999)} days ago

PRODUCTION SIGNALS:
- CI/CD: {' YES' if has_ci_cd else ' NO'}
- Deployment Config: {'YES' if has_deployment else 'NO'}
- Testing: {'YES' if has_tests else 'NO'}
- Monitoring: {'YES' if has_monitoring else 'NO'}
- Production Categories: {', '.join(prod_signals.keys()) if prod_signals else 'None'}

FILE: {file_path}

CONTENT:
{content[:8000]}  # Limit to avoid token overflow

Your task is to extract actionable patterns while being critical about context and applicability.

Return a JSON object with these fields:

{{
  "purpose": "One sentence describing what this rule file is for",
  
  "categories": ["code_style", "architecture", "testing", ...],
  
  "key_practices": [
    "Specific practice 1",
    "Specific practice 2",
    ...
  ],
  
  "reasoning": "Why these practices are recommended (2-3 sentences)",
  
  "context_constraints": {{
    "project_sizes": ["small", "medium", "large"],  # BEST GUESS - not validated with real data
    "team_sizes": ["solo", "small", "medium", "large"],  # BEST GUESS - not validated with real data
    "performance_impact": "low|medium|high",  # Estimated, not measured
    "complexity_added": "low|medium|high"  # Estimated, not measured
  }},
  
  "trade_offs": {{
    "benefits": ["Benefit 1", "Benefit 2", ...],
    "costs": ["Cost 1", "Cost 2", ...]
  }},
  
  "anti_patterns": [
    "Anti-pattern 1 that this explicitly avoids",
    "Anti-pattern 2 that contradicts this approach",
    ...
  ],
  
  "dependencies": {{
    "required_tools": ["tool1", "tool2", ...],
    "required_libraries": ["lib1", "lib2", ...],
    "assumed_stack": ["python", "fastapi", ...]
  }},
  
  "confidence_level": 1-5,  # Based on production evidence
  
  "confidence_reasoning": "Why this confidence level (consider: production signals, repo quality, maintenance status)",
  
  "alternative_approaches": [
    "Alternative 1 for solving same problems",
    "Alternative 2 with different trade-offs",
    ...
  ],
  
  "technologies": ["python", "typescript", "react", ...],
  
  "project_types": ["api", "web_app", "cli", "library", ...],
  
  "ide_types": ["cursor", "github_copilot", "vscode", ...]
}}

CRITICAL GUIDELINES:
1. BE SKEPTICAL - High stars doesn't mean battle-tested
2. CONSIDER CONTEXT - Patterns suitable for what project sizes/types?
   NOTE: Context inference (project_sizes, team_sizes) is AI BEST GUESS, not validated
3. IDENTIFY TRADE-OFFS - Every pattern has costs and benefits
4. SPOT ANTI-PATTERNS - What does this contradict or avoid?
5. CHECK PRODUCTION READINESS - Does repo show production usage?
6. SUGGEST ALTERNATIVES - What other approaches exist?
7. CONFIDENCE SCORING:
   - 5: Strong production signals (CI/CD + Tests + Deployment), recent activity, high quality
   - 4: Good signals (CI/CD + Tests), decent maintenance
   - 3: Some signals, moderate quality
   - 2: Limited signals, could be tutorial code
   - 1: No production signals, likely example/demo code

Return ONLY valid JSON, no markdown formatting.
"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict:
        """
        Parse Gemini JSON response.
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed dictionary
            
        Raises:
            MalformedDataError: If JSON parsing fails
        """
        if not response_text:
            raise MalformedDataError("Empty response text")
        
        # Remove markdown code blocks if present
        text = response_text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        try:
            parsed = json.loads(text)
            
            # Validate required fields
            required_fields = ['purpose', 'categories', 'key_practices']
            missing = [f for f in required_fields if f not in parsed]
            
            if missing:
                raise MalformedDataError(f"Missing required fields in response: {missing}")
            
            return parsed
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error: {e}")
            self.logger.debug(f"Response text: {text[:500]}")
            raise MalformedDataError(f"Invalid JSON in Gemini response: {e}") from e
    
    def _build_rule_dict(self, analysis: Dict, content: str, 
                        file_path: str, repo_data: Dict) -> Dict:
        """Build enhanced rule dictionary for Neo4j storage"""
        
        # Generate content hash for duplicate detection
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
        
        # Base fields
        rule = {
            'id': f"{repo_data.get('name', 'unknown')}:{file_path}",
            'source_repo': repo_data.get('html_url', ''),
            'file_path': file_path,
            'file_format': self._extract_format(file_path),
            'content': content,
            'content_hash': content_hash,
            
            # Analysis fields
            'purpose': analysis.get('purpose', ''),
            'categories': analysis.get('categories', []),
            'key_practices': analysis.get('key_practices', []),
            'reasoning': analysis.get('reasoning', ''),
            
            # Enhanced context fields
            'suitable_project_sizes': analysis.get('context_constraints', {}).get('project_sizes', []),
            'suitable_team_sizes': analysis.get('context_constraints', {}).get('team_sizes', []),
            'performance_impact': analysis.get('context_constraints', {}).get('performance_impact', 'medium'),
            'complexity_added': analysis.get('context_constraints', {}).get('complexity_added', 'medium'),
            
            # Trade-offs
            'trade_offs': analysis.get('trade_offs', {}),
            
            # Anti-patterns
            'anti_patterns': analysis.get('anti_patterns', []),
            
            # Dependencies
            'required_tools': analysis.get('dependencies', {}).get('required_tools', []),
            'required_libraries': analysis.get('dependencies', {}).get('required_libraries', []),
            'assumed_stack': analysis.get('dependencies', {}).get('assumed_stack', []),
            
            # Confidence
            'confidence_level': analysis.get('confidence_level', 3),
            'confidence_reasoning': analysis.get('confidence_reasoning', ''),
            
            # Alternatives
            'alternative_approaches': analysis.get('alternative_approaches', []),
            
            # Standard classification
            'technologies': analysis.get('technologies', []),
            'project_types': analysis.get('project_types', []),
            'ide_types': analysis.get('ide_types', ['cursor']),
            
            # Repo quality metrics (from quality_scorer)
            'stars': repo_data.get('stars', 0),
            'repo_quality_score': repo_data.get('repo_quality_score', 0),
            'quality_breakdown': repo_data.get('quality_breakdown', {}),
            'repo_age_days': repo_data.get('repo_age_days', 0),
            'days_since_update': repo_data.get('days_since_update', 999),
            'contributor_count': len(repo_data.get('contributors', [])),
            
            # Production signals
            'has_ci_cd': repo_data.get('has_ci_cd', False),
            'has_deployment': repo_data.get('has_deployment', False),
            'has_tests': repo_data.get('has_tests', False),
            'has_monitoring': repo_data.get('has_monitoring', False),
            'has_security': repo_data.get('has_security', False),
            'production_signals': repo_data.get('production_signals', {}),
            
            # Timestamp
            'extracted_date': repo_data.get('extracted_date', ''),
        }
        
        return rule
    
    def _extract_format(self, file_path: str) -> str:
        """Extract file format from path"""
        if '.' in file_path:
            return '.' + file_path.split('.')[-1]
        return file_path  # For files without extensions
