import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "rental_management")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
print("Connected to MongoDB successfully.")