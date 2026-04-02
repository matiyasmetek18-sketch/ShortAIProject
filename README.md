# Personalized Learning Plan Generator

This project helps early-career software engineers generate a tailored learning plan for a specific company and role. It now includes:

- A Python CLI for local use
- A Vercel-ready Python web app and API in `api/main.py`
- A Netlify-ready proxy function in `netlify/functions/main.mjs`

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

## API usage

### Local CLI

```bash
python3 main.py "Stripe" "Junior Software Engineer"
python3 main.py "Figma" "Frontend Engineer" --job-url "https://boards.greenhouse.io/figma/jobs/1234567"
```

### Web app

Open `/` in the browser for the interactive interface.

### API

`GET /api/generate?company=Stripe&role=Junior%20Software%20Engineer`

`POST /api/generate` with JSON:

```json
{
  "company": "Stripe",
  "role": "Junior Software Engineer",
  "job_url": "https://boards.greenhouse.io/example/jobs/123456"
}
```

## Optional flags

```bash
python3 main.py "Datadog" "Software Engineer" --pdf plan.pdf
python3 main.py "Figma" "Frontend Engineer" --job-url "https://boards.greenhouse.io/figma/jobs/1234567"
python3 main.py "Acme" "Backend Engineer" --job-file sample_job.txt
```

## Deploy on Vercel

Vercel’s Python backend detection expects a recognized Python entrypoint. This repo now exports a FastAPI `app` from `api/main.py`, which is the shape Vercel’s current Python backend flow recognizes most reliably. `vercel.json` and `.python-version` are included for routing and version parity.

### One-time setup

```bash
npm i -g vercel
vercel link
```

### Local test

```bash
vercel dev
```

Then open:

```bash
http://localhost:3000/?company=Stripe&role=Junior%20Software%20Engineer
```

Health check:

```bash
http://localhost:3000/health
```

API test:

```bash
http://localhost:3000/api/generate?company=Stripe&role=Junior%20Software%20Engineer
```

If you want to run the API directly without Vercel:

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### Production deploy

```bash
vercel deploy --prod
```

If GitHub is already connected in Vercel, every push to `main` will automatically trigger a new production deployment.

## Deploy on Netlify

Netlify’s current Functions docs emphasize Node.js, TypeScript, and Go runtimes rather than native Python functions, so the fastest reliable setup is:

1. Deploy the Python API to Vercel.
2. Let Netlify proxy `/api` requests to that Vercel URL using the included `netlify.toml` and `netlify/functions/main.mjs`.
3. Set `VERCEL_BACKEND_URL` in Netlify to your Vercel production URL, for example `https://short-ai-project.vercel.app/`.

### One-time setup

```bash
npm i -g netlify-cli
netlify init
```

### Local test

```bash
netlify dev
```

Then call:

```bash
http://localhost:8888/api?company=Stripe&role=Junior%20Software%20Engineer
```

### Production deploy

```bash
netlify deploy --prod
```

If the repo is linked in Netlify and the production branch is `main`, every push to `main` will automatically trigger a new production deploy there as well.

## Common deployment issues

- Public job postings change frequently, so results depend on what is available at runtime.
- Vercel needs a Python file inside `/api`; otherwise it may not recognize the project as a Python serverless app.
- Vercel may also reject the build if the Python entrypoint does not export a recognized app object. `api/main.py` now exports a FastAPI `app` for that reason.
- Missing `requirements.txt` will break dependency installation.
- Missing `VERCEL_BACKEND_URL` on Netlify will cause the Netlify function to return a clear configuration error.
- The tool prefers public ATS pages and structured `JobPosting` metadata when available.
- If no curated resource exists for a detected skill, the app generates a free fallback resource link.
