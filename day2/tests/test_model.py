"""모델 테스트 (2일차 3교시). 1일차 3~6교시의 기준을 자동으로 확인한다."""

import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import recall_score

from mlqa.evaluate import cross_validate_model
from mlqa.model import POSITIVE_LABEL, build_model

# 성능 기준 (품질 게이트). 팀이 합의해 정하는 값이다.
MIN_CV_RECALL = 0.90
MAX_NOISE_DROP = 0.02


def test_prediction_shape_and_labels(trained_model, data):
    _, X_test, _, _ = data
    pred = trained_model.predict(X_test)
    assert pred.shape == (len(X_test),)
    assert set(np.unique(pred)) <= {0, 1}


def test_beats_baseline(trained_model, data):
    X_train, X_test, y_train, y_test = data
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    assert trained_model.score(X_test, y_test) > baseline.score(X_test, y_test) + 0.1


def test_cv_recall_meets_quality_gate(data):
    X_train, _, y_train, _ = data
    cv = cross_validate_model(build_model(), X_train, y_train)
    assert cv["recall"]["mean"] >= MIN_CV_RECALL, cv["recall"]


def test_invariance_to_row_order(trained_model, data):
    """행 순서를 섞어도 각 샘플의 예측은 같아야 한다 (불변성 테스트)."""
    _, X_test, _, _ = data
    order = np.random.RandomState(0).permutation(len(X_test))
    assert np.array_equal(trained_model.predict(X_test)[order], trained_model.predict(X_test[order]))


def test_robust_to_small_noise(trained_model, data):
    """특성 표준편차의 5% 잡음에서 악성 재현율 하락이 기준 이하여야 한다 (섭동 테스트)."""
    X_train, X_test, _, y_test = data
    rng = np.random.RandomState(0)
    noise = rng.normal(size=X_test.shape) * X_train.std(axis=0) * 0.05
    base = recall_score(y_test, trained_model.predict(X_test), pos_label=POSITIVE_LABEL)
    noisy = recall_score(y_test, trained_model.predict(X_test + noise), pos_label=POSITIVE_LABEL)
    assert base - noisy <= MAX_NOISE_DROP
