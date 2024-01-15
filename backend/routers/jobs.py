# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from fastapi import APIRouter
from io import StringIO
from csv import DictWriter

router = APIRouter(
    prefix="/jobs"
)


@router.get("/")
async def list_jobs():
    pass


@router.get("/{job_id}/progress")
async def get_job_progress(job_id):
    pass


@router.post("/create")
async def create_job():
    pass


@router.post("/")
async def run_job():
    pass
