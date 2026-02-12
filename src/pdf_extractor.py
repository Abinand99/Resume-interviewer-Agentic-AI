import pymupdf
import json
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import re

load_dotenv()
OUTPUT_PATH = "./src/data/resume.json"

def text_extractor(document_path):
    try:
        doc = pymupdf.open(document_path)
        resume_text = []
        for page in doc:
            text = page.get_text()
            # print(text)
            if text:
                resume_text.append(text.strip())
        doc.close()
        clean_text = "\n".join(resume_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
        return clean_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def json_extractor(model,text):

    prompt = f"""
    You are a resume extraction agent.

    Extract structured factual data from the resume text.

    Return ONLY valid JSON in this exact format:

    {{
      "projects": [
        {{
          "name": "",
          "tech_stack": [],
          "description": ""
        }}
      ],
      "skills": [],
      "experience": [
        {{
          "company": "",
          "role": "",
          "responsibilities": []
        }}
      ]
    }}

    Rules:
    - Do NOT add opinions or judgments.
    - Do NOT infer skill levels or quality.
    - Do NOT label anything as weak or strong.
    - Only extract what is explicitly written.
    - If something is missing, return empty arrays.
    - Do not hallucinate projects or experience.
    - Output only JSON. No markdown. No explanation.

    Resume text:

    {text}
    """

    response = model.chat.completions.create(
        messages=[{"role": "user","content":prompt}],
        max_tokens=1200,
        temperature=0.0
    )
    return response.choices[0].message.content

def json_dump(response,path):
    try:
        data = json.loads(response)

        if data:
            os.makedirs(path,exist_ok=True)
            with open(OUTPUT_PATH,"w",encoding="utf-8") as f:
                json.dump(data,f,indent=2)
            json.dumps(response, indent=2)
            print("Json dump Successfull")

    except json.JSONDecodeError:
        print("JSON parsing failed. Raw output:\n")
        print(response)




if __name__=="__main__":
    
    model = InferenceClient(
        model="Qwen/Qwen2.5-7B-Instruct",
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    path = "./Resume_PDF/resume.pdf"
    text = text_extractor(path)
    json_response = json_extractor(model,text)
    path = "./src/data"
    json_save = json_dump(json_response,path)
    