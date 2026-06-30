"""
utils.py — Helper utilities for the AI Student Impact backend.
"""

BURNOUT_MAP = {"High": 0, "Low": 1, "Medium": 2}

FEATURE_RANGES = {
    "Weekly_GenAI_Hours":        (0.0, 40.0),
    "Traditional_Study_Hours":   (0.0, 10.0),
    "Skill_Retention_Score":     (0.0, 100.0),
    "Anxiety_Level_During_Exams":(0.0, 10.0),
    "Perceived_AI_Dependency":   (0.0, 10.0),
    "Pre_Semester_GPA":          (0.0, 4.0),
}


def validate_and_parse(data: dict) -> tuple:
    """
    Validate incoming request data and return (feature_list, error_string).
    feature_list is None when there is an error.
    """
    errors = []

    for field, (lo, hi) in FEATURE_RANGES.items():
        if field not in data:
            errors.append(f"Missing field: {field}")
            continue
        try:
            val = float(data[field])
            if not (lo <= val <= hi):
                errors.append(f"{field} must be between {lo} and {hi}, got {val}")
        except (ValueError, TypeError):
            errors.append(f"{field} must be a number")

    burnout_raw = data.get("Burnout_Risk_Level")
    if burnout_raw not in BURNOUT_MAP:
        errors.append("Burnout_Risk_Level must be 'Low', 'Medium', or 'High'")

    if errors:
        return None, "; ".join(errors)

    features = [
        float(data["Weekly_GenAI_Hours"]),
        float(data["Traditional_Study_Hours"]),
        float(data["Skill_Retention_Score"]),
        float(data["Anxiety_Level_During_Exams"]),
        float(data["Perceived_AI_Dependency"]),
        float(data["Pre_Semester_GPA"]),
        BURNOUT_MAP[burnout_raw],
    ]
    return features, None


def gpa_to_letter(gpa: float) -> str:
    """Convert numeric GPA to letter grade."""
    thresholds = [
        (3.7, "A / A+"), (3.3, "A-"), (3.0, "B+"),
        (2.7, "B"),      (2.3, "B-"), (2.0, "C+"),
        (1.7, "C"),      (1.0, "D"),
    ]
    for threshold, letter in thresholds:
        if gpa >= threshold:
            return letter
    return "F"


def gpa_to_insight(gpa: float) -> str:
    """Return a short motivational insight based on predicted GPA."""
    if gpa >= 3.5:
        return "Excellent trajectory! Your study habits and AI balance are working well."
    if gpa >= 3.0:
        return "Good performance. Minor improvements in study balance could push you higher."
    if gpa >= 2.5:
        return "Average performance. Consider reducing AI dependency and anxiety management."
    if gpa >= 2.0:
        return "Below expectations. Focus on traditional study hours and reducing burnout risk."
    return "Critical zone. Seek academic support and reconsider your current study strategy."
