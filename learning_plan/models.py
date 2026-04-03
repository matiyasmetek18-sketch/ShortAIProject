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
class GapAnalysis:
    current_skills: List[str] = field(default_factory=list)
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    adjacent_skills: List[str] = field(default_factory=list)
    coverage_score: int = 0
    narrative: str = ""


@dataclass
class RoadmapStage:
    label: str
    objective: str
    deliverables: List[str] = field(default_factory=list)


@dataclass
class CapstoneProject:
    title: str
    pitch: str
    outcomes: List[str] = field(default_factory=list)
    milestones: List[str] = field(default_factory=list)


@dataclass
class InterviewPrep:
    technical_focus: List[str] = field(default_factory=list)
    behavioral_focus: List[str] = field(default_factory=list)
    practice_prompts: List[str] = field(default_factory=list)


@dataclass
class ResumeBullet:
    bullet: str
    evidence: str


@dataclass
class WeeklySession:
    day: str
    focus: str
    duration: str
    tasks: List[str] = field(default_factory=list)


@dataclass
class WeeklySchedule:
    intensity: str
    hours_per_week: int
    headline: str
    sessions: List[WeeklySession] = field(default_factory=list)


@dataclass
class FitSignals:
    strengths: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    company_signal: str = ""
    hiring_story: str = ""


@dataclass
class ApplicationAssets:
    elevator_pitch: str
    outreach_note: str
    portfolio_headline: str


@dataclass
class InterviewQuestionSet:
    topic: str
    questions: List[str] = field(default_factory=list)


@dataclass
class LearningPlan:
    job: JobPosting
    summary: str
    phases: List[str]
    skills: List[SkillPlan]
    gap_analysis: GapAnalysis
    roadmap: List[RoadmapStage]
    capstone: CapstoneProject
    interview_prep: InterviewPrep
    resume_bullets: List[ResumeBullet]
    weekly_schedule: WeeklySchedule
    fit_signals: FitSignals
    application_assets: ApplicationAssets
    interview_bank: List[InterviewQuestionSet]
    standout_moves: List[str] = field(default_factory=list)
