from fastapi import FastAPI, Request, BackgroundTasks
from datetime import datetime
import httpx
import asyncio
from models.habit_model import Setting, TickPayload
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

TELEX_WEBHOOK_URL = os.getenv("TELEX_WEBHOOK_URL")
TARGET_URL = os.getenv("TARGET_URL")
TELEX_TICK_URL = os.getenv("TELEX_TICK_URL")

# Integration JSON
@app.get("/integration.json")
async def get_integration_json(request: Request):
    return {
        "data": {
            "date": {"created_at": "2025-02-20", "updated_at": "2025-02-20"},
            "descriptions": {
                "app_name": "habit-tracker",
                "app_description": "daily habit tracker",
                "app_logo": "https://th.bing.com/th/id/OIP.MJ9gcBBotfkUoj5gX7IjyQAAAA?rs=1&pid=ImgDetMain",
                "app_url": TARGET_URL,
                "background_color": "#fff"
            },
            "is_active": True,
            "integration_type": "interval",
            "integration_category": "Monitoring & Logging",
            "key_features": ["stay fit", "stay healthy"],
            "author": "Matt_Dev",
            "settings": [{
             
                {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
              
            }],
            "target_url": TARGET_URL,
            "tick_url": "https://habit-tracker-3aip.onrender.com/tick"
        }
    }

# Background Task for Sending Reminders
async def send_reminder(payload: TickPayload):
    url = "https://habit-api-q7hb.onrender.com/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        habits = response.json()

    names = [item["name"] for item in habits]
    times = [item["event_time"] for item in habits]

    message = "🔄 **Time to track your habits!**\n" + "\n".join([
        f"- {name} at {time} A.M" for name, time in zip(names, times)
    ])
 

    data = {
        "message": message,
        "username": "Habit Tracker",
        "event_name": "Daily Reminder",
        "status": "success"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(payload.return_url, json=data)
        print(response.content)

# Checking Habit Notifications
async def check_activity_notifications():
    url = "https://habit-api-q7hb.onrender.com/"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        habits = response.json()

    current_time = datetime.now().strftime("%H:%M")
    print(current_time)

    for habit in habits:
        habit_time = habit["event_time"][:5]
        if habit_time == current_time:
            await send_notification(habit["name"], habit_time)  # ✅ FIXED: Added await

# Sending Notification
async def send_notification(name, habit_time):
    message = f"⏰ Reminder: It's time for {name} at {habit_time}!"
    data = {
        "message": message,
        "username": "Habit Tracker",
        "event_name": "Habit Reminder",
        "status": "success"
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            TELEX_WEBHOOK_URL, json=data
        )
        

# Scheduling Notifications
async def schedule_notifications():
    while True:
        await check_activity_notifications()
        await asyncio.sleep(60)  # Check every 60 seconds

# Run Scheduled Notifications on Startup
@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(schedule_notifications())  # ✅ FIXED: Use FastAPI's startup event

# Tick Endpoint
@app.post("/tick", status_code=202)
async def handle_tick(payload: TickPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_reminder, payload)
    return {"status": "accepted"}
