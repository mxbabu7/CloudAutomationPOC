"""
Orchestrator
Coordinates all Stages 1-5 and manages the RFP processing pipeline
"""

import json
import csv
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from agents.requirements_agent import extract_requirements
from agents.evaluation_agent import extract_evaluation
from agents.risk_agent import identify_risks
from agents.strategy_agent import generate_strategy, format_strategy_brief
from agents.architecture_mapping_agent import map_architecture, save_architecture_mappings
from agents.diagram_agent import generate_diagram
from agents.costing_agent import estimate_costs
from agents.proposal_pack_agent import generate_proposal_pack


class RFPOrchestrator:
    """
    Orchestrates complete RFP processing pipeline (Stages 1-5)
    Coordinates requirements extraction, architecture mapping, diagram generation,
    cost estimation, and proposal generation
    """
    
    def __init__(self, config_file: str = "config.yaml", output_dir: str = "output"):
        """
        Initialize orchestrator
        
        Args:
            config_file: Path to configuration file
            output_dir: Base directory for output files
        """
        self.config = self._load_config(config_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.results = {
            "stage1": {},
            "stage2": {},
            "stage3": {},
            "stage4": {},
            "stage5": {}
        }
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"[WARN] Config file {config_file} not found, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "cloud": {"provider": "azure", "region": "eastus"},
            "scale": "medium",
            "stages": {
                f"stage{i}": {"enabled": True} for i in range(1, 6)
            },
            "llm": {"enabled": True, "model": "gpt-4o-mini"},
            "output": {
                "directories": {
                    "stage1": "output",
                    "stage2": "stage2_architecture",
                    "stage3": "stage3_diagrams",
                    "stage4": "stage4_costing",
                    "stage5": "stage5_proposal"
                }
            }
        }
    
    def run_complete_pipeline(self, rfp_text: str, llm_client: Optional[Any] = None) -> Dict[str, Any]:
        """
        Execute complete Stages 1-5 processing pipeline
        
        Args:
            rfp_text: Full text of RFP document
            llm_client: Optional LLM client for all agents
            
        Returns:
            Dictionary containing all stage outputs
        """
        
        print("=" * 80)
        print("RFP AGENTIC PLATFORM - STAGES 1-5 PROCESSING")
        print("=" * 80)
        print(f"\nCloud Provider: {self.config['cloud']['provider'].upper()}")
        print(f"Scale: {self.config['scale'].title()}")
        print("")
        
        # Stage 1: Compliance & Requirements
        if self.config["stages"]["stage1"]["enabled"]:
            self.results["stage1"] = self.run_stage1(rfp_text, llm_client)
        
        # Stage 2: Architecture Mapping
        if self.config["stages"]["stage2"]["enabled"]:
            self.results["stage2"] = self.run_stage2(
                self.results["stage1"]["requirements"],
                self.config["cloud"]["provider"],
                llm_client
            )
        
        # Stage 3: Diagram Generation
        if self.config["stages"]["stage3"]["enabled"]:
            self.results["stage3"] = self.run_stage3(
                self.results["stage2"]["mappings"],
                self.config["cloud"]["provider"]
            )
        
        # Stage 4: Cost Estimation
        if self.config["stages"]["stage4"]["enabled"]:
            self.results["stage4"] = self.run_stage4(
                self.results["stage2"]["mappings"],
                self.config["cloud"]["provider"],
                self.config["scale"],
                llm_client
            )
        
        # Stage 5: Proposal Generation
        if self.config["stages"]["stage5"]["enabled"]:
            self.results["stage5"] = self.run_stage5(
                self.results["stage1"],
                self.results["stage2"]["mappings"],
                self.results["stage4"]["cost_estimate"],
                self.config["cloud"]["provider"],
                llm_client
            )
        
        print("\n" + "=" * 80)
        print("ALL STAGES COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        return self.results
    
    def run_stage1(self, rfp_text: str, llm_client: Optional[Any] = None) -> Dict[str, Any]:
        """Execute Stage 1 processing pipeline"""
        
        print("\n" + "=" * 80)
        print("STAGE 1: COMPLIANCE & REQUIREMENTS ANALYSIS")
        print("=" * 80)
        
        stage1_results = {
            "requirements": [],
            "evaluation": {},
            "risks": [],
            "strategy": {}
        }
        
        # Step 1: Extract Requirements
        print("\n[1/4] Extracting requirements...")
        stage1_results["requirements"] = extract_requirements(rfp_text, llm_client)
        print(f"[OK] Extracted {len(stage1_results['requirements'])} requirements")
        
        # Step 2: Extract Evaluation Criteria
        print("\n[2/4] Extracting evaluation criteria...")
        stage1_results["evaluation"] = extract_evaluation(rfp_text, llm_client)
        criteria_count = len(stage1_results["evaluation"].get("criteria", []))
        print(f"[OK] Identified {criteria_count} evaluation criteria")
        
        # Step 3: Identify Risks
        print("\n[3/4] Identifying risks...")
        stage1_results["risks"] = identify_risks(stage1_results["requirements"], llm_client)
        print(f"[OK] Identified {len(stage1_results['risks'])} risks")
        
        # Step 4: Generate Strategy
        print("\n[4/4] Generating response strategy...")
        stage1_results["strategy"] = generate_strategy(
            stage1_results["requirements"],
            stage1_results["evaluation"],
            stage1_results["risks"],
            llm_client
        )
        print("[OK] Strategy generated")
        
        # Save Stage 1 outputs
        output_dir = self.config["output"]["directories"]["stage1"]
        self._save_stage1_outputs(stage1_results, output_dir)
        
        return stage1_results
    
    def run_stage2(
        self, 
        requirements: list, 
        cloud_provider: str,
        llm_client: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Execute Stage 2: Architecture Mapping"""
        
        print("\n" + "=" * 80)
        print("STAGE 2: ARCHITECTURE MAPPING")
        print("=" * 80)
        
        print(f"\n[1/2] Mapping requirements to {cloud_provider.upper()} services...")
        mappings = map_architecture(requirements, cloud_provider, llm_client)
        print(f"[OK] Mapped {len(mappings)} requirements to cloud services")
        
        print("\n[2/2] Saving architecture mappings...")
        output_dir = self.config["output"]["directories"]["stage2"]
        save_architecture_mappings(mappings, output_dir)
        
        return {"mappings": mappings}
    
    def run_stage3(self, architecture_mappings: list, cloud_provider: str) -> Dict[str, Any]:
        """Execute Stage 3: Diagram Generation"""
        
        print("\n" + "=" * 80)
        print("STAGE 3: DIAGRAM GENERATION")
        print("=" * 80)
        
        print(f"\n[1/1] Generating {cloud_provider.upper()} architecture diagram...")
        output_dir = self.config["output"]["directories"]["stage3"]
        diagram_file = generate_diagram(architecture_mappings, cloud_provider, output_dir)
        
        return {"diagram_file": diagram_file}
    
    def run_stage4(
        self,
        architecture_mappings: list,
        cloud_provider: str,
        scale: str,
        llm_client: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Execute Stage 4: Cost Estimation"""
        
        print("\n" + "=" * 80)
        print("STAGE 4: COST ESTIMATION")
        print("=" * 80)
        
        print(f"\n[1/1] Estimating costs for {scale} scale deployment...")
        output_dir = self.config["output"]["directories"]["stage4"]
        cost_estimate = estimate_costs(
            architecture_mappings,
            cloud_provider,
            scale,
            llm_client,
            output_dir
        )
        
        expected = cost_estimate.get("summary", {}).get("expected", 0)
        print(f"[OK] Expected monthly cost: ${expected:,.2f}")
        
        return {"cost_estimate": cost_estimate}
    
    def run_stage5(
        self,
        stage1_results: Dict[str, Any],
        architecture_mappings: list,
        cost_estimate: Dict[str, Any],
        cloud_provider: str,
        llm_client: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Execute Stage 5: Proposal Pack Generation"""
        
        print("\n" + "=" * 80)
        print("STAGE 5: PROPOSAL GENERATION")
        print("=" * 80)
        
        output_dir = self.config["output"]["directories"]["stage5"]
        artifacts = generate_proposal_pack(
            stage1_results,
            architecture_mappings,
            cost_estimate,
            cloud_provider,
            llm_client,
            output_dir
        )
        
        return {"artifacts": artifacts}
    
    def _save_stage1_outputs(self, results: Dict[str, Any], output_dir: str):
        """Save Stage 1 outputs"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print("\n" + "=" * 80)
        print("GENERATING STAGE 1 OUTPUT FILES")
        print("=" * 80)
        
        self._save_compliance_matrix(results, output_path)
        self._save_strategy_brief(results, output_path)
        self._save_full_report(results, output_path)
    
    def _save_compliance_matrix(self, results: Dict[str, Any], output_path: Path):
        """Save requirements as compliance matrix CSV"""
        
        output_file = output_path / "compliance_matrix.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['ID', 'Section', 'Type', 'Requirement', 'Owner', 'Status', 'Response']
            )
            writer.writeheader()
            
            for req in results["requirements"]:
                writer.writerow({
                    'ID': req['id'],
                    'Section': req['section'],
                    'Type': req['type'],
                    'Requirement': req['text'],
                    'Owner': req['owner'],
                    'Status': 'Pending',
                    'Response': ''
                })
        
        print(f"[OK] Compliance matrix saved: {output_file}")
    
    def _save_strategy_brief(self, results: Dict[str, Any], output_path: Path):
        """Save strategy as markdown brief"""
        
        output_file = output_path / "strategy_brief.md"
        
        strategy_md = format_strategy_brief(results["strategy"])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(strategy_md)
        
        print(f"[OK] Strategy brief saved: {output_file}")
    
    def _save_full_report(self, results: Dict[str, Any], output_path: Path):
        """Save complete JSON report"""
        
        output_file = output_path / "stage1_full_report.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Full report saved: {output_file}")
    
    def get_summary(self) -> str:
        """
        Get summary of all processing stages
        
        Returns:
            Formatted summary string
        """
        
        summary = []
        summary.append("\n" + "=" * 80)
        summary.append("COMPLETE PIPELINE SUMMARY")
        summary.append("=" * 80)
        
        # Stage 1 Summary
        if "stage1" in self.results and self.results["stage1"]:
            stage1 = self.results["stage1"]
            req_total = len(stage1.get("requirements", []))
            req_mandatory = sum(1 for r in stage1.get("requirements", []) if r.get('type') == 'Mandatory')
            
            summary.append(f"\n✓ STAGE 1: Compliance & Requirements")
            summary.append(f"  - Requirements: {req_total} ({req_mandatory} mandatory)")
            summary.append(f"  - Evaluation Criteria: {len(stage1.get('evaluation', {}).get('criteria', []))}")
            summary.append(f"  - Risks Identified: {len(stage1.get('risks', []))}")
        
        # Stage 2 Summary
        if "stage2" in self.results and self.results["stage2"]:
            stage2 = self.results["stage2"]
            mappings = stage2.get("mappings", [])
            
            summary.append(f"\n✓ STAGE 2: Architecture Mapping")
            summary.append(f"  - Services Mapped: {len(mappings)}")
            summary.append(f"  - Cloud Provider: {self.config['cloud']['provider'].upper()}")
        
        # Stage 3 Summary
        if "stage3" in self.results and self.results["stage3"]:
            summary.append(f"\n✓ STAGE 3: Diagram Generation")
            summary.append(f"  - Architecture diagram generated")
        
        # Stage 4 Summary
        if "stage4" in self.results and self.results["stage4"]:
            stage4 = self.results["stage4"]
            cost = stage4.get("cost_estimate", {}).get("summary", {})
            
            summary.append(f"\n✓ STAGE 4: Cost Estimation")
            summary.append(f"  - Expected Monthly: ${cost.get('expected', 0):,.2f}")
            summary.append(f"  - Range: ${cost.get('low', 0):,.2f} - ${cost.get('high', 0):,.2f}")
        
        # Stage 5 Summary
        if "stage5" in self.results and self.results["stage5"]:
            stage5 = self.results["stage5"]
            artifacts = stage5.get("artifacts", {})
            
            summary.append(f"\n✓ STAGE 5: Proposal Generation")
            summary.append(f"  - Artifacts Generated: {len(artifacts)}")
        
        summary.append("\n" + "=" * 80)
        summary.append("\nOUTPUT LOCATIONS:")
        summary.append(f"  - Stage 1: {self.config['output']['directories']['stage1']}/")
        summary.append(f"  - Stage 2: {self.config['output']['directories']['stage2']}/")
        summary.append(f"  - Stage 3: {self.config['output']['directories']['stage3']}/")
        summary.append(f"  - Stage 4: {self.config['output']['directories']['stage4']}/")
        summary.append(f"  - Stage 5: {self.config['output']['directories']['stage5']}/")
        summary.append("=" * 80)
        
        return "\n".join(summary)


def run_complete_pipeline(rfp_text: str, config_file: str = "config.yaml", llm_client: Optional[Any] = None) -> Dict[str, Any]:
    """
    Convenience function to run complete Stages 1-5 processing
    
    Args:
        rfp_text: RFP document text
        config_file: Path to configuration file
        llm_client: Optional LLM client
        
    Returns:
        Complete results from all stages
    """
    orchestrator = RFPOrchestrator(config_file=config_file)
    return orchestrator.run_complete_pipeline(rfp_text, llm_client)


# Backward compatibility alias
Stage1Orchestrator = RFPOrchestrator
