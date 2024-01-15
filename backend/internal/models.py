# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from dataclasses import dataclass

from internal.helpers import parse_schedule_time


@dataclass
class Student:
    sid: int
    name: str
    preferences: dict[str, str]


@dataclass
class Group:
    gid: int
    time_slot: str
    subject: str
    capacity: int

    def in_slot(self, time_slot: str) -> bool:
        ts_start, ts_end = parse_schedule_time(time_slot)
        g_start, g_end = parse_schedule_time(self.time_slot)

        return max(ts_start, g_start) < min(ts_end, g_end)
