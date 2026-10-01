"""2일차 노트북용 도우미 함수.

수강생은 이 파일을 읽거나 고칠 필요가 없습니다. 노트북의 입력 칸과 버튼 뒤에서 실행됩니다.
"""

import csv
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

DAY2 = Path(__file__).resolve().parent.parent
CASES_FILE = DAY2 / "test_cases" / "eligibility_cases.csv"
sys.path.insert(0, str(DAY2 / "src"))

# 테스트 이름을 사람이 읽을 수 있는 설명으로 바꾼다.
FILE_AREAS = {
    "test_case_table": "테스트 케이스 표",
    "test_preprocess": "대상 판정 규칙",
    "test_preprocess_unittest": "대상 판정 규칙",
    "test_data_checks": "데이터 품질 검사",
    "test_evaluate": "지표 계산",
    "test_model": "모델 품질 게이트",
    "test_report": "성능 리포트",
}
TEST_NAMES = {
    "test_prediction_shape_and_labels": "예측 결과의 개수와 라벨이 올바른가",
    "test_beats_baseline": "찍기(기준선)보다 정확도가 0.1 이상 높은가",
    "test_cv_recall_meets_quality_gate": "교차 검증 재현율이 기준 이상인가",
    "test_invariance_to_row_order": "데이터 순서를 바꿔도 예측이 같은가",
    "test_robust_to_small_noise": "작은 잡음에도 재현율이 버티는가",
    "test_report_files_are_created": "리포트 파일 3개가 만들어지는가",
    "test_clean_data_passes_all_checks": "깨끗한 데이터가 검사를 통과하는가",
    "test_checks_find_injected_problems": "일부러 넣은 문제를 검사가 찾는가",
    "test_split_overlap": "학습·테스트 데이터가 겹치지 않는가",
    "test_compute_metrics_accuracy_and_recall": "정확도·재현율 계산이 맞는가",
    "test_cross_validation_returns_summary": "교차 검증 결과가 평균·표준편차로 나오는가",
    "test_is_eligible_rules": "대상 판정 규칙",
    "test_is_eligible_rejects_invalid_age": "잘못된 나이를 거부하는가",
    "test_case": "표의 행",
    "test_typical_eligible": "대표적인 대상자를 대상으로 판정하는가",
    "test_too_old": "나이 초과자를 비대상으로 판정하는가",
    "test_invalid_age_raises": "잘못된 나이를 거부하는가",
    "test_no_missing_left": "결측 대체 후 빈칸이 남지 않는가",
    "test_original_not_modified": "결측 대체가 원본 데이터를 바꾸지 않는가",
}
CLASS_AREAS = {"TestIsEligible": "대상 판정 규칙", "TestImputeMedian": "결측값 대체"}


def _describe(classname, name):
    last = classname.split(".")[-1]
    area = CLASS_AREAS.get(last) or FILE_AREAS.get(last, last)   # unittest는 클래스 이름이 끝에 붙는다
    base, _, param = name.partition("[")
    if "\\u" in param:   # pytest가 한글 id를 \uXXXX로 바꿔 적은 경우 되돌린다
        param = param.encode().decode("unicode_escape")
    desc = TEST_NAMES.get(base, base.replace("test_", "").replace("_", " "))
    if param:
        desc = f"{desc} [{param.rstrip(']')}]"
    return area, desc


def run_tests(targets=("tests",), env=None):
    """테스트를 실행하고 결과를 표로 돌려준다. ✅ 통과, ❌ 실패."""
    xml_path = DAY2 / "reports" / "_results.xml"
    xml_path.parent.mkdir(exist_ok=True)
    run_env = {**os.environ, **{k: str(v) for k, v in (env or {}).items()}}
    subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                    f"--junitxml={xml_path}", *targets],
                   cwd=DAY2, env=run_env, capture_output=True, text=True)
    rows = []
    for case in ET.parse(xml_path).getroot().iter("testcase"):
        area, desc = _describe(case.get("classname", ""), case.get("name", ""))
        problem = case.find("failure")
        if problem is None:
            problem = case.find("error")
        reason = ""
        if problem is not None:
            message = problem.get("message") or ""
            reason = message.split("\n")[0].replace("AssertionError: ", "")[:120]
        rows.append({"영역": area, "확인하는 것": desc,
                     "결과": "❌ 실패" if problem is not None else "✅ 통과",
                     "실패 이유": reason})
    df = pd.DataFrame(rows)
    passed = (df["결과"] == "✅ 통과").sum()
    print(f"전체 {len(df)}개 중 통과 {passed}개, 실패 {len(df) - passed}개")
    return df


