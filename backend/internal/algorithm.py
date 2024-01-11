# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from __future__ import annotations
from typing import TYPE_CHECKING

from pulp import LpProblem, LpVariable, LpBinary, LpMaximize, lpSum
from pulp.apis import COIN_CMD

from internal.helpers import create_weight_matrix

if TYPE_CHECKING:
    from internal.models import Student, Group


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
    """

    def __init__(self,
                 students: list[Student],
                 groups: list[Group],
                 weight_wanted: int = 500,
                 weight_unwanted: int = 1,
                 time_limit: int = 600):
        """Constructor

        Args:
            students: list of students that need to be assigned to groups
            groups: list of groups that are taken into consideration in schedule division
            weight_wanted: value that will be assigned to preferred groups by students
            weight_unwanted: value that will be assigned to not preferred groups by students
            time_limit: maximum time solver can spend on solving the problem

        """
        self.students = students
        self.groups = groups

        self.weight_wanted = weight_wanted
        self.weight_unwanted = weight_unwanted
        self.time_limit = time_limit

        self.__create()


    def __repr__(self) -> str:
        """Model representation."""
        return self.model.__repr__()


    def __create(self):
        """Create model from inside attributes."""
        subjects = list(set([g.subject for g in self.groups]))
        time_slots = list(set([g.time_slot for g in self.groups]))

        ## model
        model = LpProblem(
            name  = "Class_Divider_CSAP",
            sense = LpMaximize,
        )

        # helper weights per student preference
        model.weight = create_weight_matrix(
            self.students,
            self.groups,
            self.weight_wanted,
            self.weight_unwanted,
        )

        ## variables
        # x -> group_to_student
        model.group_to_student = LpVariable.dicts(
            "x",
            [
                (g.subject, g.gid, s.sid)
                for g in self.groups
                    for s in self.students
            ],
            lowBound = 0,
            cat = LpBinary,
        )

        ## objective
        model.students_satisfaction = lpSum(
                model.group_to_student[(g.subject, g.gid, s.sid)] * model.weight[s.sid][g.gid]
                for s in self.students
                    for g in self.groups
            )
        model += model.students_satisfaction, 'obj_students_satisfaction'

        ## constraints
        # 1 student in 1 group per subject
        for s in self.students:
            for sb in subjects:
                model += lpSum(
                    model.group_to_student[(sb, g.gid, s.sid)]
                    for g in self.groups
                        if g.subject == sb
                            if sb in s.preferences.keys()
                ) <= 1, f'con_1gr_per_{sb}_per_student{s.sid}'

        # group capacity
        for g in self.groups:
            model += lpSum(
                model.group_to_student[(g.subject, g.gid, s.sid)]
                for s in self.students
            ) <= g.capacity, f'con_gr{g.gid}_capacity'

        # group slots not overlapping
        for s in self.students:
            for ts in time_slots:
                group_list = [
                    model.group_to_student[(g.subject, g.gid, s.sid)]
                    for g in self.groups
                        if g.in_slot(ts)
                ]

                if len(group_list) > 0:
                    model += lpSum( group_list ) <= 1, f'con_{ts}_student{s.sid}'

        self.model = model


    def solve(self) -> int:
        """Solve the model."""
        our_solver = COIN_CMD(timeLimit=self.time_limit, msg=False)
        self.model.solve(solver = our_solver)

        return self.model.status


    def extract_results(self) -> None:
        """Extract results from solved model.

        Results will be available via ClassDivider().data property.

        """
        data = {}

        def key_has_subject_and_student(
            x: tuple[str, int, int],
            subject: str,
            student: Student
        ) -> bool:
            sb, _, s = x
            return (sb == subject and student.sid == s)

        mvars = self.model.variables()
        for s in self.students:
            data[s] = {}
            for sb in s.preferences.keys():
                vars_student_sb = list(filter(lambda x: key_has_subject_and_student(x, sb, s), self.model.group_to_student))
                mvars_sb_g_s = [g.time_slot
                                for v in vars_student_sb
                                for x in mvars
                                for g in self.groups
                                if x.name == self.model.group_to_student[v].name
                                if g.gid == v[1]
                                if x.varValue == 1.0]

                data[s][sb] = mvars_sb_g_s[0]

        self.data = data
