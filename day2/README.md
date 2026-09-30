# 2일차 · AI 어플리케이션 품질검증 프레임워크 실습

이 폴더에는 작은 ML 프로젝트(`mlqa` 패키지)가 들어 있습니다. 유방암 진단 데이터로 **악성 종양을 찾는 모델**입니다. 오늘은 이 프로젝트에 **테스트, 교차 검증, 성능 리포트, CI, 버그 리포트**를 붙여 품질을 검증합니다.

> 이 코드에는 **결함이 몇 개 숨어 있습니다.** 제공된 테스트는 모두 통과하고 커버리지도 98%입니다. 테스트를 직접 추가해서 결함을 찾아내는 것이 오늘의 목표입니다.

## 0. 시작하기 (1교시)

1. 이 저장소 오른쪽 위 **Fork**를 눌러 내 계정으로 복사합니다.
2. 내 저장소의 **Actions** 탭에서 워크플로 실행을 허용합니다 ("I understand my workflows, go ahead and enable them").
3. 내 저장소의 **Settings → General → Features**에서 **Issues**를 체크합니다. fork한 저장소는 이슈 기능이 기본으로 꺼져 있습니다.
4. 코드를 읽고 고칠 때는 내 저장소 화면에서 **`.` 키**를 누릅니다 (웹 편집기 github.dev가 열림).
5. 테스트를 미리 돌려 보고 싶으면 Colab에서 [01_testing_in_colab.ipynb](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/01_testing_in_colab.ipynb)를 열고, 첫 셀의 `GITHUB_USER`를 내 아이디로 바꿉니다.

## 폴더 구성

```text
day2/
├── src/mlqa/
│   ├── preprocess.py     # 대상 판정 is_eligible(), 결측 대체 impute_median()
│   ├── data_checks.py    # 결측률, 범위, 범주값, 중복, 분할 누수 검사
│   ├── model.py          # 데이터 불러오기, 분할, 모델(Pipeline)
│   ├── evaluate.py       # 지표 계산, 교차 검증
│   └── report.py         # 성능 리포트 자동 생성
├── tests/                # 제공된 테스트 (unittest 1개 파일 + PyTest)
├── notebooks/            # Colab 노트북
├── reports/              # 리포트 출력 폴더 (자동 생성)
├── requirements.txt
└── pyproject.toml        # pytest 설정 (src 경로)
```

## 교시별 과제

| 교시 | 주제 | 할 일 |
| --- | --- | --- |
| 1 | unittest | `tests/test_preprocess_unittest.py`를 읽고, `TestIsEligible`에 테스트 메서드 2개를 추가한다 (예: 거주 기간 부족, 취업 상태) |
| 2 | PyTest | `tests/test_my_checks.py`를 새로 만들고 `parametrize`로 나이의 **3값 경계값** 테스트를 작성한다. 커버리지를 측정해 본다 |
| 3 | ML 코드 테스트 | 같은 파일에 ① `impute_median()`이 **학습 데이터의 중앙값만** 쓰는지 확인하는 테스트 ② `compute_metrics()`의 정밀도를 **손으로 계산한 값**과 비교하는 테스트를 추가한다 |
| 4 | 교차 검증 | [02_cross_validation.ipynb](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/02_cross_validation.ipynb)로 분할의 흔들림, StratifiedKFold, 평균 ± 표준편차를 확인한다 |
| 5 | 성능 리포트 | 리포트를 생성하고 **숫자가 서로 맞는지** 검토한다. 이상한 점을 메모한다 |
| 6 | CI | 추가한 테스트를 커밋해 Actions에서 **실패**하는 것을 확인한다. 실행 요약에서 리포트를 본다 |
| 7 | 버그 리포트 | 찾은 결함마다 **Issues → New issue → 버그 리포트** 양식으로 이슈를 등록한다. 결함을 고치는 PR을 만들고 본문에 `Fixes #이슈번호`를 적는다. CI가 통과하면 병합해 이슈가 자동으로 닫히는지 확인한다 |
| 8 | 발표 | 찾은 결함, 추가한 테스트, CI 결과, 이슈 링크를 발표한다 |

## 직접 실행하기

```bash
cd day2
pip install -r requirements.txt

python -m pytest -q                                     # 전체 테스트
python -m pytest -q --cov=mlqa --cov-report=term-missing   # 커버리지
PYTHONPATH=src python -m unittest discover -s tests -p "test_*unittest.py"   # unittest만
PYTHONPATH=src python -m mlqa.report                    # 성능 리포트 → reports/
```

## CI (GitHub Actions)

`.github/workflows/day2-ci.yml`이 `day2/` 아래 파일이 바뀔 때마다 실행됩니다.

1. 라이브러리 설치
2. 테스트 + 커버리지 (품질 게이트: 교차 검증 재현율 0.90 이상, 잡음 강건성)
3. 성능 리포트 생성 → 실행 요약(Summary)에 표시, Artifacts로 보관

## 품질 기준 (품질 게이트)

`tests/test_model.py` 위쪽의 상수가 기준입니다. 팀이 합의해 정하는 값입니다.

| 기준 | 값 |
| --- | --- |
| 5겹 교차 검증 재현율(악성) 평균 | 0.90 이상 |
| 특성 표준편차 5% 잡음에서 재현율 하락 | 0.02 이하 |
| 기준선(가장 많은 클래스로 예측) 대비 테스트 정확도 | 0.1 이상 높음 |
