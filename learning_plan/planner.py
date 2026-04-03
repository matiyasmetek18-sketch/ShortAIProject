from __future__ import annotations

from typing import List

from .models import (
    ApplicationAssets,
    CapstoneProject,
    FitSignals,
    GapAnalysis,
    InterviewPrep,
    InterviewQuestionSet,
    JobPosting,
    LearningPlan,
    ResumeBullet,
    RoadmapStage,
    SkillPlan,
    WeeklySchedule,
    WeeklySession,
)
from .resource_catalog import resource_bundle, to_resources


def build_learning_plan(
    job: JobPosting,
    skills: List[str],
    current_skills: List[str] | None = None,
    intensity: str = "balanced",
    hours_per_week: int = 8,
) -> LearningPlan:
    skill_plans: List[SkillPlan] = []
    current_skills = current_skills or []
    intensity = _normalize_intensity(intensity)
    hours_per_week = max(2, min(hours_per_week, 30))

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
    gap_analysis = _build_gap_analysis(skill_plans, current_skills)
    roadmap = _build_roadmap(job, skill_plans, gap_analysis, intensity)
    capstone = _build_capstone(job, skill_plans)
    interview_prep = _build_interview_prep(job, skill_plans, gap_analysis)
    resume_bullets = _build_resume_bullets(job, skill_plans, capstone)
    weekly_schedule = _build_weekly_schedule(skill_plans, gap_analysis, intensity, hours_per_week)
    fit_signals = _build_fit_signals(job, skill_plans, gap_analysis)
    application_assets = _build_application_assets(job, skill_plans, capstone, fit_signals)
    interview_bank = _build_interview_bank(skill_plans)
    standout_moves = _build_standout_moves(job, skill_plans, gap_analysis, capstone)
    return LearningPlan(
        job=job,
        summary=summary,
        phases=phases,
        skills=skill_plans,
        gap_analysis=gap_analysis,
        roadmap=roadmap,
        capstone=capstone,
        interview_prep=interview_prep,
        resume_bullets=resume_bullets,
        weekly_schedule=weekly_schedule,
        fit_signals=fit_signals,
        application_assets=application_assets,
        interview_bank=interview_bank,
        standout_moves=standout_moves,
    )


def _normalize_intensity(intensity: str) -> str:
    value = intensity.strip().lower()
    return value if value in {"light", "balanced", "accelerated", "sprint"} else "balanced"


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


def _normalize_skill_name(skill: str) -> str:
    return skill.strip().lower()


def _build_gap_analysis(skill_plans: List[SkillPlan], current_skills: List[str]) -> GapAnalysis:
    current_map = {_normalize_skill_name(skill): skill.strip() for skill in current_skills if skill.strip()}
    matched: List[str] = []
    missing: List[str] = []
    adjacent: List[str] = []

    for plan in skill_plans:
        normalized = _normalize_skill_name(plan.skill)
        if normalized in current_map:
            matched.append(plan.skill)
        else:
            missing.append(plan.skill)
            if plan.category in {"Software Engineering Practice", "Developer Tooling", "Architecture"}:
                adjacent.append(plan.skill)

    total = max(1, len(skill_plans))
    score = round((len(matched) / total) * 100)
    if current_skills:
        narrative = (
            f"You already cover {len(matched)} of the {len(skill_plans)} priority areas. "
            f"Focus first on {', '.join(missing[:3]) or 'the missing skills'} to close the biggest gaps quickly."
        )
    else:
        narrative = (
            "No current skills were provided, so this roadmap assumes you are starting from an early-career baseline "
            "and emphasizes the highest-leverage fundamentals first."
        )

    return GapAnalysis(
        current_skills=current_skills,
        matched_skills=matched,
        missing_skills=missing,
        adjacent_skills=adjacent[:4],
        coverage_score=score,
        narrative=narrative,
    )


def _build_roadmap(
    job: JobPosting, skill_plans: List[SkillPlan], gap_analysis: GapAnalysis, intensity: str
) -> List[RoadmapStage]:
    first_block = [plan.skill for plan in skill_plans[:3]]
    second_block = [plan.skill for plan in skill_plans[3:6]]
    stretch_block = [plan.skill for plan in skill_plans[6:9]]
    pace_note = {
        "light": "at a sustainable pace",
        "balanced": "with a healthy weekly rhythm",
        "accelerated": "with an aggressive but manageable pace",
        "sprint": "with maximum focus for a short window",
    }[intensity]
    return [
        RoadmapStage(
            label="7-day sprint",
            objective=f"Get interview-ready momentum in {', '.join(first_block) or 'core fundamentals'} {pace_note}.",
            deliverables=[
                f"Finish one high-signal tutorial for {first_block[0] if first_block else 'the primary language'}.",
                "Solve 5 targeted coding problems and write brief solution notes.",
                f"Ship one mini project that mirrors a responsibility from {job.company}'s posting.",
            ],
        ),
        RoadmapStage(
            label="30-day buildout",
            objective=f"Turn fundamentals into demonstrable skills across {', '.join(second_block) or 'role execution skills'}.",
            deliverables=[
                "Build a portfolio project with tests, README, and deployment instructions.",
                "Create a weekly study rhythm with 3 coding sessions and 1 mock interview block.",
                f"Write 3 resume bullets that connect your project to the {job.title} role.",
            ],
        ),
        RoadmapStage(
            label="90-day launch plan",
            objective=f"Develop standout evidence in {', '.join(stretch_block) or 'advanced execution and polish'}.",
            deliverables=[
                "Polish one capstone project to production-demo quality.",
                "Run 4 mock interviews covering technical and behavioral topics.",
                f"Apply to {job.company}-like roles with a portfolio and resume tailored to this skill mix.",
            ],
        ),
    ]


