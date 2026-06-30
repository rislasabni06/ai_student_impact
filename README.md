# 🎓 AI Student Impact — GPA Predictor

A full-stack web app that predicts a student's **Post-Semester GPA** based on their AI usage habits, study patterns, and stress indicators. Built with a **Linear Regression** model (R² ≈ 0.93) trained on student behavioral data.

---

## 📁 Project Structure

```
ai-student-impact/
├── frontend/
│   ├── index.html       # Main UI
│   ├── style.css        # Dark-theme styles
│   └── script.js        # Slider logic + API calls
│
├── backend/
│   ├── app.py           # Flask REST API  (/predict endpoint)
│   ├── utils.py         # Validation, encoding, GPA helpers
│   ├── model.pkl        # Trained LinearRegression model (joblib)
│   └── requirements.txt # Python dependencies
│
├── api/
│   └── predict.py       # Vercel serverless function wrapper
│
├── vercel.json          # Vercel deployment config
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1 — Clone the repo

```bash
git clone https://github.com/your-username/ai-student-impact.git
cd ai-student-impact
```

### 2 — Run the backend locally

```bash
cd backend
pip install -r requirements.txt
python app.py
# → API running at http://localhost:5000
```

### 3 — Open the frontend

Simply open `frontend/index.html` in your browser.  
> **Edit `script.js` line 7** to point to your local or deployed backend:
> ```js
> const API_BASE = "http://localhost:5000";
> ```

---

## 🌐 Deployment

### Frontend → Vercel (static)

1. Push to GitHub.
2. Import the repo at [vercel.com](https://vercel.com).
3. Vercel auto-detects `vercel.json` and deploys both the static frontend and the serverless `/api/predict` endpoint.

### Backend → Render (recommended for Flask)

1. Create a new **Web Service** on [render.com](https://render.com).
2. Point it at the `backend/` folder.
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn app:app`
5. Copy the Render URL, update `API_BASE` in `script.js`, redeploy.

---

## 🔢 Model Features

| Feature | Range | Description |
|---|---|---|
| Weekly GenAI Hours | 0–40 | Hours per week using AI tools |
| Traditional Study Hours | 0–10 | Hours per day studying without AI |
| Skill Retention Score | 0–100 | Self-assessed knowledge retention |
| Anxiety Level (Exams) | 0–10 | Stress during exams |
| Perceived AI Dependency | 0–10 | Reliance on AI for tasks |
| Pre-Semester GPA | 0–4 | GPA entering the semester |
| Burnout Risk Level | Low/Med/High | Self-assessed burnout risk |

**Target**: `Post_Semester_GPA` (0.0–4.0)

---

## 🔄 Retrain with Your Own Data

Replace `model.pkl` by running the training script on your real CSV:

```python
import pandas as pd, joblib, numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv('ai_student_impact_dataset.csv').dropna()
# Burnout encoding: High→0, Low→1, Medium→2 (alphabetical LabelEncoder order)
df['Burnout_Risk_Level'] = df['Burnout_Risk_Level'].map({'High':0,'Low':1,'Medium':2})

X = df[["Weekly_GenAI_Hours","Traditional_Study_Hours","Skill_Retention_Score",
        "Anxiety_Level_During_Exams","Perceived_AI_Dependency","Pre_Semester_GPA","Burnout_Risk_Level"]]
y = df["Post_Semester_GPA"]

model = LinearRegression()
model.fit(*train_test_split(X, y, test_size=0.2, random_state=42)[:2])
joblib.dump(model, 'backend/model.pkl')
print("Done! R²:", model.score(X, y))
```

---

## 📄 License

MIT — use freely, credit appreciated.
