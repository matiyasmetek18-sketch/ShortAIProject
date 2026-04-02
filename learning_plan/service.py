from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

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

    return build_learning_plan(job, skills)


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
