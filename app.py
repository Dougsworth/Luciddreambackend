from fastapi import FastAPI, HTTPException, Request
from aijson import Flow
import asyncio
import time
from cachetools import TTLCache

app = FastAPI()

# A simple in-memory cache with a TTL (time-to-live)
cache = TTLCache(maxsize=100, ttl=300)  # Cache up to 100 items, each for 5 minutes

async def process_flow(prompt: str):
    # Load and run the AI JSON flow
    flow = Flow.from_file('dream_analysis.ai.yaml')
    flow = flow.set_vars(dream_description=prompt)
    result = await flow.run()

    return result

@app.post("/v1/completions")
async def completions(request: Request):
    try:
        start_time = time.time()
        # Parse the OpenAI-style request
        body = await request.json()
        prompt = body.get("prompt")
        model = body.get("model")

        if not prompt or not model:
            raise HTTPException(status_code=400, detail="Model and prompt are required.")

        # Check if the result is already in the cache
        cache_key = f"{model}:{prompt}"
        if cache_key in cache:
            return {"choices": [{"text": cache[cache_key]}]}

        # Process the flow asynchronously
        result = await process_flow(prompt)

        # Cache the result
        cache[cache_key] = result

        response_time = time.time() - start_time
        print(f"Processed in {response_time} seconds")

        # Return the result
        return {"choices": [{"text": result}]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
