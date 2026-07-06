from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


from langchain_mistralai import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

data = PyPDFLoader("deeplearningbook.pdf")
docs = data.load()

embedding_model = MistralAIEmbeddings(model="mistral-embed")

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

retriever = vector_store.as_retriever(
    search_type = 'mmr', #search type can be 'mmr' or 'similarity'
    search_kargs = {'k': 2,        #k defines how many results to return,   #only retrieves relevant information doesnt answer the questions
                    'fetch_k':10,  #fetch_k defines how many documents to fetch from the vector store before applying the MMR algorithm to select the top k documents. It is used to improve the quality of the retrieved documents by considering a larger set of candidates before selecting the most relevant ones.
                    'lambda_mult':0.5} #lambda_mult is a parameter that controls the trade-off between relevance and diversity in the MMR algorithm. A higher value of lambda_mult will prioritize relevance over diversity, while a lower value will prioritize diversity over relevance.
    
)

llm = ChatMistralAI(model="mistral-small-2506")

prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful AI assisstant. Use only provided context to answer the question. If answer is not in context, say:"I couldnt find the answer in the document."'),
    ('human',"Context: {context}\n\nQuestion: {question}")
])

print('RAG system created successfully! You can now ask questions based on the document content.')
print("Type 'exit' to quit the program.")

while True:
    query = input("You:")
    if query.lower() == 'exit':
        print("Exiting the program. Goodbye!")
        break
    
    docs = retriever.invoke(query)             # to create the context for the prompt, we need to retrieve relevant documents from the vector store based on the user's query. The retriever.invoke(query) method is used to perform this retrieval. It takes the user's query as input and returns a list of documents that are relevant to the query. These documents will then be used to create the context for the prompt that will be sent to the language model for generating a response.
    context =  '\n\n'.join(
        [docs.page_content for docs in docs]
    )

    final_prompt = prompt.invoke({'context': context, 'question': query})
    response = llm.invoke(final_prompt)
    print(f"\nAI: {response.content}\n")