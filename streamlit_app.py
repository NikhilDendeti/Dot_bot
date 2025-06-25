import streamlit as st
from dotenv import load_dotenv
import os



from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

embedding = OpenAIEmbeddings()
vectorstore = FAISS.load_local("./gdot_vectorstore", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant answering questions using Georgia DOT specifications.
Use only the provided context. Always cite source like (2021 Spec, p.99).
If answer is not found, say "Not specified in the provided documents."

Context:
{context}

Question: {question}

Answer:
"""
)

llm = ChatOpenAI(model_name="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

st.set_page_config(page_title="GDOT Specs Chat", layout="wide")
st.title("📘 Georgia DOT Specification Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.chat_input("Ask a question (e.g., Explain Section 149, Filter Ring, Section 150, etc.)")

if query:
    with st.spinner("Searching GDOT specs..."):
        result = qa_chain({"query": query})
        answer = result["result"]
        sources = result["source_documents"]

        st.session_state.chat_history.append((query, answer, sources))

for q, a, srcs in reversed(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(q)

    with st.chat_message("assistant"):
        st.markdown(a)
        with st.expander("📄 Sources"):
            for doc in srcs:
                page = doc.metadata.get("page", "?")
                source = doc.metadata.get("document", "Unknown Document")
                st.write(f"Page {page} — {source}")
