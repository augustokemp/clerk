# clerk

**An agentic RAG assistant that answers business questions using both company documents and live structured data.**

`clerk` is like a knowledgeable front-desk clerk: when asked a question, it consults the company "manual" (unstructured documents, via Retrieval-Augmented Generation) and, where needed, looks up the "records" (structured order/payment data, via typed tools) - then answers, grounded in real sources and with citations.

> Status: **Phase 1 complete** - a working RAG pipeline (ingestion → semantic retrieval → grounded generation with citations). The agentic layer (function calling over structured data), evaluation harness, and HTTP API are on the roadmap below.

---

## Why this project

Large Language Models, on their own, don't know a company's private or up-to-date data and can hallucinate. `clerk` demonstrates the engineering that makes an LLM reliable in a real product: retrieving the right context, grounding answers in sources, and refusing to answer when the information isn't there.

The emphasis is on **production reliability** - correctness, grounding, and idempotent data pipelines - not just a one-off demo.

## Architecture

```
        ── INGESTION (offline, idempotent) ──
 docs ─► chunk ─► embeddings (Voyage) ─► vectors ─► Postgres + pgvector

        ── QUERY (per request) ──
 question ─► embed (query) ─► similarity search (pgvector <=>) ─► top-k chunks
          ─► prompt augmented with context ─► Claude ─► grounded answer + citations
```

## Tech stack

- **Python 3.12**
- **PostgreSQL + pgvector** - stores both business data and embeddings
- **Voyage AI** (`voyage-3-lite`) - text embeddings (512-dim)
- **Anthropic Claude** - answer generation
- **Docker Compose** - local infrastructure

## Key engineering decisions

- **Semantic retrieval** via cosine distance (`<=>`) over pgvector - finds relevant passages by meaning, not keywords.
- **Grounding / anti-hallucination** - the model is instructed to answer *only* from retrieved context and to say it doesn't know otherwise (verified: out-of-context questions return "I don't have that information").
- **Citations** - every answer reports which source documents it used.
- **Idempotent ingestion** - re-running the pipeline never duplicates data (`TRUNCATE` + reload).
- **Batched embeddings** - all chunks embedded in a single API call (fewer requests, lower cost, respects rate limits).
- **Separation of concerns** - shared clients isolated from scripts; ingestion guarded against import side effects.

## Getting started

### Prerequisites
- Docker + Docker Compose
- Python 3.12
- API keys: [Voyage AI](https://dashboard.voyageai.com/) and [Anthropic](https://console.anthropic.com/)

### Setup
```bash
# 1. Configure environment
cp .env.example .env   # then fill in POSTGRES_*, VOYAGE_API_KEY, ANTHROPIC_API_KEY

# 2. Start Postgres + pgvector
docker compose up -d

# 3. Apply the schema
docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < db/schema.sql

# 4. Python environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # or: fastapi uvicorn "psycopg[binary]" python-dotenv anthropic voyageai pgvector

# 5. Ingest the documents
python app/ingest.py

# 6. Ask a question
python app/ask.py
```

### Example
```
Q: How do I get a refund on a card payment?
A: Credit card reversals appear on your statement within up to 2 billing cycles,
   depending on the card issuer, and the full amount is always refunded.
Sources: refund-policy.md
```

## Project layout
```
clerk/
├── app/
│   ├── clients.py   # shared Postgres + Voyage clients
│   ├── ingest.py    # ingestion pipeline (docs → chunks → embeddings → pgvector)
│   ├── search.py    # semantic retrieval
│   └── ask.py       # retrieval + grounded generation with Claude
├── data/docs/       # sample knowledge base (synthetic)
├── db/schema.sql    # pgvector schema
└── docker-compose.yml
```

## Roadmap

- [ ] **Agentic layer** - typed tools (function calling) so the assistant can query live order/payment data, deciding per question whether to use documents, data, or both.
- [ ] **Evaluation harness** - a golden eval set and metrics (retrieval quality, answer correctness, hallucination rate); compare pure RAG vs. agentic RAG.
- [ ] **HTTP API** - expose `/ask` as a FastAPI endpoint with streaming.
- [ ] **Reliability layer** - tracing/observability, cost & latency tracking, guardrails (prompt-injection, PII), caching, retries.
- [ ] **Tests & CI/CD** - pytest suite and GitHub Actions.

---

*Built as a hands-on study in applied AI / LLM backend engineering.*
