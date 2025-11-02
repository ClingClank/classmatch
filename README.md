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

- **Framework:** React (Vite)
- **Routing:** React Router DOM
- **Styling:** Bootstrap 5 / Bootswatch Darkly
- **Storage:** LocalStorage API (client-side persistence)
- **Language:** JavaScript (ES6 Modules)

---

## Project Structure

```
.
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── docs/
│   ├── assignment-refs.md
│   ├── use-cases/           
│   └── diagrams/            
└── web/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── routes.jsx
        ├── style.css
        ├── lib/
        │   └── api.js
        ├── components/
        │   └── Nav.jsx
        └── pages/
            ├── Login.jsx
            ├── Signup.jsx
            ├── Matches.jsx
            ├── CreateGroup.jsx
            └── Dashboard.jsx
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/classmatch.git
cd classmatch/web
```

### 2. Install dependencies
```bash
npm install
```

### 3. Run the development server
```bash
npm run dev
```
Then open the link provided in your terminal (usually `http://localhost:5173`).

---

## Future Improvements

- Integrate a backend (Node/Express or Firebase) for real user authentication.  
- Replace local storage with a cloud database.  
- Add chat or messaging functionality for group members.  
- Implement calendar integration for availability scheduling.  
- Enhance accessibility and responsive design further.

---

## Authors

- **James Callender**  
- **Parsa Hajiha**  
- **Tri Le**
