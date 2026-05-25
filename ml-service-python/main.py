from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import joblib

app = FastAPI(title="Restaurant Review ML Service", version="1.0")

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
    """Predict sentiment from restaurant review text.
    
    Args:
        data: ReviewInput with 'review_text' field containing the review to analyze
        
    Returns:
        dict: Contains prediction_code (0/1), sentiment (Positive/Negative), and confidence score
    """
    # Validate that review text is not empty or only whitespace
    if not data.review_text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty.")
    
    try:
        # Convert text to numpy array with object dtype (compatible with Keras TextVectorization)
        input_data = np.array([data.review_text], dtype=object)
        
        # Run inference: returns probability distribution over classes (softmax output)
        predictions = model.predict(input_data, verbose=0)
        
        # Get index of class with highest probability
        class_index = np.argmax(predictions[0])
        # Get actual confidence value (probability score between 0 and 1)
        confidence = float(predictions[0][class_index])
        
        # Get original label from label encoder
        raw_label = str(le.classes_[class_index])
        
        # Convert numeric labels to human-readable sentiment strings
        # This makes the JSON response more user-friendly
        # Label 1 or index 1 = Positive, Label 0 or index 0 = Negative
        if raw_label == "1" or class_index == 1:
            human_sentiment = "Positive"
        else:
            human_sentiment = "Negative"
        
        return {
            "prediction_code": int(class_index),  # Numeric class index (0 or 1)
            "sentiment": human_sentiment,          # Human-readable sentiment label
            "confidence": confidence               # Probability score (0.0 to 1.0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal inference error: {e}")