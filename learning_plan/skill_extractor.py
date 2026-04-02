from __future__ import annotations

import re
from collections import OrderedDict
from typing import Dict, List

from .models import JobPosting


SKILL_PATTERNS: Dict[str, List[str]] = {
    "Python": [r"\bpython\b"],
    "Java": [r"\bjava\b"],
    "JavaScript": [r"\bjavascript\b", r"\bjs\b"],
    "TypeScript": [r"\btypescript\b", r"\bts\b"],
    "React": [r"\breact\b", r"\breact\.js\b"],
    "SQL": [r"\bsql\b", r"\bmysql\b", r"\bqueries\b"],
    "PostgreSQL": [r"\bpostgresql\b", r"\bpostgres\b"],
    "Git": [r"\bgit\b", r"\bgithub\b", r"\bversion control\b"],
    "Docker": [r"\bdocker\b", r"\bcontainers?\b"],
    "REST APIs": [r"\brest\b", r"\bapi\b", r"\bhttp\b"],
    "Data Structures": [r"\bdata structures?\b", r"\blists?\b", r"\btrees?\b", r"\bhash tables?\b"],
    "Algorithms": [r"\balgorithms?\b", r"\bproblem solving\b", r"\bcomplexity\b"],
    "Testing": [r"\btesting\b", r"\bunit tests?\b", r"\bintegration tests?\b", r"\bqa\b"],
    "System Design": [r"\bsystem design\b", r"\bdistributed systems?\b", r"\bscalab\w+\b"],
    "Linux": [r"\blinux\b", r"\bunix\b", r"\bshell\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b", r"\bec2\b", r"\bs3\b", r"\blambda\b"],
    "CI/CD": [r"\bci/cd\b", r"\bcontinuous integration\b", r"\bcontinuous delivery\b", r"\bgithub actions\b"],
}


CATEGORY_PRIORITY = {
    "Programming Language": 1,
    "Computer Science": 2,
    "Backend Concept": 3,
    "Database": 4,
    "Frontend Framework": 5,
    "Software Engineering Practice": 6,
    "Developer Tooling": 7,
    "Cloud": 8,
    "Architecture": 9,
    "Role-Specific Skill": 10,
}


def extract_skills(job: JobPosting) -> List[str]:
    description = job.description.lower()
    detected: "OrderedDict[str, None]" = OrderedDict()

    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(pattern, description) for pattern in patterns):
            detected[skill] = None

    generated = _extract_uncurated_technologies(job.description)
    for skill in generated:
        detected.setdefault(skill, None)

    role_text = f"{job.title} {job.role}".lower()
    if "frontend" in role_text and "React" not in detected:
        detected["React"] = None
    if "backend" in role_text and "REST APIs" not in detected:
        detected["REST APIs"] = None
    if any(word in role_text for word in ("junior", "new grad", "graduate")):
        detected.setdefault("Data Structures", None)
        detected.setdefault("Algorithms", None)
        detected.setdefault("Git", None)

    return list(detected)


def _extract_uncurated_technologies(text: str) -> List[str]:
    raw_candidates = re.findall(
        r"\b(?:Node\.js|Next\.js|Django|Flask|FastAPI|Kubernetes|Redis|GraphQL|MongoDB|Pandas|NumPy|Terraform|Jenkins|Kafka)\b",
        text,
        flags=re.IGNORECASE,
    )
    seen: "OrderedDict[str, None]" = OrderedDict()
    for item in raw_candidates:
        normalized = item.strip()
        if normalized.lower() == "node.js":
            normalized = "Node.js"
        elif normalized.lower() == "next.js":
            normalized = "Next.js"
        seen[normalized] = None
    return list(seen)
