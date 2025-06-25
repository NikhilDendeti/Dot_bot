from dotenv import load_dotenv
import os
load_dotenv()

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load and split PDF document
loader = PyMuPDFLoader("2021StandardSpecifications.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
for chunk in chunks:
    chunk.metadata["document"] = "2021 Standard Specifications"
    chunk.metadata["page"] = chunk.metadata.get("page", 0)

# Create vectorstore using FAISS
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embedding)
vectorstore.save_local("./gdot_vectorstore")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant answering questions using Georgia DOT specifications.
Use only the provided context. Always cite source like (2021 Spec, p.99).
If answer is not found, say \"Not specified in the provided documents.\"

Context:
{context}

Question: {question}

Answer:
"""
)

# QA chain using GPT-4
llm = ChatOpenAI(model_name="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)
