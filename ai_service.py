import google.generativeai as genai
from config import settings
from typing import Dict, Any, Optional
from pydantic import BaseModel
import os

# Initialize Gemini client
genai.configure(api_key=settings.gemini_api_key)

class ContentRequest(BaseModel):
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7

class AnalysisRequest(BaseModel):
    data: str
    analysis_type: str = "general"

class RecommendationRequest(BaseModel):
    context: str
    user_data: Dict[str, Any] = {}

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_content(self, request: ContentRequest) -> Dict[str, Any]:
        """Generate content using Gemini AI"""
        try:
            response = self.model.generate_content(
                request.prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=request.max_tokens,
                    temperature=request.temperature,
                )
            )
            
            # Handle safety filters and empty responses
            if not response.parts or not response.text:
                return {
                    "content": "Content could not be generated due to safety filters. Please try a different prompt.",
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                }
            
            return {
                "content": response.text,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                    "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                }
            }
        except Exception as e:
            return {
                "content": f"AI generation temporarily unavailable: {str(e)}",
                "error": str(e)
            }

    async def analyze_data(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Analyze data using Gemini AI"""
        try:
            prompt = f"""
            Analyze the following data and provide insights based on the analysis type: {request.analysis_type}
            
            Data: {request.data}
            
            Please provide:
            1. Key insights
            2. Trends or patterns
            3. Recommendations
            4. Summary
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=800,
                    temperature=0.3,
                )
            )
            
            return {
                "analysis": response.text,
                "analysis_type": request.analysis_type,
                "data_summary": request.data[:200] + "..." if len(request.data) > 200 else request.data
            }
        except Exception as e:
            return {"error": str(e), "analysis": None}

    async def get_recommendations(self, request: RecommendationRequest) -> Dict[str, Any]:
        """Get personalized recommendations using Gemini AI"""
        try:
            prompt = f"""
            Based on the following context and user data, provide personalized recommendations:
            
            Context: {request.context}
            User Data: {request.user_data}
            
            Please provide:
            1. Top 3 recommendations
            2. Reasoning for each recommendation
            3. Expected benefits
            4. Implementation steps
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=600,
                    temperature=0.4,
                )
            )
            
            return {
                "recommendations": response.text,
                "context": request.context,
                "personalization_data": request.user_data
            }
        except Exception as e:
            return {"error": str(e), "recommendations": None}

# Create a global instance of AIService
ai_service = AIService()