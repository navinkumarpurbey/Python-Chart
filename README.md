# 💬 FastAPI Chat Application with JWT, RBAC & WebSocket

This is a full-featured backend project built with **FastAPI**, designed to support a **real-time chat application** with secure **JWT authentication**,
**role-based access control (RBAC)**, and **WebSocket communication**. Data is persisted using **PostgreSQL** via **SQLAlchemy ORM**.

---

## 🚀 Features

- 🔐 User Signup & Login with JWT-based authentication
- 🛡️ Role-Based Access Control (admin vs user)
- 🔒 Protected Routes using FastAPI dependencies
- 💬 Real-Time Chat via WebSocket
- 🗄️ PostgreSQL persistence for users, messages, and chat rooms
- 🧠 Optional: Sentiment analysis with ML (Group C)
- 🌐 CORS enabled for frontend integration

---

## 🛠️ Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Auth**: JWT + OAuth2PasswordBearer
- **Database**: PostgreSQL + SQLAlchemy ORM
- **WebSocket**: FastAPI WebSocket support
- **Password Hashing**: PassLib (bcrypt)
- **Token Handling**: Python-JOSE

---

## 📂 Project Structure

project/
├── app/
│ ├── main.py # All endpoints & WebSocket
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── auth.py # JWT auth logic
│ ├── deps.py # RBAC dependencies
│ ├── database.py # DB connection
│ ├── init.py
├── requirements.txt


---

## ⚙️ Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/chat-backend.git
   cd chat-backend

   
1. Create virtual environment

bash
----
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate (Windows)

2. Install dependencies
bash
------
pip install -r requirements.txt

Set up PostgreSQL

3. Install PostgreSQL and create a database:

sql
-----
CREATE DATABASE chatdb;

4. Run the server

bash
-----
uvicorn app.main:app --reload
