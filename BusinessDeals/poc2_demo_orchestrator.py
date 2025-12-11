import json
import uuid
import subprocess
import threading
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import time
import random

class DemoPersona(Enum):
    CTO = "cto"
    SECURITY_LEAD = "security"
    FINOPS_MANAGER = "finops"
    DEVOPS_ENGINEER = "devops"

class DemoOrchestrator:
    """AI-powered demo environment orchestrator"""
    
    def __init__(self):
        self.active_demos = {}
        self.demo_scenarios = self._load_scenarios()
        self.feedback_analyzer = FeedbackAnalyzer()
        
    def create_personalized_demo(self, stakeholder_info: Dict) -> Dict:
        """Creates AI-personalized demo environment"""
        
        # Step 1: Persona analysis agent
        persona = self._analyze_persona(stakeholder_info)
        
        # Step 2: Scenario selection agent
        scenario = self._select_scenario(persona, stakeholder_info)
        
        # Step 3: Environment provisioning agent
        demo_env = self._provision_environment(scenario)
        
        # Step 4: Data injection agent
        self._inject_realistic_data(demo_env, stakeholder_info)
        
        # Step 5: Narrative generation agent
        narrative = self._generate_narrative(persona, scenario)
        
        # Step 6: Interactive guide creation
        interactive_guide = self._create_interactive_guide(scenario)
        
        demo_id = str(uuid.uuid4())
        self.active_demos[demo_id] = {
            "id": demo_id,
            "persona": persona,
            "scenario": scenario,
            "environment": demo_env,
            "narrative": narrative,
            "guide": interactive_guide,
            "start_time": time.time(),
            "feedback": []
        }
        
        return {
            "demo_id": demo_id,
            "access_url": f"https://demo.company.com/{demo_id}",
            "persona_based_scenario": scenario["name"],
            "estimated_duration": "15 minutes",
            "key_metrics_to_watch": scenario["metrics"],
            "interactive_elements": interactive_guide["branches"]
        }
    
    def _analyze_persona(self, stakeholder: Dict) -> DemoPersona:
        """AI agent that analyzes stakeholder persona"""
        # In production, uses NLP on stakeholder info
        concerns = stakeholder.get("concerns", "").lower()
        
        if any(word in concerns for word in ["cost", "budget", "roi", "tco"]):
            return DemoPersona.FINOPS_MANAGER
        elif any(word in concerns for word in ["security", "compliance", "gdpr", "hipaa"]):
            return DemoPersona.SECURITY_LEAD
        elif any(word in concerns for word in ["kubernetes", "terraform", "ci/cd", "automation"]):
            return DemoPersona.DEVOPS_ENGINEER
        else:
            return DemoPersona.CTO
    
    def _select_scenario(self, persona: DemoPersona, stakeholder: Dict) -> Dict:
        """AI selects the most relevant demo scenario"""
        scenarios = {
            DemoPersona.CTO: [
                {
                    "name": "Business Resilience Showcase",
                    "setup": "Multi-region active-active deployment",
                    "failure_scenarios": ["Region outage", "AZ failure", "Database corruption"],
                    "metrics": ["RTO achieved", "RPO achieved", "Cost of resilience"],
                    "value_prop": "Proven 99.99% uptime with 40% lower cost"
                }
            ],
            DemoPersona.SECURITY_LEAD: [
                {
                    "name": "Zero Trust Security Demo",
                    "setup": "Simulated breach environment",
                    "failure_scenarios": ["Ransomware attack", "Data exfiltration", "Insider threat"],
                    "metrics": ["Time to detect", "Time to contain", "Data protected"],
                    "value_prop": "Automated threat response in <60 seconds"
                }
            ],
            DemoPersona.FINOPS_MANAGER: [
                {
                    "name": "FinOps Transformation",
                    "setup": "Multi-cloud cost dashboard with waste",
                    "failure_scenarios": ["Cost overrun", "Resource sprawl", "Vendor lock-in"],
                    "metrics": ["Cost avoidance", "Optimization savings", "ROI timeline"],
                    "value_prop": "35% cost reduction in 90 days"
                }
            ],
            DemoPersona.DEVOPS_ENGINEER: [
                {
                    "name": "GitOps at Scale",
                    "setup": "500+ microservices deployment pipeline",
                    "failure_scenarios": ["Rollback scenario", "Canary failure", "Config drift"],
                    "metrics": ["Deployment frequency", "Change failure rate", "MTTR"],
                    "value_prop": "10x faster deployments with zero downtime"
                }
            ]
        }
        
        # AI adds personalized touches based on stakeholder info
        selected = random.choice(scenarios[persona])
        
        # Personalize based on industry
        industry = stakeholder.get("industry", "").lower()
        if industry == "finance":
            selected["value_prop"] += " with PCI-DSS compliance baked in"
        elif industry == "healthcare":
            selected["value_prop"] += " with HIPAA-ready architecture"
        
        return selected
    
    def _provision_environment(self, scenario: Dict) -> Dict:
        """Provisions the demo environment using IaC"""
        # In production, this would call Terraform/Ansible
        env_id = f"demo-{uuid.uuid4().hex[:8]}"
        
        # Simulate provisioning different components
        components = [
            {"type": "kubernetes", "status": "running", "nodes": 3},
            {"type": "monitoring", "status": "configured", "tool": "grafana"},
            {"type": "security", "status": "enabled", "tools": ["falco", "trivy"]},
            {"type": "cost_dashboard", "status": "populated", "tool": "kubecost"}
        ]
        
        # Add scenario-specific components
        if "ransomware" in scenario["name"].lower():
            components.append({"type": "attack_simulator", "status": "armed"})
        
        return {
            "id": env_id,
            "components": components,
            "access_urls": {
                "dashboard": f"https://{env_id}.demos.company.com",
                "api": f"https://api.{env_id}.demos.company.com",
                "ssh": f"ssh://demo@{env_id}.demos.company.com:2222"
            },
            "ttl_hours": 24  # Auto-destroy after 24 hours
        }
    
    def _inject_realistic_data(self, env: Dict, stakeholder: Dict):
        """AI agent that injects realistic, relevant data"""
        # Generates synthetic but realistic data
        industry = stakeholder.get("industry", "tech")
        
        data_templates = {
            "finance": {
                "transactions_per_second": 1000,
                "data_pattern": "high_frequency_trading",
                "sensitivity": "pci_data"
            },
            "healthcare": {
                "transactions_per_second": 500,
                "data_pattern": "patient_records",
                "sensitivity": "phi_data"
            },
            "ecommerce": {
                "transactions_per_second": 5000,
                "data_pattern": "shopping_cart_abandonment",
                "sensitivity": "pii_data"
            },
            "tech": {
                "transactions_per_second": 2000,
                "data_pattern": "general_workload",
                "sensitivity": "standard"
            }
        }
        
        env["injected_data"] = data_templates.get(industry, data_templates["tech"])
    
    def _load_scenarios(self) -> Dict:
        """Load demo scenarios from configuration"""
        # In production, this would load from a database or config file
        return {
            "resilience": {"name": "Business Resilience", "type": "disaster_recovery"},
            "security": {"name": "Zero Trust Security", "type": "security"},
            "finops": {"name": "Cost Optimization", "type": "finops"},
            "devops": {"name": "GitOps Pipeline", "type": "automation"}
        }
    
    def _generate_narrative(self, persona: DemoPersona, scenario: Dict) -> Dict:
        """AI generates persona-specific storytelling"""
        narratives = {
            DemoPersona.CTO: {
                "opening": "Let me show you how we guarantee business continuity...",
                "challenge": "When disaster strikes, every minute costs millions...",
                "solution": "Our architecture automatically fails over in seconds...",
                "proof": "Watch as we simulate a complete region outage...",
                "closing": "This isn't just infrastructure; it's business insurance."
            },
            DemoPersona.FINOPS_MANAGER: {
                "opening": "Let me show you hidden costs in your current setup...",
                "challenge": "Most companies overspend by 40% on cloud...",
                "solution": "Our AI identifies waste in real-time...",
                "proof": "Watch as we automatically rightsize these overprovisioned VMs...",
                "closing": "We typically find 35% savings in the first 90 days."
            }
        }
        
        return narratives.get(persona, narratives[DemoPersona.CTO])
    
    def _create_interactive_guide(self, scenario: Dict) -> Dict:
        """Creates interactive 'choose your own adventure' demo"""
        guide = {
            "title": scenario["name"],
            "branches": [
                {
                    "id": "success_path",
                    "label": "Show me the happy path",
                    "scenes": ["Setup", "Normal Operation", "Benefits Realized"]
                },
                {
                    "id": "failure_path",
                    "label": "Break something!",
                    "scenes": ["Induce Failure", "Observe Response", "Verify Recovery"]
                },
                {
                    "id": "deep_dive",
                    "label": "I'm technical - show me details",
                    "scenes": ["Architecture", "Implementation", "Monitoring"]
                }
            ],
            "metrics_dashboard": {
                "live_feed": True,
                "customizable": True,
                "exportable": True
            }
        }
        return guide
    
    def process_real_time_feedback(self, demo_id: str, feedback: Dict):
        """AI agent that adapts demo based on live feedback"""
        if demo_id not in self.active_demos:
            return
        
        analysis = self.feedback_analyzer.analyze(feedback)
        
        # AI decides to adapt demo
        if analysis["sentiment"] == "confused":
            # Simplify the narrative
            self._adjust_complexity(demo_id, -1)
        elif analysis["sentiment"] == "bored":
            # Add more failure scenarios
            self._add_more_chaos(demo_id)
        elif analysis["sentiment"] == "excited":
            # Deep dive into technical details
            self._show_technical_depth(demo_id)
        
        # Update demo based on feedback
        self.active_demos[demo_id]["feedback"].append({
            "timestamp": time.time(),
            "feedback": feedback,
            "ai_response": analysis["adaptation"]
        })
    
    def _adjust_complexity(self, demo_id: str, adjustment: int):
        """AI adjusts demo complexity in real-time"""
        pass
    
    def _add_more_chaos(self, demo_id: str):
        """AI adds more failure scenarios"""
        pass
    
    def _show_technical_depth(self, demo_id: str):
        """AI shows deeper technical details"""
        pass

