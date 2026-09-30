"""데이터 검증 테스트 (2일차 3교시). 1일차 7교시 검수 기준을 코드로 옮긴다."""

from mlqa.data_checks import (duplicate_count, invalid_category_count, missing_rates,
                              out_of_range_count, split_overlap)

RANGES = {"radius": (5, 30)}
HOSPITALS = {"A", "B", "C"}


def test_clean_data_passes_all_checks(clean_df):
    assert max(missing_rates(clean_df).values()) == 0
    assert sum(out_of_range_count(clean_df, RANGES).values()) == 0
    assert invalid_category_count(clean_df, "hospital", HOSPITALS) == 0
    assert duplicate_count(clean_df) == 0


def test_checks_find_injected_problems(dirty_df):
    assert missing_rates(dirty_df)["radius"] == 0.2          # 5행 중 1행
    assert out_of_range_count(dirty_df, RANGES)["radius"] == 1
    assert invalid_category_count(dirty_df, "hospital", HOSPITALS) == 1
    assert duplicate_count(dirty_df) == 1


def test_split_overlap():
    assert split_overlap(["P1", "P2", "P3"], ["P3", "P4"]) == {"P3"}
    assert split_overlap(["P1"], ["P2"]) == set()
