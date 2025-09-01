from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, name: str = Form(...)):
    prompt = f"In the Indian context, the name '{name}' is usually associated with which gender? Respond strictly in JSON with keys: name, gender (Male/Female/Unisex), confidence (0-1), explanation."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = response.choices[0].message.content
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "name": name})
