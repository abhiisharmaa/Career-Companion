# with open("../data/jd.txt", "r") as pdf:
#     jd_data = pdf.read()
#     jd_data = jd_data.lower()


def extract_jd_skills(text):
    text = text.lower()
    known_skills = [
        "python", "sql", "power bi", "flask", "scikit-learn", "streamlit", "numpy", "tableau",
        "tensorflow", "html", "css", "matplotlib", "pandas", "xgboost", "matlab", "MS Word", "MS Excel", "Canva",
        "javascript", "django", "flask", "fastapi", "rest api", "git", "github", "mlflow", "docker", "kubernetes",
        "sql", "mysql", "postgresql", "machine learning",
        "mongodb", "firebase", "nosql", "pytorch"
    ]

    return list(set([skill for skill in known_skills if skill in text]))

