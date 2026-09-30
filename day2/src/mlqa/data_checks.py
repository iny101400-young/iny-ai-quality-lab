"""데이터 정합성 검사. 1일차 7교시의 검수 기준을 함수로 옮긴 것이다."""

import pandas as pd


def missing_rates(df: pd.DataFrame) -> dict:
    """컬럼별 결측률."""
    return df.isna().mean().round(4).to_dict()


def out_of_range_count(df: pd.DataFrame, ranges: dict) -> dict:
    """컬럼별로 허용 범위 [low, high]를 벗어난 값의 개수. 결측은 세지 않는다."""
    result = {}
    for col, (low, high) in ranges.items():
        values = df[col]
        result[col] = int((values.notna() & ~values.between(low, high)).sum())
    return result


def invalid_category_count(df: pd.DataFrame, column: str, allowed) -> int:
    """허용 목록에 없는 범주값의 개수."""
    return int((~df[column].isin(set(allowed))).sum())


def duplicate_count(df: pd.DataFrame, subset=None) -> int:
    """중복 행의 개수 (첫 번째 행은 중복으로 세지 않음)."""
    return int(df.duplicated(subset=subset).sum())


def split_overlap(train_ids, test_ids) -> set:
    """학습·테스트 세트에 동시에 들어 있는 ID."""
    return set(train_ids) & set(test_ids)
