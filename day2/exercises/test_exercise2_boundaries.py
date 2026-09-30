"""2교시 실습: parametrize로 경계값 테스트 (빈칸 채우기)

1. 빈칸(___)을 채웁니다. 1일차 2교시의 '3값 경계값'을 떠올리세요.
2. 이 파일을 tests/ 폴더로 옮깁니다.
3. 실행:  python -m pytest -q tests/test_exercise2_boundaries.py

테스트가 실패하면 결함을 찾은 것입니다! 실패 메시지를 복사해 두세요 (7교시 이슈 등록에 씁니다).
아직 코드를 고치지는 마세요.
"""

import pytest

from mlqa.preprocess import is_eligible


@pytest.mark.parametrize("age, expected", [
    # 경계 19: 바로 아래, 경계, 바로 위
    (18, ___),
    (19, ___),
    (20, True),
    # 경계 34: 바로 아래, 경계, 바로 위
    (33, True),
    (34, ___),
    (___, False),
])
def test_age_boundaries(age, expected):
    assert is_eligible(age, 12, False) == expected
