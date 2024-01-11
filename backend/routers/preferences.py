# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from fastapi import APIRouter

router = APIRouter(
    prefix="/prefereces"
)


@router.get("/")
async def list_added_preferences():
    pass


@router.get("/json")
async def list_added_preferences_json():
    pass


@router.post("/")
async def push_preference():
    pass


@router.post("/file")
async def push_preferences_file():
    pass
