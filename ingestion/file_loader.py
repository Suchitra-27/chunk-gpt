import fitz
import os

def extract_text_from_file(filename: str, content: bytes) -> str:
    if filename.endswith(".pdf"):
        temp_path = "temp.pdf"
        try:
            with open(temp_path, "wb") as f:
                f.write(content)
            with fitz.open(temp_path) as doc:
                return "\n".join(page.get_text() for page in doc)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        return "Unsupported file type"
