from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# ----- Load fake KB -----
with open("data.json") as f:
    KB = json.load(f)

# Preload embedding model (local, no API keys)
model = SentenceTransformer("all-MiniLM-L6-v2")

questions = [item["question"] for item in KB]
question_embs = model.encode(questions)


def find_best_answer(query: str) -> str:
    """Return best matching answer from the fake KB."""
    q_vec = model.encode([query])[0]
    # cosine similarity
    scores = np.dot(question_embs, q_vec) / (
        np.linalg.norm(question_embs, axis=1) * np.linalg.norm(q_vec)
    )
    best_idx = np.argmax(scores)
    best_score = float(scores[best_idx])

    if best_score < 0.4:
        return (
            "I'm not fully sure based on my current knowledge. "
            "Please raise a ticket with the Endpoint team."
        )

    return KB[best_idx]["answer"]


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/ask")
def ask():
    data = request.get_json()
    user_msg = data.get("message", "")
    answer = find_best_answer(user_msg)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    # http://127.0.0.1:5050
    app.run(host="127.0.0.1", port=5050, debug=True)
