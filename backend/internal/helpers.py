# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from dateutil import parser

if TYPE_CHECKING:
    from internal.models import Group, Student


def parse_schedule_time(time_str: str) -> tuple[datetime, datetime]:
    day_mapping = {
        "Pon.": "Monday",
        "Wt.": "Tuesday",
        "Sr.": "Wednesday",
        "Czw.": "Thursday",
        "Pt.": "Friday",
        "Sob.": "Saturday",
        "Ndz.": "Sunday",
    }

    day, times = time_str.split(" ")
    english_day = day_mapping.get(day, "Unknown")

    start_time, end_time = times.split("-")
    start_time_full = f"{start_time}:00"
    end_time_full = f"{end_time}:00"

    start_slot = parser.parse(f"{english_day} {start_time_full}")
    end_slot = parser.parse(f"{english_day} {end_time_full}")

    return start_slot, end_slot


def create_weight_matrix(
    students: list[Student],
    groups: list[Group],
    weight_wanted: int = 500,
    weight_unwanted: int = 0,
) -> dict[int, dict[int, int]]:
    weight = {}
    for s in students:
        weight[s.sid] = {}
        for g in groups:
            for g_subject, g_tslot in s.preferences.items():
                # elective subjects are weighted 0 to exclude them from objective
                if g.subject not in s.preferences.keys():
                    weight[s.sid][g.gid] = 0
                    continue

                if g_subject == g.subject:
                    if g_tslot == g.time_slot:
                        weight[s.sid][g.gid] = weight_wanted
                    else:
                        weight[s.sid][g.gid] = weight_unwanted

    return weight