def _build_capstone(job: JobPosting, skill_plans: List[SkillPlan]) -> CapstoneProject:
    core_skills = [plan.skill for plan in skill_plans[:4]]
    primary_language = next((plan.skill for plan in skill_plans if plan.category == "Programming Language"), "Python")
    project_title = f"{job.company} Launch Simulator"
    pitch = (
        f"Build a {primary_language}-powered project inspired by the {job.title} role at {job.company}. "
        f"Use it to demonstrate practical ownership of {', '.join(core_skills[:3]) or 'the role requirements'}."
    )
    return CapstoneProject(
        title=project_title,
        pitch=pitch,
        outcomes=[
            "A deployed app or polished local demo with clear setup instructions.",
            "A technical write-up explaining tradeoffs, architecture, and future improvements.",
            "A GitHub repository with issues, milestones, tests, and sample data.",
        ],
        milestones=[
            "Week 1: Define scope, data model, and basic user flow.",
            "Week 2: Implement the core feature set and test the happy path.",
            "Week 3: Add observability, polish, and one impressive extra feature.",
            "Week 4: Record a demo video and tailor the README to the target role.",
        ],
    )


def _build_interview_prep(job: JobPosting, skill_plans: List[SkillPlan], gap_analysis: GapAnalysis) -> InterviewPrep:
    top_skills = [plan.skill for plan in skill_plans[:5]]
    missing = gap_analysis.missing_skills[:3]
    return InterviewPrep(
        technical_focus=[
            f"Be ready to discuss projects involving {skill}." for skill in top_skills[:3]
        ] + [
            "Practice explaining tradeoffs, debugging steps, and testing strategy.",
            "Prepare one strong data structures and algorithms walkthrough."
        ],
        behavioral_focus=[
            f"Why {job.company} and why this {job.title} role?",
            "A story about learning quickly, handling ambiguity, and improving from feedback.",
            "A story about shipping something end to end with clear ownership.",
        ],
        practice_prompts=[
            f"Teach back how you would ramp on {missing[0]} in the first month." if missing else "Explain how you learn unfamiliar tools quickly.",
            "Walk through a project where you made a tradeoff between speed and quality.",
            f"Describe how your capstone maps to the needs of a company like {job.company}.",
        ],
    )


def _build_resume_bullets(job: JobPosting, skill_plans: List[SkillPlan], capstone: CapstoneProject) -> List[ResumeBullet]:
    top = [plan.skill for plan in skill_plans[:4]]
    return [
        ResumeBullet(
            bullet=f"Built {capstone.title}, a project aligned to {job.company}'s {job.title} needs using {', '.join(top[:3])}.",
            evidence="Use metrics such as response time, test count, or feature completion to make this concrete.",
        ),
        ResumeBullet(
            bullet="Designed and documented a realistic engineering workflow with version control, testing, and clear technical tradeoffs.",
            evidence="Reference pull requests, test coverage, or a written architecture note.",
        ),
        ResumeBullet(
            bullet=f"Translated a live job description into a focused learning roadmap and portfolio plan targeting {job.company}-style work.",
            evidence="Show the roadmap, weekly milestones, and finished deliverables in your portfolio.",
        ),
    ]


def _build_standout_moves(
    job: JobPosting,
    skill_plans: List[SkillPlan],
    gap_analysis: GapAnalysis,
    capstone: CapstoneProject,
) -> List[str]:
    return [
        f"Record a 2-minute demo of {capstone.title} and pin it in the GitHub README.",
        f"Write a short engineering memo about how you would extend the project for {job.company}'s scale and constraints.",
        f"Turn {gap_analysis.missing_skills[0] if gap_analysis.missing_skills else skill_plans[0].skill} into a visible proof point with a mini project or blog post.",
        "Bring one before-and-after story: what you lacked, how you learned it, and the evidence that you now own it.",
    ]


