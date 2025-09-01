from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os

# Initialize
app = FastAPI()

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Mount static folder for CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def predict_gender(request: Request, name: str = Form(...)):
    try:
        # GPT prompt for confidence + reasoning
        prompt = f"""
        You are a gender prediction AI for Indian names.
        Predict the gender of the name "{name}".
        Respond in JSON with keys: gender (Male/Female/Unisex), confidence (0-100), reason.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response.choices[0].message["content"].strip()

        # Try parsing JSON
        import json
        try:
            result = json.loads(raw_text)
        except:
            result = {"gender": "Unknown", "confidence": 0, "reason": raw_text}

    except Exception as e:
        result = {"gender": "Error", "confidence": 0, "reason": str(e)}

    return templates.TemplateResponse("index.html", {"request": request, "result": result, "name": name})
