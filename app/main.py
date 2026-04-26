from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import clean, extract_body
from app.model import predict_combined, get_top_features
import json 
from datetime import datetime
app = FastAPI(title="Spam Detection API")


class InputText(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Spam Detection API is running"}

@app.post("/predict")
def predict(data: InputText):
    body = extract_body(data.message)

    if not body or not body.strip():
        body = data.message

    cleaned = clean(body)

    prob = predict_combined(cleaned)
    prediction = "Spam" if prob > 0.5 else "Ham"

    signals = get_top_features(cleaned) or ["no strong keywords detected"]

    log_prediction(data.message, prob, prediction)

    return {
        "input": data.message,
        "probability": round(prob, 4),
        "prediction": prediction,
        "risk_level": interpret(prob),
        "top_signals": signals,
        "reason": generate_reason(prediction, signals)
    }
    

    
def interpret(prob):
    if prob > 0.9:
        return "Dangerous"
    elif prob > 0.6:
        return "Suspicious"
    else:
        return "Safe"
    
def generate_reason(prediction, signals):
    if prediction == "Spam":
        return f"Detected suspicious terms like: {', '.join(signals)}"
    else:
        return f"Contains normal/technical content like: {', '.join(signals)}"
    
def log_prediction(input_text, prob, prediction):
    log = {
        "time": str(datetime.now()),
        "input": input_text[:200],  # truncate
        "probability": prob,
        "prediction": prediction
    }

    with open("logs.json", "a") as f:
        f.write(json.dumps(log) + "\n")