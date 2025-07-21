# Deliverables Checklist

- [x] 1. Reproducible dev environment + README  
- [x] 2. Pluggable ingestion for JSON/text in `training_data/` with nightly incorporation  
- [x] 3.1 Nightly knowledge refresh (re-embed) 
- [ ] 3.2 LoRA/fine‑tune hook stub 
- [x] 4. Hybrid retrieval (semantic + keyword) with metadata filters  
- [x] 5. Redis‑backed conversation memory (short + long‑term summaries)  
- [x] 6. Benchmark script + Markdown report (similarity, latency, hallucination)  
- [x] 7. DOCX report endpoint (`POST /api/user/report/generate`) & download endpoint  
- [x] 8. Background scheduler for nightly ingest + evaluation jobs  
- [x] 9. API key system + roles + rate limiting  
- [ ] 10. Observability: logging, latency, cache metrics + `/metrics` endpoint  
- [ ] 11. ≥3 performance optimizations with before/after measurements  
- [x] 12. Documentation: README, architecture diagram, extension guide  
- [x] **BONUS**: Simple UI
- [ ] **BONUS**: hallucination guard, tests, multi‑tenant, structured parser  
