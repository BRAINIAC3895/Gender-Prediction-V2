from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Initialize OpenAI client
client = OpenAI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=JSONResponse)
async def predict(name: str = Form(...)):
    try:
        prompt = f"Predict the gender for the name '{name}'. Give a confidence % and a one-line reasoning."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.choices[0].message.content.strip()

        # Basic parsing: Expecting "Gender: X | Confidence: Y% | Reason: Z"
        gender, confidence, reason = "Unknown", "N/A", result_text
        if "Gender:" in result_text:
            parts = result_text.split("|")
            gender = parts[0].replace("Gender:", "").strip()
            confidence = parts[1].replace("Confidence:", "").strip() if len(parts) > 1 else "N/A"
            reason = parts[2].replace("Reason:", "").strip() if len(parts) > 2 else result_text

        return {"gender": gender, "confidence": confidence, "reason": reason}

    except Exception as e:
        return {"error": str(e)}
