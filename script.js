const API_BASE = "https://ai-student-impact.onrender.com"; 

// ── DOM refs ─────────────────────────────────────────────────────────────────
const sliders = {
  genai:      { el: document.getElementById("genai"),      val: document.getElementById("genai-val"),      suffix: " h" },
  study:      { el: document.getElementById("study"),      val: document.getElementById("study-val"),      suffix: " h" },
  retention:  { el: document.getElementById("retention"),  val: document.getElementById("retention-val"),  suffix: "" },
  anxiety:    { el: document.getElementById("anxiety"),    val: document.getElementById("anxiety-val"),    suffix: " / 10" },
  dependency: { el: document.getElementById("dependency"), val: document.getElementById("dependency-val"), suffix: " / 10" },
  pregpa:     { el: document.getElementById("pregpa"),     val: document.getElementById("pregpa-val"),     suffix: "" },
};

const predictBtn  = document.getElementById("predictBtn");
const btnText     = predictBtn.querySelector(".btn-text");
const btnLoader   = predictBtn.querySelector(".btn-loader");
const resultCard  = document.getElementById("resultCard");
const closeResult = document.getElementById("closeResult");
const errorBanner = document.getElementById("errorBanner");
const errorMsg    = document.getElementById("errorMsg");

let selectedBurnout = "Low";

// ── Slider live update ────────────────────────────────────────────────────────
Object.values(sliders).forEach(({ el, val, suffix }) => {
  el.addEventListener("input", () => {
    const n = parseFloat(el.value);
    val.textContent = (Number.isInteger(n) ? n : n.toFixed(1)) + suffix;
    updateSliderFill(el);
  });
  updateSliderFill(el);
});

function updateSliderFill(el) {
  const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
  el.style.background = `linear-gradient(to right, #6c63ff ${pct}%, #2d3148 ${pct}%)`;
}

// ── Burnout buttons ───────────────────────────────────────────────────────────
document.querySelectorAll(".burnout-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".burnout-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedBurnout = btn.dataset.value;
  });
});

// ── Close result ──────────────────────────────────────────────────────────────
closeResult.addEventListener("click", () => {
  resultCard.classList.add("hidden");
});

// ── Predict ───────────────────────────────────────────────────────────────────
predictBtn.addEventListener("click", async () => {
  hideError();
  resultCard.classList.add("hidden");
  setLoading(true);

  const payload = {
    Weekly_GenAI_Hours:          parseFloat(sliders.genai.el.value),
    Traditional_Study_Hours:     parseFloat(sliders.study.el.value),
    Skill_Retention_Score:       parseFloat(sliders.retention.el.value),
    Anxiety_Level_During_Exams:  parseFloat(sliders.anxiety.el.value),
    Perceived_AI_Dependency:     parseFloat(sliders.dependency.el.value),
    Pre_Semester_GPA:            parseFloat(sliders.pregpa.el.value),
    Burnout_Risk_Level:          selectedBurnout,
  };

  try {
    const res  = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      showError(data.error || `Server error ${res.status}`);
      return;
    }

    displayResult(data);
  } catch (err) {
    showError("Could not reach the prediction server. Is it running? Check API_BASE in script.js.");
  } finally {
    setLoading(false);
  }
});

// ── Display result ────────────────────────────────────────────────────────────
function displayResult({ predicted_post_gpa, grade_letter, insight }) {
  document.getElementById("gpaNumber").textContent   = predicted_post_gpa.toFixed(2);
  document.getElementById("gradeBadge").textContent  = grade_letter;
  document.getElementById("insightText").textContent = insight || "";

  // Animate the bar (GPA 0–4 → 0–100%)
  const pct = (predicted_post_gpa / 4) * 100;
  setTimeout(() => {
    document.getElementById("gpaBar").style.width = `${pct}%`;
  }, 50);

  resultCard.classList.remove("hidden");
  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function setLoading(on) {
  predictBtn.disabled = on;
  btnText.classList.toggle("hidden", on);
  btnLoader.classList.toggle("hidden", !on);
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorBanner.classList.remove("hidden");
}

function hideError() {
  errorBanner.classList.add("hidden");
}
