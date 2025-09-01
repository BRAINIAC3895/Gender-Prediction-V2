import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI

# Initialize app and OpenAI client
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Setup templates and static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, name: str = Form(...)):
    try:
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a gender prediction assistant."},
                {"role": "user", "content": f"Predict the gender for the name {name}. Include confidence % and reasoning."}
            ]
        )

        result = response.choices[0].message.content.strip()
    except Exception as e:
        result = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "result": result, "name": name})
