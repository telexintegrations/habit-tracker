from fastapi import FastAPI, Request, BackgroundTasks
from typing import List
import httpx
import asyncio
from models.habit_model import Setting,TickPayload
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


# --------------- Integration JSON ---------------
@app.get("/integration.json")
async def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
  "data": {
    "date": {
      "created_at": "2025-02-20",
      "updated_at": "2025-02-20"
    },
    "descriptions": {
      "app_name": "habit-tracker",
      "app_description": "daily habit tracker",
      "app_logo": "https://th.bing.com/th/id/OIP.MJ9gcBBotfkUoj5gX7IjyQAAAA?rs=1&pid=ImgDetMain",
      "app_url": "https://live-lens.onrender.com",
      "background_color": "#fff"
    },
    "is_active": True,
    "integration_type": "interval",
    "integration_category": "Monitoring & Logging",
    "key_features": [
      "stay fit",
      "stay healthy"
    ],
    "author": "Matt_Dev",
    "settings": [
      {
        "label": "interval",
        "type": "dropdown",
        "required": True,
        "default": "Daily",
        "options": [
          "Daily",
          "Weekly",
          "Monthly"
        ]
      }
    ],
    "target_url": "https://ping.telex.im/v1/webhooks/01951a74-d144-781a-9c09-2368481d70a7",
    "tick_url": "https://health-predictor.onrender.com"
  }
}

# --------------- Background Task ---------------
async def send_reminder(payload: TickPayload):
    url = "https://habit-api.vercel.app/"
    response = requests.get(url)
    habits = response.json()
    names = [item["name"] for item in habits]
    times = [item["event_time"] for item in habits]
    
    
   
  
  
    
    # message = "🔄 **Time to track your habits!**\n" + "\n".join([f"- {habit}" for habit in habits ])
    message = "🔄 **Time to track your habits!**\n" + "\n".join([f"- {name} at {time}" for name, time in zip(names, times)])
    data = {
        "message": message,
        "username": "Habit Tracker",
        "event_name": "Daily Reminder",
        "status": "success"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(payload.return_url, json=data)
        print(response.content)

# --------------- Tick Endpoint ---------------
@app.post("/tick", status_code=202)
async def handle_tick(payload: TickPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_reminder, payload)
    return {"status": "accepted"}