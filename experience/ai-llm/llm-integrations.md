# Implement AI/LLM Integrations

> **Category:** AI & LLM Engineering
> **Relevant at:** Codixel (automated news classification, financial data extraction, event categorization, conversational features)
> **Related tech docs:** `case/data-pipeline/` neighbor docs (event-driven-pipelines, transcription-pipelines), `case/api/apis-and-communication.md` (Third-Party Integrations §49–56), `case/structures-architecture/backend-systems.md` (Backend Architecture §9–16)

---

## 1. What This Means

Implementing AI/LLM integrations means embedding **large language models** (OpenAI GPT, Anthropic Claude, Google Gemini) into production pipelines to perform tasks that traditional code can't — automated **classification, extraction, categorization, and conversational features** — reliably and at scale.

**Scope:**
- **News/event classification** — categorizing financial events into types (earnings, guidance, M&A, product launches)
- **Financial data extraction** — pulling structured data (revenue, EPS, guidance numbers) from unstructured text/transcripts
- **Event categorization** — tagging and routing events by topic, urgency, and relevance
- **Conversational features** — chat/Q&A over the indexed financial data
- **Multi-provider integration** — OpenAI, Claude, Gemini (choosing per task, with provider abstraction)
- **Production reliability** — prompt engineering, structured output, validation, retries, cost control

**Why it matters:** LLMs add capabilities that deterministic code can't — understanding unstructured financial text, extracting meaning from transcripts, answering natural-language questions. But they're **non-deterministic, expensive, and rate-limited** — production LLM integration is an engineering discipline, not a one-line API call.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Where LLMs fit in the Codixel pipeline:**
```
... transcription → [LLM Classification] → [LLM Extraction] → Publishing
                       │                       │
                  category,               revenue, EPS,
                  urgency, sentiment      guidance numbers
```
- The LLM stages process the **transcript** (from WhisperX) and produce **structured, searchable data** (indexed in Elasticsearch)
- Conversational features run on top — users ask questions, the LLM answers from the indexed data (RAG)

**Real engineering challenges:**
1. **Non-determinism** — the same input can yield different outputs. Production needs **structured output** (JSON schemas) + **validation** + **retries on malformed output**.
2. **Prompt engineering** — the prompt IS the logic. Small wording changes shift accuracy dramatically. Prompts are versioned, tested, and treated like code.
3. **Provider differences** — OpenAI, Claude, Gemini have different APIs, strengths, and pricing. Abstraction prevents lock-in.
4. **Cost control** — token-based pricing means a runaway loop or verbose prompt burns money. Token limits + caching + batching are essential.
5. **Rate limits & latency** — LLM APIs throttle and are slower than DB queries. Queue-based async processing (not blocking the request path).
6. **Hallucination** — for extraction, the model might invent numbers. Validation against the source text + confidence handling.

**The principle:** treat LLM integration like any production dependency — **structured contracts, validation, retries, monitoring, cost limits** — not a magical black box.

---

## 3. How to Implement

### Provider Abstraction — Don't Lock In

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract provider — swap OpenAI/Claude/Gemini without touching pipeline code."""
    @abstractmethod
    async def complete(self, system: str, user: str, response_format: type) -> dict: ...

class OpenAIProvider(LLMProvider):
    async def complete(self, system, user, response_format):
        return await openai.chat.completions.parse(
            model="gpt-4o", messages=[{"role": "system", "content": system},
                                       {"role": "user", "content": user}],
            response_format=response_format,   # structured JSON output
        )

class ClaudeProvider(LLMProvider):
    async def complete(self, system, user, response_format):
        # Claude uses tool_use for structured output
        ...

# The pipeline depends on the abstraction
class Classifier:
    def __init__(self, llm: LLMProvider):
        self.llm = llm
```

### Structured Output — Classification + Extraction

```python
from pydantic import BaseModel, Field

class EventClassification(BaseModel):
    """Structured contract — the LLM must return this shape."""
    category: str = Field(description="earnings | guidance | m_and_a | product | other")
    urgency: str = Field(description="high | medium | low")
    sentiment: str = Field(description="positive | neutral | negative")
    confidence: float = Field(description="0.0 to 1.0")

class FinancialExtraction(BaseModel):
    revenue: float | None = None
    eps: float | None = None
    guidance_range: tuple[float, float] | None = None
    fiscal_period: str | None = None
    currency: str = "USD"

CLASSIFY_PROMPT = """You are a financial event classifier.
Analyze the transcript and classify it. Return ONLY structured JSON.
Be conservative with confidence — if uncertain, set it below 0.7."""

async def classify_event(transcript: str, llm: LLMProvider) -> EventClassification:
    result = await llm.complete(
        system=CLASSIFY_PROMPT, user=transcript,
        response_format=EventClassification,
    )
    return result  # parsed + validated by the schema
```

**Why:** structured output + Pydantic validation means malformed/invalid responses are caught, not silently indexed. Retries on validation failure.

### Validation + Retry on Failure

```python
async def classify_with_retry(transcript: str, llm: LLMProvider, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            classification = await classify_event(transcript, llm)
            # Validate confidence — low confidence → human review queue
            if classification.confidence < 0.6:
                await enqueue_for_human_review(transcript, classification)
            return classification
        except ValidationError as e:
            logger.warning(f"Malformed LLM output (attempt {attempt}): {e}")
            if attempt == max_attempts - 1:
                await move_to_dlq(transcript, f"LLM validation failed: {e}")
                raise
```

### RAG — Conversational Features

```python
async def answer_question(question: str, company: str, es: OpenSearch) -> str:
    """Retrieval-Augmented Generation — answer from indexed data, not model memory."""
    # 1. Retrieve relevant indexed events (NOT the model's training data)
    context = await es.search(index="events", body={
        "query": {"bool": {
            "must": [{"match": {"transcript": question}}],
            "filter": [{"term": {"company": company}}],
        }},
        "size": 5,
    })

    # 2. Ground the LLM in retrieved context — reduces hallucination
    context_text = "\n".join(hit["transcript"][:2000] for hit in context["hits"])
    return await llm.complete(
        system="Answer the question using ONLY the provided context. "
               "If the context doesn't contain the answer, say so.",
        user=f"Context:\n{context_text}\n\nQuestion: {question}",
    )
```

**Why:** RAG grounds the model in your indexed data — answers cite real events, and hallucination drops dramatically vs. asking the model from memory.

### Cost + Rate Limit Control

```python
# Token limits on every call (prevent cost runaway)
await llm.complete(..., max_tokens=500)   # classification doesn't need 4000 tokens

# Cache identical classifications (same transcript hash → same result)
cache_key = f"classify:{hash(transcript)}"
if cached := await redis.get(cache_key):
    return cached

# Batch where possible; queue-based async (don't block the request path)
await sqs.send(ClassifyRequest(event_id=event_id))  # worker processes async
```

### AI/LLM Integration Checklist

- [ ] **Provider abstraction** — OpenAI/Claude/Gemini behind one interface (no lock-in)
- [ ] **Structured output** (JSON schema / Pydantic) — never raw free-text in production
- [ ] **Validation + retry** on malformed/low-confidence output
- [ ] **Prompts versioned** — treated like code, tested across examples
- [ ] **Token limits** on every call — cost control
- [ ] **Caching** — same input shouldn't re-call the LLM
- [ ] **Queue-based async** — LLM calls don't block request paths
- [ ] **RAG for Q&A** — ground answers in indexed data, not model memory
- [ ] **Hallucination guards** — extraction validated against source text
- [ ] **Monitoring** — cost, latency, error rate, confidence distribution
- [ ] **Human review queue** for low-confidence outputs

### Avoid These

- **Raw free-text output in production** — no schema = unparseable, unindexable data
- **No provider abstraction** — every prompt change for one provider is a rewrite
- **Blocking the request on an LLM call** — 5-30s latency; queue it async
- **No token limits** — a verbose prompt + runaway loop burns money
- **Asking the model from memory** — for domain data, use RAG (retrieval), not parametric knowledge
- **No validation** — a hallucinated revenue number indexed as fact is a data-integrity bug
- **Unversioned prompts** — "it worked yesterday" with no way to reproduce or roll back
- **No cost monitoring** — LLM costs scale with usage; silent spend is a real risk