def highlight(df):
    """실패한 행을 붉게 표시한다."""
    return df.style.apply(
        lambda r: ["background-color: #fde2e2" if "실패" in str(r["결과"]) else "" for _ in r], axis=1)


def show_cases():
    return pd.read_csv(CASES_FILE, dtype=str)


def add_case(age, months_resident, employed, expected, reason):
    cases = show_cases()
    case_id = f"TC-{len(cases) + 1:02d}"
    with open(CASES_FILE, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([case_id, int(age), int(months_resident), employed, expected, reason])
    print(f"{case_id} 추가: 나이 {age}, 거주 {months_resident}개월, 취업 {employed} → 기대 결과 '{expected}'")


def remove_last_case():
    cases = show_cases()
    if len(cases) <= 4:
        print("처음 제공된 4개 케이스는 지우지 않습니다.")
        return
    cases.iloc[:-1].to_csv(CASES_FILE, index=False, encoding="utf-8")
    print(f"{cases.iloc[-1]['case_id']} 삭제")


def try_service(age, months_resident, employed):
    """판정 서비스를 직접 써 본다 (탐색적 테스트)."""
    from mlqa.preprocess import is_eligible
    try:
        result = "대상" if is_eligible(age, months_resident, employed == "예") else "비대상"
    except ValueError:
        result = "입력 오류 (거부됨)"
    print(f"나이 {age}, 거주 {months_resident}개월, 취업 {employed} → 서비스 판정: {result}")


# 3교시 손 계산 확인용 예제 ---------------------------------------------------

MEDIAN_TRAIN = pd.DataFrame({"나이": [20, 30, 40, None]})
MEDIAN_TEST = pd.DataFrame({"나이": [70, 80, None]})

PRECISION_EXAMPLE = pd.DataFrame({
    "환자": [f"P{i}" for i in range(1, 9)],
    "실제": ["악성", "악성", "악성", "양성", "양성", "양성", "양성", "악성"],
    "AI 예측": ["악성", "악성", "악성", "악성", "악성", "양성", "양성", "양성"],
})


def check_median(my_answer):
    from mlqa.preprocess import impute_median
    _, _, medians = impute_median(MEDIAN_TRAIN, MEDIAN_TEST, ["나이"])
    return _compare("결측 대체값(중앙값)", my_answer, medians["나이"])


def check_precision(my_answer):
    from mlqa.evaluate import compute_metrics
    to_label = {"악성": 0, "양성": 1}
    y_true = PRECISION_EXAMPLE["실제"].map(to_label)
    y_pred = PRECISION_EXAMPLE["AI 예측"].map(to_label)
    return _compare("악성 정밀도", my_answer, compute_metrics(y_true, y_pred)["precision"])


def _compare(what, mine, tool):
    same = abs(float(mine) - float(tool)) < 0.005
    print(f"{what}  내 손 계산: {float(mine):.3f}  /  도구 결과: {float(tool):.3f}")
    print("✅ 같습니다." if same else "❌ 다릅니다. 내 계산이 맞다면 도구에 결함이 있습니다. 버그 리포트 후보!")
    return same


def cv_recall():
    from mlqa.evaluate import cross_validate_model
    from mlqa.model import build_model, load_data, split_data
    X, y = load_data()
    X_train, _, y_train, _ = split_data(X, y)
    return cross_validate_model(build_model(), X_train, y_train)["recall"]
