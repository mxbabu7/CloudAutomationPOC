"""
RFP Analysis Agent
Analyzes RFP documents and extracts key requirements, objectives, and constraints.
"""

from typing import Dict, List, Any


class RFPAnalysisAgent:
    """Agent responsible for analyzing RFP documents."""
    
    def __init__(self, llm_client):
        """
        Initialize the RFP Analysis Agent.
        
        Args:
            llm_client: LLM client for AI-powered analysis
        """
        self.llm_client = llm_client
        self.agent_name = "RFP Analysis Agent"
    
    def analyze_rfp(self, rfp_content: str) -> Dict[str, Any]:
        """
        Analyze RFP content and extract key information.
        
        Args:
            rfp_content: Raw RFP document content
            
        Returns:
            Dictionary containing analyzed RFP data
        """
        print(f"[{self.agent_name}] Analyzing RFP document...")
        
        prompt = f"""
        Analyze the following RFP document and extract:
        1. Project objectives and goals
        2. Key technical requirements
        3. Business requirements
        4. Constraints and limitations
        5. Evaluation criteria
        6. Timeline and milestones
        
        RFP Content:
        {rfp_content}
        
        Provide a structured analysis with clear sections.
        """
        
        analysis = self.llm_client.generate(prompt)
        
        result = {
            "analysis": analysis,
            "status": "completed",
            "agent": self.agent_name
        }
        
        print(f"[{self.agent_name}] Analysis completed.")
        return result
    
    def extract_requirements(self, rfp_content: str) -> List[str]:
        """
        Extract specific requirements from RFP.
        
        Args:
            rfp_content: Raw RFP document content
            
        Returns:
            List of extracted requirements
        """
        prompt = f"""
        Extract all specific requirements from the following RFP document.
        List each requirement as a separate item.
        
        RFP Content:
        {rfp_content}
        """
        
        requirements_text = self.llm_client.generate(prompt)
        requirements = [req.strip() for req in requirements_text.split('\n') if req.strip()]
        
        return requirements
