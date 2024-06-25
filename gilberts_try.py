import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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

    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: float
    alamine_aminotransferase: float


@app.get("/")
def foobar():
    return {
        "Server is up and Running"
    }

@app.post("/predict")
def predict_liver_disease(data: LiverData):
    '''
    Endpoint for checking Gilbert's syndrome based on bilirubin levels.
    '''
    try:
        # Check for Gilbert's syndrome condition
        gilberts_syndrome = data.total_bilirubin > 0.2 and data.direct_bilirubin > 0.3
        
        if gilberts_syndrome:
            return {
                "GilbertsSyndrome": True,
                "message": "High total and direct bilirubin levels indicate Gilbert's syndrome."
            }
        else:
            return {
                "GilbertsSyndrome": False,
                "message": "Bilirubin levels do not indicate Gilbert's syndrome."
            }
    except Exception as e:
        # Return an error message if an exception occurs
        return {"error_message": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
