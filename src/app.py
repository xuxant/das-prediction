from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from questionairs import Questionairs
import prediction

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://dass-prediction.mixerml.com",
    "https://app.mixerml.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/DASPridict')
def predict_das(questionairs: Questionairs):
    predict = prediction.Pridiction(questionairs)
    labels = predict.predict()
    labels['name'] = questionairs.name
    return labels

@app.get('/')
def main():
    return {"message": "DAS Prediction API"}