# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from sqlalchemy import BLOB, BOOLEAN, INTEGER, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

DBBase = declarative_base()


class DBJob(DBBase):
    """Table `jobs`

    Attributes:
        id str:   job id
        done bool: what is the progress of the job, is is done or not

    """

    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    done: Mapped[bool] = mapped_column(BOOLEAN)


class DBModel(DBBase):
    """Table `models`

    Attributes:
        id int:             model id
        job_id str:        job id, to which model is assigned to
        model_data bytes:   ClassDivider serialized
        model_checksum str: integrity check for model

    """

    __tablename__ = "models"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    model_data: Mapped[bytes] = mapped_column(BLOB)
    model_checksum: Mapped[str] = mapped_column(TEXT)


class DBStudent(DBBase):
    """Table `students`

    Attributes:
        id int:           student id
        job_id str:      job id, to which student is assigned to
        student_name str: name of the student

    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    student_name: Mapped[str] = mapped_column(TEXT)


class DBStudentsPreference(DBBase):
    """Table `students_preferences`

    Attributes:
        id int:             students preference id
        student_id int:     student id
        subject str:        subject student is enrolled to
        time_slot_pref str: time slot student prefers for the subject

    """

    __tablename__ = "students_preferences"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject: Mapped[str] = mapped_column(TEXT)
    time_slot_pref: Mapped[str] = mapped_column(TEXT)


class DBGroup(DBBase):
    """Table `groups`

    Attributes:
        id int:        group id
        job_id str:   job id group is assigned to
        subject str:   subject name to which the group refers to
        time_slot str: time slot of the group
        capacity int:  capacity of the group

    """

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    subject: Mapped[str] = mapped_column(TEXT)
    time_slot: Mapped[str] = mapped_column(TEXT)
    capacity: Mapped[int] = mapped_column(INTEGER)


class DBResult(DBBase):
    """Table `results`

    Attributes:
        id int:         result id
        job_id str:    job id group is assigned to
        student_id int: student id
        group_id int:   group id

    """

    __tablename__ = "results"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
