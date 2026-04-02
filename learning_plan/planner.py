from __future__ import annotations

from typing import List

from .models import JobPosting, LearningPlan, SkillPlan
from .resource_catalog import resource_bundle, to_resources


def build_learning_plan(job: JobPosting, skills: List[str]) -> LearningPlan:
    skill_plans: List[SkillPlan] = []

    for index, skill in enumerate(_ordered_skills(skills), start=1):
        bundle = resource_bundle(skill)
        skill_plans.append(
            SkillPlan(
                skill=skill,
                category=bundle["category"],
                priority=index,
                reason=_reason_for_skill(job, skill),
                estimated_time=bundle["estimated_time"],
                resources=to_resources(skill),
                exercises=bundle["exercises"],
            )
        )

    phases = _build_phases(job, skill_plans)
    summary = _build_summary(job, skill_plans)
    return LearningPlan(job=job, summary=summary, phases=phases, skills=skill_plans)


def _ordered_skills(skills: List[str]) -> List[str]:
    catalog_order = {
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
    return sorted(skills, key=lambda skill: (catalog_order.get(resource_bundle(skill)["category"], 99), skill))


def _reason_for_skill(job: JobPosting, skill: str) -> str:
    summary = job.company_summary or f"{job.company} appears to be hiring for this role through a public posting."
    return (
        f"This skill appears in the job requirements for {job.title} at {job.company}. "
        f"Company context: {summary}"
    )


def _build_phases(job: JobPosting, skill_plans: List[SkillPlan]) -> List[str]:
    first = ", ".join(plan.skill for plan in skill_plans[:2]) if skill_plans else "core fundamentals"
    middle = ", ".join(plan.skill for plan in skill_plans[2:5]) if len(skill_plans) > 2 else "role-specific engineering topics"
    final = ", ".join(plan.skill for plan in skill_plans[5:]) if len(skill_plans) > 5 else "portfolio and interview practice"
    return [
        f"Phase 1: Build strong foundations in {first}. Focus on syntax, problem solving, and daily coding reps.",
        f"Phase 2: Learn implementation skills in {middle}. Build small, working projects that mirror the job description.",
        f"Phase 3: Deepen production readiness through {final}. Polish a portfolio project that resembles the target role at {job.company}.",
    ]


def _build_summary(job: JobPosting, skill_plans: List[SkillPlan]) -> str:
    skills = ", ".join(plan.skill for plan in skill_plans[:6]) if skill_plans else "role-relevant fundamentals"
    return (
        f"This plan is customized for the {job.title} role at {job.company}. "
        f"It prioritizes the skills emphasized in the live job posting, especially {skills}, "
        "and orders them from fundamentals to company-specific execution skills."
    )
