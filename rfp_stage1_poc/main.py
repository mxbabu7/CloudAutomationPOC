"""
Main Entry Point for RFP Agentic Platform
Stages 1-5: End-to-End RFP Automation
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ingest.document_loader import load_document, preprocess_text
from orchestrator import RFPOrchestrator


def main():
    """Main execution function"""
    
    print("\n" + "=" * 80)
    print("RFP AGENTIC PLATFORM - STAGES 1-5")
    print("End-to-End RFP Automation: Compliance → Architecture → Diagrams → Costing → Proposal")
    print("=" * 80)
    
    # Configuration - default to PDF file in project directory
    project_dir = Path(__file__).parent
    rfp_file = str(project_dir / "MMI Cloud Requirements.pdf")
    config_file = str(project_dir / "config.yaml")
    
    # Allow custom RFP file from command line
    if len(sys.argv) > 1:
        rfp_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(rfp_file):
        print(f"\nError: RFP file not found: {rfp_file}")
        print("\nUsage: python main.py [rfp_file_path]")
        print(f"Default: python main.py (uses {rfp_file})")
        sys.exit(1)
    
    print(f"\nConfiguration: {config_file}")
    print(f"RFP Document: {rfp_file}")
    
    try:
        # Load and preprocess document
        print("\nLoading RFP document...")
        rfp_text = load_document(rfp_file)
        rfp_text = preprocess_text(rfp_text)
        
        print(f"[OK] Document loaded ({len(rfp_text)} characters)")
        
        # Initialize LLM client (optional)
        llm_client = get_llm_client()
        
        if llm_client:
            print("[OK] LLM client initialized - Using AI-enhanced agents")
        else:
            print("[WARN] No LLM configured - Using rule-based extraction")
            print("  To enable LLM: Set OPENAI_API_KEY or AZURE_OPENAI_KEY environment variable")
        
        # Create and run orchestrator for complete pipeline
        orchestrator = RFPOrchestrator(config_file=config_file)
        results = orchestrator.run_complete_pipeline(rfp_text, llm_client)
        
        # Display summary
        print(orchestrator.get_summary())
        
        # Success
        print("\n" + "=" * 80)
        print("[SUCCESS] COMPLETE PIPELINE EXECUTED SUCCESSFULLY!")
        print("=" * 80)
        
        print("\n📦 Generated Artifacts:")
        print("\n  Stage 1 - Compliance & Requirements:")
        print("    - output/compliance_matrix.csv")
        print("    - output/strategy_brief.md")
        print("    - output/stage1_full_report.json")
        
        print("\n  Stage 2 - Architecture Mapping:")
        print("    - stage2_architecture/architecture_mappings.json")
        print("    - stage2_architecture/architecture_mappings.csv")
        
        print("\n  Stage 3 - Diagrams:")
        print("    - stage3_diagrams/azure_architecture.drawio.xml")
        print("    - stage3_diagrams/architecture_summary.md")
        
        print("\n  Stage 4 - Cost Estimation:")
        print("    - stage4_costing/cost_estimate.json")
        print("    - stage4_costing/cost_breakdown.csv")
        print("    - stage4_costing/cost_summary.md")
        
        print("\n  Stage 5 - Proposal Pack:")
        print("    - stage5_proposal/MASTER_PROPOSAL.md")
        print("    - stage5_proposal/executive_summary.md")
        print("    - stage5_proposal/technical_proposal.md")
        print("    - stage5_proposal/pricing_proposal.md")
        print("    - stage5_proposal/risks_and_assumptions.md")
        
        print("\n" + "=" * 80)
        print("✓ All artifacts ready for review and delivery!")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] File not found: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] File not found: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def get_llm_client():
    """
    Initialize LLM client based on environment variables
    
    Returns:
        LLM client or None if not configured
    """
    
    try:
        # Fix SSL certificate issue by using certifi
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        
        # Try OpenAI
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            return OpenAI()
        
        # Try Azure OpenAI
        elif os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            from openai import AzureOpenAI
            return AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
    except ImportError as e:
        print(f"[WARN] Library not installed: {e}")
    except Exception as e:
        print(f"[WARN] Could not initialize LLM client: {e}")
    
    return None


def print_configuration_help():
    """Print help for LLM configuration"""
    
    print("\n" + "=" * 60)
    print("LLM CONFIGURATION")
    print("=" * 60)
    print("\nTo use OpenAI:")
    print("  export OPENAI_API_KEY='your-api-key'")
    print("\nTo use Azure OpenAI:")
    print("  export AZURE_OPENAI_KEY='your-api-key'")
    print("  export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com'")
    print("  export AZURE_OPENAI_DEPLOYMENT='gpt-4'  # optional")
    print("  export AZURE_OPENAI_API_VERSION='2024-02-15-preview'  # optional")
    print("\nWithout LLM configuration, the system will use rule-based extraction.")
    print("=" * 60)


if __name__ == "__main__":
    main()
