#!/usr/bin/env python3
"""
Test AI functionality with Gemini API
"""
import os
import asyncio
from ai_service import AIService, ContentRequest

async def test_ai():
    print("🧪 Testing AI Service with Gemini API...")
    
    try:
        ai_service = AIService()
        
        # Test content generation
        request = ContentRequest(
            prompt="Generate a short welcome message for an AI studio application",
            max_tokens=100
        )
        
        result = await ai_service.generate_content(request)
        
        if "error" in result:
            print(f"❌ AI Error: {result['error']}")
        else:
            print("✅ AI Service Working!")
            print(f"Generated: {result['content'][:150]}...")
            if 'usage' in result:
                print(f"Tokens used: {result['usage']['total_tokens']}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai())