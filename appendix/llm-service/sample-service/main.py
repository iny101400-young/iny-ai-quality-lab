"""OO시 청년 도약 지원금 안내 챗봇 (실습용 예제 서비스).

POST /chat  {"message": "..."}  ->  {"answer": "...", "sources": ["..."], "model": "...", "usage": {...}}
"""

import os
import re
from pathlib import Path

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
TOP_K = 2
POLICY_PATH = Path(__file__).resolve().parent.parent / "data" / "policy.md"

SYSTEM_PROMPT = (
    "너는 OO시 청년 도약 지원금 안내 챗봇이다. 친절하게 답한다. "
    "아래 정책 문서를 참고한다.\n\n{context}"
)

app = FastAPI(title="청년 도약 지원금 안내 챗봇")
client = OpenAI()


def load_sections(path: Path) -> list[str]:
    """정책 문서를 '## ' 제목 단위로 나눈다."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## )", text)
    return [p.strip() for p in parts if p.strip().startswith("## ")]


def bigrams(text: str) -> set[str]:
    s = re.sub(r"\s+", "", text)
    return {s[i : i + 2] for i in range(len(s) - 1)}


def retrieve(question: str, sections: list[str], k: int = TOP_K) -> list[str]:
    """글자 2-gram 겹침으로 관련 섹션을 고르는 단순 검색."""
    q = bigrams(question)
    ranked = sorted(sections, key=lambda sec: len(q & bigrams(sec)), reverse=True)
    return ranked[:k]


SECTIONS = load_sections(POLICY_PATH)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL, "sections": len(SECTIONS)}


@app.post("/chat")
def chat(req: ChatRequest):
    sources = retrieve(req.message, SECTIONS)
    res = client.chat.completions.create(
        model=MODEL,
        temperature=0.7,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context="\n\n".join(sources))},
            {"role": "user", "content": req.message},
        ],
    )
    return {
        "answer": res.choices[0].message.content,
        "sources": sources,
        "model": res.model,
        "usage": {
            "prompt_tokens": res.usage.prompt_tokens,
            "completion_tokens": res.usage.completion_tokens,
        },
    }
