# ClassMatch

**ClassMatch** is a modern web application designed to help students discover compatible classmates based on shared courses, schedules, and study preferences. It enables users to create or join study groups, manage their weekly availability, and collaborate efficiently through an intuitive and responsive interface.

---

## Overview

This project was developed for **CS 4090 - Software Engineering** to demonstrate the process of translating user stories and use cases into a functional, user-centered web application.  
The app is built using **React (Vite)** for the frontend and styled with **Bootstrap (Bootswatch Darkly)** for a clean, modern dark theme. Local storage provides lightweight persistence for prototyping purposes.

---

## Features

- **User Registration & Login** – Simple authentication with session persistence.
- **Classmate Matchmaking** – Instantly find other students taking the same courses.
- **Group Creation & Management** – Build or join study groups organized by course and interest.
- **Personal Dashboard** – View your active groups and upcoming study sessions at a glance.
- **Responsive Dark UI** – Elegant and accessible layout built on Bootswatch Darkly.

---

## Tech Stack

- **Framework:** Client: React (Vite), Server: Flask
- **Routing:** React Router DOM
- **Styling:** Bootstrap 5
- **Storage:** LocalStorage API (client-side persistence)
- **Languages:** JavaScript (ES6 Modules), Python
- **Database:** MySQL

---

## Project Structure

Top-level layout showing the main folders and where to find frontend and backend code.

```
.
├── README.md
├── .gitignore
├── docs/                      # design docs, use-cases, diagrams
│   ├── assignment-refs.md
│   ├── use-cases/
│   └── diagrams/
├── client/                    # React (Vite) frontend
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── style.css
│       ├── lib/               # api helpers & integration
│       │   ├── api.js
│       │   └── apiIntegration.js
│       ├── context/           # auth & app context
│       │   └── AuthContext.jsx
│       ├── data/              # sample data for prototyping
│       │   └── sampleData.js
│       ├── components/        # UI components grouped by feature
│       │   ├── CourseCard/
│       │   ├── GroupCard/
│       │   ├── UserMatchCard/
│       │   ├── Nav/
│       │   └── ProtectedRoute/
│       └── pages/             # top-level app pages
│           ├── Login/
│           ├── Signup/
│           ├── Dashboard/
│           ├── BrowseCourses/
│           ├── Matches/
│           └── CreateGroup/
└── server/                    # Backend (Flask/FastAPI) and DB config
    ├── app.py                 # main server entrypoint
    ├── config.py              # reads server/.env
    ├── requirements.txt

```

Notes:

- client/: frontend source (run with npm run dev inside client/)
- server/: backend service; ensure server/.env contains DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JamesRCall/classmatch.git
cd classmatch
```

### 2. Client (frontend) — located in client/

- Purpose: Frontend React app (Vite). Use these commands from the repository root.

```bash
cd client
npm install
npm run dev
```

Open the link provided in your terminal (usually http://localhost:5173).

### 3. Server (backend) — located in server/

- Purpose: Python-based backend (see server/). The server reads configuration from server/.env (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME). Ensure you create or update server/.env before starting the server.

Example server/.env (place inside the server directory):

```
DB_USER=root
DB_PASS=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=classmatch
```

Basic steps to run the server:

```bash
cd server
# create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# start the server
flask run
```

Notes:

- The server explicitly loads environment variables from server/.env (see server/config.py). Make sure DB\_\* values are set there.

---

## Backend (server) — overview

- Location: server/
- Config: server/.env (environment variables are loaded by server/config.py)
- Typical env variables: DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

---

## Testing

Unit, integration, and system validation tests are provided using `pytest`. Tests use an in-memory SQLite database and patch the application's DB engine so they run without a local MySQL server.

Run tests from the project root:

```bash
# Create virtual environment 
# (Skip this step there's venv in server folder already)
python -m venv server/venv

# Activate created enviroment
server/venv/Scripts/activate # Windows
source server/venv/bin/activate # Mac / Linux

#Install dependencies
pip install -r server/requirements.txt

# Run test
pytest
```

---

## Authors

- **James Callender**
- **Parsa Hajiha**
- **Tri Le**
