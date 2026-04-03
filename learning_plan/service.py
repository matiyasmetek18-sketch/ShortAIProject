from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .job_fetcher import JobFetcher, JobSearchError
from .models import JobPosting, LearningPlan
from .output import render_markdown
from .planner import build_learning_plan
from .skill_extractor import extract_skills


class PlanGenerationError(Exception):
    """Raised when a learning plan request cannot be completed."""


def load_job_from_text(company: str, role: str, text: str, source: str = "inline") -> JobPosting:
    return JobPosting(
        company=company,
        role=role,
        title=role,
        url=None,
        description=text,
        source=source,
    )


def load_job_from_file(company: str, role: str, path: str) -> JobPosting:
    text = Path(path).read_text(encoding="utf-8")
    return load_job_from_text(company, role, text, source=f"file:{path}")


def generate_plan(
    company: str,
    role: str,
    job_url: Optional[str] = None,
    job_file: Optional[str] = None,
    job_text: Optional[str] = None,
    current_skills: Optional[List[str]] = None,
    intensity: str = "balanced",
    hours_per_week: int = 8,
) -> LearningPlan:
    if not company or not role:
        raise PlanGenerationError('Both "company" and "role" are required.')

    try:
        if job_text:
            job = load_job_from_text(company, role, job_text)
        elif job_file:
            job = load_job_from_file(company, role, job_file)
        else:
            job = JobFetcher().fetch(company, role, job_url=job_url)
    except FileNotFoundError as exc:
        raise PlanGenerationError(f'Job description file "{job_file}" was not found.') from exc
    except JobSearchError as exc:
        raise PlanGenerationError(str(exc)) from exc
    except Exception as exc:
        raise PlanGenerationError(f"Unexpected error while retrieving the job posting: {exc}") from exc

    skills = extract_skills(job)
    if not skills:
        raise PlanGenerationError(
            "A job posting was found, but no skills could be extracted. "
            "Try providing a more detailed job description with --job-file or request body."
        )

    normalized_current_skills = [skill.strip() for skill in (current_skills or []) if skill.strip()]
    return build_learning_plan(
        job,
        skills,
        current_skills=normalized_current_skills,
        intensity=intensity,
        hours_per_week=hours_per_week,
    )


def plan_to_dict(plan: LearningPlan) -> Dict[str, Any]:
    return {
        "job": {
            "company": plan.job.company,
            "role": plan.job.role,
            "title": plan.job.title,
            "url": plan.job.url,
            "source": plan.job.source,
            "location": plan.job.location,
            "company_summary": plan.job.company_summary,
        },
        "summary": plan.summary,
        "phases": plan.phases,
        "gap_analysis": {
            "current_skills": plan.gap_analysis.current_skills,
            "matched_skills": plan.gap_analysis.matched_skills,
            "missing_skills": plan.gap_analysis.missing_skills,
            "adjacent_skills": plan.gap_analysis.adjacent_skills,
            "coverage_score": plan.gap_analysis.coverage_score,
            "narrative": plan.gap_analysis.narrative,
        },
        "weekly_schedule": {
            "intensity": plan.weekly_schedule.intensity,
            "hours_per_week": plan.weekly_schedule.hours_per_week,
            "headline": plan.weekly_schedule.headline,
            "sessions": [
                {
                    "day": session.day,
                    "focus": session.focus,
                    "duration": session.duration,
                    "tasks": session.tasks,
                }
                for session in plan.weekly_schedule.sessions
            ],
        },
        "fit_signals": {
            "strengths": plan.fit_signals.strengths,
            "risks": plan.fit_signals.risks,
            "company_signal": plan.fit_signals.company_signal,
            "hiring_story": plan.fit_signals.hiring_story,
        },
        "application_assets": {
            "elevator_pitch": plan.application_assets.elevator_pitch,
            "outreach_note": plan.application_assets.outreach_note,
            "portfolio_headline": plan.application_assets.portfolio_headline,
        },
        "roadmap": [
            {
                "label": stage.label,
                "objective": stage.objective,
                "deliverables": stage.deliverables,
            }
            for stage in plan.roadmap
        ],
        "capstone": {
            "title": plan.capstone.title,
            "pitch": plan.capstone.pitch,
            "outcomes": plan.capstone.outcomes,
            "milestones": plan.capstone.milestones,
        },
        "interview_prep": {
            "technical_focus": plan.interview_prep.technical_focus,
            "behavioral_focus": plan.interview_prep.behavioral_focus,
            "practice_prompts": plan.interview_prep.practice_prompts,
        },
        "interview_bank": [
            {
                "topic": topic.topic,
                "questions": topic.questions,
            }
            for topic in plan.interview_bank
        ],
        "resume_bullets": [
            {
                "bullet": item.bullet,
                "evidence": item.evidence,
            }
            for item in plan.resume_bullets
        ],
        "standout_moves": plan.standout_moves,
        "skills": [
            {
                "skill": skill.skill,
                "category": skill.category,
                "priority": skill.priority,
                "reason": skill.reason,
                "estimated_time": skill.estimated_time,
                "resources": [
                    {
                        "title": resource.title,
                        "url": resource.url,
                        "kind": resource.kind,
                        "estimated_time": resource.estimated_time,
                    }
                    for resource in skill.resources
                ],
                "exercises": skill.exercises,
            }
            for skill in plan.skills
        ],
        "markdown": render_markdown(plan),
    }
