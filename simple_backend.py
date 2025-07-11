#!/usr/bin/env python3
"""
Simple FastAPI backend for testing Gemini API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize Gemini
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print(f"✅ Gemini API configured with key: {api_key[:10]}...")
else:
    print("❌ GEMINI_API_KEY not found")
    model = None

app = FastAPI(title="AI Studio Simple Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7

@app.get("/health")
async def health():
    return {"status": "healthy", "gemini_configured": model is not None}

@app.post("/api/ai/generate-content")
async def generate_content(request: ContentRequest):
    try:
        if not model:
            return {
                "content": "Gemini API key not configured",
                "success": False,
                "error": "No API key"
            }
        
        # Generate content with Gemini
        response = model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request.max_tokens,
                temperature=request.temperature,
            )
        )
        
        # Handle empty responses
        if not response.parts or not response.text:
            return {
                "content": "Content filtered or empty response. Try a different prompt.",
                "success": True
            }
        
        return {
            "content": response.text,
            "success": True,
            "source": "gemini"
        }
        
    except Exception as e:
        return {
            "content": f"Error generating content: {str(e)}",
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)