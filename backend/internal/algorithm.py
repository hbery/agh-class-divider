# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from __future__ import annotations

from hashlib import sha512
from typing import TYPE_CHECKING

from bson import dumps, loads
from internal.debug import key_has_subject_and_student
from internal.helpers import create_weight_matrix
from pulp import LpBinary, LpMaximize, LpProblem, LpVariable, lpSum
from pulp.apis import COIN_CMD

if TYPE_CHECKING:
    from internal.models import Group, Student


class ClassDivider(object):
    """Model class to solve and return calculated divided schedule.

    Attributes:
        students: list of students that need to be assigned to groups
        groups: list of groups that are taken into consideration in schedule division
        model: PuLP model for solving the problem

        weight_wanted: value that will be assigned to preferred groups by students
        weight_unwanted: value that will be assigned to not preferred groups by students
        time_limit: maximum time solver can spend on solving the problem

        data: divided classed extracted from solved model
        data_beautified: divided classed extracted from solved model (beautified)

    """

    def __init__(
        self,
        students: list[Student],
        groups: list[Group],
        model: LpProblem | None = None,
        *,
        weight_wanted: int = 500,
        weight_unwanted: int = 1,
        time_limit: int = 600,
    ):
        """Constructor.

        Args:
            students: list of students that need to be assigned to groups
            groups: list of groups that are taken into
                    consideration in schedule division
            model: PuLP model for solving the problem [optional]

        Keyword Args:
            weight_wanted: value that will be assigned to preferred groups by students
            weight_unwanted: value that will be assigned
                             to not preferred groups by students
            time_limit: maximum time solver can spend on solving the problem

        """
        self.students = students
        self.groups = groups

        self.weight_wanted = weight_wanted
        self.weight_unwanted = weight_unwanted
        self.time_limit = time_limit

        if model is not None:
            self.model = model
        else:
            self.__create()

    def __repr__(self) -> str:
        """Model representation."""
        return self.model.__repr__()

    def __create(self):
        """Create model from inside attributes."""
        subjects = list(set([g.subject for g in self.groups]))
        time_slots = list(set([g.time_slot for g in self.groups]))

        # model
        model = LpProblem(
            name="Class_Divider_CSAP",
            sense=LpMaximize,
        )

        # helper weights per student preference
        weight = create_weight_matrix(
            self.students,
            self.groups,
            self.weight_wanted,
            self.weight_unwanted,
        )

        # variables
        # x -> group_to_student
        model.group_to_student = LpVariable.dicts(
            "x",
            [(g.subject, g.gid, s.sid) for g in self.groups for s in self.students],
            lowBound=0,
            cat=LpBinary,
        )

        # objective
        model += (
            lpSum(
                model.group_to_student[(g.subject, g.gid, s.sid)] * weight[s.sid][g.gid]
                for s in self.students
                for g in self.groups
            ),
            "obj_students_satisfaction",
        )

        # constraints
        # 1 student in 1 group per subject
        for s in self.students:
            for sb in subjects:
                model += (
                    lpSum(
                        model.group_to_student[(sb, g.gid, s.sid)]
                        for g in self.groups
                        if g.subject == sb
                        if sb in s.preferences.keys()
                    )
                    <= 1,
                    f"con_1gr_per_{sb}_per_student{s.sid}",
                )

        # group capacity
        for g in self.groups:
            model += (
                lpSum(
                    model.group_to_student[(g.subject, g.gid, s.sid)]
                    for s in self.students
                )
                <= g.capacity,
                f"con_gr{g.gid}_capacity",
            )

        # group slots not overlapping
        for s in self.students:
            for ts in time_slots:
                group_list = [
                    model.group_to_student[(g.subject, g.gid, s.sid)]
                    for g in self.groups
                    if g.in_slot(ts)
                ]

                if len(group_list) > 0:
                    model += lpSum(group_list) <= 1, f"con_{ts}_student{s.sid}"

        self.model = model

    def solve(self) -> int:
        """Solve the model."""
        our_solver = COIN_CMD(timeLimit=self.time_limit, msg=False)
        self.model.solve(solver=our_solver)

        return self.model.status

    def extract_results(self):
        """Extract results from solved model.

        Results will be available via ClassDivider().data property.

        """
        data = []

        mvars = self.model.variables()
        mvars_t = {}
        for mv in mvars:
            mvel = [
                el.replace("x_(", "").replace(")", "").replace("'", "")
                for el in mv.name.split(",_")
            ]
            mvars_t[(mvel[0].replace("_", " "), int(mvel[1]), int(mvel[2]))] = mv

        for s in self.students:
            for sb in s.preferences.keys():
                vars_student_sb = list(
                    filter(
                        lambda x: key_has_subject_and_student(x, sb, s),
                        list(mvars_t.keys()),
                    )
                )
                mvars_sb_g_s = [
                    g
                    for v in vars_student_sb
                    for x in mvars
                    for g in self.groups
                    if x.name == mvars_t[v].name
                    if g.gid == v[1]
                    if x.varValue == 1.0
                ]

                data.append((s, mvars_sb_g_s[0]))

        self.data = data

    def extract_results_beautified(self):
        """Extract results from solved model.

        Results will be available via ClassDivider().data_beautified property.

        """
        data = {}

        mvars = self.model.variables()
        mvars_t = {}
        for mv in mvars:
            mvel = [
                el.replace("x_(", "").replace(")", "").replace("'", "")
                for el in mv.name.split(",_")
            ]
            mvars_t[(mvel[0].replace("_", " "), int(mvel[1]), int(mvel[2]))] = mv

        for s in self.students:
            data[s.name] = {}
            for sb in s.preferences.keys():
                vars_student_sb = list(
                    filter(
                        lambda x: key_has_subject_and_student(x, sb, s),
                        list(mvars_t.keys()),
                    )
                )
                mvars_sb_g_s = [
                    g.time_slot
                    for v in vars_student_sb
                    for x in mvars
                    for g in self.groups
                    if x.name == mvars_t[v].name
                    if g.gid == v[1]
                    if x.varValue == 1.0
                ]

                data[s.name][sb] = mvars_sb_g_s[0]

        self.data_beautified = data

    def get_results(self) -> list[tuple[Student, Group]] | None:
        return self.data or None

    def get_results_dict(self) -> dict[Student, dict[str, str]] | None:
        return self.data_beautified or None

    def serialize(self) -> tuple[bytes, str]:
        modeld = dumps(self.model.toDict())
        return modeld, sha512(modeld).hexdigest()

    @classmethod
    def deserialize(cls, data: bytes, students: list[Student], groups: list[Group]):
        model_dict = loads(data)
        _, model = LpProblem.fromDict(model_dict)

        return cls(students, groups, model)
