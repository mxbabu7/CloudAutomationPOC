"""
Proposal Agent
Generates comprehensive proposal documents based on all agent outputs.
"""

from typing import Dict, List, Any


class ProposalAgent:
    """Agent responsible for generating proposal documents."""
    
    def __init__(self, llm_client):
        """
        Initialize the Proposal Agent.
        
        Args:
            llm_client: LLM client for AI-powered document generation
        """
        self.llm_client = llm_client
        self.agent_name = "Proposal Agent"
    
    def generate_proposal(self, all_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive proposal document.
        
        Args:
            all_outputs: Combined outputs from all agents
            
        Returns:
            Dictionary containing proposal document
        """
        print(f"[{self.agent_name}] Generating proposal document...")
        
        prompt = f"""
        Create a comprehensive proposal document based on the following inputs:
        
        RFP Analysis:
        {all_outputs.get('rfp_analysis', {}).get('analysis', '')}
        
        Requirements:
        {all_outputs.get('requirements', {}).get('structured_requirements', '')}
        
        Architecture:
        {all_outputs.get('architecture', {}).get('architecture_design', '')}
        
        Cost Estimate:
        {all_outputs.get('costs', {}).get('cost_estimate', '')}
        
        Security Analysis:
        {all_outputs.get('security', {}).get('security_analysis', '')}
        
        Generate a professional proposal with:
        1. Executive Summary
        2. Understanding of Requirements
        3. Proposed Solution Architecture
        4. Implementation Approach
        5. Security and Compliance
        6. Cost Breakdown and Pricing
        7. Timeline and Milestones
        8. Team and Expertise
        9. Risks and Mitigation
        10. Conclusion and Next Steps
        
        Format as a professional business proposal.
        """
        
        proposal = self.llm_client.generate(prompt)
        
        result = {
            "proposal_document": proposal,
            "status": "completed",
            "agent": self.agent_name
        }
        
        print(f"[{self.agent_name}] Proposal generation completed.")
        return result
    
    def generate_executive_summary(self, all_outputs: Dict[str, Any]) -> str:
        """
        Generate executive summary section.
        
        Args:
            all_outputs: Combined outputs from all agents
            
        Returns:
            Executive summary text
        """
        prompt = f"""
        Create a concise executive summary (1-2 pages) based on:
        
        {all_outputs}
        
        Focus on:
        - Key business value
        - Solution highlights
        - Cost overview
        - Timeline
        """
        
        summary = self.llm_client.generate(prompt)
        return summary
    
    def generate_technical_appendix(self, architecture: Dict[str, Any], security: Dict[str, Any]) -> str:
        """
        Generate technical appendix with detailed specifications.
        
        Args:
            architecture: Architecture design
            security: Security analysis
            
        Returns:
            Technical appendix text
        """
        prompt = f"""
        Create a technical appendix with detailed specifications:
        
        Architecture:
        {architecture.get('architecture_design', '')}
        
        Security:
        {security.get('security_analysis', '')}
        
        Include technical diagrams descriptions, service specifications, and configurations.
        """
        
        appendix = self.llm_client.generate(prompt)
        return appendix
