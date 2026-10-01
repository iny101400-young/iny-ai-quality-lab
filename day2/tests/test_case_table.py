"""데이터 기반 테스트 (2일차 2교시).

테스트 케이스는 코드가 아니라 표(day2/test_cases/eligibility_cases.csv)에 적습니다.
표의 한 행이 테스트 하나가 됩니다. 행을 추가하면 테스트가 늘어납니다.
"""

import csv
from pathlib import Path

import pytest

from mlqa.preprocess import is_eligible

CASES_FILE = Path(__file__).resolve().parent.parent / "test_cases" / "eligibility_cases.csv"


def load_cases():
    with open(CASES_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [pytest.param(row, id=row["case_id"]) for row in rows]


@pytest.mark.parametrize("case", load_cases())
def test_case(case):
    age = int(case["age"])
    months = int(case["months_resident"])
    employed = case["employed"].strip() == "예"
    expected = case["expected"].strip() == "대상"
    actual = is_eligible(age, months, employed)
    assert actual == expected, (
        f"{case['case_id']}: 기대 '{case['expected']}', 실제 '{'대상' if actual else '비대상'}' "
        f"(나이 {age}, 거주 {months}개월, 취업 {case['employed']})"
    )
