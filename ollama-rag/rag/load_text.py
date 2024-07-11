from langchain_community.document_loaders import Docx2txtLoader
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
def load_document(file_name):
    loader = Docx2txtLoader(file_name)
    documents = loader.load()
    print(documents)
    return documents

def get_text_chunks(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    return splits

def create_embeddings(splits):
    embeddings = OllamaEmbeddings(model="llama3")
    vector_store = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")
    print('vector store is stored')

def ollama_llm(qstn, context):
    formatted_prompt = f"You are Being a software quality engineer  : {qstn} \n\n context based on these requirements : {context}"
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
def rag_chain(question):
    embeddings = OllamaEmbeddings(model="llama3")
    vector_store = Chroma(persist_directory="./chroma_db",embedding_function= embeddings)
    retriever = vector_store.as_retriever()
    retrieved_docs = retriever.invoke(question)
    formatted_context = combine_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

def get_result():
    result = rag_chain("generate functional test cases and negative test cases in tabular form  for testing search function and results")
    print(result)

# result = rag_chain("What is adjusted_es_score calculation for search results?")
# print(result)



if __name__ =='__main__':
    # docs = load_document('Search.docx')
    # splits = get_text_chunks(docs)
    # print(splits)
    # create_embeddings(splits)
    get_result()



