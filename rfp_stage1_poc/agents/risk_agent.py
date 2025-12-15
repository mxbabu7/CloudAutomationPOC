"""
Risk Agent
Identifies and categorizes risks from RFP requirements
"""

import os
from typing import List, Dict, Any, Optional


def identify_risks(requirements: List[Dict[str, str]], llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """
    Identify risks from extracted requirements
    
    Args:
        requirements: List of requirements from requirements_agent
        llm_client: Optional LLM client
        
    Returns:
        List of identified risks with severity and mitigation
    """
    
    if llm_client is None:
        llm_client = _get_default_llm_client()
    
    if llm_client:
        return _identify_with_llm(requirements, llm_client)
    else:
        return _identify_with_rules(requirements)


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


def _identify_with_llm(requirements: List[Dict[str, str]], client: Any) -> List[Dict[str, Any]]:
    """Identify risks using LLM analysis"""
    
    import json
    
    # Prepare requirements summary
    req_summary = "\n".join([f"- {req['id']}: {req['text']}" for req in requirements[:20]])
    
    system_prompt = """You are a risk assessment expert for RFP responses. Analyze requirements and identify potential risks.

For each risk, provide:
- risk_id: Unique identifier
- description: Clear description of the risk
- category: Technical, Schedule, Resource, Financial, or Compliance
- severity: High, Medium, or Low
- probability: High, Medium, or Low
- impact: Detailed impact description
- mitigation: Suggested mitigation strategy
- related_requirements: List of requirement IDs affected

Return as JSON array."""

    user_prompt = f"""Analyze these requirements and identify risks:

{req_summary}

Return as JSON array of risk objects."""

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        # Handle different response formats
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and 'risks' in result:
            return result['risks']
        else:
            for value in result.values():
                if isinstance(value, list):
                    return value
        
    except Exception as e:
        print(f"Error calling LLM for risk analysis: {e}")
    
    return _identify_with_rules(requirements)


def _identify_with_rules(requirements: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Rule-based risk identification"""
    
    risks = []
    risk_id_counter = 1
    
    # Risk patterns to look for
    risk_patterns = {
        'technical': ['integration', 'api', 'system', 'architecture', 'performance', 'scalability'],
        'schedule': ['timeline', 'deadline', 'delivery', 'phase', 'milestone'],
        'resource': ['team', 'staff', 'expertise', 'skill', 'experience'],
        'financial': ['cost', 'budget', 'price', 'payment', 'penalty'],
        'compliance': ['security', 'compliance', 'regulation', 'gdpr', 'privacy', 'audit']
    }
    
    # Analyze each requirement
    for req in requirements:
        req_text_lower = req['text'].lower()
        
        # Check for technical complexity risks
        if any(pattern in req_text_lower for pattern in risk_patterns['technical']):
            if 'integration' in req_text_lower or 'api' in req_text_lower:
                risks.append({
                    "risk_id": f"R-{risk_id_counter:03d}",
                    "description": "Integration complexity with existing systems",
                    "category": "Technical",
                    "severity": "High",
                    "probability": "Medium",
                    "impact": "May cause delays or require additional resources",
                    "mitigation": "Conduct thorough integration testing and API documentation review",
                    "related_requirements": [req['id']]
                })
                risk_id_counter += 1
        
        # Check for compliance risks
        if any(pattern in req_text_lower for pattern in risk_patterns['compliance']):
            risks.append({
                "risk_id": f"R-{risk_id_counter:03d}",
                "description": "Compliance and security requirements complexity",
                "category": "Compliance",
                "severity": "High",
                "probability": "Medium",
                "impact": "Non-compliance could result in rejection or penalties",
                "mitigation": "Engage security and compliance experts early",
                "related_requirements": [req['id']]
            })
            risk_id_counter += 1
        
        # Check for schedule risks
        if any(pattern in req_text_lower for pattern in risk_patterns['schedule']):
            if req['type'] == 'Mandatory':
                risks.append({
                    "risk_id": f"R-{risk_id_counter:03d}",
                    "description": "Tight timeline for mandatory deliverables",
                    "category": "Schedule",
                    "severity": "Medium",
                    "probability": "Medium",
                    "impact": "May require overtime or additional resources",
                    "mitigation": "Develop detailed project plan with buffer time",
                    "related_requirements": [req['id']]
                })
                risk_id_counter += 1
    
    # Add general risks if no specific risks identified
    if not risks:
        risks.append({
            "risk_id": "R-001",
            "description": "Requirement interpretation ambiguity",
            "category": "Technical",
            "severity": "Medium",
            "probability": "Low",
            "impact": "May need clarification during execution",
            "mitigation": "Request clarification meeting with client",
            "related_requirements": []
        })
    
    return risks


def categorize_risks(risks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize risks by severity and category
    
    Args:
        risks: List of risk dictionaries
        
    Returns:
        Dictionary of risks grouped by category and severity
    """
    categorized = {
        'by_severity': {'High': [], 'Medium': [], 'Low': []},
        'by_category': {}
    }
    
    for risk in risks:
        severity = risk.get('severity', 'Medium')
        category = risk.get('category', 'Other')
        
        categorized['by_severity'][severity].append(risk)
        
        if category not in categorized['by_category']:
            categorized['by_category'][category] = []
        categorized['by_category'][category].append(risk)
    
    return categorized
