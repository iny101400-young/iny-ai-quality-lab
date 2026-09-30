"""3교시 실습: ML 코드 테스트 (빈칸 채우기)

1. 빈칸(___)을 채웁니다. 계산은 손으로 먼저 해 보세요.
2. 이 파일을 tests/ 폴더로 옮깁니다.
3. 실행:  python -m pytest -q tests/test_exercise3_ml_checks.py

테스트가 실패하면 결함을 찾은 것입니다! 실패 메시지를 복사해 두세요.
"""

import numpy as np
import pandas as pd
import pytest

from mlqa.evaluate import compute_metrics
from mlqa.preprocess import impute_median


def test_impute_uses_train_median_only():
    """결측 대체값은 학습 데이터로만 계산해야 한다 (1일차 5교시 데이터 누수)."""
    train = pd.DataFrame({"x": [1.0, 2.0, np.nan, 4.0]})
    test = pd.DataFrame({"x": [np.nan, 100.0]})
    _, test_filled, medians = impute_median(train, test, ["x"])

    # 학습 데이터의 값 1, 2, 4의 중앙값은?
    assert medians["x"] == ___
    # 테스트 데이터의 빈칸은 무엇으로 채워져야 하나?
    assert test_filled.loc[0, "x"] == ___


def test_precision_uses_positive_label():
    """정밀도는 악성(0)을 양성 클래스로 계산해야 한다 (1일차 3교시)."""
    y_true = [0, 0, 0, 0, 1, 1, 1, 1]
    y_pred = [0, 0, 0, 1, 1, 1, 0, 0]

    # 정밀도 = (악성이라고 예측했고 실제로 악성인 수) / (악성이라고 예측한 수)
    # 힌트: y_pred에서 0인 칸을 세고, 그중 y_true도 0인 칸을 세세요.
    assert compute_metrics(y_true, y_pred)["precision"] == pytest.approx(___ / ___)
