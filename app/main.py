# Import necessary modules
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from passlib.context import CryptContext  # For password hashing
from bson import ObjectId  # To work with MongoDB ObjectIDs
from datetime import datetime
from database import db  # MongoDB connection
from kafka import KafkaProducer
import json

# Initialize the FastAPI application
app = FastAPI()

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def log_event(event_type, details):
    event = {
        "event_type": event_type,
        "details": details
    }
    producer.send("event_logs", value=event)


# -------------------------
# Password Hashing Setup
# -------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------
# Role-Based Access Control
# -------------------------

# Mock function to get user role (TEMPORARY; replace with real logic later)
def get_current_user_role():
    # Simulate roles for testing; returns "EMPLOYEE" or "CUSTOMER"
    return "EMPLOYEE"  # Change to "CUSTOMER" to test behavior for customers


# Role validator to restrict endpoint access
def validate_role(required_role: str, current_role: str = Depends(get_current_user_role)):
    if current_role != required_role:
        raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")


# -------------------------
# Models
# -------------------------

# User model for registration
class User(BaseModel):
    name: str
    email: str
    password: str
    role: str  # Can be "CUSTOMER" or "EMPLOYEE"


# Vehicle model for MongoDB
class Vehicle(BaseModel):
    make: str
    model: str
    type: str
    rental_price_per_day: float
    availability_status: str
    location: str


# Booking model for rentals
class Booking(BaseModel):
    vehicle_id: str
    customer_id: str
    rental_start_date: str  # Format: YYYY-MM-DD
    rental_end_date: str  # Format: YYYY-MM-DD


# -------------------------
# Utility Functions
# -------------------------

# Hashes a plain password
def hash_password(password):
    return pwd_context.hash(password)


# -------------------------
# User Authentication Routes
# -------------------------

# Register a new user
@app.post("/register/")
@app.post("/register/")
def register_user(user: User):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    db.users.insert_one(user_data)

    # Log event
    log_event("USER_REGISTERED", {"email": user.email, "role": user.role})

    return {"message": "User registered successfully"}


# Login user and return their role
@app.post("/login/")
def login_user(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "role": user["role"]}


# -------------------------
# Vehicle Management Routes
# -------------------------

# Add a vehicle (EMPLOYEE only)
@app.post("/vehicles/")
def add_vehicle(vehicle: Vehicle, role: str = Depends(get_current_user_role)):
    validate_role("EMPLOYEE", role)
    existing_vehicle = db.vehicles.find_one({
        "make": vehicle.make,
        "model": vehicle.model,
        "type": vehicle.type,
        "location": vehicle.location
    })
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle already exists")

    # Debugging line to check insertion data
    print("Inserting vehicle:", vehicle.dict())

    db.vehicles.insert_one(vehicle.dict())
    return {"message": "Vehicle added successfully"}


# List all vehicles
@app.get("/vehicles/")
def get_vehicles():
    return {"vehicles": list(db.vehicles.find({}, {"_id": 0}))}


# Browse available vehicles with filters
@app.get("/browse/")
def browse_vehicles(vehicle_type: str = None, max_price: float = None, location: str = None):
    query = {}
    if vehicle_type:
        query["type"] = vehicle_type
    if max_price:
        query["rental_price_per_day"] = {"$lte": max_price}
    if location:
        query["location"] = location
    vehicles = list(db.vehicles.find(query, {"_id": 0}))
    return {"available_vehicles": vehicles}


# -------------------------
# Vehicle Booking Route
# -------------------------

# Book a vehicle
active_connections = []  # For WebSocket notifications


async def send_notification(message: str):
    # Send a notification to all active WebSocket clients
    for connection in active_connections:
        await connection.send_text(message)


@app.post("/book/")
@app.post("/book/")
async def book_vehicle(booking: Booking):
    vehicle = db.vehicles.find_one({
        "_id": ObjectId(booking.vehicle_id),
        "availability_status": "AVAILABLE"
    })
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle is not available for booking")

    start_date = datetime.strptime(booking.rental_start_date, "%Y-%m-%d")
    end_date = datetime.strptime(booking.rental_end_date, "%Y-%m-%d")
    days = (end_date - start_date).days
    if days <= 0:
        raise HTTPException(status_code=400, detail="Invalid rental period")
    total_cost = vehicle["rental_price_per_day"] * days

    rental_data = {
        "vehicle_id": booking.vehicle_id,
        "customer_id": booking.customer_id,
        "rental_start_date": start_date,
        "rental_end_date": end_date,
        "total_cost": total_cost
    }
    db.rentals.insert_one(rental_data)
    db.vehicles.update_one(
        {"_id": ObjectId(booking.vehicle_id)},
        {"$set": {"availability_status": "RENTED"}}
    )

    # Log event
    log_event("VEHICLE_BOOKED", {"vehicle_id": booking.vehicle_id, "total_cost": total_cost})

    # Send notification
    await send_notification(f"Vehicle {vehicle['make']} {vehicle['model']} has been booked.")

    return {"message": "Vehicle booked successfully", "total_cost": total_cost}


# -------------------------
# Rental History Routes
# -------------------------

# Get customer rental history
@app.get("/rental-history/{customer_id}/")
def customer_rental_history(customer_id: str):
    rentals = list(db.rentals.find({"customer_id": customer_id}, {"_id": 0}))
    return {"rental_history": rentals}


# Employee can view all rentals
@app.get("/all-rentals/")
def all_rentals(role: str = Depends(get_current_user_role)):
    validate_role("EMPLOYEE", role)
    rentals = list(db.rentals.find({}, {"_id": 0}))
    return {"all_rentals": rentals}


# -------------------------
# WebSocket for Notifications
# -------------------------

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    # Accept WebSocket connection
    await websocket.accept()
    active_connections.append(websocket)
    print("Client connected")
    try:
        while True:
            await websocket.receive_text()  # Keeps connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")
