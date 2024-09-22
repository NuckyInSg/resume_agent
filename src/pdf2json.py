import os
from typing import Dict, Any
import json
from pypdf import PdfReader
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

PROMPT_TEMPLATE = """You are an AI assistant tasked with extracting information from a software engineer's resume and transforming it into a structured JSON format. Your goal is to accurately capture all relevant details from the input resume and organize them according to the specified JSON structure, if the original content is not in English, translate the content accurately into English.

Here is the input resume text:

<resume>
{RESUME_TEXT}
</resume>

Follow these steps to extract and structure the information:

1. Carefully read through the entire resume text.

2. Extract the following information and organize it according to the JSON structure:
   - Name
   - Contact information (email, phone number, website if available)
   - Education history (for each entry: institution, degree, GPA if provided, location, duration)
   - Work experience (for each entry: company, position, location, duration, and key projects/responsibilities)
   - Personal projects (if any)
   - Skills (languages and technologies)

3. For each work experience and project entry, try to identify distinct projects and their descriptions. If specific project titles are not provided, use key responsibilities or achievements as project titles.

4. If any information is missing or unclear, leave the corresponding field empty in the JSON structure. Do not invent or assume any information not explicitly stated in the resume.

5. Ensure consistency in formatting:
   - Use the same date format throughout (e.g., "Mon. YYYY - Mon. YYYY" or "Mon. YYYY - Present")
   - Capitalize proper nouns and acronyms correctly
   - Use consistent punctuation
   - If the name is not in English, translate it into English by pronunciation

6. Structure the extracted information into the following JSON format, follow the format given in the value of each key strictly, for nullable value, output empty, like "" for nullable string value:

{{
  "name": "not nullable, translate to English if not in English",
  "contact": {{
    "email": "not nullable",
    "mobile": "not nullable",
    "website": "nullable"
  }},
  "education": [
    {{
      "institution": "not nullable",
      "degree": "not nullable",
      "gpa": "nullable",
      "location": "not nullable",
      "duration": "not nullable, format: Mon. YYYY - Mon. YYYY or Mon. YYYY - Present"
    }}
  ],
  "experience": [
    {{
      "company": "not nullable, maximum 50 characters",
      "position": "not nullable",
      "location": "nullable",
      "duration": "not nullable, format: Mon. YYYY - Mon. YYYY or Mon. YYYY - Present",
      "projects": [
        {{
          "title": "not nullable",
          "description": "not nullable"
        }}
      ]
    }}
  ],
  "projects": [
    {{
      "title": "not nullable",
      "description": "not nullable"
    }}
  ],
  "academic_experience": [
    {{
      "title": "not nullable",
      "description": "not nullable"
    }}
  ],
  "skills": {{
    "languages": ["up to 5 languages"],
    "technologies": ["up to 5 technologies, 40 characters total"]
  }}
}}

7. Review the extracted information to ensure accuracy and completeness, the json content will be used for latex pdf generation, Handle special characters with escaping, such as &, %, $, #, _, {{, }}, ~, ^, \, |, <, >, and ensure they are properly escaped.

8. Output the final raw JSON without any prefix or suffix.

Remember to focus solely on the information provided in the resume. Do not add any details that are not explicitly stated in the input text."""

def create_resume_extraction_chain():
    """Create a Langchain chain for resume extraction using the custom prompt."""
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    anthropic_api_url = os.getenv("ANTHROPIC_API_URL")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0, anthropic_api_key=anthropic_api_key, anthropic_api_url=anthropic_api_url)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    parser = JsonOutputParser()

    chain = (
        {"RESUME_TEXT": RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )
    return chain

def extract_resume_info(pdf_path: str) -> Dict[str, Any]:
    """Extract resume information from a PDF file using the custom prompt."""
    resume_content = extract_text_from_pdf(pdf_path)
    chain = create_resume_extraction_chain()
    result = chain.invoke(resume_content)
    return result

def pdf2json(pdf_path: str, output_path: str):
    extracted_info = extract_resume_info(pdf_path)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_info, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pdf2json("../input/original.pdf", "../input/original.json")