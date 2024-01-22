#!/usr/bin/env python
# vim: ts=4 : sts=4 : sw=4 : et :

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path
from sys import exit

from requests import Session

BASE_URL = "http://localhost:8000"
BASE_PATH = Path(__file__).parent

# curl -X POST "http://localhost:8000/jobs/create"
# curl -X POST "http://localhost:8000/schedule/file?jobid=${jobid}" --form "file=@data/suite_1/plan1.csv"
# curl -X POST "http://localhost:8000/preferences/file?jobid=${jobid}" --form "file=@data/suite_1/podzial1_1.csv"
# curl -X POST "http://localhost:8000/jobs/${jobid}/prepare"
# curl -X POST "http://localhost:8000/jobs/${jobid}/run"
# curl -X GET  "http://localhost:8000/jobs/${jobid}/progress" [optional]
# curl -X GET  "http://localhost:8000/results/${jobid}/schedule/file"


def parse_args() -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-S", "--test-suite", action="store", default=1, help="choose test suite"
    )
    parser.add_argument(
        "-O",
        "--test-option",
        action="store",
        default=1,
        help="choose test suite option",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print(f"# Base path: {BASE_PATH}")
    print(f"*** Running Suite {args.test_suite}, Option {args.test_option}")

    with Session() as s:
        resp = s.post(f"{BASE_URL}/jobs/create")
        if resp.status_code != 200:
            return 1
        job_id = resp.json()["job_id"]

    schedule_f = {
        "file": open(
            BASE_PATH.joinpath(
                f"data/suite_{args.test_suite}/plan{args.test_suite}.csv"
            ),
            "rb",
        )
    }
    preferences_f = {
        "file": open(
            BASE_PATH.joinpath(
                f"data/suite_{args.test_suite}/podzial{args.test_suite}_{args.test_option}.csv"
            ),
            "rb",
        )
    }

    with Session() as s:
        resp = s.post(f"{BASE_URL}/schedule/file?jobid={job_id}", files=schedule_f)
        if resp.status_code != 200:
            print(f"ERROR: Return is: {resp.status_code} ->", resp.text)
            return 2
        print(f"*** Schedule: rows written = {resp.json()['rows_written']}")

    with Session() as s:
        resp = s.post(
            f"{BASE_URL}/preferences/file?jobid={job_id}", files=preferences_f
        )
        if resp.status_code != 200:
            print(f"ERROR: Return is: {resp.status_code} ->", resp.text)
            return 3
        print(f"*** Preferences: rows written = {resp.json()['rows_written']}")

    with Session() as s:
        resp = s.post(f"{BASE_URL}/jobs/{job_id}/prepare")
        if resp.status_code != 200:
            print(f"ERROR: Return is: {resp.status_code} ->", resp.text)
            return 4
        print("*** Model prepared")

    with Session() as s:
        resp = s.post(f"{BASE_URL}/jobs/{job_id}/run")
        if resp.status_code != 200:
            print(f"ERROR: Return is: {resp.status_code} ->", resp.text)
            return 5
        print("*** Model solved")

    with Session() as s:
        resp = s.get(f"{BASE_URL}/results/{job_id}/schedule/file", stream=True)
        if resp.status_code != 200:
            print(f"ERROR: Return is: {resp.status_code} ->", resp.text)
            return 6
        with open(BASE_PATH.joinpath(f"test-{job_id}.csv"), "wb") as f:
            for chunk in resp.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"==> File written to: {BASE_PATH.joinpath(f'test-{job_id}.csv')}")

    return 0


if __name__ == "__main__":
    exit(main())
