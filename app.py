from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from flask import Flask,render_template

from src.load_and_extract_text import extract_text_from_pdf,extract_pdf_sections,parse_sections,find_abstract
from src.detect_and_split_sections import refine_sections,split_sections_with_content
from src.summary import generate_detailed_summary
from src.create_vector_db import create_vector_db
from src.rag_retrival_chain import get_qa_chain
                      
from dotenv import load_dotenv
import os, json

load_dotenv()

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'
#ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)

groq_api_key = os.getenv("GROQ_API_KEY")
llm_model = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

llm=ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)

#initialize embeddings using huggingface model
embedder=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

#print(llm.invoke("why ganesha chturthi is celebrated?"))

@app.route('/')
def index():
    return render_template('index.html')

"""@app.route('/upload',methods=['POST'])
def upload_pdf():
    file=request.files.get('file')
    if not file:
       return jsonify({"error":"No file uploaded"}),400
    
    filename=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
    #print(filename)
    file.save(filename)"""

if __name__ == "__main__":
    app.run()
    
    #extracted_text=extract_text_from_pdf("ResearchPaper.pdf")
    #print(extracted_text)    
    #extracted_sections=extract_pdf_sections(full_text = extracted_text)
    #with open("extracted_sections.json","w") as f:
    #   json.dump(extracted_sections,f,indent=4)
    
    #refined_sections=refine_sections(extracted_sections,llm)
    #with open("refined_sections.json","w") as f:
    #   json.dump(refined_sections,f,indent=4)
    
    #split_sections_with_content=split_sections_with_content(extracted_text,refined_sections)
    #with open("split_sections_with_content.json","w") as f:
    #    json.dump(split_sections_with_content,f,indent=4)