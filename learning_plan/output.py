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
