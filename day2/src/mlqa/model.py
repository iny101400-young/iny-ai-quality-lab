"""데이터 불러오기와 모델 만들기."""

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# 유방암 데이터: 0 = malignant(악성), 1 = benign(양성 종양).
# 우리가 찾으려는 양성 클래스(positive)는 악성(0)이다.
POSITIVE_LABEL = 0
RANDOM_STATE = 42


def load_data():
    """(X, y) numpy 배열을 돌려준다."""
    return load_breast_cancer(return_X_y=True)


def split_data(X, y, test_size=0.25):
    """층화 분할. (X_train, X_test, y_train, y_test)"""
    return train_test_split(X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y)


def build_model(C=1.0):
    """스케일링과 로지스틱 회귀를 묶은 Pipeline. 스케일러는 학습 데이터로만 fit된다."""
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=1000))
