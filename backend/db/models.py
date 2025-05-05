import asyncpg
import os
from fastapi import Depends

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/game_db")
pool = None

async def get_db():
    global pool
    if not pool:
        pool = await asyncpg.create_pool(dsn=DB_URL)
    return pool

async def increment_global_count(db, guess):
    async with db.acquire() as conn:
        await conn.execute("""
        INSERT INTO guesses(word, count)
        VALUES($1, 1)
        ON CONFLICT(word) DO UPDATE SET count = guesses.count + 1
        """, guess.lower())

async def get_guess_count(db, guess):
    async with db.acquire() as conn:
        row = await conn.fetchrow("SELECT count FROM guesses WHERE word=$1", guess.lower())
        return row["count"] if row else 0