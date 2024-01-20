from logging import INFO, basicConfig, getLogger
from os import getenv
from sys import exit

from database.connection import create_database
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from routers.jobs import job_router
from routers.preferences import pref_router
from routers.results import res_router
from routers.schedule import sched_router

basicConfig(level=INFO)
log = getLogger(__name__)

dbloc = getenv("DB_LOCATION")
if dbloc is None:
    log.error("No DB_LOCATION env variable. Don't know where to find db.")
    exit(1)

create_database("schema.dbml")


def openapi_settings():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ClassDivider API Spec",
        version="1.0.0",
        summary="This is the backend API for ClassDivider application.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()

app.include_router(job_router)
app.include_router(sched_router)
app.include_router(pref_router)
app.include_router(res_router)

app.openapi = openapi_settings


@app.get("/")
async def get_base() -> JSONResponse:
    return JSONResponse(
        {
            "detail": [
                {"msg": "This is ClassDivider backend API. It will solve your problem."}
            ]
        }
    )
