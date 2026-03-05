import os
import sys
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from keras_self_attention import SeqSelfAttention
from keras_multi_head import MultiHeadAttention
from datetime import datetime, date

class MLModelService:
    """Service class to handle ML model operations for Django integration"""
    
    def __init__(self):
        self.model = None
        self.class_names = [
            'Alopecia Areata',
            'Contact Dermatitis', 
            'Folliculitis',
            'Head Lice',
            'Lichen Planus',
            'Male Pattern Baldness',
            'Psoriasis',
            'Seborrheic Dermatitis',
            'Telogen Effluvium',
            'Tinea Capitis'
        ]
        self.load_model()
    
    def load_model(self):
        """Load the trained model with custom objects"""
        try:
            # Get the path to the model file (assuming it's in the parent directory)
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hair-diseases.h5')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            
            self.model = load_model(
                model_path,
                custom_objects={
                    "SeqSelfAttention": SeqSelfAttention,
                    "MultiHeadAttention": MultiHeadAttention
                }
            )
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            self.model = None
    
    def preprocess_image(self, img: Image.Image):
        """Preprocess image for model prediction"""
        try:
            img = img.resize((128, 128))  # Match model's input size
            img_array = np.array(img) / 255.0
            return np.expand_dims(img_array, axis=0)
        except Exception as e:
            print(f"❌ Error preprocessing image: {str(e)}")
            return None
    
    def calculate_disease_stage(self, predicted_class, confidence, symptom_start_date):
        """Calculate disease stage based on confidence and time elapsed"""
        try:
            # Parse the symptom start date
            if isinstance(symptom_start_date, str):
                start_date = datetime.strptime(symptom_start_date, '%Y-%m-%d').date()
            else:
                start_date = symptom_start_date
            
            # Calculate days elapsed
            today = date.today()
            days_elapsed = (today - start_date).days
            
            # Ensure days_elapsed is not negative
            if days_elapsed < 0:
                return "Invalid Date", "Symptom start date cannot be in the future", "Invalid", 0
            
            # Stage calculation based on confidence and time elapsed
            # Higher confidence + more time = more advanced stage
            
            # Base stage from confidence
            if confidence >= 0.9:
                base_stage = 3  # High confidence suggests advanced condition
            elif confidence >= 0.7:
                base_stage = 2  # Medium confidence
            else:
                base_stage = 1  # Lower confidence suggests early stage
            
            # Time factor adjustment
            if days_elapsed <= 7:  # Within a week
                time_factor = 0
                time_desc = "Recent onset"
            elif days_elapsed <= 30:  # Within a month
                time_factor = 1
                time_desc = "Short-term"
            elif days_elapsed <= 90:  # Within 3 months
                time_factor = 2
                time_desc = "Medium-term"
            elif days_elapsed <= 180:  # Within 6 months
                time_factor = 3
                time_desc = "Long-term"
            else:  # More than 6 months
                time_factor = 4
                time_desc = "Chronic"
            
            # Calculate final stage (1-5 scale)
            final_stage = min(5, max(1, base_stage + time_factor - 1))
            
            # Stage descriptions
            stage_descriptions = {
                1: "Early Stage - Recent symptoms with mild presentation",
                2: "Developing Stage - Symptoms becoming more noticeable", 
                3: "Moderate Stage - Clear symptoms requiring attention",
                4: "Advanced Stage - Well-established condition needing treatment",
                5: "Severe/Chronic Stage - Long-standing condition requiring immediate care"
            }
            
            return f"Stage {final_stage}", stage_descriptions[final_stage], time_desc, days_elapsed
            
        except Exception as e:
            print(f"❌ Error calculating disease stage: {str(e)}")
            return "Unknown Stage", "Unable to determine stage", "Unknown", 0
    
    def predict(self, image_file, symptom_start_date=None):
        """Make prediction on uploaded image"""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Open and convert image
            img = Image.open(image_file).convert("RGB")
            
            # Preprocess image
            processed = self.preprocess_image(img)
            if processed is None:
                return {"error": "Failed to preprocess image"}
            
            # Make prediction
            prediction = self.model.predict(processed)
            predicted_class = self.class_names[np.argmax(prediction)]
            confidence = float(np.max(prediction))
            
            result = {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "success": True
            }
            
            # Calculate disease stage if symptom start date is provided
            if symptom_start_date:
                stage, stage_desc, time_desc, days_elapsed = self.calculate_disease_stage(
                    predicted_class, confidence, symptom_start_date
                )
                result.update({
                    "stage": stage,
                    "stage_description": stage_desc,
                    "time_description": time_desc,
                    "days_elapsed": days_elapsed,
                    "symptom_start_date": symptom_start_date
                })
            
            return result
            
        except Exception as e:
            print(f"❌ Error during prediction: {str(e)}")
            return {"error": f"Prediction failed: {str(e)}"}

# Global instance
ml_service = MLModelService()