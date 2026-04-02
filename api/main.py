from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from learning_plan.service import PlanGenerationError, generate_plan, plan_to_dict
from learning_plan.web import render_app_html


class PlanRequest(BaseModel):
    company: str
    role: str
    job_url: str | None = None
    job_text: str | None = None
    current_skills: list[str] | None = None


app = FastAPI(
    title="Personalized Learning Plan API",
    description="Generate a role-specific software engineering learning plan from a public job posting.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_plan(
    company: str,
    role: str,
    job_url: str | None = None,
    job_text: str | None = None,
    current_skills: list[str] | None = None,
) -> dict:
    company = company.strip()
    role = role.strip()
    if not company or not role:
        raise HTTPException(status_code=400, detail='Both "company" and "role" are required.')

    try:
        plan = generate_plan(
            company=company,
            role=role,
            job_url=job_url,
            job_text=job_text,
            current_skills=current_skills,
        )
    except PlanGenerationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {exc}") from exc

    return plan_to_dict(plan)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return render_app_html()


@app.get("/api/generate")
def generate_get(
    company: str,
    role: str,
    job_url: str | None = None,
    job_text: str | None = None,
    current_skills: str | None = None,
) -> dict:
    parsed_skills = [item.strip() for item in current_skills.split(",")] if current_skills else None
    return _build_plan(
        company=company,
        role=role,
        job_url=job_url,
        job_text=job_text,
        current_skills=parsed_skills,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/generate")
def generate_post(request: PlanRequest) -> dict:
    return _build_plan(
        company=request.company,
        role=request.role,
        job_url=request.job_url,
        job_text=request.job_text,
        current_skills=request.current_skills,
    )
