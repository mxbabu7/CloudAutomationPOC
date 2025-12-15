"""
Evaluation Agent
Extracts evaluation criteria and scoring methodology from RFP
"""

import json
import os
from typing import List, Dict, Any, Optional


def extract_evaluation(text: str, llm_client: Optional[Any] = None) -> Dict[str, Any]:
    """
    Extract evaluation criteria from RFP text
    
    Args:
        text: RFP document text
        llm_client: Optional LLM client
        
    Returns:
        Structured evaluation criteria with weights and scoring
    """
    
    if llm_client is None:
        llm_client = _get_default_llm_client()
    
    if llm_client:
        return _extract_with_llm(text, llm_client)
    else:
        return _extract_with_rules(text)


def _get_default_llm_client():
    """Initialize default LLM client"""
    try:
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            return OpenAI()
        elif os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            from openai import AzureOpenAI
            return AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
    except ImportError:
        return None
    
    return None


def _extract_with_llm(text: str, client: Any) -> Dict[str, Any]:
    """Extract evaluation criteria using LLM"""
    
    system_prompt = """You are an RFP evaluation expert. Extract evaluation criteria and scoring methodology.

Identify:
- Evaluation criteria (Technical, Financial, Experience, etc.)
- Weights/percentages for each criterion
- Scoring methodology
- Pass/fail thresholds

Return as structured JSON."""

    user_prompt = f"""Extract evaluation criteria from this RFP:

{text[:4000]}

Return as JSON:
{{
  "criteria": [
    {{
      "name": "Technical Solution",
      "weight": 40,
      "description": "Quality and completeness of technical approach",
      "max_score": 100
    }}
  ],
  "methodology": "Weighted scoring",
  "pass_threshold": 70
}}"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"Error calling LLM for evaluation: {e}")
        return _extract_with_rules(text)


def _extract_with_rules(text: str) -> Dict[str, Any]:
    """Rule-based evaluation extraction (fallback)"""
    
    # Look for common evaluation keywords
    text_lower = text.lower()
    
    criteria = []
    
    # Common evaluation areas
    if 'technical' in text_lower:
        criteria.append({
            "name": "Technical Solution",
            "weight": 40,
            "description": "Quality and completeness of technical approach",
            "max_score": 100
        })
    
    if 'price' in text_lower or 'cost' in text_lower or 'financial' in text_lower:
        criteria.append({
            "name": "Financial Proposal",
            "weight": 30,
            "description": "Cost competitiveness and value for money",
            "max_score": 100
        })
    
    if 'experience' in text_lower or 'qualification' in text_lower:
        criteria.append({
            "name": "Experience & Qualifications",
            "weight": 20,
            "description": "Vendor experience and team qualifications",
            "max_score": 100
        })
    
    if 'reference' in text_lower or 'past performance' in text_lower:
        criteria.append({
            "name": "References",
            "weight": 10,
            "description": "Past performance and client references",
            "max_score": 100
        })
    
    # Default if nothing found
    if not criteria:
        criteria = [
            {
                "name": "Technical Solution",
                "weight": 50,
                "description": "Quality and completeness of technical approach",
                "max_score": 100
            },
            {
                "name": "Financial Proposal",
                "weight": 30,
                "description": "Cost competitiveness and value for money",
                "max_score": 100
            },
            {
                "name": "Experience",
                "weight": 20,
                "description": "Vendor experience and qualifications",
                "max_score": 100
            }
        ]
    
    return {
        "criteria": criteria,
        "methodology": "Weighted scoring with normalized weights",
        "pass_threshold": 70,
        "total_weight": sum(c['weight'] for c in criteria)
    }


def validate_evaluation(evaluation: Dict[str, Any]) -> bool:
    """Validate evaluation structure"""
    
    if 'criteria' not in evaluation:
        return False
    
    total_weight = sum(c.get('weight', 0) for c in evaluation['criteria'])
    
    # Allow some tolerance for weight totals
    if total_weight < 90 or total_weight > 110:
        print(f"Warning: Total weights = {total_weight}, expected ~100")
    
    return True
