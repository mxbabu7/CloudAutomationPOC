"""
Architecture Agent
Designs cloud-agnostic logical architecture based on RFP analysis using AI
"""
import json
from config.ai_config import config
from utils.ai_client import ai_client


class ArchitectureAgent:
    def __init__(self):
        self.use_ai = config.ai_enabled
    
    def run(self, rfp_analysis: dict) -> dict:
        """
        Creates logical architecture based on RFP analysis
        
        Args:
            rfp_analysis: Structured RFP analysis from RFPAnalysisAgent
            
        Returns:
            Cloud-agnostic architecture specification
        """
        if self.use_ai:
            return self._design_with_ai(rfp_analysis)
        else:
            return self._design_static(rfp_analysis)
    
    def _design_with_ai(self, rfp_analysis: dict) -> dict:
        """Use AI to design architecture"""
        system_prompt = """You are a cloud solutions architect. Design a cloud-agnostic logical architecture based on the RFP analysis provided.

Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks):
{
  "layers": [
    {
      "name": "Layer Name",
      "components": ["Component1", "Component2"],
      "responsibilities": ["Responsibility1", "Responsibility2"]
    }
  ],
  "data_flow": [
    {
      "from": "Component A",
      "to": "Component B",
      "protocol": "HTTPS"
    }
  ],
  "security_controls": ["Control1", "Control2"],
  "scalability_approach": "Description of scaling strategy",
  "disaster_recovery": {
    "rpo": "Time value",
    "rto": "Time value",
    "strategy": "DR strategy description"
  }
}

Design a comprehensive, production-ready architecture."""

        try:
            print("🤖 Using AI to design architecture...")
            rfp_summary = json.dumps(rfp_analysis, indent=2)
            response = ai_client.analyze_with_prompt(
                system_prompt, 
                f"RFP Analysis:\n{rfp_summary}\n\nDesign the architecture based on these requirements.",
                temperature=0.4
            )
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
            print("✓ AI architecture design complete")
            return result
            
        except Exception as e:
            print(f"⚠️ AI architecture design failed: {e}")
            print("⚠️ Falling back to static architecture")
            return self._design_static(rfp_analysis)
    
    def _design_static(self, rfp_analysis: dict) -> dict:
        """Static fallback architecture"""
        # TODO: Integrate with LLM for intelligent architecture design
        
        return {
            "layers": [
                {
                    "name": "Presentation Layer",
                    "components": ["Web Application", "Mobile App", "CDN"],
                    "responsibilities": [
                        "User interface",
                        "Client-side logic",
                        "Content delivery"
                    ]
                },
                {
                    "name": "API Gateway Layer",
                    "components": ["API Gateway", "Load Balancer"],
                    "responsibilities": [
                        "Request routing",
                        "Rate limiting",
                        "Authentication"
                    ]
                },
                {
                    "name": "Application Layer",
                    "components": ["Compute Instances", "Container Orchestration"],
                    "responsibilities": [
                        "Business logic",
                        "Application services",
                        "Microservices"
                    ]
                },
                {
                    "name": "Data Layer",
                    "components": ["Relational Database", "Object Storage", "Cache"],
                    "responsibilities": [
                        "Data persistence",
                        "Data caching",
                        "File storage"
                    ]
                },
                {
                    "name": "Security & Identity Layer",
                    "components": ["Identity Provider", "Security Services"],
                    "responsibilities": [
                        "User authentication",
                        "Authorization",
                        "Threat detection"
                    ]
                },
                {
                    "name": "Monitoring & Operations Layer",
                    "components": ["Monitoring Service", "Logging Service"],
                    "responsibilities": [
                        "System monitoring",
                        "Log aggregation",
                        "Alerting"
                    ]
                }
            ],
            "data_flow": [
                {
                    "from": "Web Application",
                    "to": "API Gateway",
                    "protocol": "HTTPS"
                },
                {
                    "from": "API Gateway",
                    "to": "Application Layer",
                    "protocol": "HTTP/gRPC"
                },
                {
                    "from": "Application Layer",
                    "to": "Data Layer",
                    "protocol": "SQL/NoSQL"
                }
            ],
            "security_controls": [
                "End-to-end encryption",
                "Identity and Access Management",
                "Network segmentation",
                "DDoS protection",
                "Security monitoring and logging"
            ],
            "scalability_approach": "Horizontal scaling with auto-scaling groups",
            "disaster_recovery": {
                "rpo": "1 hour",
                "rto": "4 hours",
                "strategy": "Multi-region active-passive deployment"
            }
        }
