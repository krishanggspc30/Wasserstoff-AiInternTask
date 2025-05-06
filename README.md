# WhatBeatsRock

# GenAI Game – Internship Task Submission

This project is a GenAI-powered game built using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. Players try to beat the previous word in a Rock-Paper-Scissors-like logic using natural language input, judged by a generative AI.

---

## 🌟 Features

- 🎮 Game logic with AI-based decision making  
- 🤖 Uses Gemini API (or similar LLM) to determine winning moves  
- ⚡ FastAPI for backend RESTful services  
- 🧠 Caching AI responses with Redis to reduce redundant calls  
- 🗃 PostgreSQL for logging and stats  
- 🖼 Simple HTML UI interface  
- 🐳 Fully containerized with Docker and Docker Compose  

---

## 🚀 Project Structure

genai-intern-game/
│
├── backend/
│ ├── main.py # FastAPI app
│ ├── core/
│ │ ├── ai_client.py # AI query logic
│ │ ├── cache.py # Redis caching logic
│ │ ├── game_logic.py # Session & game rules
│ │ └── moderation.py # Text moderation logic
│ ├── db/
│ │ ├── models.py # DB models and DB functions
│ └── static/
│ └── index.html # Frontend HTML
│
├── .env # Environment variables
├── Dockerfile # Backend image
├── docker-compose.yml # Container orchestration
└── README.md # This file

yaml
Copy
Edit

---

## ⚙️ Environment Setup

Create a `.env` file in the root directory with the following content:

```env
AI_API_URL=https://generativeai.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
AI_API_KEY=your_google_api_key
🐳 Run with Docker
Make sure Docker is installed and running.

Then execute:

bash
Copy
Edit
docker-compose up --build
This starts:

api on http://localhost:8000

PostgreSQL on port 5432

Redis on port 6379

🔗 API Endpoints
Method	Endpoint	Description
GET	/	Welcome message
GET	/test-ai	Tests AI with sample input
POST	/sessions	Starts a new game session
POST	/guess	Submit a guess to continue game
GET	/history/{id}	View session history

🧠 How it Works
Session Initialization: A new session UUID is created and stored in memory.

User Guess: Player submits a guess via UI or API.

AI Decision: AI decides if the guess beats the previous word.

Cache Check: If result is cached, returns directly. Otherwise, stores it after querying.

Validation: Guess is moderated and checked for duplicates.

Score Update: Score is increased, and stats logged in PostgreSQL.

Frontend: Static HTML interfaces with the API.

🧪 Example Usage
To test locally:

bash
Copy
Edit
curl -X POST http://localhost:8000/sessions
Then submit a guess using the session ID returned.
