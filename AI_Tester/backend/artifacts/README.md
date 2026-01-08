
***

## backend/artifacts/README.md
```md
# artifacts/

This folder stores "raw, non-structured artifacts" produced during analysis and file ingestion.

What goes here?

1) Raw LLM responses

When analysis is generated, the backend writes the raw model output to a timestamped file such as:
   `groq_raw_<timestamp>.txt`
   `pplx_raw_<timestamp>.txt`

These files are useful for debugging when:
   The model returns invalid JSON.
   The scenario has incorrect selectors/actions.
   You need to inspect the exact prompt/response behavior.
