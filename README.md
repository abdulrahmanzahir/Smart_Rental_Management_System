
# 🚗 DriveEase – Smart Rental Management System

![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-brightgreen)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Logging-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 📌 Overview
DriveEase is a **vehicle rental system** built with FastAPI, MongoDB, and Kafka. It allows users to browse, book, and manage vehicles with **role-based access**. Real-time updates and event logging are handled via WebSocket and Apache Kafka respectively.

---

## 🚀 Features
- 🔐 User authentication with hashed passwords  
- 👥 Role management (EMPLOYEE / CUSTOMER)  
- 🚙 Add, view, and filter vehicles  
- 🔔 Real-time notifications using WebSockets  
- 📝 Event logging via Kafka

---

## 🛠️ Tech Stack
- **FastAPI** (backend)
- **MongoDB** (database)
- **Apache Kafka** (event logging)
- **WebSocket** (real-time updates)
- **Python 3.8+**

---

## 📂 File Structure

```bash
📁 project-root/
├── app/
│   ├── main.py              # FastAPI application entry point
│   └── database.py          # MongoDB connection logic
├── db_backup/               # JSON files for users, vehicles, rentals
├── tests/
│   └── test_register.py     # Unit tests for user registration
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/driveease-rental-system
cd driveease-rental-system
pip install -r requirements.txt
```

1. Start **MongoDB**  
2. Run **Zookeeper** and **Kafka**:
   ```bash
   # Windows example:
   bin/windows/zookeeper-server-start.bat config/zookeeper.properties
   bin/windows/kafka-server-start.bat config/server.properties
   ```

3. Launch the server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Visit Swagger Docs: `http://127.0.0.1:8000/docs`

---

## 💾 DB Backup / Restore

```bash
mongorestore --db rental_management ./db_backup/rental_management
```

---

## 🙌 Author
Abdulrahman Zahir  
[GitHub Profile](https://github.com/abdulrahmanzahir)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
