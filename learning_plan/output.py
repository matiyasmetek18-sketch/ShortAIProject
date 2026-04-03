from __future__ import annotations

from pathlib import Path
from textwrap import fill

from .models import LearningPlan


def render_console(plan: LearningPlan) -> str:
    lines = [
        f"Company: {plan.job.company}",
        f"Role: {plan.job.title}",
        f"Source: {plan.job.url or plan.job.source}",
        "",
        "Summary",
        fill(plan.summary, width=100),
        "",
        "Recommended Learning Order",
    ]
    for phase in plan.phases:
        lines.append(f"- {phase}")

    lines.extend(
        [
            "",
            "Gap Analysis",
            f"- Coverage score: {plan.gap_analysis.coverage_score}%",
            f"- Current strengths: {', '.join(plan.gap_analysis.matched_skills) or 'Not provided yet'}",
            f"- Priority gaps: {', '.join(plan.gap_analysis.missing_skills[:5]) or 'None detected'}",
            f"- Narrative: {plan.gap_analysis.narrative}",
            "",
            f"Weekly Execution Plan ({plan.weekly_schedule.intensity}, {plan.weekly_schedule.hours_per_week} hrs/week)",
            f"- {plan.weekly_schedule.headline}",
        ]
    )
    for session in plan.weekly_schedule.sessions:
        lines.append(f"- {session.day}: {session.focus} ({session.duration})")
        for task in session.tasks:
            lines.append(f"  - {task}")

    lines.extend(
        [
            "",
            "7 / 30 / 90 Day Roadmap",
        ]
    )
    for stage in plan.roadmap:
        lines.append(f"- {stage.label}: {stage.objective}")
        for deliverable in stage.deliverables:
            lines.append(f"  - {deliverable}")

    lines.extend(
        [
            "",
            f"Capstone Project: {plan.capstone.title}",
            fill(plan.capstone.pitch, width=100),
        ]
    )
    for milestone in plan.capstone.milestones:
        lines.append(f"- {milestone}")

    lines.extend(["", "Fit Signals", f"- Company signal: {plan.fit_signals.company_signal}", f"- Hiring story: {plan.fit_signals.hiring_story}"])
    for item in plan.fit_signals.strengths:
        lines.append(f"- Strength: {item}")
    for item in plan.fit_signals.risks:
        lines.append(f"- Risk: {item}")

    lines.extend(["", "Application Assets", f"- Elevator pitch: {plan.application_assets.elevator_pitch}", f"- Outreach note: {plan.application_assets.outreach_note}", f"- Portfolio headline: {plan.application_assets.portfolio_headline}"])

    lines.append("")
    lines.append("Skill-by-Skill Plan")
    for item in plan.skills:
        lines.extend(
            [
                f"{item.priority}. {item.skill} ({item.category})",
                f"   Time: {item.estimated_time}",
                f"   Why: {fill(item.reason, width=90, subsequent_indent='   ')}",
                "   Free resources:",
            ]
        )
        for resource in item.resources:
            lines.append(f"   - {resource.title} [{resource.kind}] - {resource.url}")
        lines.append("   Practice:")
        for exercise in item.exercises:
            lines.append(f"   - {exercise}")
        lines.append("")
    return "\n".join(lines)


