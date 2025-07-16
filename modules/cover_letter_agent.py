import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_cover_letter(resume_text, job_description):
    prompt = f"""
You are an AI career assistant. Write a personalized, professional cover letter based on the following:

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Instructions:
- Address it to "Hiring Manager"
- Highlight 2–3 matching skills or experiences
- Keep it under 250 words
- Use a confident, polite tone
- End with a positive call to action
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ faster and free-tier friendly
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error generating cover letter: {e}"
