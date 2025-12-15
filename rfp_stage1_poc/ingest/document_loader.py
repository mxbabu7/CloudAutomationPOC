"""
Document Loader Module
Handles loading and preprocessing of RFP documents
Supports: TXT, PDF, DOCX formats
"""

import os
from pathlib import Path


def load_document(file_path: str) -> str:
    """
    Load document content from various formats
    
    Args:
        file_path: Path to the RFP document
        
    Returns:
        Text content of the document
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document not found: {file_path}")
    
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.txt':
        return _load_text(file_path)
    elif file_extension == '.pdf':
        return _load_pdf(file_path)
    elif file_extension == '.docx':
        return _load_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def _load_text(file_path: str) -> str:
    """Load plain text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def _load_pdf(file_path: str) -> str:
    """Load PDF file using PyPDF2"""
    try:
        import PyPDF2
        text = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF support. Install: pip install PyPDF2")


def _load_docx(file_path: str) -> str:
    """Load DOCX file using python-docx"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except ImportError:
        raise ImportError("python-docx is required for DOCX support. Install: pip install python-docx")


def preprocess_text(text: str) -> str:
    """
    Clean and normalize document text
    
    Args:
        text: Raw text from document
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace within lines but preserve line breaks
    lines = text.split('\n')
    cleaned_lines = [' '.join(line.split()) for line in lines]
    text = '\n'.join(cleaned_lines)
    
    # Remove excessive blank lines (more than 2 consecutive)
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    
    return text.strip()
