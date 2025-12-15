"""
Orchestrator Agent
Coordinates execution of all specialized agents
"""
from agents.rfp_analysis_agent import RFPAnalysisAgent
from agents.architecture_agent import ArchitectureAgent
from agents.diagram_agent import DiagramAgent
from agents.cloud_mapping_agent import CloudMappingAgent
from agents.cost_agent import CostAgent
from agents.proposal_agent import ProposalAgent
from agents.roadmap_agent import RoadmapAgent
from agents.ai_diagram_agent import AIDiagramAgent
from agents.word_document_agent import WordDocumentAgent
from utils.drawio_generator import generate_drawio_from_json
import json
from pathlib import Path


class Orchestrator:
    def __init__(self, target_cloud: str):
        """
        Initialize orchestrator with target cloud provider
        
        Args:
            target_cloud: Target cloud provider (Azure, AWS, GCP)
        """
        self.target_cloud = target_cloud
        print(f"🚀 Initializing Agentic Pre-Sales POC for {target_cloud}")

    def execute(self, rfp_text: str):
        """
        Execute all agents in sequence and generate outputs
        
        Args:
            rfp_text: Raw RFP text input
        """
        print("\n" + "="*60)
        print("AGENTIC PRE-SALES POC - EXECUTION STARTED")
        print("="*60 + "\n")
        
        # Step 1: RFP Analysis
        print("📋 Step 1/7: Analyzing RFP...")
        rfp = RFPAnalysisAgent().run(rfp_text)
        print("✓ RFP Analysis Complete")
        
        # Step 2: Architecture Design
        print("\n🏗️  Step 2/7: Designing Architecture...")
        arch = ArchitectureAgent().run(rfp)
        print("✓ Architecture Design Complete")
        
        # Step 3: Diagram Generation
        print("\n📊 Step 3/7: Generating Diagram Specification...")
        diagram = DiagramAgent().run(arch)
        print("✓ Diagram Specification Complete")
        
        # Step 4: Cloud Mapping
        print(f"\n☁️  Step 4/7: Mapping to {self.target_cloud} Services...")
        mapping = CloudMappingAgent().run(arch, self.target_cloud)
        print("✓ Cloud Mapping Complete")
        
        # Step 5: Cost Estimation
        print("\n💰 Step 5/7: Generating Cost Estimate...")
        cost = CostAgent().run(mapping)
        print(f"✓ Cost Estimate Complete: ${cost['summary']['total_monthly']:,.2f}/month")
        
        # Step 6: Proposal Generation
        print("\n📄 Step 6/7: Generating Proposal Document...")
        proposal = ProposalAgent().run(rfp, arch, cost)
        print("✓ Proposal Document Complete")
        
        # Step 7: Roadmap Generation
        print("\n🗓️  Step 7/7: Generating Delivery Roadmap...")
        roadmap = RoadmapAgent().run()
        print("✓ Delivery Roadmap Complete")
        
        # Save all outputs
        print("\n💾 Saving outputs...")
        Path("output").mkdir(exist_ok=True)
        self._save("rfp_analysis.json", rfp)
        self._save("architecture.json", arch)
        self._save("diagram.json", diagram)
        self._save("cost.json", cost)
        Path("output/proposal.md").write_text(proposal)
        Path("output/roadmap.json").write_text(json.dumps(roadmap, indent=2))
        
        # Generate Draw.io diagram
        print("\n🎨 Generating Draw.io diagram...")
        try:
            drawio_file = generate_drawio_from_json("output/diagram.json", "output/architecture.drawio")
            print("✓ Draw.io diagram generated successfully")
        except Exception as e:
            print(f"⚠️ Failed to generate Draw.io diagram: {e}")
        
        # Generate Python diagrams code (AI-powered)
        print("\n🐍 Generating Python diagrams code...")
        try:
            python_diagram_code = AIDiagramAgent().run(arch, mapping)
            Path("output/generate_python_diagram.py").write_text(python_diagram_code, encoding='utf-8')
            print("✓ Python diagrams code generated successfully")
            print("  Run: python output/generate_python_diagram.py")
        except Exception as e:
            print(f"⚠️ Failed to generate Python diagrams code: {e}")
        
        # Generate Word Document (Professional submission format)
        print("\n📄 Generating Word Document...")
        try:
            word_agent = WordDocumentAgent()
            word_agent.generate(
                rfp_file="output/rfp_analysis.json",
                arch_file="output/architecture.json",
                cost_file="output/cost.json",
                proposal_file="output/proposal.md",
                roadmap_file="output/roadmap.json",
                diagram_image="mmi_complete_architecture.png"
            )
            word_agent.save("output/Infrastructure_Solution_Architecture.docx")
            print("✓ Word document generated successfully")
        except Exception as e:
            print(f"⚠️ Failed to generate Word document: {e}")
            print(f"   Install python-docx: pip install python-docx")
        
        print("\n" + "="*60)
        print("✅ EXECUTION COMPLETE!")
        print("="*60)
        print("\n📂 Output files generated in ./output/:")
        print("   - rfp_analysis.json")
        print("   - architecture.json")
        print("   - diagram.json")
        print("   - architecture.drawio ⭐ (Open in Draw.io)")
        print("   - generate_python_diagram.py 🐍 (Run to create PNG)")
        print("   - Infrastructure_Solution_Architecture.docx 📄 (Submission ready)")
        print("   - cost.json")
        print("   - proposal.md")
        print("   - roadmap.json")
        print("\n💡 To view diagrams:")
        print("   📊 Draw.io: https://app.diagrams.net/ → Open architecture.drawio")
        print("   🐍 Python: python output/generate_python_diagram.py")
        print("\n💼 Professional Documents:")
        print("   📄 Word: output/Infrastructure_Solution_Architecture.docx")
        print("\n" + "="*60 + "\n")

    def _save(self, name: str, data: dict):
        """Save data to JSON file"""
        Path(f"output/{name}").write_text(json.dumps(data, indent=2))
