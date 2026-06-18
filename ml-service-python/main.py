from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import joblib
import os
from pymongo import MongoClient
from datetime import datetime

# Read external cloud infrastructure pointers from injected environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Initialize and establish connection handshake with cloud database cluster
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['restaurant_review_db']
    collection = db['reviews_history']
    
    # Execute network ping command to force immediate credentials validation
    client.admin.command('ping')
    print("Database connection successfully established with cloud cluster storage!")
except Exception as e:
    print(f"Critical error trying to authenticate or connect to the cloud database: {e}")

app = FastAPI(title="Restaurant Review ML Service", version="2.0")

# Load trained model and label encoder once at startup (improves performance)
# Keep these in memory for all predictions during API lifetime
try:
    model = tf.keras.models.load_model('modelo_sentimento.keras')
    le = joblib.load('label_encoder.pkl')
except Exception as e:
    raise RuntimeError(f"Error loading model artifacts: {e}")

# Define the expected JSON request structure from Go Gateway service
class ReviewInput(BaseModel):
    review_text: str

@app.post("/v1/predict")
def predict_sentiment(data: ReviewInput):
    """Predict sentiment from restaurant review text using calibrated encoder maps.
    
    Args:
        data: ReviewInput with 'review_text' field containing the review to analyze
        
    Returns:
        dict: Contains prediction_code (0/1), sentiment (Positive/Negative), and confidence score
    """
    if not data.review_text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty.")
    
    try:
        # Convert text to numpy array with object dtype
        input_data = np.array([data.review_text], dtype=object)
        
        # Run inference: returns probability distribution over classes
        predictions = model.predict(input_data, verbose=0)
        
        # Get index of class with highest probability
        class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][class_index])
        
        # DYNAMIC DECODING: Use LabelEncoder directly to decode the true class mapping
        # This completely eliminates hardcoded index discrepancies
        decoded_target = le.inverse_transform([class_index])[0]
        
        # Standardize output string based on the encoder's mapping payload
        # Converts 1/true profiles to Positive and 0/false profiles to Negative
        if str(decoded_target) == "1":
            human_sentiment = "Positive"
        else:
            human_sentiment = "Negative"
        
        # PERSISTENCE LAYER: Structure analytical payload to upload to MongoDB Atlas
        # Injecting UTC timestamp for tracking data drifts and processing time metrics
        # NOTE: Review text is NOT persisted - only aggregate statistics (prediction, sentiment, confidence)
        log_payload = {
            "prediction_code": int(class_index),
            "sentiment": human_sentiment,
            "confidence": round(confidence, 4),
            "timestamp": datetime.utcnow()
        }
        
        # Commit anonymized transaction log into the cloud database historical collection
        collection.insert_one(log_payload)
        
        return {
            "prediction_code": int(class_index),  # Numeric class index (0 or 1)
            "sentiment": human_sentiment,          # Human-readable sentiment label
            "confidence": round(confidence, 4)     # Probability score (0.0 to 1.0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal inference error: {e}")