def _build_weekly_schedule(
    skill_plans: List[SkillPlan], gap_analysis: GapAnalysis, intensity: str, hours_per_week: int
) -> WeeklySchedule:
    top = [plan.skill for plan in skill_plans[:4]]
    session_count = {
        "light": 3,
        "balanced": 4,
        "accelerated": 5,
        "sprint": 6,
    }[intensity]
    days = ["Monday", "Tuesday", "Thursday", "Saturday", "Sunday", "Wednesday"]
    duration_hours = max(1, round(hours_per_week / session_count))
    sessions: List[WeeklySession] = []

    templates = [
        ("Core skill lab", [f"Study {top[0] if top else 'the main skill'} fundamentals", "Take structured notes", "Finish one guided exercise"]),
        ("Problem-solving block", [f"Solve two problems focused on {top[1] if len(top) > 1 else 'algorithms'}", "Review patterns and mistakes"]),
        ("Build session", [f"Implement one feature using {top[2] if len(top) > 2 else 'role skills'}", "Commit code and update README"]),
        ("Career assets", ["Refine resume bullets", "Practice one interview story", "Log learning wins and gaps"]),
        ("Capstone polish", ["Improve tests, UX, or architecture", "Prepare a quick demo clip or screenshot"]),
        ("Mock interview", ["Do one timed interview round", "Reflect on clarity, tradeoffs, and gaps"]),
    ]

    for index in range(session_count):
        focus, tasks = templates[index]
        sessions.append(
            WeeklySession(
                day=days[index],
                focus=focus,
                duration=f"{duration_hours} hr",
                tasks=tasks,
            )
        )

    missing = ", ".join(gap_analysis.missing_skills[:2]) or "role-specific gaps"
    headline = f"A {hours_per_week}-hour {intensity} schedule focused on closing {missing} while producing visible proof of progress."
    return WeeklySchedule(
        intensity=intensity,
        hours_per_week=hours_per_week,
        headline=headline,
        sessions=sessions,
    )


def _build_fit_signals(job: JobPosting, skill_plans: List[SkillPlan], gap_analysis: GapAnalysis) -> FitSignals:
    strengths = [
        f"The role strongly matches a growth arc in {skill_plans[0].skill}." if skill_plans else "The role is aligned with core software engineering growth.",
        f"You already have traction in {', '.join(gap_analysis.matched_skills[:2])}." if gap_analysis.matched_skills else "The plan starts with foundational skills that are learnable quickly.",
        f"The company context suggests this role values ownership, execution, and practical project work at {job.company}.",
    ]
    risks = [
        f"Closing the gap in {gap_analysis.missing_skills[0]} will be important before interviews." if gap_analysis.missing_skills else "Maintain consistency so your strengths stay sharp.",
        "If scraping is incomplete, use the pasted job description mode for the clearest output.",
        "You will need visible portfolio evidence, not just coursework, to stand out.",
    ]
    company_signal = (
        job.company_summary
        or f"{job.company} appears to value engineers who can ramp quickly, collaborate well, and ship production-quality work."
    )
    hiring_story = (
        f"The strongest story for this {job.title} application is: you identified the exact skills {job.company} wants, "
        "closed the highest-risk gaps deliberately, and built proof through a capstone and crisp interview narratives."
    )
    return FitSignals(
        strengths=strengths,
        risks=risks,
        company_signal=company_signal,
        hiring_story=hiring_story,
    )


def _build_application_assets(
    job: JobPosting, skill_plans: List[SkillPlan], capstone: CapstoneProject, fit_signals: FitSignals
) -> ApplicationAssets:
    top_skills = ", ".join(plan.skill for plan in skill_plans[:3]) or "core engineering skills"
    elevator_pitch = (
        f"I'm an early-career engineer targeting {job.title} roles, and I built {capstone.title} to prove I can contribute in "
        f"{top_skills}. I like turning ambiguous requirements into clean, tested work and I’m especially excited about how {job.company} operates."
    )
    outreach_note = (
        f"Hi, I’m exploring {job.title} opportunities at {job.company}. I used one of your role descriptions to build a focused learning roadmap "
        f"and a capstone project called {capstone.title}. I’d love to share the demo and hear what early-career candidates do especially well in your process."
    )
    portfolio_headline = f"{job.title} candidate building company-specific proof of work for teams like {job.company}"
    return ApplicationAssets(
        elevator_pitch=elevator_pitch,
        outreach_note=outreach_note,
        portfolio_headline=portfolio_headline,
    )


def _build_interview_bank(skill_plans: List[SkillPlan]) -> List[InterviewQuestionSet]:
    bank: List[InterviewQuestionSet] = []
    for plan in skill_plans[:4]:
        bank.append(
            InterviewQuestionSet(
                topic=plan.skill,
                questions=[
                    f"How have you used {plan.skill} in a project, and what tradeoffs did you make?",
                    f"What would a beginner usually misunderstand about {plan.skill}, and how would you explain it clearly?",
                    f"If you had one week to improve your {plan.skill} skills for an interview, what would you build or practice first?",
                ],
            )
        )
    return bank
