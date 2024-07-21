import numpy as np
from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
import pickle

app = FastAPI()

# Load the pre-trained model and scaler
model = pickle.load(open('liver_disease_model.pkl', 'rb'))
scaler = pickle.load(open('liver_disease_scaler.pkl', 'rb'))


# Setup CORS
origins = [
    "http://localhost:3000",  # Update this with the actual origin of your frontend
    "https://www.e-hospital.ca",  # Add additional origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LiverData(BaseModel):
    total_bilirubin: float = Field(..., gt=0, description="Total bilirubin level")
    direct_bilirubin: float = Field(..., gt=0, description="Direct bilirubin level")
    alkaline_phosphotase: float = Field(..., gt=0, description="Alkaline phosphatase level")
    albumin: float = Field(..., gt=0, description="Albumin level")  # Added albumin field

@app.get("/")
def read_root():
    return {
        "message": "Server is up and Running"
    }

# Load the pre-trained model
with open("liver_disease_model.pkl", "rb") as model_file:
    model = pickle.load(liver_disease_model.pkl)

@app.post("/predict")
def predict_liver_disease(data: LiverData):
    """
    Endpoint for predicting liver conditions based on bilirubin levels and albumin using an ML model.
    """
    try:
        # Prepare the data for prediction
        input_data = [
            data.total_bilirubin,
            data.direct_bilirubin,
            data.alkaline_phosphotase,
            data.albumin
        ]

        # Make a prediction using the ML model
        prediction = model.predict([input_data])
        
        # Interpret the prediction result
        liver_cholestasis = prediction[0] == 0
        liver_cirrhosis = prediction[0] == 1
        gilberts_syndrome = prediction[0] == 2

        # Prepare the response
        response = {
            "GilbertsSyndrome": gilberts_syndrome,
            "LiverCholestasis": liver_cholestasis,
            "LiverCirrhosis": liver_cirrhosis,
        }

        if gilberts_syndrome:
            response["message"] = "High total and direct bilirubin levels indicate Gilbert's syndrome."
        elif liver_cholestasis:
            response["message"] = "High bilirubin levels indicate liver cholestasis."
        elif liver_cirrhosis:
            response["message"] = "Low albumin levels indicate liver cirrhosis."
        else:
            response["message"] = "Bilirubin and albumin levels do not indicate any specific liver condition."

        return response

    except Exception as e:
        # Return an error message if an exception occurs
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

