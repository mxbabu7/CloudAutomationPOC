"""
Strategy Agent
Generates response strategy based on requirements, evaluation criteria, and risks
"""

import os
from typing import List, Dict, Any, Optional


def generate_strategy(
    requirements: List[Dict[str, str]], 
    evaluation: Dict[str, Any],
    risks: List[Dict[str, Any]],
    llm_client: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Generate response strategy
    
    Args:
        requirements: Extracted requirements
        evaluation: Evaluation criteria
        risks: Identified risks
        llm_client: Optional LLM client
        
    Returns:
        Structured response strategy
    """
    
    if llm_client is None:
        llm_client = _get_default_llm_client()
    
    if llm_client:
        return _generate_with_llm(requirements, evaluation, risks, llm_client)
    else:
        return _generate_with_rules(requirements, evaluation, risks)


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


def _generate_with_llm(
    requirements: List[Dict[str, str]], 
    evaluation: Dict[str, Any],
    risks: List[Dict[str, Any]],
    client: Any
) -> Dict[str, Any]:
    """Generate strategy using LLM"""
    
    import json
    
    # Prepare context
    req_summary = f"{len(requirements)} requirements ({sum(1 for r in requirements if r['type'] == 'Mandatory')} mandatory)"
    eval_summary = f"{len(evaluation.get('criteria', []))} evaluation criteria"
    risk_summary = f"{len(risks)} risks identified ({sum(1 for r in risks if r.get('severity') == 'High')} high severity)"
    
    system_prompt = """You are an RFP response strategist. Generate a winning response strategy.

Provide:
- Executive summary
- Key themes to emphasize
- Differentiation strategy
- Risk mitigation approach
- Resource allocation recommendations
- Timeline recommendations

Return as structured JSON."""

    user_prompt = f"""Generate response strategy for this RFP:

Requirements: {req_summary}
Evaluation: {eval_summary}
Risks: {risk_summary}

Top evaluation criteria:
{chr(10).join([f"- {c['name']} ({c['weight']}%)" for c in evaluation.get('criteria', [])[:3]])}

High-priority risks:
{chr(10).join([f"- {r['description']}" for r in risks if r.get('severity') == 'High'][:3])}

Return comprehensive strategy as JSON."""

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"Error calling LLM for strategy: {e}")
        return _generate_with_rules(requirements, evaluation, risks)


def _generate_with_rules(
    requirements: List[Dict[str, str]], 
    evaluation: Dict[str, Any],
    risks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Rule-based strategy generation"""
    
    # Count requirement types
    mandatory_count = sum(1 for r in requirements if r['type'] == 'Mandatory')
    optional_count = sum(1 for r in requirements if r['type'] == 'Optional')
    
    # Get top evaluation criteria
    criteria = evaluation.get('criteria', [])
    top_criteria = sorted(criteria, key=lambda x: x.get('weight', 0), reverse=True)[:3]
    
    # Count high severity risks
    high_risks = [r for r in risks if r.get('severity') == 'High']
    
    # Generate strategy
    strategy = {
        "executive_summary": f"""
This RFP response strategy addresses {mandatory_count} mandatory and {optional_count} optional requirements.
Our approach focuses on maximizing scores in the top-weighted evaluation criteria while mitigating {len(high_risks)} high-severity risks.
        """.strip(),
        
        "key_themes": [
            "Technical Excellence: Demonstrate robust, scalable solution architecture",
            "Proven Experience: Showcase relevant past projects and success stories",
            "Risk Mitigation: Address identified risks proactively",
            "Value Proposition: Balance cost-effectiveness with quality"
        ],
        
        "evaluation_focus": [
            {
                "criterion": c['name'],
                "weight": c['weight'],
                "strategy": _get_criterion_strategy(c['name'])
            }
            for c in top_criteria
        ],
        
        "risk_mitigation": {
            "high_priority_risks": len(high_risks),
            "approach": "Address high-severity risks in technical proposal with specific mitigation plans",
            "key_actions": [
                "Early engagement with compliance/security team for regulatory requirements",
                "Detailed integration testing plan for technical complexity",
                "Buffer time in project schedule for critical deliverables"
            ]
        },
        
        "resource_allocation": {
            "technical_writers": "2-3 FTE for proposal development",
            "subject_matter_experts": "4-5 SMEs for technical content",
            "reviewers": "2 senior reviewers for quality assurance",
            "estimated_effort": "40-60 person-days"
        },
        
        "timeline": {
            "phase_1": "Requirements analysis and compliance matrix (3-5 days)",
            "phase_2": "Technical solution development (7-10 days)",
            "phase_3": "Pricing and financial proposal (3-5 days)",
            "phase_4": "Review and finalization (2-3 days)",
            "total_duration": "15-23 business days"
        },
        
        "differentiators": [
            "Innovative technical approach leveraging latest technologies",
            "Strong track record with similar clients",
            "Comprehensive risk mitigation strategy",
            "Competitive pricing with clear value proposition"
        ],
        
        "compliance_approach": {
            "mandatory_requirements": f"100% compliance ({mandatory_count} requirements)",
            "optional_requirements": f"Target 80%+ coverage ({optional_count} requirements)",
            "validation": "Line-by-line compliance matrix with RFP traceability"
        }
    }
    
    return strategy


def _get_criterion_strategy(criterion_name: str) -> str:
    """Get specific strategy for evaluation criterion"""
    
    strategies = {
        "technical": "Emphasize architecture diagrams, scalability metrics, and technical innovation",
        "financial": "Provide competitive pricing with clear cost breakdown and ROI analysis",
        "experience": "Showcase 3-5 relevant case studies with quantifiable results",
        "references": "Include strong client testimonials and independent verification"
    }
    
    # Match criterion name to strategy
    criterion_lower = criterion_name.lower()
    for key, strategy in strategies.items():
        if key in criterion_lower:
            return strategy
    
    return "Provide detailed, evidence-based response with supporting documentation"


def format_strategy_brief(strategy: Dict[str, Any]) -> str:
    """
    Format strategy as markdown brief
    
    Args:
        strategy: Strategy dictionary
        
    Returns:
        Markdown formatted strategy document
    """
    
    md = "# RFP Response Strategy Brief\n\n"
    
    # Executive Summary
    md += "## Executive Summary\n\n"
    md += strategy.get('executive_summary', '') + "\n\n"
    
    # Key Themes
    md += "## Key Themes\n\n"
    for theme in strategy.get('key_themes', []):
        md += f"- {theme}\n"
    md += "\n"
    
    # Evaluation Focus
    md += "## Evaluation Criteria Focus\n\n"
    for focus in strategy.get('evaluation_focus', []):
        md += f"### {focus['criterion']} ({focus['weight']}%)\n"
        md += f"{focus['strategy']}\n\n"
    
    # Risk Mitigation
    md += "## Risk Mitigation Approach\n\n"
    risk_mitigation = strategy.get('risk_mitigation', {})
    md += f"**High Priority Risks:** {risk_mitigation.get('high_priority_risks', 0)}\n\n"
    md += f"**Approach:** {risk_mitigation.get('approach', '')}\n\n"
    md += "**Key Actions:**\n"
    for action in risk_mitigation.get('key_actions', []):
        md += f"- {action}\n"
    md += "\n"
    
    # Timeline
    md += "## Recommended Timeline\n\n"
    timeline = strategy.get('timeline', {})
    for phase, duration in timeline.items():
        if phase != 'total_duration':
            md += f"- **{phase.replace('_', ' ').title()}:** {duration}\n"
    md += f"\n**Total Duration:** {timeline.get('total_duration', 'TBD')}\n\n"
    
    # Differentiators
    md += "## Key Differentiators\n\n"
    for diff in strategy.get('differentiators', []):
        md += f"- {diff}\n"
    
    return md
