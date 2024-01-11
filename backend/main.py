from fastapi import FastAPI

from .routers import jobs, schedule, preferences, results

app = FastAPI()

app.include_router(jobs.router)
app.include_router(schedule.router)
app.include_router(preferences.router)
app.include_router(results.router)

@app.get("/")
async def get_base():
    return {"Hello": "World"}
