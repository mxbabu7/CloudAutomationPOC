"""
Security Agent
Analyzes security requirements and provides security recommendations.
"""

from typing import Dict, List, Any


class SecurityAgent:
    """Agent responsible for security analysis and recommendations."""
    
    def __init__(self, llm_client):
        """
        Initialize the Security Agent.
        
        Args:
            llm_client: LLM client for AI-powered security analysis
        """
        self.llm_client = llm_client
        self.agent_name = "Security Agent"
    
    def analyze_security(self, architecture: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze security aspects of the architecture.
        
        Args:
            architecture: Architecture design
            requirements: Requirements including compliance needs
            
        Returns:
            Dictionary containing security analysis
        """
        print(f"[{self.agent_name}] Analyzing security requirements...")
        
        prompt = f"""
        Analyze the security aspects of the following architecture and requirements:
        
        Architecture:
        {architecture.get('architecture_design', '')}
        
        Requirements:
        {requirements.get('structured_requirements', '')}
        
        Provide:
        1. Security controls and measures
        2. Identity and Access Management (IAM) recommendations
        3. Data encryption (at rest and in transit)
        4. Network security (firewalls, VPNs, security groups)
        5. Compliance considerations (GDPR, HIPAA, SOC2, etc.)
        6. Threat modeling and risk assessment
        7. Security monitoring and incident response
        
        Provide detailed security recommendations with best practices.
        """
        
        security_analysis = self.llm_client.generate(prompt)
        
        result = {
            "security_analysis": security_analysis,
            "status": "completed",
            "agent": self.agent_name
        }
        
        print(f"[{self.agent_name}] Security analysis completed.")
        return result
    
    def create_security_checklist(self, security_analysis: Dict[str, Any]) -> List[str]:
        """
        Create a security implementation checklist.
        
        Args:
            security_analysis: Security analysis results
            
        Returns:
            List of security checklist items
        """
        prompt = f"""
        Based on the following security analysis, create a detailed implementation checklist:
        
        {security_analysis.get('security_analysis', '')}
        
        Format as a checklist with actionable items.
        """
        
        checklist_text = self.llm_client.generate(prompt)
        checklist = [item.strip() for item in checklist_text.split('\n') if item.strip()]
        
        return checklist
    
    def assess_compliance(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess compliance requirements and provide guidance.
        
        Args:
            requirements: Requirements including compliance needs
            
        Returns:
            Compliance assessment and recommendations
        """
        prompt = f"""
        Assess compliance requirements based on:
        
        {requirements.get('structured_requirements', '')}
        
        Identify applicable compliance frameworks and provide implementation guidance.
        """
        
        compliance_assessment = self.llm_client.generate(prompt)
        
        return {
            "compliance_assessment": compliance_assessment,
            "status": "completed"
        }
