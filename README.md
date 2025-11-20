
# Endpoint Gemini-style Demo

This is a local fake demo that simulates a Gemini-style UI for an Endpoint Support AI assistant.

## 1. Backend (Flask)

### Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

The backend will start on `http://127.0.0.1:5050`.

## 2. Frontend (React + Tailwind via CDN, no build step)

In a separate terminal:

```bash
cd frontend
python3 -m http.server 3000
```

Then open:

```
http://localhost:3000
```

You will see a Gemini-like landing page with:

- "Hello," greeting
- Center prompt bar
- Example chips with typical endpoint questions
- Chat bubbles for conversation

Click any example chip or type your own question and hit **Send**.
The frontend will call the Flask backend at `/ask` and display the answer.

## 3. Changing the Q&A content

Edit `backend/dummy_kb.json`.

Each entry has:

```json
{
  "keywords": ["vpn"],
  "answer": "For VPN issues, do X, Y, Z..."
}
```

Add more entries with suitable keywords. The backend matches the first entry where any keyword is contained in the user's question (case-insensitive).
