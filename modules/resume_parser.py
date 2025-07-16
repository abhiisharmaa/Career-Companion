from pypdf import PdfReader
import re


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def extract_emails(text):
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.findall(pattern, text)
def extract_phone_numbers(text):
    pattern = r'(?:\+91[\-\s]?|91[\-\s]?|0)?\d{10}'
    return [match.group() for match in re.finditer(pattern, text)]

known_skills = [
  "python", "sql", "power bi", "flask", "scikit-learn", "streamlit","numpy","tableau",
  "tensorflow", "html", "css", "matplotlib", "pandas", "xgboost","matlab", "MS Word", "MS Excel", "Canva",
   "javascript","django","flask","fastapi", "rest api","git","github","mlflow", "docker", "kubernetes","sql", "mysql", "postgresql",
    "mongodb", "firebase", "nosql","pytorch"
]

def extract_resume_skills(resume_text):
    found_skills = []
    for skills in known_skills:
        if skills in resume_text:
            found_skills.append(skills)

    return list(set(found_skills))


def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return {
        "raw_text": text,
        "emails": extract_emails(text),
        "phones": extract_phone_numbers(text),
        "skills": extract_resume_skills(text)
    }


