# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

import pandas as pd
from internal.models import Group, Student


def create_groups(groups_df: pd.DataFrame) -> list[Group]:
    counter = 1
    groups = []

    for _, row in groups_df.iterrows():
        for header in groups_df:
            if not pd.isna(row[header]) and row[header] != "":
                fields = str(row[header]).split("/")
                groups.append(Group(counter, fields[0], header, int(fields[1])))
            counter = counter + 1

    return groups


def create_students_preferences(
    students_df: pd.DataFrame, student_name_col: str = "IMIĘ I NAZWISKO"
) -> list[Student]:
    counter = 1
    students = []

    students_names = students_df.pop(student_name_col)

    for idx, row in students_df.iterrows():
        pref = {}
        for header in students_df[:-1]:
            if not pd.isna(row[header]):
                pref.update({header: row[header]})
        students.append(Student(counter, str(students_names[idx]), pref))
        counter = counter + 1

    return students
