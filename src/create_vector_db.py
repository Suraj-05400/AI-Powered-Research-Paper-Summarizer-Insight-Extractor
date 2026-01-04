from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def create_vector_db(text,embedder):
    doc=Document(page_content=text)
    
    #split text into chunks
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n","\n","."," ",]
    )
    docs=splitter.split_documents([doc])
    print(docs)
    
    #create faiss vector database
    vectordb=FAISS.from_documents(docs,embedding=embedder)
    
    #save locally
    vectordb.save_local("research_paper_vector_db")
    
    return vectordb