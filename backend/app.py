
from flask import Flask, request, jsonify, make_response
import json
import os

app = Flask(__name__)

KB_PATH = os.path.join(os.path.dirname(__file__), "dummy_kb.json")

with open(KB_PATH) as f:
    KB = json.load(f)

def find_answer(question: str) -> str:
    q = question.lower()
    for entry in KB:
        for kw in entry.get("keywords", []):
            if kw in q:
                return entry.get("answer", "")
    return "This is a demo AI assistant for the Endpoint team. I couldn't match your question exactly, but in a real system I would search policies, runbooks, and logs to generate a detailed answer."

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        resp = make_response("", 204)
    else:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "")
        answer = find_answer(question)
        resp = jsonify({"answer": answer})

    # CORS headers
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

if __name__ == "__main__":
    # Run on port 5050 so it doesn't clash with frontend
    app.run(host="0.0.0.0", port=5050, debug=True)
