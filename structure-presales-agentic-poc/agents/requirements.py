"""
Requirements Agent
Processes and structures requirements extracted from RFP analysis.
"""

from typing import Dict, List, Any


class RequirementsAgent:
    """Agent responsible for processing and structuring requirements."""
    
    def __init__(self, llm_client):
        """
        Initialize the Requirements Agent.
        
        Args:
            llm_client: LLM client for AI-powered processing
        """
        self.llm_client = llm_client
        self.agent_name = "Requirements Agent"
    
    def process_requirements(self, rfp_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and categorize requirements from RFP analysis.
        
        Args:
            rfp_analysis: Analysis results from RFP Analysis Agent
            
        Returns:
            Dictionary containing structured requirements
        """
        print(f"[{self.agent_name}] Processing requirements...")
        
        prompt = f"""
        Based on the following RFP analysis, categorize and structure the requirements into:
        1. Functional Requirements
        2. Non-Functional Requirements
        3. Technical Requirements
        4. Business Requirements
        5. Compliance Requirements
        
        RFP Analysis:
        {rfp_analysis.get('analysis', '')}
        
        Provide a detailed categorization with priorities (High/Medium/Low).
        """
        
        structured_requirements = self.llm_client.generate(prompt)
        
        result = {
            "structured_requirements": structured_requirements,
            "status": "completed",
            "agent": self.agent_name
        }
        
        print(f"[{self.agent_name}] Requirements processing completed.")
        return result
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate requirements for completeness and clarity.
        
        Args:
            requirements: Structured requirements to validate
            
        Returns:
            Validation results with recommendations
        """
        prompt = f"""
        Validate the following requirements for:
        1. Completeness
        2. Clarity and specificity
        3. Measurability
        4. Feasibility
        5. Conflicts or contradictions
        
        Requirements:
        {requirements}
        
        Provide validation results and recommendations for improvement.
        """
        
        validation = self.llm_client.generate(prompt)
        
        return {
            "validation": validation,
            "status": "completed"
        }
