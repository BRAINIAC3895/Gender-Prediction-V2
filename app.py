from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=JSONResponse)
async def predict(name: str = Form(...)):
    try:
        prompt = f"Predict the gender for the name '{name}'. Give result in JSON with fields: gender, confidence (0-100), reason."
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that predicts gender from names."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content

        import json
        try:
            data = json.loads(reply)
        except:
            data = {
                "gender": "Unknown",
                "confidence": "N/A",
                "reason": reply
            }

        return JSONResponse(content=data)

    except Exception as e:
        return JSONResponse(content={"gender": "Error", "confidence": "N/A", "reason": str(e)})
