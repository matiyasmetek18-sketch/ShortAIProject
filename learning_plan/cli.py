from __future__ import annotations

import argparse

from .output import render_console, save_markdown, save_pdf
from .service import PlanGenerationError, generate_plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a personalized software engineering learning plan from a public job posting."
    )
    parser.add_argument("company", help="Company name, for example Stripe")
    parser.add_argument("role", help='Role title, for example "Junior Software Engineer"')
    parser.add_argument("--job-url", help="Optional direct link to a public job posting")
    parser.add_argument("--job-file", help="Optional local file containing a job description")
    parser.add_argument("--current-skills", help="Optional comma-separated list of current skills")
    parser.add_argument("--intensity", default="balanced", help="Learning intensity: light, balanced, accelerated, or sprint")
    parser.add_argument("--hours-per-week", type=int, default=8, help="Weekly study budget in hours")
    parser.add_argument("--markdown", help="Optional path to save the plan as Markdown")
    parser.add_argument("--pdf", help="Optional path to save the plan as PDF")
    return parser.parse_args()

def main() -> int:
    args = parse_args()

    try:
        plan = generate_plan(
            company=args.company,
            role=args.role,
            job_url=args.job_url,
            job_file=args.job_file,
            current_skills=(args.current_skills.split(",") if args.current_skills else []),
            intensity=args.intensity,
            hours_per_week=args.hours_per_week,
        )
    except PlanGenerationError as exc:
        print(f"Error: {exc}")
        return 1
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
