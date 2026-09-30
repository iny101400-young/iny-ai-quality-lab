# 공통 예제 서비스: OO시 청년 도약 지원금 안내 챗봇

팀 서비스 API가 없는 조가 경로 A(E2E 테스트)와 비기능 테스트를 해 볼 수 있는 실습용 서비스입니다.
정책 문서([`data/policy.md`](../data/policy.md))는 **가상의 제도**이며 실제 정책과 관계없습니다.

## 구조

```text
질문 ─▶ 검색 (정책 문서 섹션 중 관련 높은 2개) ─▶ 프롬프트 조립 ─▶ LLM ─▶ 답변 + 근거 섹션
```

## 실행 (로컬)

```bash
cd sample-service
pip install -r requirements.txt
export OPENAI_API_KEY=...        # 강사가 배포한 키. 파일에 저장하지 않습니다.
uvicorn main:app --port 8000
```

## 실행 (Colab)

```python
!pip install -q fastapi uvicorn openai
%cd /content/ai-quality-lab/sample-service
!nohup uvicorn main:app --port 8000 > server.log 2>&1 &
```

같은 Colab 런타임 안에서 `http://localhost:8000`으로 호출할 수 있습니다.

## API

```bash
curl -s http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "얼마씩 몇 달 줘?"}'
```

```json
{
  "answer": "...",
  "sources": ["## 3. 지원 내용 ..."],
  "model": "gpt-4.1-mini",
  "usage": {"prompt_tokens": 312, "completion_tokens": 85}
}
```

- 모델 변경: 환경 변수 `CHAT_MODEL`
- 상태 확인: `GET /health`
