# document_parser.py
"""
Utility functions to parse documents into plain text.
Supports: PDF, DOCX, CSV
"""

import pandas as pd
import docx
from pdfminer.high_level import extract_text
from fastapi import UploadFile
import os
import tempfile

# ---------------------------
# Main function
# ---------------------------

async def parse_file(file: UploadFile) -> str:
    """
    Detect file type and extract text content.
    Returns plain text string.
    """

    # Save the file temporarily so parsers can read it
    filename = file.filename if file.filename is not None else ""
    suffix = os.path.splitext(filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Decide which parser to use
    if suffix == ".pdf":
        text = parse_pdf(tmp_path)
    elif suffix == ".docx":
        text = parse_docx(tmp_path)
    elif suffix == ".csv":
        text = parse_csv(tmp_path)
    else:
        text = ""

    # Clean up temp file
    os.remove(tmp_path)

    return text


# ---------------------------
# PDF parser
# ---------------------------

def parse_pdf(path: str) -> str:
    """Extract text from PDF using pdfminer."""
    try:
        text = extract_text(path)
    except Exception as e:
        text = f"Error parsing PDF: {str(e)}"
    return text


# ---------------------------
# DOCX parser
# ---------------------------

def parse_docx(path: str) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        doc = docx.Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        text = f"Error parsing DOCX: {str(e)}"
    return text


# ---------------------------
# CSV parser
# ---------------------------

def parse_csv(path: str) -> str:
    """Extract text from CSV by joining rows into one string."""
    try:
        df = pd.read_csv(path)
        text = df.astype(str).apply(lambda x: " | ".join(x), axis=1)
        return "\n".join(text.tolist())
    except Exception as e:
        return f"Error parsing CSV: {str(e)}"