def render_markdown(plan: LearningPlan) -> str:
    lines = [
        f"# Learning Plan for {plan.job.title} at {plan.job.company}",
        "",
        f"- Source: {plan.job.url or plan.job.source}",
        f"- Location: {plan.job.location or 'Not specified'}",
        "",
        "## Summary",
        plan.summary,
        "",
        "## Learning Order",
    ]
    for phase in plan.phases:
        lines.append(f"- {phase}")

    lines.extend(
        [
            "",
            "## Gap Analysis",
            f"- Coverage score: {plan.gap_analysis.coverage_score}%",
            f"- Current strengths: {', '.join(plan.gap_analysis.matched_skills) or 'Not provided yet'}",
            f"- Priority gaps: {', '.join(plan.gap_analysis.missing_skills[:5]) or 'None detected'}",
            f"- Guidance: {plan.gap_analysis.narrative}",
            "",
            "## Weekly Execution Plan",
            f"- Intensity: {plan.weekly_schedule.intensity}",
            f"- Hours per week: {plan.weekly_schedule.hours_per_week}",
            f"- Headline: {plan.weekly_schedule.headline}",
            "",
            "## 7 / 30 / 90 Day Roadmap",
        ]
    )
    for session in plan.weekly_schedule.sessions:
        lines.append(f"### {session.day}: {session.focus} ({session.duration})")
        for task in session.tasks:
            lines.append(f"- {task}")
        lines.append("")

    for stage in plan.roadmap:
        lines.append(f"### {stage.label}")
        lines.append(stage.objective)
        for deliverable in stage.deliverables:
            lines.append(f"- {deliverable}")
        lines.append("")

    lines.extend(
        [
            "## Capstone Project",
            f"### {plan.capstone.title}",
            plan.capstone.pitch,
            "",
            "#### Outcomes",
        ]
    )
    for outcome in plan.capstone.outcomes:
        lines.append(f"- {outcome}")
    lines.append("")
    lines.append("#### Milestones")
    for milestone in plan.capstone.milestones:
        lines.append(f"- {milestone}")

    lines.extend(["", "## Interview Prep"])
    for item in plan.interview_prep.technical_focus:
        lines.append(f"- Technical: {item}")
    for item in plan.interview_prep.behavioral_focus:
        lines.append(f"- Behavioral: {item}")
    for item in plan.interview_prep.practice_prompts:
        lines.append(f"- Prompt: {item}")

    lines.extend(["", "## Interview Bank"])
    for topic in plan.interview_bank:
        lines.append(f"### {topic.topic}")
        for question in topic.questions:
            lines.append(f"- {question}")
        lines.append("")

    lines.extend(["## Fit Signals", f"- Company signal: {plan.fit_signals.company_signal}", f"- Hiring story: {plan.fit_signals.hiring_story}"])
    for item in plan.fit_signals.strengths:
        lines.append(f"- Strength: {item}")
    for item in plan.fit_signals.risks:
        lines.append(f"- Risk: {item}")

    lines.extend(["", "## Application Assets", f"- Elevator pitch: {plan.application_assets.elevator_pitch}", f"- Outreach note: {plan.application_assets.outreach_note}", f"- Portfolio headline: {plan.application_assets.portfolio_headline}"])

    lines.extend(["", "## Resume Bullets"])
    for item in plan.resume_bullets:
        lines.append(f"- {item.bullet}")
        lines.append(f"  - Evidence to add: {item.evidence}")

    lines.extend(["", "## Standout Moves"])
    for move in plan.standout_moves:
        lines.append(f"- {move}")

    lines.append("")
    lines.append("## Skill-by-Skill Plan")
    for item in plan.skills:
        lines.extend(
            [
                f"### {item.priority}. {item.skill}",
                f"- Category: {item.category}",
                f"- Estimated time: {item.estimated_time}",
                f"- Why it matters: {item.reason}",
                "- Free resources:",
            ]
        )
        for resource in item.resources:
            lines.append(f"  - [{resource.title}]({resource.url}) ({resource.kind})")
        lines.append("- Suggested exercises:")
        for exercise in item.exercises:
            lines.append(f"  - {exercise}")
        lines.append("")
    return "\n".join(lines)


def save_markdown(plan: LearningPlan, path: str) -> Path:
    target = Path(path)
    target.write_text(render_markdown(plan), encoding="utf-8")
    return target


def save_pdf(plan: LearningPlan, path: str) -> Path:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    target = Path(path)
    pdf = canvas.Canvas(str(target), pagesize=letter)
    width, height = letter
    y = height - 50

    def write_line(text: str, font: str = "Helvetica", size: int = 10) -> None:
        nonlocal y
        if y < 60:
            pdf.showPage()
            y = height - 50
        pdf.setFont(font, size)
        pdf.drawString(40, y, text[:110])
        y -= 14

    write_line(f"Learning Plan for {plan.job.title} at {plan.job.company}", "Helvetica-Bold", 14)
    write_line(f"Source: {plan.job.url or plan.job.source}")
    write_line("")
    for paragraph in [plan.summary, *plan.phases]:
        for line in fill(paragraph, width=95).splitlines():
            write_line(line)
        write_line("")
    for item in plan.skills:
        write_line(f"{item.priority}. {item.skill} [{item.category}]", "Helvetica-Bold", 11)
        write_line(f"Estimated time: {item.estimated_time}")
        for resource in item.resources:
            write_line(f"Resource: {resource.title} ({resource.kind})")
            write_line(resource.url)
        for exercise in item.exercises:
            write_line(f"Exercise: {exercise}")
        write_line("")

    pdf.save()
    return target
