from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def form_post(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, name: str = Form(...)):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a gender prediction assistant."},
                {"role": "user", "content": f"Predict the gender for the name {name}. "
                                            f"Also give confidence % and a short reason."}
            ]
        )
        result = response.choices[0].message["content"].strip()
    except Exception as e:
        result = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "result": result, "name": name})
