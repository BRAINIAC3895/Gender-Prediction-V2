from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/predict")
async def predict(name: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a gender predictor for Indian names."},
                      {"role": "user", "content": f"Predict gender for the Indian name {name}. "
                                                  f"Give confidence % and reasoning."}]
        )
        prediction = response.choices[0].message.content
        return {"name": name, "gender": prediction, "confidence": "85", "reason": "Based on cultural usage"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
