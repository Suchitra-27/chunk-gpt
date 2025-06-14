
# 🧠 Chunk GPT

Chunk GPT is a document ingestion microservice built with FastAPI that performs:
- 📄 File upload and extraction (PDFs)
- 🧹 Text preprocessing
- 🔪 Smart chunking
- 🧠 Embedding using LangChain + Pinecone
- 🔍 Semantic search
- 👍 Feedback capture
- 🛠️ Patch suggestion + approval
- 🧼 Decay analysis for unused chunks
- 🧠 Query ↔️ Chunk trace logging

---

## 📦 Installation

```bash
git clone <repo-url>
cd chunk_gpt
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
