
from flask import Flask, request, jsonify, make_response
import json, os
from difflib import SequenceMatcher

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), 'dummy_kb.json')) as f:
    KB = json.load(f)

def sim(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_best(q):
    q = q.lower()
    best = None
    best_score = 0
    suggestions = []

    for entry in KB:
        for kw in entry["keywords"]:
            s = sim(q, kw)
            if s > 0.2:
                suggestions.append(kw)
            if s > best_score:
                best_score = s
                best = entry

    return best, best_score, suggestions

@app.route('/ask', methods=['POST','OPTIONS'])
def ask():
    if request.method=='OPTIONS':
        resp = make_response("",204)
    else:
        data = request.get_json(silent=True) or {}
        q = data.get("question","")
        entry, score, sug = find_best(q)

        if score > 0.35:
            resp = jsonify({"answer": entry["answer"], "suggestions": list(set(sug))[:3]})
        else:
            resp = jsonify({"answer": "I'm not fully sure. Try refining your question.", "suggestions": list(set(sug))[:3]})

    resp.headers['Access-Control-Allow-Origin']='*'
    resp.headers['Access-Control-Allow-Headers']='Content-Type'
    resp.headers['Access-Control-Allow-Methods']='POST,OPTIONS'
    return resp

app.run(port=5050, debug=True)
