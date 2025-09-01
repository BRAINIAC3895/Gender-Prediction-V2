from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from openai import OpenAI

# Init FastAPI
app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, name: str = Form(...)):
    try:
        # Call GPT for prediction
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a gender prediction engine for Indian names. Reply only 'Male' or 'Female'."},
                {"role": "user", "content": f"What is the likely gender for the Indian name '{name}'?"}
            ],
            max_tokens=5
        )
        result = response.choices[0].message.content.strip()
    except Exception as e:
        result = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "result": result, "name": name})
