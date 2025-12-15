"""
Requirements Agent
Extracts structured requirements from RFP text using LLM
Supports: OpenAI, Azure OpenAI, and other LLM providers
"""

import json
import os
from typing import List, Dict, Any, Optional


def extract_requirements(text: str, llm_client: Optional[Any] = None) -> List[Dict[str, str]]:
    """
    Extract requirements from RFP text
    
    Args:
        text: RFP document text
        llm_client: Optional LLM client (OpenAI, Azure OpenAI, etc.)
        
    Returns:
        List of structured requirements with metadata
    """
    
    if llm_client is None:
        # Use default OpenAI client if available
        llm_client = _get_default_llm_client()
    
    if llm_client:
        return _extract_with_llm(text, llm_client)
    else:
        # Fallback to rule-based extraction for demo
        return _extract_with_rules(text)


def _get_default_llm_client():
    """Initialize default LLM client based on environment variables"""
    try:
        # Check for OpenAI API key
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            return OpenAI()
        
        # Check for Azure OpenAI configuration
        elif os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            from openai import AzureOpenAI
            return AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
    except ImportError:
        print("Warning: OpenAI library not installed. Using rule-based extraction.")
        return None
    
    return None


def _extract_with_llm(text: str, client: Any) -> List[Dict[str, str]]:
    """Extract requirements using LLM with structured output"""
    
    system_prompt = """You are an expert RFP analyst. Extract all requirements from the RFP document.
    
For each requirement, provide:
- id: Unique identifier (e.g., M-001 for Mandatory, O-001 for Optional)
- text: The actual requirement statement
- section: Section number from the RFP (if available)
- type: "Mandatory", "Optional", or "Desirable"
- owner: Default to "TBD"

Return ONLY a valid JSON array with no additional text."""

    user_prompt = f"""Extract all requirements from this RFP text:

{text[:4000]}

Return as JSON array following this schema:
[
  {{
    "id": "M-001",
    "text": "requirement text",
    "section": "3.2.1",
    "type": "Mandatory",
    "owner": "TBD"
  }}
]"""

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
        
        # Try to parse as JSON
        try:
            result = json.loads(content)
            # Handle both direct array and object with array
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and 'requirements' in result:
                return result['requirements']
            else:
                # Return first value if it's an array
                for value in result.values():
                    if isinstance(value, list):
                        return value
        except json.JSONDecodeError:
            print(f"Warning: Could not parse LLM response as JSON. Using rule-based fallback.")
            return _extract_with_rules(text)
            
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return _extract_with_rules(text)
    
    return []


def _extract_with_rules(text: str) -> List[Dict[str, str]]:
    """
    Rule-based requirement extraction (fallback/demo mode)
    Looks for common requirement patterns
    """
    requirements = []
    lines = text.split('\n')
    
    # Common requirement indicators
    mandatory_keywords = ['shall', 'must', 'required', 'mandatory']
    optional_keywords = ['should', 'may', 'optional', 'desirable']
    
    req_id_counter = {'M': 1, 'O': 1, 'D': 1}
    
    # Track current section for better context
    current_section = "Unknown"
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Detect section headers (e.g., "3.1.1 High Availability")
        if line_stripped and len(line_stripped) < 100 and any(c.isdigit() for c in line_stripped[:10]):
            # Likely a section header
            current_section = line_stripped
        
        # Skip empty lines or very short lines
        if len(line_lower) < 20:
            continue
        
        # Check if line contains requirement indicators
        is_mandatory = any(kw in line_lower for kw in mandatory_keywords)
        is_optional = any(kw in line_lower for kw in optional_keywords)
        
        if is_mandatory or is_optional:
            req_type = "Mandatory" if is_mandatory else "Optional"
            prefix = "M" if is_mandatory else "O"
            
            req_id = f"{prefix}-{req_id_counter[prefix]:03d}"
            req_id_counter[prefix] += 1
            
            # Clean up the requirement text
            req_text = line_stripped
            
            # If the line is very long (likely merged), try to split it into sentences
            if len(req_text) > 200:
                # Take the first sentence that contains the requirement keyword
                sentences = req_text.replace('. ', '.\n').split('\n')
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if any(kw in sentence_lower for kw in (mandatory_keywords if is_mandatory else optional_keywords)):
                        req_text = sentence.strip()
                        break
            
            requirements.append({
                "id": req_id,
                "text": req_text,
                "section": current_section,
                "type": req_type,
                "owner": "TBD"
            })
    
    # If no requirements found, create a sample one
    if not requirements:
        requirements.append({
            "id": "M-001",
            "text": "The solution shall support high availability.",
            "section": "3.2.1",
            "type": "Mandatory",
            "owner": "TBD"
        })
    
    return requirements


def validate_requirements(requirements: List[Dict[str, str]]) -> bool:
    """
    Validate requirements structure
    
    Args:
        requirements: List of requirement dictionaries
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'text', 'section', 'type', 'owner']
    
    for req in requirements:
        if not all(field in req for field in required_fields):
            return False
        
        if req['type'] not in ['Mandatory', 'Optional', 'Desirable']:
            return False
    
    return True
