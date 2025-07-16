import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def suggest_resume_improvements(resume_text, job_description):
    prompt = f"""
You are an expert career coach and resume writer.

Given the RESUME and JOB DESCRIPTION below, suggest 3 personalized improvements the candidate should make to their resume to align better with the role.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Make the suggestions:
- Specific and actionable
- Based on skills or experiences missing
- Written as bullet points
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
