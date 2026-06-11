import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI

# =========================
# LOAD .ENV
# =========================
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=API_KEY)

MODEL = "gpt-4.1-mini"
PDF_PATH = "/home/yugesh/Desktop/New Folder 1/pdfs/pdf2.pdf"
OUTPUT_PATH = "output.md"


# =========================
# STEP 1: Extract PDF text
# =========================
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")
        text += f"\n\n--- Page {page_num} ---\n\n"
        text += page_text

    return text


# =========================
# STEP 2: Chunk text
# =========================
def chunk_text(text, chunk_size=6000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# =========================
# STEP 3: Convert to Markdown
# =========================
def to_markdown(text_chunk):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Convert extracted PDF text into clean Markdown. "
                    "Preserve headings, lists, and tables. "
                    "Do not add explanations or commentary."
                )
            },
            {
                "role": "user",
                "content": text_chunk
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# =========================
# STEP 4: Pipeline
# =========================
def main():
    print("Loading PDF...")
    text = extract_text(PDF_PATH)

    print("Chunking...")
    chunks = chunk_text(text)

    print(f"Processing {len(chunks)} chunks...")

    full_md = ""

    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}/{len(chunks)}")
        full_md += to_markdown(chunk) + "\n\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_md)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()