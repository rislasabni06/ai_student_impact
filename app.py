from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

BURNOUT_MAP = {"High": 0, "Low": 1, "Medium": 2}

FEATURE_ORDER = [
    "Weekly_GenAI_Hours",
    "Traditional_Study_Hours",
    "Skill_Retention_Score",
    "Anxiety_Level_During_Exams",
    "Perceived_AI_Dependency",
    "Pre_Semester_GPA",
    "Burnout_Risk_Level",
]

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "AI Student Impact API is running."})


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json(force=True)

    try:
        burnout_raw = data.get("Burnout_Risk_Level", "Low")
        burnout_encoded = BURNOUT_MAP.get(burnout_raw)
        if burnout_encoded is None:
            return jsonify({"error": "Burnout_Risk_Level must be Low, Medium, or High"}), 400

        features = np.array([[
            float(data["Weekly_GenAI_Hours"]),
            float(data["Traditional_Study_Hours"]),
            float(data["Skill_Retention_Score"]),
            float(data["Anxiety_Level_During_Exams"]),
            float(data["Perceived_AI_Dependency"]),
            float(data["Pre_Semester_GPA"]),
            burnout_encoded,
        ]])

        prediction = float(np.clip(model.predict(features)[0], 0.0, 4.0))

        return jsonify({
            "predicted_post_gpa": round(prediction, 2),
            "grade_letter": gpa_to_letter(prediction),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def gpa_to_letter(gpa):
    if gpa >= 3.7: return "A / A+"
    if gpa >= 3.3: return "A-"
    if gpa >= 3.0: return "B+"
    if gpa >= 2.7: return "B"
    if gpa >= 2.3: return "B-"
    if gpa >= 2.0: return "C+"
    if gpa >= 1.7: return "C"
    if gpa >= 1.0: return "D"
    return "F"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)