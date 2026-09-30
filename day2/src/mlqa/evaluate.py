"""지표 계산과 교차 검증."""

import numpy as np
from sklearn.metrics import (accuracy_score, f1_score, make_scorer, precision_score,
                             recall_score)
from sklearn.model_selection import StratifiedKFold, cross_validate

from .model import POSITIVE_LABEL, RANDOM_STATE


def compute_metrics(y_true, y_pred, pos_label=POSITIVE_LABEL) -> dict:
    """정확도, 정밀도, 재현율, F1. 정밀도·재현율·F1은 pos_label을 양성 클래스로 본다."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=pos_label, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=pos_label, zero_division=0),
    }


def cross_validate_model(model, X, y, n_splits=5, pos_label=POSITIVE_LABEL) -> dict:
    """층화 K겹 교차 검증. 지표마다 폴드별 점수, 평균, 표준편차를 돌려준다."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    scoring = {
        "accuracy": "accuracy",
        "precision": make_scorer(precision_score, pos_label=pos_label, zero_division=0),
        "recall": make_scorer(recall_score, pos_label=pos_label, zero_division=0),
        "f1": make_scorer(f1_score, pos_label=pos_label, zero_division=0),
    }
    raw = cross_validate(model, X, y, cv=cv, scoring=scoring)
    summary = {}
    for name in scoring:
        scores = np.asarray(raw[f"test_{name}"])
        summary[name] = {"folds": scores.round(4).tolist(),
                         "mean": float(scores.mean()),
                         "std": float(scores.std())}
    return summary
