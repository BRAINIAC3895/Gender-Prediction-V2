from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/predict")
async def predict(name: str = Form(...)):
    try:
        prompt = f"Predict the gender for the name '{name}'. Provide three fields: Gender, Confidence (in %), and Reason."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI gender predictor."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content

        # ✅ Parse response cleanly (very simple format enforcement)
        # Example expected format: Gender: Male | Confidence: 90% | Reason: Culturally a male name
        gender, confidence, reason = "Unknown", "N/A", "Could not determine"
        for line in content.split("\n"):
            if "Gender" in line:
                gender = line.split(":")[-1].strip()
            elif "Confidence" in line:
                confidence = line.split(":")[-1].strip()
            elif "Reason" in line:
                reason = line.split(":")[-1].strip()

        return JSONResponse(content={
            "name": name,
            "gender": gender,
            "confidence": confidence,
            "reason": reason
        })

    except Exception as e:
        return JSONResponse(content={
            "name": name,
            "gender": "Error",
            "confidence": "N/A",
            "reason": str(e)
        })
