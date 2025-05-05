import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("AI_API_URL")
API_KEY = os.getenv("AI_API_KEY")

async def query_ai(guess, against, persona="default"):
    prompt = f"You're a {persona} game host. Does '{guess}' beat '{against}'? Reply only with YES or NO."
    
    # Format for Gemini API
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 5
        }
    }
    
    params = {"key": API_KEY}
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(API_URL, json=payload, params=params, timeout=10)
            resp.raise_for_status()
            
            # Extract response from Gemini format
            response_data = resp.json()
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                content = response_data["candidates"][0]["content"]["parts"][0]["text"]
                return content.strip().upper()
            return "NO"
    except Exception as e:
        logging.error(f"AI API failed: {e}")
        return "NO"
