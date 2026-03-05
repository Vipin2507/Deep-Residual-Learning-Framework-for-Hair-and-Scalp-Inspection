# myapp/ml_service.py
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from datetime import datetime, date

class MLModelService:
    """Service class to handle ML model operations for Django integration"""

    def __init__(self):
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.class_names = [
            'Alopecia Areata',
            'Contact Dermatitis',
            'Folliculitis',
            'Head Lice',
            'Lichen Planus',
            'Male Pattern Baldness',
            'No Disease',
            'Psoriasis',
            'Seborrheic Dermatitis',
            'Telogen Effluvium',
            'Tinea Capitis'
        ]
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])
        self.load_model()

    def load_model(self):
        """Load the trained PyTorch model"""
        try:
            # Try to get model path from Django settings (for production)
            try:
                from django.conf import settings
                if hasattr(settings, 'ML_MODEL_PATH'):
                    model_path = settings.ML_MODEL_PATH
                else:
                    # Fallback to relative path
                    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "best_model.pth")
            except:
                # If Django not configured, use relative path
                model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "best_model.pth")
            
            # Additional fallback for development
            if not os.path.exists(model_path):
                dev_path = r"D:\disease prediction model\required_files\best_model.pth"
                if os.path.exists(dev_path):
                    model_path = dev_path
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")

            print(f"🖥️ Using device: {self.device}")
            print(f"📂 Loading model from: {model_path}")
            print(f"🔢 Number of classes: {len(self.class_names)}")
            print(f"🏷️ Classes: {self.class_names}")

            # Load ResNet50 architecture (matching your test code)
            model = models.resnet50(weights=None)
            num_ftrs = model.fc.in_features
            model.fc = nn.Linear(num_ftrs, len(self.class_names))

            # Load trained weights with strict=True (matching your test code)
            state_dict = torch.load(model_path, map_location=self.device)
            model.load_state_dict(state_dict, strict=True)

            self.model = model.to(self.device)
            self.model.eval()
            print(f"✅ PyTorch model loaded successfully on {self.device}")
            print(f"✅ Model ready to predict {len(self.class_names)} classes including 'No Disease'")

        except Exception as e:
            print(f"❌ Error loading PyTorch model: {str(e)}")
            import traceback
            traceback.print_exc()
            self.model = None

    def calculate_disease_stage(self, predicted_class, confidence, symptom_start_date):
        """Calculate disease stage based on confidence, time elapsed, and disease-specific factors"""
        try:
            # No stage calculation for "No Disease"
            if predicted_class == "No Disease":
                return {
                    "stage": None,
                    "stage_number": None,
                    "severity": None,
                    "days_elapsed": 0,
                    "weeks_elapsed": 0,
                    "progression_rate": None,
                    "clinical_notes": "No disease detected. Scalp appears healthy."
                }
                
            if not symptom_start_date:
                return {
                    "stage": "Unknown",
                    "stage_number": None,
                    "severity": "Unknown",
                    "days_elapsed": 0,
                    "weeks_elapsed": 0,
                    "progression_rate": "Unknown",
                    "clinical_notes": "Symptom start date not provided."
                }
            
            # Parse the date
            start_date = datetime.strptime(symptom_start_date, '%Y-%m-%d').date()
            today = date.today()
            days_elapsed = (today - start_date).days
            weeks_elapsed = days_elapsed / 7
            
            # Ensure days_elapsed is not negative
            if days_elapsed < 0:
                return {
                    "stage": "Invalid Date",
                    "stage_number": None,
                    "severity": "Error",
                    "days_elapsed": 0,
                    "weeks_elapsed": 0,
                    "progression_rate": "Error",
                    "clinical_notes": "Symptom start date cannot be in the future."
                }
            
            # Disease-specific stage calculation
            stage_info = self._calculate_disease_specific_stage(
                predicted_class, confidence, days_elapsed, weeks_elapsed
            )
            
            return stage_info
                
        except Exception as e:
            print(f"❌ Error calculating stage: {str(e)}")
            return {
                "stage": "Unknown",
                "stage_number": None,
                "severity": "Unknown",
                "days_elapsed": 0,
                "weeks_elapsed": 0,
                "progression_rate": "Unknown",
                "clinical_notes": f"Error calculating stage: {str(e)}"
            }
    
    def _calculate_disease_specific_stage(self, disease, confidence, days, weeks):
        """Calculate stage based on disease-specific progression patterns"""
        
        # Disease-specific progression rates
        fast_progression = ['Head Lice', 'Contact Dermatitis', 'Folliculitis']
        moderate_progression = ['Seborrheic Dermatitis', 'Tinea Capitis', 'Psoriasis']
        slow_progression = ['Alopecia Areata', 'Lichen Planus', 'Telogen Effluvium', 'Male Pattern Baldness']
        
        # Determine stage based on disease type and time
        if disease in fast_progression:
            # Fast progression diseases
            if days <= 3:
                stage_num = 1
                stage_name = "Stage I - Initial Onset"
                severity = "Mild"
                progression = "Rapid"
                notes = f"Early presentation detected. Immediate treatment recommended for optimal outcomes."
            elif days <= 7:
                stage_num = 2
                stage_name = "Stage II - Active Phase"
                severity = "Moderate"
                progression = "Rapid"
                notes = f"Active symptoms progressing. Prompt treatment advised to prevent advancement."
            elif days <= 14:
                stage_num = 3
                stage_name = "Stage III - Established"
                severity = "Moderate to Severe"
                progression = "Rapid"
                notes = f"Established condition requiring intensive treatment protocol."
            else:
                stage_num = 4
                stage_name = "Stage IV - Chronic"
                severity = "Severe"
                progression = "Chronic"
                notes = f"Persistent condition requiring comprehensive long-term management."
                
        elif disease in moderate_progression:
            # Moderate progression diseases
            if days <= 7:
                stage_num = 1
                stage_name = "Stage I - Early Phase"
                severity = "Mild"
                progression = "Moderate"
                notes = f"Early stage with good prognosis. Treatment initiation recommended."
            elif days <= 21:
                stage_num = 2
                stage_name = "Stage II - Progressive Phase"
                severity = "Moderate"
                progression = "Moderate"
                notes = f"Progressive condition. Treatment advised to prevent further advancement."
            elif days <= 60:
                stage_num = 3
                stage_name = "Stage III - Advanced Phase"
                severity = "Moderate to Severe"
                progression = "Moderate"
                notes = f"Advanced presentation requiring consistent treatment regimen."
            else:
                stage_num = 4
                stage_name = "Stage IV - Chronic Phase"
                severity = "Severe"
                progression = "Chronic"
                notes = f"Chronic condition requiring long-term management strategy."
                
        else:  # slow_progression
            # Slow progression diseases
            if days <= 14:
                stage_num = 1
                stage_name = "Stage I - Initial Phase"
                severity = "Mild"
                progression = "Gradual"
                notes = f"Initial stage detected. Early intervention beneficial for best outcomes."
            elif days <= 60:
                stage_num = 2
                stage_name = "Stage II - Developing Phase"
                severity = "Mild to Moderate"
                progression = "Gradual"
                notes = f"Developing condition. Treatment can effectively slow progression."
            elif days <= 180:
                stage_num = 3
                stage_name = "Stage III - Established Phase"
                severity = "Moderate"
                progression = "Gradual"
                notes = f"Well-established condition requiring comprehensive treatment approach."
            else:
                stage_num = 4
                stage_name = "Stage IV - Advanced"
                severity = "Moderate to Severe"
                progression = "Chronic"
                notes = f"Long-standing condition requiring ongoing management and monitoring."
        
        # Adjust based on confidence level
        confidence_note = ""
        if confidence >= 0.95:
            confidence_note = "AI confidence: Very High (≥95%)."
        elif confidence >= 0.85:
            confidence_note = "AI confidence: High (≥85%)."
        elif confidence >= 0.70:
            confidence_note = "AI confidence: Moderate (≥70%)."
        else:
            confidence_note = "AI confidence: Lower (<70%). Clinical verification recommended."
            severity = severity + " (Uncertain)"
        
        return {
            "stage": stage_name,
            "stage_number": stage_num,
            "severity": severity,
            "days_elapsed": days,
            "weeks_elapsed": round(weeks, 1),
            "progression_rate": progression,
            "clinical_notes": f"{notes} {confidence_note}",
            "confidence_level": confidence
        }

    def predict(self, image_file, symptom_start_date=None):
        """Make prediction on uploaded image"""
        if self.model is None:
            return {"error": "Model not loaded", "success": False}

        try:
            # Open and preprocess image
            img = Image.open(image_file).convert("RGB")
            print(f"📸 Image loaded: {img.size}")
            
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            print(f"🔄 Image tensor shape: {img_tensor.shape}")

            # Inference
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probs = torch.nn.functional.softmax(outputs, dim=1)
                conf, pred = torch.max(probs, 1)

            predicted_class = self.class_names[pred.item()]
            confidence = float(conf.item())
            
            print(f"🎯 Prediction: {predicted_class} (confidence: {confidence:.3f})")
            
            # Get top 3 predictions for debugging
            top3_probs, top3_indices = torch.topk(probs, 3)
            print("📊 Top 3 predictions:")
            for i in range(3):
                class_name = self.class_names[top3_indices[0][i].item()]
                prob = top3_probs[0][i].item()
                print(f"   {i+1}. {class_name}: {prob:.3f}")
            
            # Calculate disease stage
            stage_info = self.calculate_disease_stage(predicted_class, confidence, symptom_start_date)
            
            if stage_info and stage_info.get("stage"):
                print(f"📈 Disease stage: {stage_info['stage']} (Severity: {stage_info['severity']})")
                print(f"📊 Stage details: {stage_info['clinical_notes']}")
            else:
                print(f"ℹ️ No stage calculation (predicted: {predicted_class})")

            result = {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "stage_info": stage_info,
                "symptom_start_date": symptom_start_date,
                "success": True
            }
            
            print(f"✅ Prediction successful")
            return result

        except Exception as e:
            print(f"❌ Error during prediction: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": f"Prediction failed: {str(e)}", "success": False}

# Global instance
ml_service = MLModelService()
