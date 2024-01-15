# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from fastapi import APIRouter

router = APIRouter(
    prefix="/results"
)


@router.get("/")
async def get_results():
    pass


@router.get("/json")
async def get_results_in_json():
    pass
