"""
Cost Agent
Estimates cloud costs based on architecture design.
"""

from typing import Dict, List, Any


class CostAgent:
    """Agent responsible for estimating cloud costs."""
    
    def __init__(self, llm_client):
        """
        Initialize the Cost Agent.
        
        Args:
            llm_client: LLM client for AI-powered cost estimation
        """
        self.llm_client = llm_client
        self.agent_name = "Cost Agent"
    
    def estimate_costs(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate costs for the proposed architecture.
        
        Args:
            architecture: Architecture design from Architecture Agent
            
        Returns:
            Dictionary containing cost estimates
        """
        print(f"[{self.agent_name}] Estimating costs...")
        
        prompt = f"""
        Estimate the cloud costs for the following architecture:
        
        {architecture.get('architecture_design', '')}
        
        Provide:
        1. Monthly cost breakdown by service
        2. Annual cost projections
        3. Cost optimization recommendations
        4. Pricing tier recommendations (pay-as-you-go vs reserved instances)
        5. Potential cost drivers and variables
        
        Include ranges (min/typical/max) based on usage patterns.
        """
        
        cost_estimate = self.llm_client.generate(prompt)
        
        result = {
            "cost_estimate": cost_estimate,
            "status": "completed",
            "agent": self.agent_name
        }
        
        print(f"[{self.agent_name}] Cost estimation completed.")
        return result
    
    def analyze_cost_optimization(self, costs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and suggest cost optimization opportunities.
        
        Args:
            costs: Cost estimates
            
        Returns:
            Cost optimization recommendations
        """
        prompt = f"""
        Analyze the following cost estimates and provide optimization recommendations:
        
        {costs.get('cost_estimate', '')}
        
        Include:
        1. Immediate cost-saving opportunities
        2. Long-term optimization strategies
        3. Right-sizing recommendations
        4. Alternative service options
        5. Cost monitoring and alerting suggestions
        """
        
        optimization = self.llm_client.generate(prompt)
        
        return {
            "optimization_recommendations": optimization,
            "status": "completed"
        }
