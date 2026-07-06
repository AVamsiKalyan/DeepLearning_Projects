from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

loader = PyPDFLoader("deeplearningbook.pdf")
loaded_docs = loader.load()        #loading the document into memory as a list of Document objects

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap = 200
)                                    #creating an instance of the RecursiveCharacterTextSplitter class with a chunk size of 1000 characters and an overlap of 200 characters between chunks

chunks = splitter.split_documents(loaded_docs)     #splitting the loaded document into smaller chunks using the split_documents method of the splitter instance. The resulting chunks are stored in the chunks variable as a list of Document objects.

embedding_model = MistralAIEmbeddings(model="mistral-embed")   #creating an instance of the MistralAIEmbeddings class with the model parameter set to "mistral-embed". This instance will be used to generate embeddings for the document chunks.

vector_store = Chroma.from_documents(
    documents = chunks,
    embedding = embedding_model,
    persist_directory = "chroma_db"
)                                             #creating an instance of the Chroma vector store using the from_documents method. It takes the list of document chunks, the embedding model, and a directory path to persist the vector store. The resulting vector store is stored in the vector_store variable.


