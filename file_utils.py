import os
from typing import Tuple, Dict

import PyPDF2
from docx import Document
from bs4 import BeautifulSoup


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _read_pdf(path: str) -> str:
    text_parts = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            txt = page.extract_text() or ""
            text_parts.append(txt)
    return "\n".join(text_parts)


def _read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def _read_html(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")


def load_text_from_file(file_obj) -> Tuple[str, Dict]:
    """
    file_obj is the Gradio file (we used type='filepath', so it's just a path string).
    Returns (text, meta_dict)
    """
    if isinstance(file_obj, str):
        path = file_obj
    else:
        # Gradio sometimes passes an object with "name" or "orig_name"
        path = getattr(file_obj, "name", None) or getattr(file_obj, "orig_name", None)
        if not path:
            raise ValueError("Cannot determine file path from uploaded file object.")

    ext = os.path.splitext(path)[1].lower()

    if ext in [".txt"]:
        text = _read_txt(path)
    elif ext in [".pdf"]:
        text = _read_pdf(path)
    elif ext in [".docx"]:
        text = _read_docx(path)
    elif ext in [".html", ".htm"]:
        text = _read_html(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    size_bytes = os.path.getsize(path)

    meta = {
        "path": path,
        "extension": ext,
        "size_bytes": size_bytes,
        "chars": len(text),
    }

    print(f"[app] file={os.path.basename(path)}, chars={len(text)}, size_bytes={size_bytes}")
    return text, meta

