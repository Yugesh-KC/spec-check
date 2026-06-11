# PV Inverter Spec Compliance Checker

An AI agent pipeline that automatically checks whether PV inverter specifications from Chinese exporters comply with Nepal's **NEPQA 2025** requirements. It uses LangChain agents, OpenAI GPT-4.1-mini, Tavily web search, and a ChromaDB vector store to extract, compare, and generate a formal compliance report.

---

## Project Structure

```
spec_check/
├── agent.ipynb              # Main pipeline — run this notebook end-to-end
├── main.py                  # Placeholder entry point
├── pyproject.toml           # Project dependencies
├── .env                     # API keys (not committed)
│
├── misc                     # Outputs of previous run 
├── pdfs/
│   ├── NEPQA 2025.pdf       # Nepal quality requirements document
│   ├── pdf1.pdf             # Chinese exporter spec (full, 72 pages)
│   ├── pdf1-1-8.pdf         # Pages 1–8 of pdf1 (pre-extracted)
│   ├── pdf1-9-72.pdf        # Pages 9–72 of pdf1 → loaded into vector DB
│   └── pdf2.pdf             # Second exporter spec document
│
├── markdowns/
│   ├── specifications.md    # NEPQA PV inverter section (manually extracted)
│   ├── section133.md        # Referenced sub-section from NEPQA
│   ├── product_spec1.md     # pdf1 pages 1–8 converted to markdown
│   ├── product_spec2.md     # pdf2 converted to markdown
│   └── output/              # Raw markdown output from MinerU PDF parser
│
├── outputs/
│   ├── requirements.json    # Extracted NEPQA requirements (structured)
│   ├── specs1.json          # Extracted specs from product 1
│   ├── specs2.json          # Extracted specs from product 2
│   └── combined_specs.json  # Merged specs from both products
│
├── chroma_db/               # Persisted ChromaDB vector store (pdf1 pages 9–72)
├── final_output.md          # Final compliance report output
│
└── utils/
    ├── vector_db.py         # Builds ChromaDB from pdf1-9-72.pdf
    └── pdftomd.py           # Converts PDFs to markdown via GPT-4.1-mini
```

---

## How It Works

The pipeline runs 6 agents sequentially:

1. **Requirements Agent** — Reads NEPQA markdown files and extracts structured compliance requirements into JSON, using Tavily web search to resolve references to external standards.
2. **Extractor Agent (Product 1)** — Reads the first 8 pages of the product spec and maps values to the requirements JSON. Uses a calculator tool to derive any values not explicitly stated.
3. **Filler Agent** — Searches ChromaDB (pages 9–72 of product 1) to fill any `NOT_GIVEN` fields left by the extractor.
4. **Extractor Agent (Product 2)** — Runs the same extraction on the second product's full spec document.
5. **Combiner Agent** — Merges both spec JSONs into a single unified document, preserving conflicts with source attribution.
6. **Compliance Agent** — Compares the combined specs against requirements and generates a formal audit-style report saved to `final_output.md`.

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Yugesh-KC/spec-check
cd spec_check
```

### 2. Install dependencies

```bash
pip install uv
uv sync
```



### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Build the vector database

> Skip this step if the `chroma_db/` directory already exists.

```bash
python utils/vector_db.py
```

This loads `pdfs/pdf1-9-72.pdf` into a local ChromaDB vector store for RAG retrieval.

### 5. Run the pipeline

Open `agent.ipynb` in Jupyter and run all cells top to bottom:

```bash
jupyter notebook agent.ipynb
```

The final compliance report will be saved to `final_output.md`.

---

## Requirements

- Python 3.13+
- OpenAI API key (GPT-4.1-mini)
- Tavily API key (web search)
