import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_learning_resources(missing_skills):
    prompt = f"""
You are a career coach. For each of the following skills, provide:
1. A short description of what the skill is used for
2. Best free resources ( 2 or 3) link to learn it(can also include youtube channels)
3. An estimated time to learn

Skills: {', '.join(missing_skills)}

Format clearly per skill with bullet points or numbered steps.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text.strip()

def suggest_projects_from_jd(jd_text):
    prompt = f"""
You are a career mentor. Based on the following job description and current market trends, suggest 3 real-world project ideas a candidate should build to strengthen their portfolio and match the role. Analyse various resources and suggest the projects one for each - easy , medium and hard for that role.

JOB DESCRIPTION:
{jd_text}

Instructions:
- Make each project practical and unique
- Mention what the project solves
- Use key tools or skills from the JD
- Suggest a dataset or tech stack if relevant
- Format clearly using headings or bullet points
- Can also suggest projects playlists from youtube.
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()