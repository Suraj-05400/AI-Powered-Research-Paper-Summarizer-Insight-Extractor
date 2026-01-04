"""from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

def get_qa_chain(vectordb,llm):
    create a retrieval-based QA chain using the vector database and llm.
    retriever=vectordb.as_retriever(score_threshold=0.7)
    
    #create a propmt
    prompt_template=
    you are an assistan. Answer the question **only using te information provided in the context below**.
    do not use any outside knowledge. 
    context:
    {context}
    question:
    {question}
    
    instructions:
    -if the answer can be found in the context, provide it concisely.
    -if the answer is not in the context, respond exactly: "I don't know."
    
    prompt=PromptTemplate(
        template=prompt_template,
        input_variables=["context","question"]
    )
    chain=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt":prompt}
    )
    return chain"""
    
from langchain_classic.chains import create_retrieval_chain
#from langchain_classic.chains.retrieval import RetrievalChain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def get_qa_chain(vectordb, llm):
    """Create a retrieval-based QA chain using the modern LCEL constructors."""
    
    # 1. Setup the Retriever
    # Note: score_threshold requires "similarity_score_threshold" search type
    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.7}
    )
    
    # 2. Define the System Prompt
    # In the new system, we use 'context' and 'input' as standard variables
    system_prompt = (
        "You are an assistant. Answer the question **only using the information "
        "provided in the context below**. Do not use any outside knowledge."
        "I don't know.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # 3. Create the 'Combine Documents' Chain
    # This replaces the 'chain_type="stuff"' argument
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # 4. Create the Final Retrieval Chain
    # This creates a chain that first retrieves, then passes to combine_docs_chain
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    
    return retrieval_chain