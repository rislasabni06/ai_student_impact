"""
Vercel serverless function: /api/predict
This thin wrapper loads the model and handles one prediction per invocation.
"""
from http.server import BaseHTTPRequestHandler
import json, os, sys, numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import joblib
from utils import validate_and_parse, gpa_to_letter, gpa_to_insight

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model.pkl')
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


class handler(BaseHTTPRequestHandler):

    def _send(self, status, body: dict):
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

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self._send(400, {"error": "Invalid JSON"})
            return

        features, err = validate_and_parse(data)
        if err:
            self._send(400, {"error": err})
            return

        model = get_model()
        pred = float(np.clip(model.predict([features])[0], 0.0, 4.0))

        self._send(200, {
            "predicted_post_gpa": round(pred, 2),
            "grade_letter": gpa_to_letter(pred),
            "insight": gpa_to_insight(pred),
        })
