# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from __future__ import annotations
from typing import TYPE_CHECKING

from pulp import LpProblem

if TYPE_CHECKING:
    from internal.models import Student, Group


def key_has_subject_and_student(
    x: tuple[str, int, int],
    subject: str,
    student: Student
) -> bool:
    sb, _, s = x
    return (sb == subject and student.sid == s)


def show_classes_per_student(
    model: LpProblem,
    students: list[Student],
    groups: list[Group]
) -> None:
    mvars = model.variables()
    for s in students:
        print(f"Classes for student {s.name}:")
        for sb in s.preferences.keys():
            vars_student_sb = list(filter(lambda x: key_has_subject_and_student(x, sb, s), model.group_to_student))
            mvars_sb_g_s = [g.time_slot
                            for v in vars_student_sb
                                for x in mvars
                                  for g in groups
                                      if x.name == model.group_to_student[v].name
                                          if g.gid == v[1]
                                              if x.varValue == 1.0]
            print(f" - {sb}:", *mvars_sb_g_s)
