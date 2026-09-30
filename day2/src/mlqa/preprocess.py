"""전처리 함수."""

import pandas as pd


def is_eligible(age, months_resident, employed):
    """청년 지원 대상인지 판정한다 (1일차 2교시 예제 요구사항).

    - 나이: 만 19세 이상 34세 이하
    - 해당 지역 거주 6개월 이상
    - 미취업 상태
    - 나이가 숫자가 아니거나 0~120 범위 밖이면 ValueError
    """
    if isinstance(age, bool) or not isinstance(age, (int, float)) or not (0 <= age <= 120):
        raise ValueError(f"invalid age: {age!r}")
    if 18 <= age <= 34 and months_resident >= 6 and not employed:
        return True
    return False


def impute_median(train: pd.DataFrame, test: pd.DataFrame, columns):
    """결측값을 중앙값으로 채운다.

    중앙값은 학습 데이터로만 계산해야 한다 (1일차 5교시 데이터 누수).
    반환: (채운 train, 채운 test, 사용한 중앙값 dict)
    """
    combined = pd.concat([train, test])
    medians = {col: combined[col].median() for col in columns}
    train_filled = train.copy()
    test_filled = test.copy()
    for col, value in medians.items():
        train_filled[col] = train_filled[col].fillna(value)
        test_filled[col] = test_filled[col].fillna(value)
    return train_filled, test_filled, medians
