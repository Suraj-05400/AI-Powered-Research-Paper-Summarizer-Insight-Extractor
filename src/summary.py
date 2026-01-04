

def generate_detailed_summary(input_text,llm_model):
    """Generate a detailed, well-expailed summary of the input text using a groq llm"""
    
    #prompt fot llm
    prompt=f"""
    you are an expert research analyst and technical writer.
    your task is to carefully read the following text and generate a comprehensive, structered summary that covers all
    key ideas, concepts, and insights. no pre. 
    
    instructions:
    1. provide a structered summary including:
    -main idea or theme  of the text
    -important subtopics or sections
    -key findings,facts , or arguments 
    -any examples or data mentioned
    2. explain complex terms or contents in a simple and intuitive way,as if teaching new to the topic. 
    3. ensure clearity and depth - avoid vegue or generic summaries. 
    4. present the output in a clear format with headings, bullet points, and short paragraphs. 
    5. if the text is technical  or academic, include a section:"Explanations in simple terms". 
    input text:
    {input_text}
    
    output format:
    -title or theme
    -summary(well-structured paragraphs)
    -key points(bullet format)
    -explanations in simple terms(for laypersons understanding)
    """
    #call the llm
    response=llm_model.invoke(prompt)
    
    if isinstance(response,str):
        return response.strip()
    elif hasattr(response,'content'):
        return response.content.strip()
    elif hasattr(response,'text'):
        return response.text.strip()
    else:
        return str(response).strip()
    
    