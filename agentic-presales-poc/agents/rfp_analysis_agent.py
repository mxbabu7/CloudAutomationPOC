"""
RFP Analysis Agent
Analyzes RFP text and extracts structured requirements using AI
"""
import json
from config.ai_config import config
from utils.ai_client import ai_client


class RFPAnalysisAgent:
    def __init__(self):
        self.use_ai = config.ai_enabled
        
    def run(self, rfp_text: str) -> dict:
        """
        Analyzes RFP text and returns structured analysis
        
        Args:
            rfp_text: Raw RFP text input
            
        Returns:
            Structured dictionary containing RFP analysis
        """
        if self.use_ai:
            return self._analyze_with_ai(rfp_text)
        else:
            return self._analyze_static(rfp_text)
    
    def _analyze_with_ai(self, rfp_text: str) -> dict:
        """Use AI to analyze RFP"""
        system_prompt = """You are an expert RFP analyst. Analyze the provided RFP document and extract structured information.

Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks, just raw JSON):
{
  "business_goals": ["goal1", "goal2", ...],
  "functional_requirements": ["req1", "req2", ...],
  "non_functional_requirements": {
    "performance": "description",
    "security": "description",
    "availability": "description",
    "compliance": ["standard1", "standard2", ...]
  },
  "constraints": ["constraint1", "constraint2", ...],
  "assumptions": ["assumption1", "assumption2", ...],
  "risks": ["risk1", "risk2", ...]
}

Extract as much detail as possible from the RFP. Be specific and comprehensive."""

        try:
            print("🤖 Using AI to analyze RFP...")
            response = ai_client.analyze_with_prompt(system_prompt, rfp_text, temperature=0.3)
            
            # Clean the response (remove markdown code blocks if present)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
            print("✓ AI analysis complete")
            return result
            
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            print("⚠️ Falling back to static analysis")
            return self._analyze_static(rfp_text)
    
    def _analyze_static(self, rfp_text: str) -> dict:
        """Static fallback analysis"""
        return {
            "business_goals": [
                "Modernize infrastructure",
                "Improve scalability",
                "Enhance security posture",
                "Reduce operational costs"
            ],
            "functional_requirements": [
                "Web application hosting",
                "Database management",
                "User authentication and authorization",
                "API integration capabilities"
            ],
            "non_functional_requirements": {
                "performance": "Low latency (<100ms response time)",
                "security": "IAM, encryption at rest and in transit",
                "availability": "99.9% uptime SLA",
                "compliance": ["ISO 27001", "SOC 2", "GDPR"]
            },
            "constraints": [
                "Budget-conscious implementation",
                "6-month delivery timeline",
                "Use cloud-native services"
            ],
            "assumptions": [
                "Greenfield deployment",
                "Cloud infrastructure available",
                "Team has cloud expertise"
            ],
            "risks": [
                "Legacy integration complexity",
                "Data migration challenges",
                "Skill gap in cloud technologies"
            ]
        }
