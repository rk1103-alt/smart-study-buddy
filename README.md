# Smart Study Buddy

**Team Members:** [Kipruto, Robert] and [Shafer, Cassidey J]

## Description
Smart Study Buddy is an AI-powered web application that helps students study. Users can paste their class notes, and the app uses Google Gemini AI to generate three practice questions based on those notes. The app saves the notes and generated questions to a local SQLite database so users can review their study history.

## Tech Stack
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Backend:** Python (Flask)
- **Database:** SQLite
- **AI Service:** Google Gemini API (gemini-1.5-flash)

## How to Run
1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory and add your API key: `GEMINI_API_KEY=your_key_here`
6. Run the app: `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.

## Contributions
- **[Your Name]:** Backend development, AI integration, database setup.
- **[Partner's Name]:** Frontend UI design, testing, and documentation.

## Known Limitations
- The app currently only generates questions, not answers.
- The UI is basic and could be styled further with CSS frameworks.