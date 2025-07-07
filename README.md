# Rental Management System

## Description
This project is a **Rental Management System** built with FastAPI. It allows users to manage vehicle rentals, handle bookings, and send real-time notifications. MongoDB is used for the database, and Apache Kafka logs important booking events.

---

## Features  
- **User Authentication**: Register and login users with hashed passwords.  
- **Role Management**: EMPLOYEE and CUSTOMER roles.  
- **Vehicle Management**: Add, browse, and book vehicles.  
- **Real-time Notifications**: WebSockets for live updates.  
- **Event Logging**: Apache Kafka for logging booking events.  

---

## Prerequisites
Ensure the following are installed:  
- **Python 3.8+**  
- **MongoDB**  
- **Apache Kafka**  
- **Dependencies** listed in `requirements.txt`.

---

## Installation and Setup
1. Copy the project files to your local machine.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
3. Start MongoDB and ensure it is accessible.
4. Start Zookeeper and Kafka servers:
- **Run Zookeeper**: bin/windows/zookeeper-server-start.bat config/zookeeper.properties
- **Run Kafka**: bin/windows/kafka-server-start.bat config/server.properties
5. Launch the FastAPI server: uvicorn main:app --reload
6. Access the API documentation at http://127.0.0.1:8000/docs.

## Database Backup and Restore

- Database exported to *db_backup* folder.
- **To restore**: mongorestore --db rental_management ./db_backup/rental_management

## How to Use
1. Register users and log in through the API.
2. Add vehicles and browse them based on filters.
3. Book vehicles and receive real-time updates via WebSocket.
4. Check booking logs via Kafka.

## File Structure

- **main.py**: Core FastAPI application.
- **database.py**: MongoDB connection setup.
- **models/**: Pydantic models for user, vehicle, and booking.
- **kafka_producer.py**: Event logging implementation.
- **db_backup/**: Backup of the MongoDB database.


