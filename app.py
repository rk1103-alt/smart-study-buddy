import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
import google.generativeai as genai

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database.db"

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

def initialize_database():
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    notes TEXT NOT NULL,
                    questions TEXT NOT NULL
                )
                """
            )

initialize_database()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/generate")
def generate():
    payload = request.get_json(silent=True)
    notes = payload.get("notes") if isinstance(payload, dict) else None
    if not isinstance(notes, str) or not notes.strip():
        return jsonify(error="Enter some notes before generating questions."), 400

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify(error="GEMINI_API_KEY is not configured."), 503

    try:
        print("DEBUG: Connecting to Gemini...")
        genai.configure(api_key=api_key)
        
        # We are using gemini-2.5-flash which is the current free tier model
        model = genai.GenerativeModel("gemini-3.8-flash")
        
        print("DEBUG: Sending prompt to AI...")
        response = model.generate_content(
            "Create exactly 3 useful practice questions based on the notes. "
            'Return only a JSON object with one key, "questions", whose value is '
            "an array of 3 strings. Do not include answers.\n\n"
            f"Notes:\n{notes.strip()}",
            generation_config={"response_mime_type": "application/json"},
        )
        print("DEBUG: Response received!")
        response_text = response.text
        result = json.loads(response_text)
        questions = result.get("questions")
        
        if not isinstance(questions, list) or len(questions) != 3:
            raise ValueError("The AI did not return exactly 3 questions.")

    except Exception as e:
        print("\n\n" + "="*50)
        print("!!! ERROR OCCURRED !!!")
        print(str(e))
        print("="*50 + "\n\n")
        return jsonify(error=f"AI Error: {str(e)}"), 502

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO study_sessions (notes, questions) VALUES (?, ?)",
                (notes.strip(), json.dumps(questions)),
            )
            session_id = cursor.lastrowid

    return jsonify(id=session_id, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)