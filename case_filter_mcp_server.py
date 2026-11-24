#!/usr/bin/env python3
"""
MCP Server (Model Context Protocol) for The Dated Record Method / Case Filter (v1.3)
Author: Irina Vetlugina (Samara, Russia) | IP Priority: n'RIS No. 852-137-831 (2026-11-20)
License: Dual License — CC BY-NC 4.0 (Free for Non-Commercial) / Paid Commercial (polutshe@mail.ru)

Zero-dependency JSON-RPC 2.0 stdio server acting as a deterministic structural firewall
for AI agents (Claude Desktop, Cursor, Windsurf, LangChain, CrewAI).
"""

import sys
import json
import re
from typing import Dict, Any, List


class DeterministicCaseFirewall:
    def __init__(self):
        # Gate 1: Creator's Boundary (Intent without action -> Zero Act 0)
        self.intent_ru = [
            r"\b(планируем|планирует|собираемся|собирается|хотим|стремимся|намерены|будем улучшать)\b"
        ]
        self.intent_en = [
            r"\b(we|i|company|team)\s+(plan|aim|intend|hope|strive|want|are going)\s+to\b"
        ]

        # Gate 2: Passive & Reflexive Impostors (Cell 14 -> EMPTY SEAT)
        self.passive_ru = [
            r"\b(было|была|были|будет)\s+[а-яё]+(?:но|на|ны|то|та|ты)\b",
            r"\b[а-яё]{4,}(?:лось|лась|лись|ётся|утся|ются|ится|атся|ятся)\b",
            r"\b(принято|решено|сделано|выполнено|утверждено|отправлено|подписано|производится|осуществляется)\b"
        ]
        self.passive_en = [
            r"\b(was|were|is|are|been|be)\s+(decided|made|approved|shifted|delayed|solved|confirmed|proven|done|sent|signed)\b",
            r"\b(deadlines?|terms?|schedule)\s+(shifted|moved|changed)\b",
            r"\b(error|bug|issue|failure)\s+(occurred|happened)\b"
        ]

        # Gate 3: Impostor Nominative (Cell 11) & Time-Impostor (Cell 13)
        self.nominative_impostors = [
            r"\b(уч[её]ные|эксперты|аналитики|исследователи)\s+(доказали|подтвердили|отмечают|считают|утверждают)\b",
            r"\b(наука|история|рынок|природа)\s+(доказала|показывает|повторяется|расставит)\b",
            r"\b(scientists?|experts?|researchers?|analysts?)\s+(proved|proven|say|claim|believe|show)\b",
            r"\b(science|history|market)\s+(proved|shows|decided)\b"
        ]
        self.time_impostors = [
            r"\bвремя\s+(покажет|расставит|лечит|рассудит)\b",
            r"\btime\s+will\s+(tell|show|decide)\b"
        ]

        # Gate 4: Rubber Deadlines / Left Edge [R]
        self.rubber_deadlines = [
            r"\bв\s+разумный\s+срок\b",
            r"\bв\s+ближайшее\s+время\b",
            r"\bпо\s+мере\s+(возможности|готовности)\b",
            r"\b(своевременно|оперативно|скоро|вскоре|позже|дополнительно)\b",
            r"\bin\s+a\s+reasonable\s+time\b",
            r"\bin\s+the\s+near\s+future\b",
            r"\b(soon|eventually|shortly|later|timely)\b"
        ]

        # Gate 5: Unanchored Metrics (Cell 17) & Forbidden Words
        self.percent_pat = r"\b\d+(?:[.,]\d+)?\s*%"
        self.baseline_markers = [
            r"\bс\s+\d+.*?\s+до\s+\d+",
            r"\bот\s+\d+.*?\s+к\s+\d+",
            r"\bfrom\s+\d+.*?\s+to\s+\d+",
            r"\b(база|выборка|baseline|sample|n\s*=)\b"
        ]
        self.forbidden_words = [
            r"\b(доказано|подтверждено|бесспорно|очевидно|гарантированно|100%\s+гарантия)\b",
            r"\b(proven|undeniably|guaranteed|obviously|indisputably)\b"
        ]

    def verify_statement(self, text: str) -> Dict[str, Any]:
        cells: List[str] = []
        tokens: List[str] = []
        score = 100
        low = text.lower()

        for pat in self.intent_ru + self.intent_en:
            m = re.search(pat, low)
            if m:
                cells.append("Zero Act (0): Intent/Plan did not cross Creator's Boundary")
                tokens.append(m.group(0))
                score -= 25

        for pat in self.passive_ru + self.passive_en:
            m = re.search(pat, low)
            if m:
                cells.append("Cell 14: Passive/Reflexive Impostor (EMPTY SEAT)")
                tokens.append(m.group(0))
                score -= 30

        for pat in self.nominative_impostors:
            m = re.search(pat, low)
            if m:
                cells.append("Cell 11: Impostor Nominative / Window-Dressing")
                tokens.append(m.group(0))
                score -= 25

        for pat in self.time_impostors:
            m = re.search(pat, low)
            if m:
                cells.append("Cell 13: Time-Impostor assigned as executor")
                tokens.append(m.group(0))
                score -= 25

        for pat in self.rubber_deadlines:
            m = re.search(pat, low)
            if m:
                cells.append("Left Edge [R]: Rubber Deadline (No Verification Date)")
                tokens.append(m.group(0))
                score -= 25

        pct = re.search(self.percent_pat, low)
        if pct:
            if not any(re.search(b, low) for b in self.baseline_markers):
                cells.append("Cell 17: Unanchored Percentage (No Baseline)")
                tokens.append(pct.group(0))
                score -= 25

        for pat in self.forbidden_words:
            m = re.search(pat, low)
            if m:
                cells.append(f"Forbidden Epistemic Claim -> '{m.group(0)}'")
                tokens.append(m.group(0))
                score -= 20

        score = max(0, score)
        unique_cells = list(dict.fromkeys(cells))

        if not unique_cells:
            return {
                "status": "APPROVED",
                "gate": "ALL_GATES_PASSED",
                "purity_index": 100,
                "detected_cells": [],
                "action_directive": "SAFE TO PROCEED. Statement satisfies Dated Record structural rules."
            }
        return {
            "status": "BLOCKED",
            "gate": "GATE_1_TO_5_STRUCTURAL_VIOLATION",
            "purity_index": score,
            "detected_cells": unique_cells,
            "matched_tokens": list(dict.fromkeys(tokens)),
            "action_directive": "DO NOT SEND OR COMMIT. Rewrite text with active subject, baseline metrics, and dated verification window."
        }

    def audit_contract_clause(self, clause: str) -> Dict[str, Any]:
        res = self.verify_statement(clause)
        if res["status"] == "APPROVED":
            return {
                "clause_status": "APPROVED_SOLID_OBLIGATION",
                "detected_cells": [],
                "recommendation": "Clause meets Dated Record standards."
            }
        return {
            "clause_status": "REJECTED_UNSAFE_CLAUSE",
            "detected_cells": res["detected_cells"],
            "recommendation": "Replace passive voice with named payer/executor, add exact calendar date [t2], and specify deliverable artifact E."
        }


