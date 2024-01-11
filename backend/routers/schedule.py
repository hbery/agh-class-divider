# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from fastapi import APIRouter

router = APIRouter(
    prefix="/schedule"
)


@router.get("/")
async def list_added_schedules():
    pass


@router.get("/json")
async def list_added_schedules_json():
    pass


@router.post("/create")
async def create_schedule():
    pass


@router.post("/")
async def push_schedule_line():
    pass


@router.post("/csv")
async def push_schedule_csv():
    pass
