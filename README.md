# 🚧 DOT Bot – AI Chatbot for Highway & Roadway Standard Specifications

**DOT Bot** is an AI-powered chatbot built using **LangChain**, **OpenAI**, and **Streamlit** that enables engineers, contractors, and transportation departments to query official highway construction specifications (e.g., 2021 Standard Specifications, MUTCD, Erosion Control Manuals, etc.) with **zero hallucination** and **verified source references**.

---

## 🔍 Features

* ✅ **Document-grounded Answers**: Pulls answers directly from DOT PDFs (e.g., 2021 Standard Specifications, Section 150, Section 160, MUTCD, etc.).
* 📖 **Section-aware QA**: Understands structure and can answer by section (e.g., "Explain 149.3.06").
* 🧠 **RAG (Retrieval-Augmented Generation)** pipeline for precise and contextual answers.
* 🗂️ **Handles Multiple Docs**: Supports multiple documents like:

  * 2021 Standard Specifications
  * MUTCD
  * Erosion & Sediment Control Manual
  * Supplemental Specifications (Sections 150, 160)
* 💬 **Streamlit Chat Interface** with source page references.
* 🔗 **LangChain + OpenAI + ChromaDB** based implementation.

---

## 📁 Directory Structure

```
dot_bot_project/
│
├── rag_pipeline.py          # RAG processing pipeline (loader, embedder, vectorstore)
├── streamlit_app.py         # Streamlit frontend to interact with the chatbot
├── /docs                    # Folder containing all reference PDFs
│   ├── 2021StandardSpecifications.pdf
│   ├── MUTCD.pdf
│   ├── Section150.pdf
│   └── Section160.pdf
├── /venv                    # Python virtual environment
├── requirements.txt         # Python dependencies
└── README.md                # You're here!
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dot-bot.git
cd dot-bot
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Place Documents in `/docs` Folder

Ensure these files exist:

* `2021StandardSpecifications.pdf`
* `Section150.pdf`
* `Section160.pdf`
* `MUTCD.pdf`
* `ErosionManual.pdf` (if applicable)

Update the paths in `rag_pipeline.py` if your file names differ.

---

## 🚀 Running the App

### Step 1: Build the Vector Index

```bash
python rag_pipeline.py
```

> ⚠️ Only run this when PDFs change. It will embed and persist documents using ChromaDB.

### Step 2: Launch Chatbot

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Example Questions to Ask

```markdown
1. Explain Section 149.
2. Can a contractor redesign the project plan?
3. What does Section 104.03 say about altering plans?
4. What is the process of quality acceptance in 149.3.06?
5. What are the warranty and maintenance clauses in 149?
6. What does Section 150 cover (MUTCD)?
7. Define a Filter Ring (Erosion Manual).
8. Describe the GDOT Daily Inspection Report.
```

---

## 🛠️ Tech Stack

* **LangChain** – Retrieval + LLM Orchestration
* **OpenAI GPT** – LLM for response generation
* **ChromaDB** – Vector database for document embeddings
* **Streamlit** – Simple and clean chatbot UI
* **PyMuPDFLoader** – PDF loader for parsing DOT documents
* **OpenAIEmbeddings** – Converts text into vector format

---

## 🧹 Deprecation Warnings Fix (Optional but Recommended)

Update old imports to new structure:

```bash
pip install -U langchain langchain-community langchain-openai
```

Update imports like:

```python
# OLD (Deprecated)
from langchain.vectorstores import Chroma

# NEW
from langchain_community.vectorstores import Chroma
```

Refer to [LangChain v0.2 Migration Guide](https://python.langchain.com/docs/versions/v0_2/) for details.

---

## 📌 Future Enhancements

* [ ] Add dropdown to explore content section-wise
* [ ] Chat memory or follow-up clarification questions
* [ ] Admin interface to manage documents
* [ ] Scoring + test mode for QA verification

---

## 🧠 Author

**Nikhil Dendeti**
💪 Passionate about AI + Infrastructure Tech

---

## 📜 License

This project is licensed under the MIT License.
