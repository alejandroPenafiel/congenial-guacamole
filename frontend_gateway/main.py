from fastapi import FastAPI, WebSocket
from broadcaster import Broadcast
import asyncio
import redis
import json
from libs.shared_utils.db import query_historical_data

broadcast = Broadcast("redis://redis:6379")
cache = redis.Redis(host='redis', port=6379, db=2)
app = FastAPI(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async with broadcast.subscribe(channel="agent-events") as subscriber:
            async for event in subscriber:
                await websocket.send_text(event.message)
    finally:
        await websocket.close()


@app.get("/api/chart_data")
async def get_chart_data(symbol: str, timeframe: str, start: str, end: str):
    key = f"chart:{symbol}:{timeframe}:{start}:{end}"
    cached = cache.get(key)
    if cached:
        return json.loads(cached)
    data = query_historical_data(symbol, timeframe, start, end)
    cache.set(key, json.dumps(data), ex=60)
    return data