class FeedbackAnalyzer:
    """AI agent that analyzes stakeholder feedback in real-time"""
    
    def analyze(self, feedback: Dict) -> Dict:
        # Simple sentiment analysis - in production would use NLP
        text = feedback.get("text", "").lower()
        
        positive_words = ["good", "great", "interesting", "impressive", "cool"]
        negative_words = ["confusing", "boring", "slow", "complex", "expensive"]
        
        sentiment = "neutral"
        if any(word in text for word in positive_words):
            sentiment = "excited"
        elif any(word in text for word in negative_words):
            sentiment = "confused" if "confus" in text else "bored"
        
        return {
            "sentiment": sentiment,
            "confidence": 0.85,
            "adaptation": self._suggest_adaptation(sentiment),
            "key_topics": self._extract_topics(text)
        }
    
    def _suggest_adaptation(self, sentiment: str) -> str:
        adaptations = {
            "excited": "Deep dive into technical architecture",
            "confused": "Simplify with more analogies",
            "bored": "Induce a major failure scenario",
            "neutral": "Ask more qualifying questions"
        }
        return adaptations.get(sentiment, "Continue current path")
    
    def _extract_topics(self, text: str) -> List[str]:
        topics = []
        if "cost" in text:
            topics.append("pricing")
        if "security" in text:
            topics.append("security")
        if "scale" in text:
            topics.append("scalability")
        return topics

