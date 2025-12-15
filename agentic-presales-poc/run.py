"""
Agentic Pre-Sales POC - Main Entry Point
"""
import os
import sys

# Fix SSL certificate issues (common in corporate environments)
# Remove problematic SSL_CERT_FILE if it points to non-existent file
if 'SSL_CERT_FILE' in os.environ:
    ssl_cert = os.environ['SSL_CERT_FILE']
    if not os.path.exists(ssl_cert):
        print(f"⚠️ Removing invalid SSL_CERT_FILE: {ssl_cert}")
        del os.environ['SSL_CERT_FILE']

from agents.orchestrator import Orchestrator
from pathlib import Path
from utils.pdf_reader import read_rfp


if __name__ == "__main__":
    # Read sample RFP - supports both .txt and .pdf files
    rfp_text = read_rfp("sample_input/MMI Cloud Requirements.pdf")
    
    # Verify PDF reading - save extracted text for review
    print("\n" + "="*60)
    print("PDF TEXT EXTRACTION VERIFICATION")
    print("="*60)
    print(f"\n📄 File: sample_input/MMI Cloud Requirements.pdf")
    print(f"📊 Extracted text length: {len(rfp_text)} characters")
    print(f"📝 First 500 characters:\n")
    print(rfp_text[:500])
    print("\n" + "="*60 + "\n")
    
    # Save extracted text for review
    Path("output").mkdir(exist_ok=True)
    Path("output/extracted_rfp_text.txt").write_text(rfp_text, encoding='utf-8')
    print("✓ Full extracted text saved to: output/extracted_rfp_text.txt\n")

    # Initialize orchestrator with target cloud
    # Options: "Azure", "AWS", "GCP"
    orchestrator = Orchestrator(target_cloud="AWS")
    
    # Execute the POC
    orchestrator.execute(rfp_text)
