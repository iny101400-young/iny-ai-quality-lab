# ai-quality-lab

**AI SW·어플리케이션 품질검증 특강** 실습 자료입니다.

- **1일차 · AI 품질검증의 이해**: 소프트웨어 테스팅 기초, 분류·회귀 모델 평가 지표, 과적합·데이터 편향·강건성, 데이터 품질 관리
- **2일차 · AI 어플리케이션 품질검증 프레임워크 실습**: unittest·PyTest, 교차 검증과 성능 리포트 자동 생성, GitHub Actions CI, 이슈 트래커 버그 리포트 (준비 중)

## 시작하기

1. Google 계정으로 Colab에 로그인합니다.
2. 아래 표의 **열기** 링크로 노트북을 열고, `파일 > Drive에 사본 저장`을 누릅니다.
3. 위에서부터 차례로 실행합니다 (`Shift + Enter`). 필요한 라이브러리는 Colab에 기본으로 들어 있고, 데이터는 다운로드가 필요 없습니다.

## 강의 슬라이드

- [1일차. AI 품질검증의 이해 (PDF)](slides/day1-ai-quality-understanding.pdf)

## 1일차 노트북

| 교시 | 주제 | Colab |
| --- | --- | --- |
| 3교시 | 분류 모델 평가 지표 (혼동 행렬, Accuracy, Precision, Recall, F1) | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day1/notebooks/01_classification_metrics.ipynb) |
| 4교시 | 회귀 모델 평가 지표 (MAE, MSE, RMSE, R²) | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day1/notebooks/02_regression_metrics.ipynb) |
| 5교시 | 과적합과 데이터 누수 | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day1/notebooks/03_overfitting.ipynb) |
| 6교시 | 데이터 편향과 강건성 | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day1/notebooks/04_bias_robustness.ipynb) |
| 7·8교시 | 데이터 품질 검사 | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day1/notebooks/05_data_quality.ipynb) |

**1일차 과제 템플릿**: [데이터 품질 검수 기준서](day1/templates/data-quality-checklist.md)

## 폴더 구성

```text
ai-quality-lab/
├── day1/
│   ├── notebooks/        # 1일차 Colab 노트북 5개
│   └── templates/        # 데이터 품질 검수 기준서 양식
├── day2/                 # 2일차 실습 (준비 중)
├── slides/               # 강의 슬라이드 PDF
└── appendix/
    └── llm-service/      # [부록] 생성형 AI(LLM) 서비스 품질검증 실습
```

## 부록

- [생성형 AI(LLM) 서비스 품질검증 실습](appendix/llm-service/README.md): promptfoo, DeepEval, 레드팀, 예제 챗봇

## 참고 자료

- [scikit-learn: Metrics and scoring](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [scikit-learn: Common pitfalls (데이터 누수)](https://scikit-learn.org/stable/common_pitfalls.html)
- [ISTQB Certified Tester Foundation Level v4.0](https://www.istqb.com/ctfl-v4-0/)
- [신뢰할 수 있는 인공지능 개발 안내서](https://tta-trustworthy-ai.gitbook.io/general) — 과학기술정보통신부·TTA
