https://doi.org/10.5281/zenodo.24516089

# CASE FILTER & MACRO-OS ECOSYSTEM (v1.3 — v7.0 + MCP / PyPI)
**The Dated Record Method & Semantic Role Logic: A Deterministic Structural Guardrail Against LLM Hallucinations and Contractual Ambiguity.**

- **Author:** Irina Vetlugina (Samara, Russia)
- **IP Priority:** Base protocol `v1.2` officially deposited in the National Registry of Intellectual Property (**n'RIS**), Reg. No. **852-137-831** (`2026-11-20`, valid through `2027-11-20`).
- **License:** Dual License — Free for Non-Commercial & Research Use (`CC BY-NC 4.0`) / Paid Commercial License (`polutshe@mail.ru`), Copyright © 2026 Irina Vetlugina.

---

## 1. REPOSITORY ARCHITECTURE

### Software Infrastructure & Research
1. **`case_filter_mcp_server.py`** — Zero-dependency **Model Context Protocol (MCP) Server** for Claude Desktop, Cursor, Windsurf, and autonomous AI agents. Acts as a deterministic firewall (`< 0.5 ms` latency) that blocks agent actions when texts contain passive-voice evasion (`EMPTY SEAT`), unanchored percentages, or undated deadlines.
2. **`case_compiler.py`** — Standalone Python deterministic text compiler & CLI auditor (zero LLM token cost).
3. **`pyproject.toml`** — PyPI packaging manifest (`pip install case-filter`).
4. **`whitepaper_dated_record_method.md`** — Formal academic preprint ready for Zenodo / arXiv DOI registration.

### Portable LLM Action Prompts (`MACRO-OS`)
5. **`padezhny-filtr-v1.3.md`** — Core theoretical & operational engine.
6. **`macro-os-v4.0-ultimate.md`** — 10-layer single-record X-ray (`ULTRA:`) + plain-language rewrite.
7. **`macro-os-v5.0-deep-engine-en.md`** — Multi-layer document stripping (`ONION:`), cross-document contradiction audit (`PAIR-CHECK:`), and boundary stress-testing (`DEGENERATION:`).
8. **`macro-os-v6.0-architect-en.md`** — Active legal synthesis (`CONSTRUCTOR:`), adversarial simulation (`DEVIL'S ADVOCATE:`), and prompt-injection defense (`ARMOR`).
9. **`macro-os-v7.0-tribunal-en.md`** — Multi-agent consensus council (`TRIBUNAL`: Prosecutor / Defender / Judge) and cross-model `ARBITRAGE`.

---

## 2. QUICK START: MCP SERVER INTEGRATION

Add the deterministic guardrail to your **Claude Desktop** or **Cursor** configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "case-filter": {
      "command": "python3",
      "args": ["/absolute/path/to/case_filter_mcp_server.py"]
    }
  }
}
```

Available MCP Tools exposed to your AI agent:
- `verify_statement` — blocks hallucinated claims, passive evasion, and unanchored metrics before execution.
- `audit_contract_clause` — detects rubber deadlines and missing deliverables in legal clauses.
- `get_cell_registry` — returns the canonical taxonomy of structural failures (`Cells 1–18 + R6`).

---

## 3. QUICK START: ZERO-CODE CHAT USAGE

Paste **`macro-os-v7.0-tribunal-en.md`** (or `v6.0` / `v5.0`) at the start of any ChatGPT, Claude, Gemini, or DeepSeek session and run:
- `ULTRA: [text]` — 10-layer audit + plain-language rewrite.
- `PAIR-CHECK: [Text A] /// [Text B]` — compare marketing promises against actual contract terms.
- `CONSTRUCTOR: [task]` — synthesize airtight legal clauses with zero passive voice.
- `DEVIL'S ADVOCATE: [document]` — simulate an opposing counsel attack and generate patches.
- `TRIBUNAL: [disputed text]` — run a 3-role adversarial review (Prosecutor, Defender, Judge).
- `MIRROR` — audit the AI's own previous response and compute its **Honesty Index (%)**.

---

## 4. DUAL LICENSE

**Copyright © 2026 Irina Vetlugina. All rights reserved.**
- **Non-Commercial (`CC BY-NC 4.0`):** Free for individuals, researchers, and educators with mandatory attribution to Irina Vetlugina and n'RIS Reg. No. `852-137-831`.
- **Commercial:** Integration into SaaS platforms, commercial API pipelines, corporate consulting, or paid products requires a commercial license agreement (`polutshe@mail.ru`).
