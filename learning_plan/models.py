from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class JobPosting:
    company: str
    role: str
    title: str
    url: Optional[str]
    description: str
    source: str
    location: Optional[str] = None
    company_summary: Optional[str] = None


@dataclass
class Resource:
    title: str
    url: str
    kind: str
    estimated_time: str


@dataclass
class SkillPlan:
    skill: str
    category: str
    priority: int
    reason: str
    estimated_time: str
    resources: List[Resource] = field(default_factory=list)
    exercises: List[str] = field(default_factory=list)


@dataclass
class LearningPlan:
    job: JobPosting
    summary: str
    phases: List[str]
    skills: List[SkillPlan]
