# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from hashlib import sha512
from logging import getLogger

from database.connection import get_session
from database.models import (
    DBGroup,
    DBJob,
    DBModel,
    DBResult,
    DBStudent,
    DBStudentsPreference,
)
from internal.algorithm import ClassDivider
from internal.models import Group, Student
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

log = getLogger(__name__)


def select_job(job_id: str) -> DBJob:
    with get_session() as session:
        with session.begin():
            done = session.execute(select(DBJob).where(DBJob.id == job_id)).first()

        if done is None:
            raise NoResultFound(f"Cannot find the job {job_id}")

        return done[0]


def select_all_jobs() -> list[dict[str, str | bool]]:
    with get_session() as session:
        with session.begin():
            jobs = session.execute(select(DBJob)).all()

        if jobs is None:
            raise NoResultFound("No jobs found")

        return [{"job_id": j.DBJob.id, "done": j.DBJob.done} for j in jobs]


def select_students(job_id: str | None = None) -> list[Student]:
    students_final = []

    with get_session() as session:
        stmt = None
        if job_id is None:
            stmt = select(DBStudent)
        else:
            stmt = select(DBStudent).where(DBStudent.job_id == job_id)

        with session.begin():
            students = session.execute(stmt).all()

            if students is None:
                raise NoResultFound(f"Cannot find student records for the job {job_id}")

            for s in students:
                prefs = session.execute(
                    select(DBStudentsPreference).where(
                        DBStudentsPreference.student_id == s.DBStudent.id
                    )
                ).all()

                if prefs is None:
                    raise NoResultFound(
                        "Cannot find preferences for student",
                        f"{s.DBStudent.id},",
                        f"{s.DBStudent.student_name}",
                    )

                students_final.append(
                    Student(
                        sid=s.DBStudent.id,
                        name=s.DBStudent.student_name,
                        preferences={
                            p.DBStudentsPreference.subject: p.DBStudentsPreference.time_slot_pref
                            for p in prefs
                        },
                    )
                )

            return students_final


def select_groups(job_id: str | None = None) -> list[Group]:
    with get_session() as session:
        stmt = None
        if job_id is None:
            stmt = select(DBGroup)
        else:
            stmt = select(DBGroup).where(DBGroup.job_id == job_id)

        with session.begin():
            groups = session.execute(stmt).all()

        if groups is None:
            raise NoResultFound(f"Cannot find group records for the job {job_id}")

        return [
            Group(
                gid=g.DBGroup.id,
                subject=g.DBGroup.subject,
                time_slot=g.DBGroup.time_slot,
                capacity=g.DBGroup.capacity,
            )
            for g in groups
        ]


def select_results(job_id: str) -> list[dict[str, dict[str, str]]]:
    with get_session() as session:
        with session.begin():
            results = session.execute(
                select(DBResult, DBStudent, DBGroup)
                .join(DBStudent, DBStudent.id == DBResult.student_id)
                .join(DBGroup, DBGroup.id == DBResult.group_id)
                .where(DBResult.job_id == job_id)
            ).all()

        if results is None:
            raise NoResultFound(f"Cannot find result records for the job {job_id}")

        results_final = {}
        for res in results:
            if res.DBStudent.student_name not in results_final:
                results_final[res.DBStudent.student_name] = {}

            results_final[res.DBStudent.student_name][
                res.DBGroup.subject
            ] = res.DBGroup.time_slot

        results_final_list = [
            {"student": s, "schedule": d} for s, d in results_final.items()
        ]

        return results_final_list


def select_model(job_id: str) -> ClassDivider:
    with get_session() as session:
        with session.begin():
            model = session.execute(
                select(DBModel).where(DBModel.job_id == job_id)
            ).first()

        if model is None:
            raise NoResultFound(f"Cannot find result records for the job {job_id}")

        students = select_students(job_id)
        groups = select_groups(job_id)

        mbytes = model.DBModel.model_data
        if sha512(mbytes).hexdigest() != model.DBModel.model_checksum:
            raise ValueError("Model data is corrupted")

        return ClassDivider.deserialize(mbytes, students, groups)
