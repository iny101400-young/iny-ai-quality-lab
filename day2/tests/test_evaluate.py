"""지표 계산과 교차 검증 테스트 (2일차 3·4교시)."""

import pytest

from mlqa.evaluate import compute_metrics, cross_validate_model
from mlqa.model import build_model


def test_compute_metrics_accuracy_and_recall():
    # 0 = 악성(양성 클래스). 실제 악성 4건 중 3건을 찾음, 실제 양성종양 4건은 모두 맞춤
    y_true = [0, 0, 0, 0, 1, 1, 1, 1]
    y_pred = [0, 0, 0, 1, 1, 1, 1, 1]
    m = compute_metrics(y_true, y_pred)
    assert m["accuracy"] == pytest.approx(7 / 8)
    assert m["recall"] == pytest.approx(3 / 4)


def test_cross_validation_returns_summary(data):
    X_train, _, y_train, _ = data
    cv = cross_validate_model(build_model(), X_train, y_train, n_splits=5)
    assert set(cv) == {"accuracy", "precision", "recall", "f1"}
    for summary in cv.values():
        assert len(summary["folds"]) == 5
        assert 0.0 <= summary["mean"] <= 1.0
        assert summary["std"] >= 0.0
