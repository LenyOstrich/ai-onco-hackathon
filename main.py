import aiofiles
from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from ai_client import call_agent

app = FastAPI()

AI_AGENT_DOCTOR = os.getenv("YANDEX_DOCTOR_AGENT_ID")
AI_AGENT_PATIENT = os.getenv("YANDEX_PATIENT_AGENT_ID")

@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    mode: str = Form("doctor")):

    content = await file.read()
    history_text = content.decode("utf-8")

    if len(history_text) > 30000:
        raise HTTPException(status_code=400, detail="Text too long")


    agent_id = AI_AGENT_PATIENT if mode == "patient" else AI_AGENT_DOCTOR

    result = await call_agent(history_text, agent_id)

    # сохраняем ответ в файл
    async with aiofiles.open("last_response.txt", "w", encoding="utf-8") as f:
        await f.write(result)

    return {"analysis": result}

app.mount("/", StaticFiles(directory="static", html=True), name="static")