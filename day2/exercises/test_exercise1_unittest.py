"""1교시 실습: unittest 테스트 추가 (빈칸 채우기)

1. 빈칸(___)을 채웁니다.
2. 이 파일을 tests/ 폴더로 옮깁니다 (파일 이름은 그대로).
3. 실행:  PYTHONPATH=src python -m unittest discover -s tests -p "test_*unittest.py" -v
          또는  python -m pytest -q tests/test_exercise1_unittest.py

힌트: 요구사항은 "만 19~34세, 거주 6개월 이상, 미취업"을 모두 만족하면 대상(True)입니다.
"""

import unittest

from mlqa.preprocess import is_eligible


class TestIsEligibleMore(unittest.TestCase):

    def test_short_residence(self):
        # 거주 기간이 3개월이면 대상이 아니어야 한다.
        # 힌트: 결과가 False인지 확인하는 assert 메서드 이름을 쓰세요.
        self.___(is_eligible(25, 3, False))

    def test_employed(self):
        # 취업 상태이면 대상이 아니어야 한다.
        # 힌트: 세 번째 인자 employed에 어떤 값을 넣어야 할까요?
        self.assertFalse(is_eligible(25, 12, ___))

    def test_string_age_raises(self):
        # 나이가 숫자가 아니면 ValueError가 나야 한다.
        with self.assertRaises(___):
            is_eligible("스물", 12, False)


if __name__ == "__main__":
    unittest.main()
