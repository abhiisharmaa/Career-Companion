def compare_skills(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set.intersection(jd_set)
    missing = jd_set.difference(resume_set)

    # Calculate match score
    if len(jd_set) == 0:
        match_score = 0.0
    else:
        match_score = (len(matched) / len(jd_set)) * 100

    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "match_score": round(match_score, 2)
    }