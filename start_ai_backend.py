#!/usr/bin/env python3
"""
Start AI backend with proper process management
"""
import os
import sys
import subprocess
import time
import signal
import atexit

def start_backend():
    """Start the AI backend server"""
    # Kill existing processes
    os.system("pkill -f 'uvicorn.*8000' || true")
    time.sleep(2)
    
    # Environment setup
    env = os.environ.copy()
    api_key = env.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return None
    
    print(f"✅ Starting backend with API key: {api_key[:10]}...")
    
    # Start server
    cmd = [
        sys.executable, '-c',
        '''
import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    prompt: str

@app.get("/health")
async def health():
    return {"status": "healthy", "gemini": True}

@app.post("/api/ai/generate-content")
async def generate_content(request: ContentRequest):
    try:
        response = model.generate_content(request.prompt)
        return {"content": response.text, "success": True}
    except Exception as e:
        return {"content": f"Error: {str(e)}", "success": False}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
        '''
    ]
    
    proc = subprocess.Popen(cmd, env=env)
    
    # Wait for startup
    time.sleep(8)
    
    # Test if running
    try:
        import requests
        resp = requests.get("http://localhost:8000/health", timeout=5)
        if resp.status_code == 200:
            print("✅ Backend running successfully")
            return proc
        else:
            print(f"❌ Backend health check failed: {resp.status_code}")
            return None
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return None

if __name__ == "__main__":
    proc = start_backend()
    if proc:
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()