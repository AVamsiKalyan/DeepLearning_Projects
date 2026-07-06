import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

st.set_page_config(page_title="RAG Chat", page_icon="📄")
st.title("📄 Chat with your PDF")

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "current_file" not in st.session_state:
    st.session_state.current_file = None

llm = ChatMistralAI(model="mistral-small-2506")

prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful AI assistant. Use only provided context to '
               'answer the question. If the answer is not in the context, say: '
               '"I couldn\'t find the answer in the document."'),
    ('human', "Context: {context}\n\nQuestion: {question}")
])


@st.cache_resource(show_spinner=False)
def build_retriever(file_path: str, file_name: str):
    """Load, split, embed, and index the PDF. Cached per file so re-runs
    of the Streamlit script don't rebuild the vector store every time."""
    data = PyPDFLoader(file_path)
    docs = data.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embedding_model = MistralAIEmbeddings(model="mistral-embed")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=f"chroma_db_{file_name}",
    )

    return vector_store.as_retriever(
        search_type='mmr',
        search_kwargs={'k': 2, 'fetch_k': 10, 'lambda_mult': 0.5}
    )


# ---------- Sidebar: file upload ----------
with st.sidebar:
    st.header("Upload a document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None and uploaded_file.name != st.session_state.current_file:
        with st.spinner("Reading and indexing your document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name

            st.session_state.retriever = build_retriever(tmp_path, uploaded_file.name)
            st.session_state.current_file = uploaded_file.name
            st.session_state.messages = []  # reset chat for the new document

        st.success(f"'{uploaded_file.name}' is ready. Ask away!")

# ---------- Main chat area ----------
if st.session_state.retriever is None:
    st.info("Upload a PDF from the sidebar to get started.")
else:
    # Show past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask a question about your document...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                docs = st.session_state.retriever.invoke(query)
                context = '\n\n'.join(doc.page_content for doc in docs)

                final_prompt = prompt.invoke({'context': context, 'question': query})
                response = llm.invoke(final_prompt)

                st.markdown(response.content)

        st.session_state.messages.append({"role": "assistant", "content": response.content})