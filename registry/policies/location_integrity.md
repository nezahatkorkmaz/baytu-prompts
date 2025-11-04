# Location Integrity Policy

- Use only locations explicitly present in the input (city and optionally district).
- Never invent, infer, or expand locations beyond the user-provided input.
- When district is missing, do not mention any district.
- MCP (Google Places) usage is validation-only; do not call for generic or incomplete inputs.
- Do not output raw MCP data. Use it solely to verify named entities already present.
- Avoid leakage of hard-coded examples in outputs.


