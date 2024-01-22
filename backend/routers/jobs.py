# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from logging import getLogger

from database.reads import (
    select_all_jobs,
    select_groups,
    select_job,
    select_model,
    select_students,
)
from database.writes import insert_job, insert_model, insert_results, update_job
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from internal.algorithm import ClassDivider

job_router = APIRouter(prefix="/jobs")

log = getLogger(__name__)


@job_router.get("/")
async def list_jobs() -> JSONResponse:
    jobs = select_all_jobs()
    return JSONResponse(content=jobs)


@job_router.post("/create")
async def create_job() -> JSONResponse:
    jobid = insert_job()
    return JSONResponse(content=dict(job_id=jobid))


@job_router.get("/{job_id}/progress")
async def get_job_progress(job_id: str) -> JSONResponse:
    is_done = select_job(job_id).done
    return JSONResponse(content=dict(done=is_done))


@job_router.post("/{job_id}/prepare")
async def get_prepare_job(job_id: str) -> JSONResponse:
    students = select_students(job_id)
    groups = select_groups(job_id)

    new_model = ClassDivider(students, groups)
    mbytes, chksum = new_model.serialize()
    rows = insert_model(job_id, mbytes, chksum)

    return JSONResponse(content=dict(rows_written=rows))


@job_router.post("/{job_id}/run")
async def run_job(job_id: str) -> JSONResponse:
    model = select_model(job_id)

    status = model.solve()
    if status != 1:
        return JSONResponse(
            content=dict(msg="Cannot solve this problem."), status_code=500
        )

    model.extract_results()
    data = model.get_results()
    data = [(st.sid, gr.gid) for st, gr in data] if isinstance(data, list) else None
    if data is None:
        return JSONResponse(
            content=dict(msg="Something went wrong with data conversion.")
        )

    insert_results(job_id, data)
    uid = update_job(job_id, True)

    return JSONResponse(
        content=dict(msg=f"Job {uid} has finished running and problem is sovled.")
    )
