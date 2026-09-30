"""여러 테스트에서 함께 쓰는 fixture."""

import numpy as np
import pandas as pd
import pytest

from mlqa.model import build_model, load_data, split_data


@pytest.fixture(scope="session")
def data():
    """(X_train, X_test, y_train, y_test). 세션 동안 한 번만 만든다."""
    X, y = load_data()
    return split_data(X, y)


@pytest.fixture(scope="session")
def trained_model(data):
    X_train, _, y_train, _ = data
    return build_model().fit(X_train, y_train)


@pytest.fixture
def clean_df():
    """명세를 모두 지키는 작은 데이터."""
    return pd.DataFrame({
        "patient_id": ["P1", "P2", "P3", "P4"],
        "hospital": ["A", "B", "C", "A"],
        "radius": [12.0, 15.5, 20.1, 9.8],
        "label": [1, 0, 0, 1],
    })


@pytest.fixture
def dirty_df(clean_df):
    """결측 1건, 범위 밖 1건, 잘못된 범주 1건, 중복 1건을 섞은 데이터."""
    df = clean_df.copy()
    df.loc[1, "radius"] = np.nan
    df.loc[2, "radius"] = 999.0
    df.loc[3, "hospital"] = "Z"
    return pd.concat([df, df.iloc[[0]]], ignore_index=True)
