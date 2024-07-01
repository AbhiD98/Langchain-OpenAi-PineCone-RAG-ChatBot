from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Document Pre-Processing
def doc_processing():
    loader = PyPDFDirectoryLoader("document/", glob='**/*.pdf')
    docs = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    docs_split = text_splitter.split_documents(docs)
    return docs_split

# Embedding DB
@st.cache_resource
def embedding_db():
    embeddings = OpenAIEmbeddings()
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if 'abhi-alemeno' not in pc.list_indexes().names():
        pc.create_index(
            name='abhi-alemeno',
            dimension=1536,  # Use 1536 dimensions for text-embedding-ada-002
            metric='cosine',  # Use cosine similarity
            spec=ServerlessSpec(
                cloud='aws',
                region=PINECONE_ENV
            )
        )

    doc_split = doc_processing()
    vectorstore = PineconeVectorStore.from_documents(doc_split, embedding=embeddings, index_name='abhi-alemeno')
    return vectorstore

llm = ChatOpenAI()  # Instantiate the ChatOpenAI model
doc_db = embedding_db()

def retrieval_answer(query):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=doc_db.as_retriever(),
    )
    result = qa.run(query)
    return result

def main():
    st.title("Abhi-Alemeno RAG CHAT-BOT")
    
    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input using chat input widget
    prompt = st.chat_input("Ask Your Query...")
    
    if prompt:
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        
        # Display user message in chat
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Retrieve and display assistant response
        answer = retrieval_answer(prompt)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        
        with st.chat_message("assistant"):
            st.markdown(answer)

if __name__ == "__main__":
    main()