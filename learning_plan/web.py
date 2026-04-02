from __future__ import annotations


def render_app_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LaunchPlan</title>
  <style>
    :root {
      --bg: #f6efe7;
      --surface: rgba(255, 250, 245, 0.82);
      --surface-strong: #fffaf5;
      --ink: #1f2937;
      --muted: #6b7280;
      --line: rgba(120, 93, 70, 0.16);
      --accent: #d97706;
      --accent-dark: #b45309;
      --accent-soft: rgba(217, 119, 6, 0.12);
      --green: #0f766e;
      --shadow: 0 30px 80px rgba(66, 37, 16, 0.12);
      --radius-xl: 28px;
      --radius-lg: 22px;
      --radius-md: 16px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(245, 158, 11, 0.18), transparent 28%),
        radial-gradient(circle at right 20%, rgba(15, 118, 110, 0.14), transparent 24%),
        linear-gradient(180deg, #fcf7f2 0%, var(--bg) 100%);
      min-height: 100vh;
    }

    .shell {
      max-width: 1240px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }

    .hero {
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 24px;
      align-items: stretch;
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }

    .hero-copy {
      padding: 34px;
      position: relative;
      overflow: hidden;
    }

    .hero-copy::after {
      content: "";
      position: absolute;
      right: -40px;
      top: -40px;
      width: 180px;
      height: 180px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(217, 119, 6, 0.18), transparent 66%);
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.72);
      border: 1px solid var(--line);
      color: var(--green);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    h1 {
      margin: 18px 0 14px;
      font-size: clamp(40px, 7vw, 72px);
      line-height: 0.95;
      letter-spacing: -0.04em;
      max-width: 10ch;
    }

    .lede {
      max-width: 58ch;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
      margin-bottom: 28px;
    }

    .feature-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .feature {
      padding: 16px;
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.62);
      border: 1px solid rgba(120, 93, 70, 0.1);
    }

    .feature strong {
      display: block;
      margin-bottom: 6px;
      font-size: 15px;
    }

    .feature span {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }

    .hero-form {
      padding: 28px;
      display: flex;
      flex-direction: column;
    }

    .card-title {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 14px;
      margin-bottom: 20px;
    }

    .card-title h2 {
      margin: 0;
      font-size: 26px;
      letter-spacing: -0.03em;
    }

    .card-title span {
      color: var(--muted);
      font-size: 14px;
    }

    form {
      display: grid;
      gap: 14px;
    }

    label {
      display: grid;
      gap: 8px;
      font-weight: 600;
      font-size: 14px;
    }

    input, textarea {
      width: 100%;
      border: 1px solid rgba(120, 93, 70, 0.18);
      border-radius: 14px;
      padding: 14px 16px;
      font: inherit;
      background: rgba(255, 255, 255, 0.92);
      color: var(--ink);
      transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }

    input:focus, textarea:focus {
      outline: none;
      border-color: rgba(217, 119, 6, 0.55);
      box-shadow: 0 0 0 4px rgba(217, 119, 6, 0.12);
      transform: translateY(-1px);
    }

    textarea {
      min-height: 120px;
      resize: vertical;
    }

    .button-row {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 8px;
    }

    button {
      border: 0;
      border-radius: 999px;
      padding: 14px 20px;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.2s ease, opacity 0.2s ease, box-shadow 0.2s ease;
    }

    button:hover { transform: translateY(-1px); }
    button:disabled { opacity: 0.7; cursor: wait; }

    .primary {
      background: linear-gradient(135deg, var(--accent) 0%, #f59e0b 100%);
      color: white;
      box-shadow: 0 12px 30px rgba(217, 119, 6, 0.28);
    }

    .secondary {
      background: rgba(255, 255, 255, 0.84);
      color: var(--ink);
      border: 1px solid var(--line);
    }

    .examples {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }

    .chip {
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
      color: var(--ink);
      border-radius: 999px;
      padding: 10px 14px;
      font-size: 13px;
      cursor: pointer;
    }

    .content {
      margin-top: 24px;
      display: grid;
      gap: 24px;
    }

    .status {
      padding: 14px 16px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.72);
      border: 1px solid var(--line);
      color: var(--muted);
      display: none;
    }

    .status.visible { display: block; }
    .status.error {
      color: #991b1b;
      background: rgba(254, 242, 242, 0.96);
      border-color: rgba(239, 68, 68, 0.18);
    }

    .results {
      display: none;
      grid-template-columns: 320px 1fr;
      gap: 24px;
      align-items: start;
    }

    .results.visible { display: grid; }

    .summary-card, .details-card {
      padding: 24px;
    }

    .meta {
      display: grid;
      gap: 14px;
    }

    .meta-block {
      padding: 16px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.74);
      border: 1px solid var(--line);
    }

    .meta-block small {
      display: block;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 11px;
      margin-bottom: 8px;
    }

    .phase-list, .skill-list {
      display: grid;
      gap: 14px;
    }

    .phase, .skill {
      padding: 18px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.76);
    }

    .phase strong, .skill strong {
      display: block;
      margin-bottom: 8px;
      font-size: 16px;
    }

    .skill-head {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      margin-bottom: 10px;
    }

    .badge {
      padding: 8px 10px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent-dark);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }

    .skill p, .phase p, .details-card p, .meta-block p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
    }

    .resource-list, .exercise-list {
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--ink);
      line-height: 1.6;
    }

    .resource-list a {
      color: var(--green);
      text-decoration: none;
    }

    .resource-list a:hover { text-decoration: underline; }

    .footer-note {
      margin-top: 28px;
      color: var(--muted);
      font-size: 13px;
      text-align: center;
    }

    @media (max-width: 980px) {
      .hero, .results { grid-template-columns: 1fr; }
      .feature-grid { grid-template-columns: 1fr; }
      h1 { max-width: none; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="panel hero-copy">
        <div class="eyebrow">LaunchPlan for early-career engineers</div>
        <h1>Turn job posts into a real learning roadmap.</h1>
        <p class="lede">
          Pick a company and role, then get a tailored learning plan with free resources, practice ideas,
          and a clear order from fundamentals to production-ready skills.
        </p>
        <div class="feature-grid">
          <div class="feature">
            <strong>Job-specific</strong>
            <span>Built from a real posting or your pasted job description, not a generic template.</span>
          </div>
          <div class="feature">
            <strong>Free resources</strong>
            <span>Prioritizes docs, YouTube, MOOCs, and practical open-source materials.</span>
          </div>
          <div class="feature">
            <strong>Actionable output</strong>
            <span>Every skill includes time estimates and project ideas so you can actually practice.</span>
          </div>
        </div>
      </div>

      <section class="panel hero-form">
        <div class="card-title">
          <h2>Generate a plan</h2>
          <span>Usually takes a few seconds</span>
        </div>
        <form id="plan-form">
          <label>
            Company
            <input id="company" name="company" placeholder="Stripe" required>
          </label>
          <label>
            Job title
            <input id="role" name="role" placeholder="Junior Software Engineer" required>
          </label>
          <label>
            Public job posting URL
            <input id="job_url" name="job_url" placeholder="https://boards.greenhouse.io/...">
          </label>
          <label>
            Or paste a job description
            <textarea id="job_text" name="job_text" placeholder="Paste the full posting here if you want a faster, more reliable plan."></textarea>
          </label>
          <div class="button-row">
            <button class="primary" id="submit-btn" type="submit">Generate learning plan</button>
            <button class="secondary" id="demo-btn" type="button">Try demo data</button>
          </div>
        </form>
        <div class="examples">
          <button class="chip" type="button" data-company="Figma" data-role="Frontend Engineer">Figma Frontend</button>
          <button class="chip" type="button" data-company="Stripe" data-role="Junior Software Engineer">Stripe Junior SWE</button>
          <button class="chip" type="button" data-company="Datadog" data-role="Backend Engineer">Datadog Backend</button>
        </div>
      </section>
    </section>

    <section class="content">
      <div class="status" id="status"></div>

      <section class="results" id="results">
        <aside class="panel summary-card">
          <div class="card-title">
            <h2>Plan snapshot</h2>
            <span id="result-company">Waiting for results</span>
          </div>
          <div class="meta" id="meta"></div>
        </aside>

        <section class="panel details-card">
          <div class="card-title">
            <h2 id="result-title">Your personalized roadmap</h2>
            <span id="skill-count"></span>
          </div>
          <p id="summary-copy">Submit a role to see the customized breakdown.</p>
          <h3>Learning order</h3>
          <div class="phase-list" id="phases"></div>
          <h3>Skill-by-skill plan</h3>
          <div class="skill-list" id="skills"></div>
        </section>
      </section>
    </section>

    <p class="footer-note">Tip: Pasting a job description is the fastest and most reliable path during deployment demos.</p>
  </main>

  <script>
    const form = document.getElementById("plan-form");
    const statusBox = document.getElementById("status");
    const results = document.getElementById("results");
    const submitBtn = document.getElementById("submit-btn");
    const companyInput = document.getElementById("company");
    const roleInput = document.getElementById("role");
    const jobUrlInput = document.getElementById("job_url");
    const jobTextInput = document.getElementById("job_text");

    function setStatus(message, type = "info") {
      statusBox.textContent = message;
      statusBox.className = "status visible" + (type === "error" ? " error" : "");
    }

    function clearStatus() {
      statusBox.className = "status";
      statusBox.textContent = "";
    }

    function renderMeta(plan) {
      const meta = document.getElementById("meta");
      meta.innerHTML = "";

      const blocks = [
        ["Company", plan.job.company],
        ["Role", plan.job.title],
        ["Source", plan.job.url || plan.job.source],
        ["Location", plan.job.location || "Not specified"],
      ];

      blocks.forEach(([label, value]) => {
        const block = document.createElement("div");
        block.className = "meta-block";
        block.innerHTML = `<small>${label}</small><p>${value}</p>`;
        meta.appendChild(block);
      });
    }

    function renderPhases(phases) {
      const phasesRoot = document.getElementById("phases");
      phasesRoot.innerHTML = "";
      phases.forEach((phase, index) => {
        const node = document.createElement("article");
        node.className = "phase";
        node.innerHTML = `<strong>Phase ${index + 1}</strong><p>${phase}</p>`;
        phasesRoot.appendChild(node);
      });
    }

    function renderSkills(skills) {
      const skillsRoot = document.getElementById("skills");
      skillsRoot.innerHTML = "";
      skills.forEach((skill) => {
        const resourceItems = skill.resources
          .map((resource) => `<li><a href="${resource.url}" target="_blank" rel="noreferrer">${resource.title}</a> · ${resource.kind} · ${resource.estimated_time}</li>`)
          .join("");
        const exerciseItems = skill.exercises.map((exercise) => `<li>${exercise}</li>`).join("");

        const node = document.createElement("article");
        node.className = "skill";
        node.innerHTML = `
          <div class="skill-head">
            <strong>${skill.priority}. ${skill.skill}</strong>
            <span class="badge">${skill.category}</span>
          </div>
          <p>${skill.reason}</p>
          <ul class="resource-list">${resourceItems}</ul>
          <ul class="exercise-list">${exerciseItems}</ul>
        `;
        skillsRoot.appendChild(node);
      });
    }

    function renderPlan(plan) {
      document.getElementById("result-company").textContent = plan.job.company;
      document.getElementById("result-title").textContent = `${plan.job.title} roadmap`;
      document.getElementById("summary-copy").textContent = plan.summary;
      document.getElementById("skill-count").textContent = `${plan.skills.length} focus areas`;
      renderMeta(plan);
      renderPhases(plan.phases);
      renderSkills(plan.skills);
      results.classList.add("visible");
    }

    async function submitPlan(payload) {
      submitBtn.disabled = true;
      setStatus("Researching the role and building your plan...");
      try {
        const response = await fetch("/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || data.error || "Request failed.");
        }
        clearStatus();
        renderPlan(data);
      } catch (error) {
        setStatus(error.message || "Something went wrong while generating the plan.", "error");
      } finally {
        submitBtn.disabled = false;
      }
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitPlan({
        company: companyInput.value,
        role: roleInput.value,
        job_url: jobUrlInput.value || null,
        job_text: jobTextInput.value || null
      });
    });

    document.getElementById("demo-btn").addEventListener("click", async () => {
      companyInput.value = "SampleCo";
      roleInput.value = "Junior Software Engineer";
      jobUrlInput.value = "";
      jobTextInput.value = "We are hiring a Junior Software Engineer with experience in Python, SQL, REST APIs, Git, testing, and AWS. You will build backend services, write clean code, work with PostgreSQL, and apply data structures and algorithms.";
      await submitPlan({
        company: companyInput.value,
        role: roleInput.value,
        job_text: jobTextInput.value
      });
    });

    document.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        companyInput.value = chip.dataset.company || "";
        roleInput.value = chip.dataset.role || "";
      });
    });
  </script>
</body>
</html>"""
