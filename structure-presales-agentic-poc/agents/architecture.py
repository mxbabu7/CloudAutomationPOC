"""
Architecture Agent
Designs cloud architecture solutions based on requirements.
"""

from typing import Dict, List, Any


class ArchitectureAgent:
    """Agent responsible for designing cloud architecture solutions."""
    
    def __init__(self, llm_client):
        """
        Initialize the Architecture Agent.
        
        Args:
            llm_client: LLM client for AI-powered design
        """
        self.llm_client = llm_client
        self.agent_name = "Architecture Agent"
    
    def design_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design cloud architecture based on requirements.
        
        Args:
            requirements: Structured requirements from Requirements Agent
            
        Returns:
            Dictionary containing architecture design
        """
        print(f"[{self.agent_name}] Designing cloud architecture...")
        
        prompt = f"""
        Design a cloud architecture solution based on the following requirements:
        
        {requirements.get('structured_requirements', '')}
        
        Include:
        1. High-level architecture overview
        2. Cloud services and components (AWS/Azure/GCP)
        3. Data flow and integration points
        4. Scalability and high availability design
        5. Security architecture
        6. Network design
        
        Provide a detailed architecture design with rationale for choices.
        """
        
        architecture_design = self.llm_client.generate(prompt)
        
        result = {
            "architecture_design": architecture_design,
            "status": "completed",
            "agent": self.agent_name
        }
        
        print(f"[{self.agent_name}] Architecture design completed.")
        return result
    
    def create_component_mapping(self, architecture: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Create mapping of requirements to architecture components.
        
        Args:
            architecture: Architecture design
            
        Returns:
            Mapping of requirements to components
        """
        prompt = f"""
        Based on the following architecture design, create a mapping of:
        - Requirements to specific cloud services
        - Components to their purposes
        - Integration points between services
        
        Architecture:
        {architecture.get('architecture_design', '')}
        
        Provide a clear component mapping.
        """
        
        mapping = self.llm_client.generate(prompt)
        
        return {
            "component_mapping": mapping,
            "status": "completed"
        }
