# ai-quality-lab

**AI 품질검증 특강** 실습 자료입니다. 이틀 동안 우리 팀 AI 서비스의 품질 기준을 세우고, 직접 검증해서 **품질검증 보고서**와 **출시 판단**까지 만듭니다.

- 1일차: AI 품질검증의 이해 — 품질 요구사항 정의서, 테스트 계획서, 골든셋
- 2일차: AI 어플리케이션 품질검증 프레임워크 실습 — E2E 테스트, 응답 품질 평가, 비기능·보안 테스트, 보고서

## 시작하기

1. Google 계정으로 Colab에 로그인합니다.
2. 강사가 나눠 준 API 키를 Colab 왼쪽 **🔑 보안 비밀** 메뉴에 `OPENAI_API_KEY` 이름으로 등록합니다.
   **키를 코드, 파일, 저장소, 채팅방에 붙여 넣지 않습니다.**
3. 아래 노트북을 열고 위에서부터 차례로 실행합니다. 노트북이 이 저장소를 자동으로 내려받습니다.

| 교시 | 실습 | Colab |
| --- | --- | --- |
| 2일차 2교시 | [실습①] 서비스 E2E 테스트 (promptfoo) | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/01_promptfoo_e2e.ipynb) |
| 2일차 3교시 | [실습②] AI 응답 품질 평가 (DeepEval) | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/02_deepeval_response_quality.ipynb) |
| 2일차 4교시 | [실습③] 응답시간·비용·견고성 | [열기](https://colab.research.google.com/github/leejaehee1/ai-quality-lab/blob/main/day2/notebooks/03_latency_cost_robustness.ipynb) |

## 실습 대상: 두 가지 경로

- **경로 A (팀 서비스)**: 팀 서비스를 HTTP API로 호출할 수 있으면, 노트북의 `SERVICE_URL`과 [`path-a-service`](day2/promptfoo/path-a-service/promptfooconfig.yaml) 설정을 팀 API에 맞게 고칩니다.
- **경로 B (공통 예제)**: 팀 서비스가 없으면 [공통 예제 챗봇](sample-service/)을 씁니다. 정책 문서([`data/policy.md`](data/policy.md))는 **가상의 제도**입니다.

## 폴더 구성

```text
ai-quality-lab/
├── data/policy.md                      # 공통 예제 정책 문서 (가상)
├── day1/templates/
│   ├── quality-requirements.md         # 품질 요구사항 정의서
│   ├── test-plan.md                    # 테스트 계획서
│   └── goldenset.csv                   # 골든셋 예시
├── day2/
│   ├── notebooks/                      # Colab 실습 노트북 3개
│   ├── promptfoo/
│   │   ├── path-a-service/             # 서비스 API E2E 테스트 설정
│   │   └── path-b-sample/              # 모델 + 프롬프트 테스트 설정, prompt_v1.json
│   ├── checklists/                     # 견고성·fallback, 사용성·투명성 점검표
│   ├── redteam/                        # 공격 카드, 결함 보고서 템플릿
│   ├── ci/llm-quality-gate.yml         # GitHub Actions 품질 게이트 예시
│   └── report-template.md              # 품질검증 보고서 템플릿
└── sample-service/                     # 공통 예제 챗봇 (FastAPI)
```

## 결과물을 포트폴리오로

이 저장소를 **fork**해서 팀 설정 파일, 골든셋, 결함 보고서, 품질검증 보고서를 채워 두면, "AI 서비스를 검증할 줄 안다"는 것을 보여 주는 포트폴리오가 됩니다. 종합 프로젝트 저장소에는 [`day2/ci/llm-quality-gate.yml`](day2/ci/llm-quality-gate.yml)을 적용해 보세요.

## 참고 자료

- [promptfoo 문서](https://www.promptfoo.dev/docs/intro/) · [DeepEval 문서](https://deepeval.com/docs/getting-started) · [RAGAS 문서](https://docs.ragas.io/) · [Langfuse 문서](https://langfuse.com/docs)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [신뢰할 수 있는 인공지능 개발 안내서](https://tta-trustworthy-ai.gitbook.io/general) — 과학기술정보통신부·TTA
- [인공지능 발전과 신뢰 기반 조성 등에 관한 기본법](https://www.law.go.kr/lsInfoP.do?lsiSeq=268543) — 국가법령정보센터