firewall = DeterministicCaseFirewall()


def handle_request(req: Dict[str, Any]) -> Dict[str, Any] | None:
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "case-filter-mcp", "version": "1.0.0"}
            }
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "verify_statement",
                        "description": "Deterministic structural firewall against LLM hallucinations, passive voice (EMPTY SEAT), undated forecasts, and unanchored metrics.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "Statement or agent output to verify"}
                            },
                            "required": ["text"]
                        }
                    },
                    {
                        "name": "audit_contract_clause",
                        "description": "Audits a legal contract clause or SLA for passive acceptance traps, rubber deadlines, and missing deliverables.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "clause": {"type": "string", "description": "Contract clause text"}
                            },
                            "required": ["clause"]
                        }
                    },
                    {
                        "name": "get_cell_registry",
                        "description": "Returns the Dated Record taxonomy of linguistic and logical failure modes (Cells 1-18 + R6).",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }

    if method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "verify_statement":
            output = firewall.verify_statement(args.get("text", ""))
        elif tool_name == "audit_contract_clause":
            output = firewall.audit_contract_clause(args.get("clause", ""))
        elif tool_name == "get_cell_registry":
            output = {
                "registry": {
                    "Zero Act (0)": "Intent or plan that did not cross Creator's Boundary",
                    "Cell 1": "Record without act (claim without payment ticks)",
                    "Cell 11": "Impostor nominative / window-dressing ('science proved')",
                    "Cell 13": "Time-impostor assigned as executor ('time will tell')",
                    "Cell 14": "Passive/reflexive impostor hiding executor (EMPTY SEAT)",
