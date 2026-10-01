# 2일차 · AI 어플리케이션 품질검증 프레임워크 실습

오늘은 **코드를 직접 고치지 않습니다.** PM으로서 품질검증 도구를 **다루고, 결과를 읽고, 판단하는** 연습을 합니다.

이 폴더에는 작은 AI 서비스(`mlqa` 패키지)가 들어 있습니다. 청년 지원금 대상 판정 규칙과, 유방암 진단 데이터로 **악성 종양을 찾는 모델**입니다.

> 이 서비스에는 **결함이 몇 개 숨어 있습니다.** 개발자가 만든 자동 테스트는 모두 통과합니다. 테스트 케이스를 추가하고, 손 계산과 도구 결과를 비교해서 결함을 찾아내는 것이 오늘의 목표입니다.

## 시작하기

1. Google 계정으로 Colab에 로그인합니다.
2. 아래 표의 노트북을 열고 위에서부터 ▶ 버튼을 누릅니다. 코드는 숨겨져 있고, **오른쪽 입력 칸(슬라이더·목록)만 바꾸면** 됩니다.
3. 7교시 버그 리포트는 [ai-quality-bug-bash](https://github.com/leejaehee1/ai-quality-bug-bash) 저장소에 이슈로 등록합니다. **GitHub 계정**이 필요합니다.

| 노트북 | 교시 | Colab |
| --- | --- | --- |
| 01 코드 없이 테스트 돌려 보기 | 1·2·3·5교시 | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/01_testing_in_colab.ipynb) |
| 02 교차 검증 | 4교시 | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/02_cross_validation.ipynb) |

## 교시별 활동

| 교시 | 주제 | 할 일 |
| --- | --- | --- |
| 1 | 자동 테스트 (unittest·PyTest) | 자동 테스트를 실행하고 결과표(✅/❌)를 읽는다. "모두 통과 = 결함 없음"인지 토론한다 |
| 2 | 테스트 케이스 설계 | 서비스를 직접 써 보고, **테스트 케이스 표**(`test_cases/eligibility_cases.csv`)에 경계값 행을 추가해 결함을 찾는다 |
| 3 | AI 결과 검증 | 작은 예제를 **손으로 계산**해 도구 결과와 비교한다. **품질 게이트** 기준값을 슬라이더로 정해 본다 |
| 4 | 교차 검증 | 노트북 02로 분할의 흔들림, 평균 ± 표준편차를 확인하고 배포 후보 모델을 고른다 |
| 5 | 성능 리포트 | 리포트를 버튼 한 번으로 만들고 숫자가 서로 맞는지 검토한다. [리포트 개선안 양식](templates/report_redesign.md)을 채운다 |
| 6 | CI (GitHub Actions) | 강사 시연: 테스트 케이스 한 줄을 올리면 자동으로 테스트가 돌고 ❌ → 고친 뒤 ✅. [Actions 화면](https://github.com/leejaehee1/ai-quality-lab/actions)을 직접 읽어 본다 |
| 7 | 버그 리포트 | [ai-quality-bug-bash](https://github.com/leejaehee1/ai-quality-bug-bash)에서 화면 결함을 찾고, 오전에 찾은 결함과 함께 이슈로 등록한다 |
| 8 | 발표·정리 | 팀별로 가장 심각한 결함과 이유, 정한 품질 게이트를 발표한다 |

## 폴더 구성

```text
day2/
├── test_cases/
│   └── eligibility_cases.csv  # 테스트 케이스 표 (한 행 = 테스트 하나)
├── templates/
│   └── report_redesign.md     # 5교시 리포트 개선안 양식
├── notebooks/                 # Colab 노트북 (lab_helpers.py는 노트북 도우미)
├── src/mlqa/                  # 서비스 코드 (읽거나 고칠 필요 없음)
├── tests/                     # 개발자가 만든 자동 테스트
├── exercises/                 # [심화·선택] 코드로 테스트를 써 보고 싶은 사람용 빈칸 과제
├── reports/                   # 리포트 출력 폴더 (자동 생성)
├── requirements.txt
└── pyproject.toml
```

## [심화·선택] 코드로 해 보기

Python에 익숙하다면 `exercises/`의 빈칸 과제(unittest, 경계값 parametrize, ML 검사)를 채워 `tests/`로 옮겨 볼 수 있습니다. 빈칸(`___`)을 모두 채운 뒤 옮기세요. 수업 필수 과정은 아닙니다.

## (개발자용) 직접 실행하기

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

저장소 관리자는 Actions 탭 → day2-ml-quality → **Run workflow**에서 품질 게이트 기준값을 입력해 코드 수정 없이 다시 실행할 수 있습니다 (예: 재현율 기준 0.96 → ❌, 0.90 → ✅).

## 품질 기준 (품질 게이트)

`tests/test_model.py` 위쪽의 상수가 기준입니다. 팀이 합의해 정하는 값입니다.

| 기준 | 값 |
| --- | --- |
| 5겹 교차 검증 재현율(악성) 평균 | 0.90 이상 |
| 특성 표준편차 5% 잡음에서 재현율 하락 | 0.02 이하 |
| 기준선(가장 많은 클래스로 예측) 대비 테스트 정확도 | 0.1 이상 높음 |
