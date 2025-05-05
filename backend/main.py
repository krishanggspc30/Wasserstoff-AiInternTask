from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import uuid
from backend.core.cache import get_cached_verdict, cache_verdict
from backend.core.ai_client import query_ai
from backend.core.moderation import moderate_text, get_persona_response
from backend.core.game_logic import GameManager
from backend.db.models import get_db, increment_global_count, get_guess_count

app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/static"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("backend/static/index.html")


sessions = {}  # In-memory user sessions


# @app.get("/")
# async def root():
#     return {"Welcome to the Game API!"}

@app.get("/test-ai")
async def test_ai():
    return await query_ai("Paper", "Rock", "default")




@app.post("/sessions", status_code=201)
async def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = GameManager()
    return {"session_id": session_id, "message": "Session created successfully"}



class GuessRequest(BaseModel):
    session_id: str
    guess: str
    persona: str = "default"

@app.post("/guess")
async def make_guess(req: GuessRequest, db=Depends(get_db)):
    session = sessions.get(req.session_id, GameManager())
    if not moderate_text(req.guess):
        raise HTTPException(status_code=400, detail="Inappropriate content")

    last = session.last_guess() or "Rock"
    verdict = await get_cached_verdict(req.guess, last)

    if verdict is None:
        verdict = await query_ai(req.guess, last, req.persona)
        await cache_verdict(req.guess, last, verdict)

    if verdict != "YES":
        return JSONResponse(content={"result": f"❌ Nope! '{req.guess}' doesn't beat '{last}'. Game Over."})

    if not session.add_guess(req.guess):
        return JSONResponse(content={"result": "❌ Duplicate guess. Game Over."})

    await increment_global_count(db, req.guess)
    count = await get_guess_count(db, req.guess)
    sessions[req.session_id] = session

    return FileResponse(content={
        "result": get_persona_response(req.guess, last, count, req.persona),
        "score": session.score(),
        "history": session.history()
    })

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"history": session.history(), "score": session.score()}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)