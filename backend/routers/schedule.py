# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from dataclasses import asdict
from io import StringIO
from logging import getLogger
from typing import Annotated

from database.reads import select_groups
from database.writes import insert_groups
from fastapi import APIRouter, File
from fastapi.responses import JSONResponse
from internal.parser import create_groups
from numpy import NaN
from pandas import read_csv

sched_router = APIRouter(prefix="/schedule")

log = getLogger(__name__)


@sched_router.get("/")
async def list_added_schedules(job_id: str | None = None) -> JSONResponse:
    groups = select_groups(job_id)
    groups_json = [asdict(g) for g in groups]
    return JSONResponse(content=groups_json)


@sched_router.post("/")
async def push_schedule_line() -> JSONResponse:
    log.warn("Got unimplemented request!")
    return JSONResponse(
        content=dict(detail=list(dict(msg="This endpoint is not implemented"))),
        status_code=501,
    )


@sched_router.post("/file")
async def push_schedule_file(
    file: Annotated[bytes, File()], jobid: str
) -> JSONResponse:
    data = StringIO(file.decode("utf-8"))
    csv_df = (
        read_csv(data, sep=";", lineterminator="\r")
        .replace("\n", "", regex=True)
        .replace("", NaN)
        .dropna(how="all")
    )

    groups = create_groups(csv_df)
    rows = insert_groups(jobid, groups)

    return JSONResponse(content=dict(rows_written=rows))
