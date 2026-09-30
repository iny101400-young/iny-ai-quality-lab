"""PyTest 스타일 테스트 (2일차 2교시)."""

import pytest

from mlqa.preprocess import is_eligible


@pytest.mark.parametrize(
    "age, months_resident, employed, expected",
    [
        (25, 12, False, True),    # 모든 조건 충족
        (40, 12, False, False),   # 나이 초과
        (25, 3, False, False),    # 거주 기간 부족
        (25, 12, True, False),    # 취업 상태
    ],
)
def test_is_eligible_rules(age, months_resident, employed, expected):
    assert is_eligible(age, months_resident, employed) == expected


@pytest.mark.parametrize("bad_age", [-1, 121, "스물", None])
def test_is_eligible_rejects_invalid_age(bad_age):
    with pytest.raises(ValueError):
        is_eligible(bad_age, 12, False)
