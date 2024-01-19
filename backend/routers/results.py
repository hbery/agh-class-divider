# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from io import BytesIO
from logging import getLogger

from database.reads import select_results
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from pandas import DataFrame

res_router = APIRouter(prefix="/results")

log = getLogger(__name__)


@res_router.get("/{job_id}/schedule")
async def get_results_schedule(job_id: str) -> JSONResponse:
    results = select_results(job_id)
    return JSONResponse(content=results)


@res_router.get("/{job_id}/schedule/file")
async def get_results_schedule_file(job_id: str) -> StreamingResponse:
    results = select_results(job_id)

    all_subjects = set()
    for st_schedule in results:
        all_subjects.update(st_schedule["schedule"].keys())

    dt_flat = []
    for st_schedule in results:
        item = {"STUDENT": st_schedule["student"]}
        for subject in all_subjects:
            item[subject] = st_schedule["schedule"].get(subject, "")

        dt_flat.append(item)

    df = DataFrame(dt_flat)
    csv_content = df.to_csv(index=False, sep=";")
    bytecsv = BytesIO(csv_content.encode())

    return StreamingResponse(
        content=bytecsv,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=subject_group_students.csv"
        },
    )


@res_router.get("/{job_id}/groups")
async def get_results_groups(job_id: str) -> JSONResponse:
    results = select_results(job_id)

    subgr_d = {}
    for item in results:
        student_name = item["student"]
        for subject, group in item["schedule"].items():
            sb_gr = f"{subject}_{group}"
            if sb_gr not in subgr_d:
                subgr_d[sb_gr] = []
            subgr_d[sb_gr].append(student_name)

    result_final = [
        {"subject_group": key, "student": val} for key, val in subgr_d.items()
    ]

    return JSONResponse(content=result_final)


@res_router.get("/{job_id}/groups/file")
async def get_results_groups_file(job_id: str) -> StreamingResponse:
    results = select_results(job_id)

    subgr_d = {}
    for item in results:
        student_name = item["student"]
        for subject, group in item["schedule"].items():
            sb_gr = f"{subject}_{group}"
            if sb_gr not in subgr_d:
                subgr_d[sb_gr] = []
            subgr_d[sb_gr].append(student_name)

    result_final = [
        {"SUBJECT_GROUP": key, "STUDENT": val} for key, val in subgr_d.items()
    ]
    df = (
        DataFrame(result_final)
        .pivot(index=None, columns="subject_group", values="students")
        .fillna("")
    )
    csv_content = df.to_csv(index=False, sep=";")
    bytecsv = BytesIO(csv_content.encode())

    return StreamingResponse(
        content=bytecsv,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=subject_group_students.csv"
        },
    )
