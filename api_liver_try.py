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
    "https://yourfrontendapp.com",  # Add additional origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LiverData(BaseModel):
    #age: float
    #gender: float
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: float
    alamine_aminotransferase: float
    #aspartate_aminotransferase: float
    #total_protiens: float
    #albumin: float
    #albumin_and_globulin_ratio: float

@app.get("/")
def foobar():
    return {
        "Server is up and Running"
    }

@app.post("/predict")
def predict_liver_disease(data: LiverData):
    '''
    Endpoint for predicting liver disease using the trained model.
    '''
    try:
        # Create a NumPy array from the input data
        input_data = np.array([[ data.total_bilirubin, data.direct_bilirubin,
                                data.alkaline_phosphotase, data.alamine_aminotransferase,
                               ]])

        # Standardize the input data using the previously fitted scaler
        input_data = scaler.transform(input_data)

        # Make prediction using the pre-trained model
        prediction = model.predict_proba(input_data)

        # Check if prediction is not None
        if prediction is not None and prediction[0] is not None:
            # Determine result based on a threshold (e.g., 0.5)
            result = True if prediction[0][1] > 0.5 else False

            # Return the prediction result as a boolean and the predicted probability
            return {
            
            "GilbertsSyndrome": gilberts_syndrome,
            "LiverCholestasis": liver_cholestasis,
            "LiverCirrhosis": liver_cirrhosis,
            }
        else:
            # Handle the case where prediction is None
            return {"LiverDisease": None, "error_message": "Unable to make a prediction for the given input."}

    except Exception as e:
        # Return an error message if an exception occurs
        return {"error_message": f"An error occurred: {str(e)}"}
