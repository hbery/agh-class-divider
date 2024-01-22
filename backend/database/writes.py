# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING
from uuid import uuid4

from database.connection import get_session
from database.models import (
    DBGroup,
    DBJob,
    DBModel,
    DBResult,
    DBStudent,
    DBStudentsPreference,
)
from sqlalchemy import insert, update
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

if TYPE_CHECKING:
    from internal.models import Group, Student

log = getLogger(__name__)


def insert_job() -> str:
    with get_session() as session:
        uuid_id = str(uuid4())
        session.begin()
        try:
            session.execute(insert(DBJob).values(id=uuid_id, done=False))
        except SQLAlchemyError as e:
            log.error(e)
            return ""
        else:
            session.commit()

        return uuid_id


def update_job(job_id: str, is_done: bool) -> bool | None:
    with get_session() as session:
        stmt = (
            update(DBJob)
            .where(DBJob.id == job_id)
            .values(done=is_done)
            .returning(DBJob)
        )
        session.begin()
        try:
            job = session.execute(stmt).first()
        except SQLAlchemyError as e:
            log.error(e)
            return None
        else:
            session.commit()

        if job is None:
            raise NoResultFound(f"Cannot find job records for the job {job_id}")

        return job[0].done


def insert_students(job_id: str, students: list[Student]) -> int:
    counter = 0
    for s in students:
        sdb = DBStudent(job_id=job_id, student_name=s.name)

        with get_session() as session:
            session.begin()
            try:
                session.add(sdb)
            except SQLAlchemyError as e:
                session.rollback()
                log.error(e)
                return counter
            else:
                session.commit()
                counter += 1

            session.refresh(sdb)

        with get_session() as session:
            st_pref = [
                DBStudentsPreference(
                    student_id=sdb.id, subject=sb.replace("-", " "), time_slot_pref=pref
                )
                for sb, pref in s.preferences.items()
            ]

            session.begin()
            try:
                session.add_all(st_pref)
            except SQLAlchemyError as e:
                log.error(e)
                return counter
            else:
                session.commit()
                counter += len(st_pref)

    return counter


def insert_groups(job_id: str, groups: list[Group]) -> int:
    with get_session() as session:
        counter = 0
        groups = [
            DBGroup(
                job_id=job_id,
                subject=g.subject.replace("-", " "),
                time_slot=g.time_slot,
                capacity=g.capacity,
            )
            for g in groups
        ]

        session.begin()
        try:
            session.add_all(groups)
        except SQLAlchemyError as e:
            log.error(e)
            return counter
        else:
            session.commit()
            counter += len(groups)

        return counter


def insert_model(job_id: str, model: bytes, checksum: str) -> int:
    with get_session() as session:
        session.begin()
        try:
            session.add(
                DBModel(job_id=job_id, model_data=model, model_checksum=checksum)
            )
        except SQLAlchemyError as e:
            log.error(e)
            return 0
        else:
            session.commit()
            return 1


def insert_results(job_id: str, results: list[tuple[int, int]]) -> int:
    with get_session() as session:
        counter = 0
        results_db = [
            DBResult(job_id=job_id, student_id=res_s, group_id=res_g)
            for res_s, res_g in results
        ]

        session.begin()
        try:
            session.add_all(results_db)
        except SQLAlchemyError as e:
            log.error(e)
            return counter
        else:
            session.commit()
            counter += len(results_db)

        return counter
