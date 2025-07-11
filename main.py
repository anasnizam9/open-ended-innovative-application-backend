from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from database import Base, engine
from routes import auth, ai, dashboard
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Studio API", version="1.0.0")

# Configure CORS for production
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5000")
allowed_origins = [frontend_url, "http://localhost:5000", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Studio API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# For production deployment
def create_app():
    return app
