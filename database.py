from deta import Deta
import os
from dotenv import load_dotenv
import streamlit as st
import uuid

# Load environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# Connect to database
db = deta.Base("ratings")


# Insert a row (the key is the unique identifier)
def insert_period(slider_rating):
    unique_id = str(uuid.uuid4())
        
    # Create a data structure with only the rating and a unique identifier
    data = {
        "id": unique_id,
        "rating": slider_rating
    }
    
    # Insert the data with the unique identifier as the key
    return db.put(data)

def get_average_rating():
    # Retrieve all ratings from the database
    all_ratings = list(db.fetch().items)
    
    if not all_ratings:
        return None
    
    # Calculate the average rating
    total_ratings = len(all_ratings)
    total_sum = sum(item["rating"] for item in all_ratings)
    average_rating = total_sum / total_ratings
    
    return average_rating
