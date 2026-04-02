<<<<<<< HEAD
# Personalized Learning Plan Generator

This Python CLI helps early-career software engineers generate a tailored learning plan for a specific company and role.

## What it does

- Searches public job postings for a company and role
- Extracts skills, tools, and core engineering concepts from the posting
- Builds a step-by-step learning plan with free resources
- Prints the plan in the console and can save it as Markdown or PDF

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py "Stripe" "Junior Software Engineer" --markdown stripe_plan.md
```

## Optional flags

```bash
python3 main.py "Datadog" "Software Engineer" --pdf plan.pdf
python3 main.py "Figma" "Frontend Engineer" --job-url "https://boards.greenhouse.io/figma/jobs/1234567"
python3 main.py "Acme" "Backend Engineer" --job-file sample_job.txt
```

## Notes

- Public job postings change frequently, so results depend on what is available at runtime.
- The tool prefers public ATS pages and structured `JobPosting` metadata when available.
- If no curated resource exists for a detected skill, the app generates a free fallback resource link.
=======
# ShortAIProject
>>>>>>> 037f512afcc4e26e0a40e71ce161402122f16b99
