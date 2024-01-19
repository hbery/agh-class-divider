# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from dataclasses import asdict
from io import StringIO
from logging import getLogger
from typing import Annotated

from database.reads import select_students
from database.writes import insert_students
from fastapi import APIRouter, File
from fastapi.responses import JSONResponse
from internal.parser import create_students_preferences
from numpy import NaN
from pandas import read_csv

pref_router = APIRouter(prefix="/preferences")

log = getLogger(__name__)


@pref_router.get("/")
async def list_added_preferences(job_id: str | None = None) -> JSONResponse:
    students = select_students(job_id)
    students_json = [asdict(s) for s in students]
    return JSONResponse(content=students_json)


@pref_router.post("/")
async def push_preference() -> JSONResponse:
    log.warn("Got unimplemented request!")
    return JSONResponse(
        content=dict(detail=list(dict(msg="This endpoint is not implemented"))),
        status_code=501,
    )


@pref_router.post("/file")
async def push_preferences_file(
    file: Annotated[bytes, File()], jobid: str
) -> JSONResponse:
    data = StringIO(file.decode("utf-8"))
    csv_df = (
        read_csv(data, sep=";", lineterminator="\r")
        .replace("\n", "", regex=True)
        .replace("", NaN)
        .dropna(how="all")
    )

    students = create_students_preferences(csv_df)
    rows = insert_students(jobid, students)

    return JSONResponse(content=dict(rows_written=rows))
