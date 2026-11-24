#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПАДЕЖНЫЙ КОМПИЛЯТОР v1.0 (Deterministic Pre-Filter Engine)
Детерминированный программный анализатор текста на базе ядра «Падежный фильтр» v1.3.
Автор метода: Ирина Ветлугина (Самара) | Приоритет: n'RIS № 852-137-831 (20.11.2026)
Лицензия: Dual License — CC BY-NC 4.0 (некоммерческое) / Платно для коммерции (polutshe@mail.ru)
"""

import re
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict

@dataclass
class AuditCard:
    record: str
    gates_triggered: List[str] = field(default_factory=list)
    cells: List[str] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    verdict: str = "CANDIDATE_FOR_LLM_E"
    honesty_score: int = 100

class CaseCompiler:
    def __init__(self):
        # Шлюз 1: Граница творца (намерения, планы, обещания)
        self.intent_patterns = [
            r"\b(планиру[ею][мт]?|планируем|намерен[ыа]?|стреми[мт]ся|собира[ею][мт]ся|постара[ею][мт]ся|буд[еу][мт]?\s+\w+ть)\b"
        ]
        # Шлюз 2: Пассив и возвратные глаголы (Клетка 14 - ПУСТОЕ КРЕСЛО)
        self.passive_participles = [
            r"\b(принят[оаы]?|решен[оаы]?|сделан[оаы]?|выделен[оаы]?|проведен[оаы]?|проведён[оаы]?|оказан[оаы]?|подписан[оаы]?|направлен[оаы]?|рассмотрен[оаы]?|выполнен[оаы]?|установлен[оаы]?)\b"
        ]
        self.reflexive_verbs = [
            r"\b[а-яё]{4,}(?:ет|ут|ют|ит|ат|ят|ал|ала|ало|али|ил|ила|ило|или)(?:ся|сь)\b"
        ]
        # Шлюз 3: Бесконечный процесс (несовершенный вид / бюрократический туман)
        self.process_patterns = [
            r"\b(прорабатыва[ею][мт]?|улучша[ею][мт]?|оптимизиру[ею][мт]?|оказыва[ею][мт]?\s+содействие|вед[её][мт]?\s+работ[уы]|проводит?ся\s+работа)\b"
        ]
        # Шлюз 4: Резиновые сроки (Левый край) и Время-самозванец (Клетка 13)
        self.rubber_time_patterns = [
            r"\b(в\s+разумный\s+срок|в\s+ближайшее\s+время|по\s+мере\s+возможности|по\s+мере\s+готовности|своевременно|оперативно|в\s+установленном\s+порядке|дополнительно)\b"
        ]
        self.time_impostor_patterns = [
            r"\b(время\s+покажет|время\s+расставит|история\s+рассудит|рынок\s+всё\s+расставит|жизнь\s+покажет)\b"
        ]
        # Шлюз 5: Анонимные авторитеты и витрина (Клетка 11 / Уровень 3)
        self.ghost_authority_patterns = [
            r"\b(учёные\s+доказали|ученые\s+доказали|по\s+мнению\s+экспертов|эксперты\s+считают|эксперты\s+отмечают|как\s+известно|по\s+данным\s+аналитиков|все\s+знают|общеизвестно)\b"
        ]
        # Шлюз 6: Цифры-самозванцы (Клетка 17 - проценты и разы без базы)
        self.percent_or_times = r"(\d+(?:[.,]\d+)?\s*(?:%|процент[аов]*|раз[а]?))"
        self.base_markers = r"\b(от\s+\d+|с\s+\d+\s+до\s+\d+|выборк[аеи]|из\s+\d+|баз[аеу]|составил[аои]?)\b"
        # Шлюз 7: Запрещённые оценочные ярлыки и газлайтинг (Клетка 18)
        self.manipulative_patterns = [
            r"\b(гарантированно|бесспорно|очевидно|абсолютно\s+точно|100%|ты\s+вечно|ты\s+всегда|ты\s+никогда)\b"
        ]
        # Маркеры легального документа или даты
        self.date_or_doc_markers = r"(\d{2}\.\d{2}\.\d{4}|\d{4}\s*год[ауе]?|акт\s*№|договор\s*№|приказ\s*№|эпикриз\s*№|отчёт\s*№|отчет\s*№|ст\.\s*\d+)"

    def analyze(self, text: str) -> AuditCard:
        card = AuditCard(record=text.strip())
        low = text.lower()
        penalty = 0

        # 1. Граница творца
        for pat in self.intent_patterns:
            m = re.findall(pat, low)
            if m:
                card.gates_triggered.append("Gate 1: Creator Boundary")
                card.cells.append("НУЛЕВОЙ АКТ (0)")
                card.findings.append(f"Замысел/план без действия: {set(m)}")
                penalty += 30

        # 2. Залог (пассив и -ся/-сь)
        passives = []
        for pat in self.passive_participles:
            passives.extend(re.findall(pat, low))
        reflexives = []
        for pat in self.reflexive_verbs:
            reflexives.extend(re.findall(pat, low))
        if passives or reflexives:
            card.gates_triggered.append("Gate 2: Voice & Empty Seat")
            card.cells.append("Клетка 14 (ПУСТОЕ КРЕСЛО)")
            card.findings.append(f"Скрытый исполнитель (пассив/возвратный): {set(passives + reflexives)}")
            penalty += 25

        # 3. Бесконечный процесс
        for pat in self.process_patterns:
            m = re.findall(pat, low)
            if m:
                card.gates_triggered.append("Gate 3: Imperfective Process")
                card.cells.append("ПРОЦЕСС [Р]")
                card.findings.append(f"Процесс без артефакта E: {set(m)}")
                penalty += 20

        # 4. Время и сроки
        for pat in self.rubber_time_patterns:
            m = re.findall(pat, low)
            if m:
                card.gates_triggered.append("Gate 4: Rubber Deadline")
                card.cells.append("ЛЕВЫЙ КРАЙ [Р]")
                card.findings.append(f"Резиновый срок без даты сверки: {set(m)}")
                penalty += 25
        for pat in self.time_impostor_patterns:
            m = re.findall(pat, low)
            if m:
                card.gates_triggered.append("Gate 4: Time Impostor")
                card.cells.append("Клетка 13 (Время-самозванец)")
                card.findings.append(f"Время назначено исполнителем: {set(m)}")
                penalty += 30

        # 5. Анонимные авторитеты
        for pat in self.ghost_authority_patterns:
            m = re.findall(pat, low)
            if m:
                card.gates_triggered.append("Gate 5: Ghost Authority")
                card.cells.append("Клетка 11 / Уровень 3 [Р]")
                card.findings.append(f"Ссылка на призрака вместо документа: {set(m)}")
                penalty += 25

        # 6. Цифры без базы
        nums = re.findall(self.percent_or_times, low)
        has_base = re.search(self.base_markers, low)
        if nums and not has_base:
            card.gates_triggered.append("Gate 6: Baseless Metric")
            card.cells.append("Клетка 17 (Цифра без базы)")
            card.findings.append(f"Относительная цифра без стартовой базы: {set(nums)}")
            penalty += 25

        # 7. Манипуляции и обобщения
        for pat in self.manipulative_patterns:
            m = re.findall(pat, low)
            if m:
                card.gates_triggered.append("Gate 7: Logical Leap / Gaslighting")
                card.cells.append("Клетка 18 (Логический скачок)")
                card.findings.append(f"Манипулятивный маркер/обобщение: {set(m)}")
                penalty += 20

        # Проверка наличия твёрдых якорей (дата/документ)
        has_anchor = re.search(self.date_or_doc_markers, low)

        card.honesty_score = max(0, 100 - penalty)
        if not card.cells and has_anchor:
            card.verdict = "LEGAL_RECORD_CANDIDATE (E)"
        elif not card.cells and not has_anchor:
            card.verdict = "UNVERIFIED_STATEMENT (Нет даты/документа)"
            card.honesty_score = 50
        else:
            card.verdict = "REJECTED_BY_COMPILER (" + " + ".join(dict.fromkeys(card.cells)) + ")"

        return card

if __name__ == "__main__":
    compiler = CaseCompiler()
    samples = [
        "По акту №1 от 20.11.2026 мама вымыла 2 рамы за 30 минут, площадь остекления выросла с 1 до 2 кв.м.",
        "Ваше обращение рассмотрено, в настоящее время проводится проработка вопроса, о результатах будет сообщено дополнительно в разумный срок.",
        "Учёные доказали, что новая платформа гарантированно увеличит продажи на 200%, и вообще ты вечно сомневаешься.",
        "В 2027 году мы планируем запустить новый сервис, а дальше время покажет."
    ]
    for idx, s in enumerate(samples, 1):
        res = compiler.analyze(s)
        print(f"=== ЗАПИСЬ #{idx} ===")
        print(f"ТЕКСТ: {res.record}")
        print(f"ВЕРДИКТ: {res.verdict}")
        print(f"ИНДЕКС ЧИСТОТЫ: {res.honesty_score}%")
        for f in res.findings:
            print(f"  - {f}")
        print()
