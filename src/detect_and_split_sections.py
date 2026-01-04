import json
from typing import List, Dict

def refine_sections(input_list:str, llm)->List[Dict]:
    prompt=f"""You are aprecise data processor.
    i will give you a list of sections from a research paper. each item may have:
    -"sections"(string)
    -optional "subsection"(string)
    -"start"(integer)
    
    some entries are unnecessary and must be **removed completely**:
    1.figures or tables captions(any "section" starting with "Figure" or "Table").
    2.incomplete,meaningless,or fragment sections(e.g.,"making","length nis smaller.....")
    3.any other irrelevant entries that do not proper sections or subsections.any
    
    your task is to **refine this list**:
    
    -keep only meaningful main sections and subsections.
    -main sections should be in the the format:
    {{"section":"section name","start":number}}
    -subsections should be in the format:
    {{"section":"parent section","subsection":"subsection name","start":number}}
    -the output must be **strictly a json array of dictionaries**.
    -do **not** include explanations,notes,extra text,or commentary.
    -if a section is unnecessary(e.g.,,figure,table,fragment), **exclude it completely**. 
    
    here is the input json:
    {input_list}
    always return list of dictionaries only,no preamble. 
    """
    #call the llm- returns a string
    try:
        assistant_text=llm.invoke(prompt).content.strip()
        #print(assistant_text)
        #print("raw llm output:\n",assistant_text)
        #parse json and return
        sections=json.loads(assistant_text)
    except(json.JSONDecodeError,KeyError,TypeError) as e:
        print("warning: llm output not json. returning empty list.")
        print("error:",e)
        sections=[]
    return sections

def split_sections_with_content(text:str,detected_sections:List[Dict])->List[Dict]:
    """split the text into sections/subsections using detected start positions.
    returns a list of dicts with: sections, subsections(if any), start,content."""
    if not detected_sections:
        return {"full_paper":text}
    
    #sort by start index ascending
    detected_sections=sorted(detected_sections,key=lambda x:x["start"])
    results={}
    
    for i,sec in enumerate(detected_sections):
        start=sec["start"]
        end=detected_sections[i+1]["start"] if i+1<len(detected_sections) else len(text)
        
        #section details
        section_name=sec["section"]
        subsection_name=sec.get("subsection",None)
        section_text=text[start:end].strip()
        
        results[section_name]=section_text
        if subsection_name:
            results[section_name]=results.pop(section_name)
    return results