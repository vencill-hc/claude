---
name: rag-pipeline
description: Use when building RAG pipelines, vector search systems, document processing for LLMs, digital personas, or knowledge bases. Covers chunking, metadata injection, PDF conversion, image handling, hybrid retrieval, and re-ranking.
---

# RAG Pipeline Engineering

## Core Principle

RAG = Retrieval + Generation. Retrieval finds the relevant chunk; generation crafts the answer. A weak pipeline causes hallucinations, incomplete answers, and lost context.

## Ingestion Optimizations

### 1. Smart Chunking With Overlaps

Never use naive chunking. Overlap boundaries to preserve context.

```python
# Example: 5-sentence overlap
chunk_a_end = 50
chunk_b_start = 45  # Not 51
```

**Why**: Ideas span paragraphs. Overlap prevents context discontinuity.

### 2. Metadata Injection Per Chunk

Every chunk gets:
- 1-2 line LLM-generated micro-summary
- 2-3 distilled keywords

```python
chunk_metadata = {
    "summary": "Discusses async team alignment strategies",
    "keywords": ["remote work", "alignment", "async protocols"],
    "source": "handbook.pdf",
    "page": 23,
    "chunk_index": 12
}
```

**Why**: Enables semantic retrieval. User asks "remote team alignment" even if doc says "asynchronous team alignment protocols."

### 3. PDF to Markdown Conversion

Raw PDFs break structure. Convert to Markdown first:
- Preserve headings hierarchy
- Preserve lists
- Convert tables properly
- Maintain spacing

Tools: `pymupdf`, `pdfplumber`, `unstructured`, `marker-pdf`

### 4. Vision-Led Descriptions for Visual Content

For graphs, charts, complex tables:

```python
if has_visual_content(chunk):
    description = vision_llm.describe(image)
    # "Line chart: revenue $100 -> $150, Jan-March"
    chunk.text += f"\n[Visual: {description}]"
```

**Why**: Vector search is blind to images without this.

## Retrieval Optimizations

### 5. Hybrid Retrieval (Keyword + Vector)

```python
keyword_results = bm25_search(query)      # Catches: product names, codes, abbreviations
vector_results = vector_search(query)      # Catches: concepts, paraphrases, reasoning

final = hybrid_score(keyword_results, vector_results, alpha=0.5)
```

### 6. Multi-Stage Re-ranking

```python
# Stage 1: Fast vector search -> large candidate set (top 50)
candidates = vector_search(query, k=50)

# Stage 2: Re-ranker model -> deep comparison (top 5)
reranked = reranker.score(query, candidates)[:5]
```

Re-rankers: `cross-encoder/ms-marco-MiniLM-L-6-v2`, Cohere Rerank, Jina Reranker

### 7. Context Window Optimization

Before sending to LLM:
- De-duplicate overlapping content
- Remove contradictory chunks
- Merge related sections
- Respect token limits

```python
context = dedupe(chunks)
context = remove_contradictions(context)
context = merge_related(context)
context = truncate_to_limit(context, max_tokens=4000)
```

## Implementation Checklist

- [ ] Overlapping chunk boundaries (5-10 sentence overlap)
- [ ] Metadata injection (summary + keywords per chunk)
- [ ] PDF/doc conversion to structured Markdown
- [ ] Vision descriptions for images/charts/tables
- [ ] Hybrid retrieval (BM25 + vector)
- [ ] Re-ranking stage before LLM
- [ ] Context deduplication and optimization

## Common Libraries

| Purpose | Options |
|---------|---------|
| Vector DB | Pinecone, Weaviate, Qdrant, Chroma, pgvector |
| Embeddings | OpenAI, Cohere, sentence-transformers |
| PDF parsing | pymupdf, pdfplumber, unstructured |
| Re-ranking | cross-encoder, Cohere Rerank |
| Chunking | langchain, llama-index, custom |

## Anti-Patterns

- Naive fixed-size chunking without overlap
- Ignoring visual content in documents
- Pure vector search without keyword fallback
- Sending raw retrieval results without re-ranking
- No metadata = poor semantic matching
