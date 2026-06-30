# 🎓 AI Student Impact — GPA Predictor

Predicts a student's **Post-Semester GPA** based on AI usage habits, study patterns, and stress indicators. Fully deployable on **Vercel** with zero external services.

---

## 📁 Structure

```
├── public/
│   ├── index.html      # UI
│   ├── style.css       # Dark theme
│   └── script.js       # Slider logic + API call
├── api/
│   └── predict.py      # Vercel serverless function (pure Python, no sklearn)
├── vercel.json         # Routing config
└── .gitignore
```

---

## 🚀 Deploy to Vercel (3 steps)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-student-impact.git
git push -u origin main
```

### 2. Import on Vercel
- Go to [vercel.com](https://vercel.com) → **Add New Project**
- Import your GitHub repo
- No environment variables needed
- Click **Deploy** ✅

### 3. Done!
Your app is live at `https://your-project.vercel.app`

---

## 🖥️ Run Locally

```bash
npm i -g vercel      # install Vercel CLI once
vercel dev           # runs frontend + serverless function together
```
Open `http://localhost:3000`

---

## 🔢 Model Info

Linear Regression trained on AI student behavior data (R² ≈ 0.93).  
Coefficients are hardcoded in `api/predict.py` — no model file needed.

| Feature | Range |
|---|---|
| Weekly GenAI Hours | 0–40 h |
| Traditional Study Hours | 0–10 h/day |
| Skill Retention Score | 0–100 |
| Anxiety Level (Exams) | 0–10 |
| Perceived AI Dependency | 0–10 |
| Pre-Semester GPA | 0.0–4.0 |
| Burnout Risk Level | Low / Medium / High |

---

## 📄 License
MIT
