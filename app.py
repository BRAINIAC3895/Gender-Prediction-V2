import os, json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# OpenAI client (uses your Render env var OPENAI_API_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class NameIn(BaseModel):
    name: str

@app.get("/", response_class=HTMLResponse)
async def home(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})

@app.post("/predict", response_class=JSONResponse)
async def predict(payload: NameIn):
    name = payload.name.strip()
    if not name:
        return {"gender":"Unknown","confidence":"0","reason":"No name provided."}

    # Ask for STRICT JSON so the frontend never shows 'undefined'
    prompt = (
        f"Predict the gender for the Indian name '{name}'. "
        "Return STRICT JSON with keys exactly: gender (Male/Female/Unisex), "
        "confidence (0-100 number), reason (short sentence). No extra text."
    )

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a precise API. Always return valid JSON."},
                {"role":"user","content": prompt}
            ],
            temperature=0.2
        )
        raw = res.choices[0].message.content.strip()

        # Parse JSON safely; if it fails, fall back gracefully
        data = json.loads(raw)
        gender = str(data.get("gender","Unknown"))
        confidence = str(data.get("confidence","0"))
        reason = str(data.get("reason",""))
        return {"name": name, "gender": gender, "confidence": confidence, "reason": reason}

    except Exception as e:
        return {"name": name, "gender":"Error","confidence":"0","reason": str(e)}
