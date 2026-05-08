# RAG Pipeline Skill

Expert knowledge for building production-quality Retrieval-Augmented Generation (RAG) systems.

## When to Use

Trigger this skill when:
- Building RAG pipelines or vector search systems
- Processing documents for LLM consumption
- Creating digital personas or knowledge bases
- Optimizing retrieval quality and reducing hallucinations

## What It Covers

### Ingestion Optimizations
- **Smart chunking** with overlapping boundaries (5-10 sentence overlap)
- **Metadata injection** per chunk (summaries, keywords, source info)
- **PDF to Markdown** conversion preserving structure
- **Vision-led descriptions** for images, charts, and tables

### Retrieval Optimizations
- **Hybrid retrieval** combining keyword (BM25) and vector search
- **Multi-stage re-ranking** for precision
- **Context window optimization** (deduplication, contradiction removal)

## Key Concepts

### The Core Principle
RAG = Retrieval + Generation. Retrieval finds the relevant chunk; generation crafts the answer. A weak pipeline causes hallucinations, incomplete answers, and lost context.

### Why Overlapping Chunks?
Ideas span paragraphs. Naive chunking breaks context. Overlap boundaries preserve meaning.

### Why Metadata Injection?
Enables semantic retrieval. User asks "remote team alignment" even if the document says "asynchronous team alignment protocols."

### Why Hybrid Retrieval?
- **Keyword search** catches: product names, codes, abbreviations
- **Vector search** catches: concepts, paraphrases, reasoning
- Combined = better recall

## Common Libraries

| Purpose | Options |
|---------|---------|
| Vector DB | Pinecone, Weaviate, Qdrant, Chroma, pgvector |
| Embeddings | OpenAI, Cohere, sentence-transformers |
| PDF parsing | pymupdf, pdfplumber, unstructured, marker-pdf |
| Re-ranking | cross-encoder, Cohere Rerank, Jina Reranker |
| Chunking | langchain, llama-index, custom |

## Anti-Patterns to Avoid

- Naive fixed-size chunking without overlap
- Ignoring visual content in documents
- Pure vector search without keyword fallback
- Sending raw retrieval results without re-ranking
- No metadata = poor semantic matching

## Usage

Copy the `SKILL.md` file to your project's `.claude/skills/rag-pipeline/` directory, or reference this skill from your Claude Code configuration.
