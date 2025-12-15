"""
PDF Reader Utility
Extracts text content from PDF files
"""
from pathlib import Path
from pypdf import PdfReader


def read_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    pdf_path = Path(file_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"File must be a PDF: {file_path}")
    
    reader = PdfReader(str(pdf_path))
    
    # Extract text from all pages
    text_content = []
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if text.strip():
            text_content.append(text)
    
    combined_text = "\n\n".join(text_content)
    
    if not combined_text.strip():
        raise ValueError(f"No text content extracted from PDF: {file_path}")
    
    return combined_text


def read_rfp(file_path: str) -> str:
    """
    Read RFP from file (supports .txt and .pdf)
    
    Args:
        file_path: Path to RFP file
        
    Returns:
        RFP text content
    """
    path = Path(file_path)
    
    if path.suffix.lower() == '.pdf':
        return read_pdf(file_path)
    elif path.suffix.lower() in ['.txt', '.md']:
        return path.read_text(encoding='utf-8')
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .pdf, .txt, or .md")
