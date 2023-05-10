from fastapi import FastAPI
import joblib
from questionairs import Questionairs
import prediction

app = FastAPI()

@app.post('/DASPridict')
def predict_das(questionairs: Questionairs):
    predict = prediction.Pridiction(questionairs)
    labels = predict.predict()
    labels['name'] = questionairs.name
    return labels