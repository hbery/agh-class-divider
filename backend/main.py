from logging import Logger
from os import getenv
from pathlib import Path
from sys import exit

from database.connection import create_database
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers.jobs import job_router
from routers.preferences import pref_router
from routers.results import res_router
from routers.schedule import sched_router

log = Logger(__file__)

dbloc = getenv("DB_LOCATION")
if dbloc is None:
    log.error("No DB_LOCATION env variable. Don't know where to find db.")
    exit(1)

if not Path(dbloc).exists:
    create_database("schema.dbml")

app = FastAPI()

app.include_router(job_router)
app.include_router(sched_router)
app.include_router(pref_router)
app.include_router(res_router)


@app.get("/")
async def get_base() -> JSONResponse:
    return JSONResponse(
        content=dict(
            detail=list(
                dict(
                    msg="This is ClassDivider backend API. It will solve your problem."
                )
            )
        )
    )
