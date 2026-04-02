from __future__ import annotations

import argparse
from pathlib import Path

from .job_fetcher import JobFetcher, JobSearchError
from .models import JobPosting
from .output import render_console, save_markdown, save_pdf
from .planner import build_learning_plan
from .skill_extractor import extract_skills


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a personalized software engineering learning plan from a public job posting."
    )
    parser.add_argument("company", help="Company name, for example Stripe")
    parser.add_argument("role", help='Role title, for example "Junior Software Engineer"')
    parser.add_argument("--job-url", help="Optional direct link to a public job posting")
    parser.add_argument("--job-file", help="Optional local file containing a job description")
    parser.add_argument("--markdown", help="Optional path to save the plan as Markdown")
    parser.add_argument("--pdf", help="Optional path to save the plan as PDF")
    return parser.parse_args()


def load_job_from_file(company: str, role: str, path: str) -> JobPosting:
    text = Path(path).read_text(encoding="utf-8")
    return JobPosting(
        company=company,
        role=role,
        title=role,
        url=None,
        description=text,
        source=f"file:{path}",
    )


def main() -> int:
    args = parse_args()

    try:
        if args.job_file:
            job = load_job_from_file(args.company, args.role, args.job_file)
        else:
            job = JobFetcher().fetch(args.company, args.role, job_url=args.job_url)
    except FileNotFoundError:
        print(f'Error: job description file "{args.job_file}" was not found.')
        return 1
    except JobSearchError as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:
        print(f"Unexpected error while retrieving the job posting: {exc}")
        return 1

    skills = extract_skills(job)
    if not skills:
        print("Error: a job posting was found, but no skills could be extracted.")
        return 1

    plan = build_learning_plan(job, skills)
    print(render_console(plan))

    if args.markdown:
        target = save_markdown(plan, args.markdown)
        print(f"\nSaved Markdown plan to {target}")

    if args.pdf:
        try:
            target = save_pdf(plan, args.pdf)
            print(f"Saved PDF plan to {target}")
        except ImportError:
            print("Could not save PDF because reportlab is not installed.")
            return 1

    return 0
