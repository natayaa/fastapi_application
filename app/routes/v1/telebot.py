import requests, io
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi import File, UploadFile, Form

from decouple import config

TOKEN_BOT = config("TELEGRAM_BOT_TOKEN")
API_TELE_BOT = "https://api.telegram.org/bot"
chat_id = config("TELEGRAM_CHATID") # -> Target to Chat

tele_bot_client = APIRouter(prefix="/app/handler/v2", tags=["Tele Bot"])\

@tele_bot_client.post("/telebot_hook")
async def telebot_webhook(
    req: Request,
    chat_type: str = Form("sendMessage"),
    message: str = Form(None),
    chat_id: str = Form(None),
    ff: UploadFile = File(None)
):
    if chat_type == "sendDocument" and ff:
        const_ = f"{API_TELE_BOT}{TOKEN_BOT}/sendDocument"
        files = {"document": (ff.filename, await ff.read())}
        payload = {"chat_id": chat_id, "caption": message}
    else:
        const_ = f"{API_TELE_BOT}{TOKEN_BOT}/sendMessage"
        files = None
        payload = {"chat_id": chat_id, "text": message}
    
    res = requests.post(url=const_, files=files, data=payload)
    return {"status_code": res.status_code, "response": res.json()}