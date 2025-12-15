"""
Orchestrator
Coordinates the workflow between all agents to process RFP and generate proposal.
"""

from typing import Dict, Any
from agents.rfp_analysis import RFPAnalysisAgent
from agents.requirements import RequirementsAgent
from agents.architecture import ArchitectureAgent
from agents.cost import CostAgent
from agents.security import SecurityAgent
from agents.proposal import ProposalAgent


class Orchestrator:
    """Orchestrates the multi-agent workflow for RFP processing."""
    
    def __init__(self, llm_client):
        """
        Initialize the Orchestrator with all agents.
        
        Args:
            llm_client: LLM client to be shared across agents
        """
        self.llm_client = llm_client
        
        # Initialize all agents
        self.rfp_agent = RFPAnalysisAgent(llm_client)
        self.requirements_agent = RequirementsAgent(llm_client)
        self.architecture_agent = ArchitectureAgent(llm_client)
        self.cost_agent = CostAgent(llm_client)
        self.security_agent = SecurityAgent(llm_client)
        self.proposal_agent = ProposalAgent(llm_client)
        
        print("🚀 Orchestrator initialized with all agents")
    
    def process_rfp(self, rfp_content: str) -> Dict[str, Any]:
        """
        Process RFP through the entire agent workflow.
        
        Args:
            rfp_content: Raw RFP document content
            
        Returns:
            Dictionary containing all outputs and final proposal
        """
        print("\n" + "="*60)
        print("Starting RFP Processing Pipeline")
        print("="*60 + "\n")
        
        outputs = {}
        
        # Stage 1: RFP Analysis
        print("📋 Stage 1: RFP Analysis")
        outputs['rfp_analysis'] = self.rfp_agent.analyze_rfp(rfp_content)
        print("✓ Stage 1 completed\n")
        
        # Stage 2: Requirements Processing
        print("📝 Stage 2: Requirements Processing")
        outputs['requirements'] = self.requirements_agent.process_requirements(outputs['rfp_analysis'])
        print("✓ Stage 2 completed\n")
        
        # Stage 3: Architecture Design
        print("🏗️  Stage 3: Architecture Design")
        outputs['architecture'] = self.architecture_agent.design_architecture(outputs['requirements'])
        print("✓ Stage 3 completed\n")
        
        # Stage 4: Cost Estimation
        print("💰 Stage 4: Cost Estimation")
        outputs['costs'] = self.cost_agent.estimate_costs(outputs['architecture'])
        print("✓ Stage 4 completed\n")
        
        # Stage 5: Security Analysis
        print("🔒 Stage 5: Security Analysis")
        outputs['security'] = self.security_agent.analyze_security(
            outputs['architecture'],
            outputs['requirements']
        )
        print("✓ Stage 5 completed\n")
        
        # Stage 6: Proposal Generation
        print("📄 Stage 6: Proposal Generation")
        outputs['proposal'] = self.proposal_agent.generate_proposal(outputs)
        print("✓ Stage 6 completed\n")
        
        print("="*60)
        print("✅ RFP Processing Pipeline Completed Successfully")
        print("="*60 + "\n")
        
        return outputs
    
    def save_outputs(self, outputs: Dict[str, Any], output_dir: str = "output") -> None:
        """
        Save all outputs to files.
        
        Args:
            outputs: All agent outputs
            output_dir: Directory to save outputs
        """
        import os
        import json
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save proposal document
        proposal_path = os.path.join(output_dir, "proposal.md")
        with open(proposal_path, 'w', encoding='utf-8') as f:
            f.write(outputs['proposal']['proposal_document'])
        print(f"💾 Proposal saved to: {proposal_path}")
        
        # Save all outputs as JSON
        json_path = os.path.join(output_dir, "all_outputs.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)
        print(f"💾 All outputs saved to: {json_path}")
    
    def get_summary(self, outputs: Dict[str, Any]) -> str:
        """
        Generate a summary of the processing results.
        
        Args:
            outputs: All agent outputs
            
        Returns:
            Summary string
        """
        summary = "\n" + "="*60 + "\n"
        summary += "PROCESSING SUMMARY\n"
        summary += "="*60 + "\n\n"
        
        for stage, data in outputs.items():
            status = data.get('status', 'unknown')
            agent = data.get('agent', stage)
            summary += f"✓ {agent}: {status}\n"
        
        summary += "\n" + "="*60 + "\n"
        return summary
