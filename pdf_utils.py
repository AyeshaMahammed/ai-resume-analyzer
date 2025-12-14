import pdfplumber

def extract_text_from_pdf(path: str) -> str:
    text_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            text_chunks.append(txt)
    full = "\n".join(text_chunks)
    # strip common noise like 'Page 2 of 4'
    return full.replace("Page2of4", "").replace("Page3of4", "").replace("Page4of4", "")

