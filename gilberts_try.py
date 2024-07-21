import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: float
    albumin: float  # Added albumin field

@app.get("/")
def foobar():
    return {
        "Server is up and Running"
    }

@app.post("/predict")
def predict_liver_disease(data: LiverData):
    '''
    Endpoint for checking liver conditions based on bilirubin levels and albumin.
    '''
    try:
        # Conditions for liver cholestasis
        liver_cholestasis = data.total_bilirubin > 2.0 and data.direct_bilirubin > 0.4
        
        # Conditions for liver cirrhosis
        liver_cirrhosis = data.albumin < 3.5

        # Conditions for Gilbert's syndrome
        gilberts_syndrome = data.total_bilirubin > 0.2 and data.direct_bilirubin > 0.3
        
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
        return {"error_message": f"An error occurred: {str(e)}"}
