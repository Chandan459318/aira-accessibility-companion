# 🛫 AIRA – AI-Driven Real-Time Accessibility Companion

**AIRA** (AI-Driven Real-Time Accessibility Companion) is a smart accessibility assistant built for the airline industry. It connects passengers and crew members through an intelligent interface that improves travel experiences for people with accessibility needs, anxiety, first-time travelers, and more.

---

## 🚀 Project Overview

**AIRA** provides:
- 🧍‍♂️ A user-friendly **Passenger Support Form** for requesting in-flight assistance.
- 🤖 A context-aware **AI Smart Assistant** that generates real-time message suggestions.
- 🧑‍✈️ A responsive **Crew Dashboard** to manage passenger needs and reply to messages.
- 🔄 A **Flight Update Module** for crew to send boarding, landing, and luggage updates.

All interactions are secured through **role-based authentication**, and data is stored using **SQLite** for fast, local testing and prototyping.

---

## 🎯 Key Features

| Module              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| 🧍 Passenger Form    | Collects flight number, seat, accessibility needs, and custom notes.       |
| 🤖 AI Assistant      | Bi-directional chat for crew and passengers, with context-based suggestions.|
| 👩‍✈️ Crew Dashboard   | Lists filtered passenger requests and flags high-priority cases.            |
| 🛬 Flight Info Panel | Crew sends boarding/landing/luggage alerts to all passengers.               |
| 🔐 Login System      | Role-based login for secure module access (Passenger / Crew).               |

---

## 🧱 Tech Stack

| Tech       | Usage                            |
|------------|----------------------------------|
| **Python** | Core backend + logic             |
| **Streamlit** | UI rendering and interactivity |
| **SQLite** | Lightweight local DB             |
| **HTML/CSS** | Styling enhancements            |
| **Git**    | Version control                  |

---

## 🛠 Setup Instructions

### 1. 🔁 Clone the Repository
```bash
git clone https://github.com/YourUsername/aira-accessibility-companion.git
cd aira-accessibility-companion
```
### 2. 📦 Install Requirements
```bash
pip install -r requirements.txt
```
### 3. 🚀 Run the Application
```bash
python -m streamlit run app.py
