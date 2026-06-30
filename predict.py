from http.server import BaseHTTPRequestHandler
import json

# ── Model coefficients (LinearRegression, extracted from trained model) ───────
# Feature order: Weekly_GenAI_Hours, Traditional_Study_Hours, Skill_Retention_Score,
#                Anxiety_Level_During_Exams, Perceived_AI_Dependency,
#                Pre_Semester_GPA, Burnout_Risk_Level
COEFFICIENTS = [
    0.004282600031015573,   # Weekly_GenAI_Hours
    0.04808808467957935,    # Traditional_Study_Hours
    0.009866237558562377,   # Skill_Retention_Score
   -0.04107090496073348,    # Anxiety_Level_During_Exams
   -0.02678525320142828,    # Perceived_AI_Dependency
    0.6099442250124041,     # Pre_Semester_GPA
    0.09735825615691762,    # Burnout_Risk_Level
]
INTERCEPT = -0.17700786527662338

# Burnout encoding (matches LabelEncoder alphabetical order)
BURNOUT_MAP = {"High": 0, "Low": 1, "Medium": 2}

REQUIRED_FIELDS = [
    "Weekly_GenAI_Hours",
    "Traditional_Study_Hours",
    "Skill_Retention_Score",
    "Anxiety_Level_During_Exams",
    "Perceived_AI_Dependency",
    "Pre_Semester_GPA",
]

FIELD_RANGES = {
    "Weekly_GenAI_Hours":         (0, 40),
    "Traditional_Study_Hours":    (0, 10),
    "Skill_Retention_Score":      (0, 100),
    "Anxiety_Level_During_Exams": (0, 10),
    "Perceived_AI_Dependency":    (0, 10),
    "Pre_Semester_GPA":           (0, 4),
}


def predict_gpa(features: list) -> float:
    result = INTERCEPT + sum(c * f for c, f in zip(COEFFICIENTS, features))
    return max(0.0, min(4.0, result))


def gpa_to_letter(gpa: float) -> str:
    for threshold, letter in [(3.7,"A / A+"),(3.3,"A-"),(3.0,"B+"),(2.7,"B"),
                               (2.3,"B-"),(2.0,"C+"),(1.7,"C"),(1.0,"D")]:
        if gpa >= threshold:
            return letter
    return "F"


def gpa_to_insight(gpa: float) -> str:
    if gpa >= 3.5:
        return "Excellent trajectory! Your study habits and AI balance are working well."
    if gpa >= 3.0:
        return "Good performance. Minor improvements in study balance could push you higher."
    if gpa >= 2.5:
        return "Average performance. Consider reducing AI dependency and managing exam anxiety."
    if gpa >= 2.0:
        return "Below expectations. Focus on traditional study hours and reducing burnout."
    return "Critical zone. Seek academic support and reconsider your current study strategy."


def validate(data: dict):
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing: {field}")
            continue
        try:
            val = float(data[field])
            lo, hi = FIELD_RANGES[field]
            if not (lo <= val <= hi):
                errors.append(f"{field} must be {lo}–{hi}")
        except (ValueError, TypeError):
            errors.append(f"{field} must be a number")

    burnout = data.get("Burnout_Risk_Level")
    if burnout not in BURNOUT_MAP:
        errors.append("Burnout_Risk_Level must be Low, Medium, or High")

    if errors:
        return None, "; ".join(errors)

    features = [
        float(data["Weekly_GenAI_Hours"]),
        float(data["Traditional_Study_Hours"]),
        float(data["Skill_Retention_Score"]),
        float(data["Anxiety_Level_During_Exams"]),
        float(data["Perceived_AI_Dependency"]),
        float(data["Pre_Semester_GPA"]),
        BURNOUT_MAP[burnout],
    ]
    return features, None


class handler(BaseHTTPRequestHandler):

    def _send(self, status: int, body: dict):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self._send(200, {})

    def do_GET(self):
        self._send(200, {"status": "ok", "message": "AI Student Impact API"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
        except Exception:
            self._send(400, {"error": "Invalid JSON body"})
            return

        features, err = validate(data)
        if err:
            self._send(400, {"error": err})
            return

        gpa = predict_gpa(features)
        self._send(200, {
            "predicted_post_gpa": round(gpa, 2),
            "grade_letter": gpa_to_letter(gpa),
            "insight": gpa_to_insight(gpa),
        })

    def log_message(self, *args):
        pass  # silence default request logs
