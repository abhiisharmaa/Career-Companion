import google.generativeai as genai

genai.configure(api_key="AIzaSyCh-BkPs-c1AUGG-ubaqK5m5EgQ8QixJE0")

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