# CLI Interface for testing
def main():
    """Test the demo orchestrator"""
    orchestrator = DemoOrchestrator()
    
    # Different stakeholder personas
    stakeholders = [
        {
            "name": "Sarah Chen",
            "title": "CTO",
            "company": "FinTech Startup",
            "concerns": "We can't afford downtime during trading hours",
            "industry": "finance",
            "tech_stack": ["AWS", "Kubernetes", "PostgreSQL"]
        },
        {
            "name": "David Park",
            "title": "FinOps Director",
            "company": "E-commerce Giant",
            "concerns": "Our cloud bill grew 300% last year with no visibility",
            "industry": "ecommerce",
            "tech_stack": ["Multi-cloud", "Microservices", "Databricks"]
        }
    ]
    
    print("🎭 AI-Powered Demo Orchestrator")
    print("=" * 50)
    
    for stakeholder in stakeholders:
        print(f"\n👤 Creating demo for: {stakeholder['name']} - {stakeholder['title']}")
        print(f"   Concerns: {stakeholder['concerns']}")
        
        demo = orchestrator.create_personalized_demo(stakeholder)
        
        print(f"\n🎯 AI-Selected Demo Scenario:")
        print(f"   Scenario: {demo['persona_based_scenario']}")
        print(f"   Access URL: {demo['access_url']}")
        print(f"   Interactive Elements: {len(demo['interactive_elements'])}")
        
        # Simulate real-time feedback
        feedbacks = [
            {"text": "This is interesting but can you show me the cost breakdown?", "timestamp": time.time()},
            {"text": "I'm confused about how the failover works", "timestamp": time.time() + 10}
        ]
        
        for feedback in feedbacks:
            print(f"\n💬 Real-time Feedback: '{feedback['text']}'")
            orchestrator.process_real_time_feedback(demo['demo_id'], feedback)
            # AI would adapt demo here
        
        print("\n✨ Differentiators Demonstrated:")
        print("   1. Persona-aware demo personalization")
        print("   2. Real-time adaptation to feedback")
        print("   3. Interactive 'choose your own adventure' paths")
        print("   4. Industry-specific data injection")

if __name__ == "__main__":
    main()
