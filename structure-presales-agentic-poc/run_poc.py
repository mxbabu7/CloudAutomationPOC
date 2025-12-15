"""
Main entry point for the Presales Agentic POC
Runs the complete RFP processing pipeline
"""

import os
import sys
from dotenv import load_dotenv
from orchestrator import Orchestrator
from llm_client import LLMClient


def load_rfp_content(file_path: str) -> str:
    """
    Load RFP content from file (supports .txt and .pdf).
    
    Args:
        file_path: Path to RFP file
        
    Returns:
        RFP content as string
    """
    try:
        # Check if file is PDF
        if file_path.lower().endswith('.pdf'):
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                print(f"✓ Loaded RFP from PDF: {file_path}\n")
                return content
            except ImportError:
                print("❌ Error: PyPDF2 not installed. Run: pip install PyPDF2")
                sys.exit(1)
        else:
            # Load as text file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✓ Loaded RFP from: {file_path}\n")
            return content
    except FileNotFoundError:
        print(f"❌ Error: RFP file not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading RFP: {str(e)}")
        sys.exit(1)


def setup_llm_client() -> LLMClient:
    """
    Setup and return LLM client.
    
    Returns:
        Configured LLM client
    """
    provider = os.getenv('LLM_PROVIDER', 'openai')
    model = os.getenv('LLM_MODEL', 'gpt-4')
    
    print(f"🤖 Setting up {provider} client with model: {model}")
    
    if provider == "openai":
        return LLMClient(
            provider="openai",
            model=model,
            api_key=os.getenv('OPENAI_API_KEY')
        )
    elif provider == "azure":
        return LLMClient(
            provider="azure",
            model=model,
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'azure'.")


def main():
    """Main execution function."""
    # Load environment variables first
    load_dotenv()
    
    print("\n" + "="*60)
    print("PRESALES AGENTIC POC - RFP PROCESSING SYSTEM")
    print("="*60 + "\n")
    
    # Configuration
    RFP_FILE = os.getenv('RFP_FILE', 'MMI Cloud Requirements.pdf')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    
    # Setup
    llm_client = setup_llm_client()
    orchestrator = Orchestrator(llm_client)
    
    # Load RFP
    rfp_content = load_rfp_content(RFP_FILE)
    
    # Process RFP
    outputs = orchestrator.process_rfp(rfp_content)
    
    # Save outputs
    print("\n💾 Saving outputs...")
    orchestrator.save_outputs(outputs, OUTPUT_DIR)
    
    # Print summary
    summary = orchestrator.get_summary(outputs)
    print(summary)
    
    print("🎉 POC execution completed successfully!")
    print(f"📂 Check the '{OUTPUT_DIR}' directory for all outputs.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
