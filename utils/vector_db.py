from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = "pdfs/pdf1-9-72.pdf"
DB_PATH = "./chroma_db"

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

print(f"Loaded {len(docs)} pages")

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory=DB_PATH,
)

print("Vector store created and saved.")