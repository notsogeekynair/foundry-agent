Role: You are a senior Azure serverless + AI engineer.
Goal: Bootstrap a production-grade starter project for a “Dual‑Mode Invoice/Document Extractor” where a Microsoft Copilot Studio agent calls Python Azure Functions hosting the extraction logic. The function supports two extraction modes: (1) text-based PDF parsing using PyMuPDF + regex heuristics, (2) OCR/layout extraction using Azure Document Intelligence; and also supports “auto” mode that selects between them.
Context & constraints:

This is for a TopGear-style challenge whose core requirement is: “Develop Azure Function Apps Python to host core AI logic.” [Fw: 📢 Nom...equirement | Outlook]
For text-based extraction, follow patterns like Python + PyMuPDF + regex used in Amazon Invoice Bot.docx (PDF parsing + mapping/logging style). [Knowledge...e Clusters | SharePoint]
For OCR/layout extraction, use Azure Document Intelligence like referenced in FY'25-26 - 330 - AI-Powered Contract Intelligence for Renewable Energy Operations.pdf. [Closing th...t Practice | Event]
The solution must be easy to integrate with Copilot Studio via a single HTTP action, using an OpenAPI spec.

Deliver exactly the following outputs (in this order):

High-level architecture (Copilot Studio → Azure Function → Extractors → Postprocess → Validation → Optional persistence), with a brief explanation of the responsibilities of each layer.
Repo scaffolding: a complete folder structure for an Azure Functions (Python v2 programming model) project. Include modules:

extractors/text_extractor.py
extractors/docint_extractor.py
router.py (mode routing: auto | text | docintelligence)
schemas.py (Pydantic models for request/response)
postprocess/normalize.py
validation/validate_invoice.py
openapi.yaml


API contract: propose request/response JSON for POST /extract that includes:

mode enum: auto | text | docintelligence
document (base64 payload + filename + mimeType)
hints (optional)
Response must return:
modeUsed
summary
fields with {value, confidence, source}
lineItems[]
issues[] with {type, severity, message}
nextActions[]


Mode decision logic for auto: start with text-extraction; if no PDF text layer / too many critical fields missing / confidence below threshold → switch to docintelligence. If user explicitly chooses text or docintelligence, never override—just warn with issues.
Minimal implementation code (not pseudo): provide:

Azure Function entrypoint for /extract
text_extractor that extracts at least invoice number/date/total/vendor using PyMuPDF + regex
docint_extractor stub that shows how to call Azure Document Intelligence and parse key fields (use placeholders for endpoint/key)
a validate_invoice that checks totals and required fields


OpenAPI spec (openapi.yaml) compatible with Copilot Studio custom action import (single endpoint /extract, schemas included).
Local run instructions and deployment steps (Azure Functions Core Tools + az commands) but keep it short and accurate.
A Copilot Studio topic flow outline: how the agent asks user to choose mode, uploads document, calls /extract, and prompts user to confirm low-confidence fields.
Non-functional requirements checklist: security (no secrets in code, Key Vault/env vars), logging with correlation id, error handling, timeouts, and PII-safe logs.

Coding requirements:

Python 3.10+
Use azure-functions Python v2 model conventions
Use Pydantic for schemas
Avoid any hardcoded secrets; refer to env vars:

DOCINT_ENDPOINT
DOCINT_KEY
DOCINT_MODEL_ID (or prebuilt invoice model id if used)


Ensure all responses are valid JSON and deterministic.

Quality bar:

Keep it clean, production-ready, and immediately runnable as a starter template.
Include comments where important, but avoid walls of text.