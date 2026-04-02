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
      --bg: #f5efe7;
      --paper: rgba(255, 250, 244, 0.86);
      --paper-strong: #fffaf4;
      --ink: #172033;
      --muted: #667085;
      --line: rgba(78, 61, 44, 0.12);
      --amber: #d97706;
      --amber-deep: #b45309;
      --teal: #0f766e;
      --rose: #9f1239;
      --shadow: 0 30px 80px rgba(54, 33, 17, 0.12);
      --radius-xl: 30px;
      --radius-lg: 22px;
      --radius-md: 16px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(217, 119, 6, 0.18), transparent 24%),
        radial-gradient(circle at 80% 10%, rgba(15, 118, 110, 0.12), transparent 22%),
        radial-gradient(circle at bottom right, rgba(159, 18, 57, 0.08), transparent 28%),
        linear-gradient(180deg, #fff8f2 0%, var(--bg) 100%);
      min-height: 100vh;
    }

    .shell {
      max-width: 1320px;
      margin: 0 auto;
      padding: 28px 20px 64px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 18px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .mark {
      width: 44px;
      height: 44px;
      border-radius: 14px;
      display: grid;
      place-items: center;
      font-weight: 800;
      color: white;
      background: linear-gradient(135deg, var(--amber), var(--teal));
      box-shadow: 0 12px 28px rgba(15, 118, 110, 0.2);
    }

    .brand h1 {
      margin: 0;
      font-size: 20px;
      letter-spacing: -0.03em;
    }

    .brand p, .topbar span {
      margin: 2px 0 0;
      color: var(--muted);
      font-size: 13px;
    }

    .hero {
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 24px;
      margin-top: 14px;
    }

    .panel {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }

    .hero-copy {
      padding: 36px;
      position: relative;
      overflow: hidden;
    }

    .hero-copy::before {
      content: "";
      position: absolute;
      inset: auto -50px -60px auto;
      width: 220px;
      height: 220px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(217, 119, 6, 0.16), transparent 70%);
    }

    .eyebrow {
      display: inline-flex;
      gap: 8px;
      align-items: center;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.78);
      border: 1px solid var(--line);
      color: var(--teal);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    .hero-copy h2 {
      margin: 18px 0 14px;
      font-size: clamp(44px, 7vw, 78px);
      line-height: 0.92;
      letter-spacing: -0.05em;
      max-width: 10ch;
    }

    .lede {
      max-width: 60ch;
      font-size: 18px;
      line-height: 1.65;
      color: var(--muted);
    }

    .hero-stats {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 26px;
    }

    .stat {
      padding: 18px;
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.7);
      border: 1px solid var(--line);
    }

    .stat strong {
      display: block;
      font-size: 28px;
      letter-spacing: -0.05em;
      margin-bottom: 6px;
    }

    .stat span {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }

    .hero-form {
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 14px;
    }

    .card-head h3 {
      margin: 0;
      font-size: 28px;
      letter-spacing: -0.03em;
    }

    .card-head span {
      color: var(--muted);
      font-size: 13px;
    }

    form {
      display: grid;
      gap: 14px;
    }

    .split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }

    label {
      display: grid;
      gap: 8px;
      font-weight: 700;
      font-size: 14px;
    }

    input, textarea {
      width: 100%;
      border-radius: 14px;
      border: 1px solid rgba(78, 61, 44, 0.16);
      background: rgba(255, 255, 255, 0.92);
      padding: 14px 16px;
      color: var(--ink);
      font: inherit;
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    input:focus, textarea:focus {
      outline: none;
      transform: translateY(-1px);
      border-color: rgba(217, 119, 6, 0.5);
      box-shadow: 0 0 0 4px rgba(217, 119, 6, 0.1);
    }

    textarea {
      min-height: 112px;
      resize: vertical;
    }

    .helper {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      margin-top: -2px;
    }

    .button-row, .chip-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    button {
      border: 0;
      border-radius: 999px;
      padding: 14px 20px;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
      transition: transform 0.2s ease, opacity 0.2s ease;
    }

    button:hover { transform: translateY(-1px); }
    button:disabled { opacity: 0.68; cursor: wait; }

    .primary {
      background: linear-gradient(135deg, var(--amber), #f59e0b);
      color: white;
      box-shadow: 0 16px 34px rgba(217, 119, 6, 0.28);
    }

    .secondary, .chip {
      background: rgba(255, 255, 255, 0.8);
      color: var(--ink);
      border: 1px solid var(--line);
    }

    .chip {
      padding: 10px 14px;
      font-size: 13px;
    }

    .status {
      margin-top: 22px;
      display: none;
      padding: 14px 16px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.76);
      border: 1px solid var(--line);
      color: var(--muted);
    }

    .status.visible { display: block; }
    .status.error {
      color: #991b1b;
      background: rgba(255, 241, 242, 0.95);
      border-color: rgba(239, 68, 68, 0.16);
    }

    .results {
      display: none;
      margin-top: 26px;
      gap: 22px;
    }

    .results.visible { display: grid; }

    .summary-grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr 0.9fr 0.9fr;
      gap: 16px;
    }

    .metric, .section, .sticky-card {
      padding: 22px;
      border-radius: var(--radius-lg);
      background: var(--paper);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }

    .metric h4, .section h4, .sticky-card h4 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: -0.03em;
    }

    .metric strong {
      display: block;
      font-size: 42px;
      letter-spacing: -0.06em;
      margin-bottom: 8px;
    }

    .metric p, .section p, .sticky-card p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
    }

    .layout {
      display: grid;
      grid-template-columns: 330px 1fr;
      gap: 22px;
      align-items: start;
    }

    .sticky-wrap {
      display: grid;
      gap: 18px;
      position: sticky;
      top: 18px;
    }

    .stack {
      display: grid;
      gap: 18px;
    }

    .pill-list, .timeline, .bullet-list, .skill-grid {
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .pill {
      display: inline-flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      border-radius: 999px;
      width: fit-content;
      background: rgba(255, 255, 255, 0.82);
      border: 1px solid var(--line);
      margin: 0 8px 8px 0;
      font-size: 13px;
    }

    .timeline-card, .bullet-card, .skill-card {
      padding: 18px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.76);
      border: 1px solid var(--line);
    }

    .timeline-card strong, .bullet-card strong, .skill-card strong {
      display: block;
      margin-bottom: 8px;
      font-size: 16px;
    }

    .mini-list {
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--ink);
      line-height: 1.6;
    }

    .mini-list a {
      color: var(--teal);
      text-decoration: none;
    }

    .mini-list a:hover { text-decoration: underline; }

    .tag {
      display: inline-flex;
      align-items: center;
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(217, 119, 6, 0.12);
      color: var(--amber-deep);
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 10px;
    }

    .banner {
      padding: 18px 20px;
      border-radius: 18px;
      background: linear-gradient(135deg, rgba(15, 118, 110, 0.12), rgba(217, 119, 6, 0.12));
      border: 1px solid rgba(15, 118, 110, 0.12);
      color: var(--ink);
    }

    .footer-note {
      margin-top: 24px;
      text-align: center;
      color: var(--muted);
      font-size: 13px;
    }

    @media (max-width: 1100px) {
      .hero, .layout, .summary-grid { grid-template-columns: 1fr; }
      .sticky-wrap { position: static; }
    }

    @media (max-width: 700px) {
      .split, .hero-stats { grid-template-columns: 1fr; }
      .hero-copy, .hero-form { padding: 22px; }
      .hero-copy h2 { max-width: none; font-size: clamp(38px, 12vw, 62px); }
    }
  </style>
</head>
<body>
  <main class="shell">
    <div class="topbar">
      <div class="brand">
        <div class="mark">LP</div>
        <div>
          <h1>LaunchPlan</h1>
          <p>AI career copilot for early-career software engineers</p>
        </div>
      </div>
      <span>Built for standout demos, fast planning, and real job targeting</span>
    </div>

    <section class="hero">
      <section class="panel hero-copy">
        <div class="eyebrow">Personalized learning, portfolio, and interview prep</div>
        <h2>From job post to offer-ready game plan.</h2>
        <p class="lede">
          LaunchPlan turns a company role into a competitive roadmap: skill gap analysis, 7/30/90-day plan,
          capstone idea, resume bullets, and targeted interview prep. This is the version you show judges.
        </p>
        <div class="hero-stats">
          <div class="stat">
            <strong>7/30/90</strong>
            <span>Structured timeline that feels concrete, not generic.</span>
          </div>
          <div class="stat">
            <strong>Gap-aware</strong>
            <span>Compares the job against what the candidate already knows.</span>
          </div>
          <div class="stat">
            <strong>Portfolio-ready</strong>
            <span>Outputs a role-specific capstone and resume talking points.</span>
          </div>
        </div>
      </section>

      <section class="panel hero-form">
        <div class="card-head">
          <h3>Build your plan</h3>
          <span>Best demo path: paste the job description</span>
        </div>
        <form id="plan-form">
          <div class="split">
            <label>
              Company
              <input id="company" placeholder="Stripe" required>
            </label>
            <label>
              Job title
              <input id="role" placeholder="Junior Software Engineer" required>
            </label>
          </div>

          <label>
            Current skills
            <input id="current_skills" placeholder="Python, Git, SQL, React">
            <span class="helper">Comma-separated. This powers the gap analysis and personalized learning order.</span>
          </label>

          <label>
            Public job posting URL
            <input id="job_url" placeholder="https://boards.greenhouse.io/...">
          </label>

          <label>
            Or paste a job description
            <textarea id="job_text" placeholder="Paste the role here for the most reliable demo experience."></textarea>
          </label>

          <div class="button-row">
            <button class="primary" id="submit-btn" type="submit">Generate winner-mode plan</button>
            <button class="secondary" id="demo-btn" type="button">Load polished demo</button>
          </div>
        </form>

        <div class="chip-row">
          <button class="chip" type="button" data-company="Stripe" data-role="Junior Software Engineer" data-skills="Python, Git, SQL">Payments backend</button>
          <button class="chip" type="button" data-company="Figma" data-role="Frontend Engineer" data-skills="JavaScript, TypeScript, React">Frontend product</button>
          <button class="chip" type="button" data-company="Datadog" data-role="Backend Engineer" data-skills="Python, Docker, AWS">Infra platform</button>
        </div>
      </section>
    </section>

    <div class="status" id="status"></div>

    <section class="results" id="results">
      <section class="summary-grid">
        <article class="metric">
          <h4>Target role</h4>
          <strong id="metric-role">-</strong>
          <p id="metric-company">Select a company and role to generate a tailored roadmap.</p>
        </article>
        <article class="metric">
          <h4>Coverage score</h4>
          <strong id="metric-coverage">0%</strong>
          <p>How much of the target skill set you already cover.</p>
        </article>
        <article class="metric">
          <h4>Focus areas</h4>
          <strong id="metric-skills">0</strong>
          <p>High-priority skills extracted from the job posting.</p>
        </article>
        <article class="metric">
          <h4>Demo value</h4>
          <strong>High</strong>
          <p>Capstone, resume bullets, and interview prep are included automatically.</p>
        </article>
      </section>

      <section class="layout">
        <aside class="sticky-wrap">
          <article class="sticky-card">
            <h4>Gap snapshot</h4>
            <p id="gap-narrative">Your gap analysis will appear here.</p>
            <div id="gap-pills"></div>
          </article>

          <article class="sticky-card">
            <h4>Standout moves</h4>
            <div class="pill-list" id="standout-list"></div>
          </article>
        </aside>

        <section class="stack">
          <article class="section">
            <div class="tag">Executive summary</div>
            <h4>Why this role and roadmap fit together</h4>
            <p id="summary-copy">Generate a plan to see your tailored story.</p>
          </article>

          <article class="section">
            <div class="tag">7 / 30 / 90 day roadmap</div>
            <h4>Time-boxed milestones that feel concrete</h4>
            <div class="timeline" id="roadmap"></div>
          </article>

          <article class="section">
            <div class="tag">Capstone project</div>
            <h4 id="capstone-title">A company-aligned proof of work</h4>
            <p id="capstone-pitch">Your capstone recommendation will appear here.</p>
            <div class="banner" id="capstone-outcomes"></div>
            <ul class="mini-list" id="capstone-milestones"></ul>
          </article>

          <article class="section">
            <div class="tag">Interview prep</div>
            <h4>What to practice before you apply</h4>
            <div class="split">
              <div>
                <strong>Technical</strong>
                <ul class="mini-list" id="technical-focus"></ul>
              </div>
              <div>
                <strong>Behavioral</strong>
                <ul class="mini-list" id="behavioral-focus"></ul>
              </div>
            </div>
            <strong style="display:block;margin-top:16px;">Practice prompts</strong>
            <ul class="mini-list" id="practice-prompts"></ul>
          </article>

          <article class="section">
            <div class="tag">Resume bullets</div>
            <h4>Talking points that sell your growth</h4>
            <div class="bullet-list" id="resume-bullets"></div>
          </article>

          <article class="section">
            <div class="tag">Skill roadmap</div>
            <h4>What to learn, in what order, and how to practice</h4>
            <div class="skill-grid" id="skills"></div>
          </article>
        </section>
      </section>
    </section>

    <p class="footer-note">For a live demo, pasted job descriptions are the most reliable because they remove scraping variance.</p>
  </main>

  <script>
    const statusBox = document.getElementById("status");
    const results = document.getElementById("results");
    const submitBtn = document.getElementById("submit-btn");
    const companyInput = document.getElementById("company");
    const roleInput = document.getElementById("role");
    const currentSkillsInput = document.getElementById("current_skills");
    const jobUrlInput = document.getElementById("job_url");
    const jobTextInput = document.getElementById("job_text");

    function asList(value) {
      return value ? value.split(",").map((item) => item.trim()).filter(Boolean) : [];
    }

    function setStatus(message, type = "info") {
      statusBox.textContent = message;
      statusBox.className = "status visible" + (type === "error" ? " error" : "");
    }

    function clearStatus() {
      statusBox.textContent = "";
      statusBox.className = "status";
    }

    function renderPills(rootId, items, tone = "default", append = false) {
      const root = document.getElementById(rootId);
      if (!append) {
        root.innerHTML = "";
      }
      items.forEach((item) => {
        const pill = document.createElement("span");
        pill.className = "pill";
        if (tone === "alert") {
          pill.style.background = "rgba(159, 18, 57, 0.08)";
          pill.style.color = "var(--rose)";
        }
        if (tone === "good") {
          pill.style.background = "rgba(15, 118, 110, 0.1)";
          pill.style.color = "var(--teal)";
        }
        pill.textContent = item;
        root.appendChild(pill);
      });
    }

    function renderRoadmap(stages) {
      const root = document.getElementById("roadmap");
      root.innerHTML = "";
      stages.forEach((stage) => {
        const card = document.createElement("article");
        card.className = "timeline-card";
        card.innerHTML = `<strong>${stage.label}</strong><p>${stage.objective}</p>`;
        const list = document.createElement("ul");
        list.className = "mini-list";
        stage.deliverables.forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          list.appendChild(li);
        });
        card.appendChild(list);
        root.appendChild(card);
      });
    }

    function renderSimpleList(rootId, items) {
      const root = document.getElementById(rootId);
      root.innerHTML = "";
      items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        root.appendChild(li);
      });
    }

    function renderResumeBullets(items) {
      const root = document.getElementById("resume-bullets");
      root.innerHTML = "";
      items.forEach((item) => {
        const card = document.createElement("article");
        card.className = "bullet-card";
        card.innerHTML = `<strong>${item.bullet}</strong><p>${item.evidence}</p>`;
        root.appendChild(card);
      });
    }

    function renderSkills(skills) {
      const root = document.getElementById("skills");
      root.innerHTML = "";
      skills.forEach((skill) => {
        const resources = skill.resources
          .map((resource) => `<li><a href="${resource.url}" target="_blank" rel="noreferrer">${resource.title}</a> · ${resource.kind} · ${resource.estimated_time}</li>`)
          .join("");
        const exercises = skill.exercises.map((exercise) => `<li>${exercise}</li>`).join("");
        const card = document.createElement("article");
        card.className = "skill-card";
        card.innerHTML = `
          <div class="tag">${skill.category}</div>
          <strong>${skill.priority}. ${skill.skill}</strong>
          <p>${skill.reason}</p>
          <ul class="mini-list">${resources}</ul>
          <ul class="mini-list">${exercises}</ul>
        `;
        root.appendChild(card);
      });
    }

    function renderPlan(plan) {
      document.getElementById("metric-role").textContent = plan.job.title;
      document.getElementById("metric-company").textContent = plan.job.company;
      document.getElementById("metric-coverage").textContent = `${plan.gap_analysis.coverage_score}%`;
      document.getElementById("metric-skills").textContent = String(plan.skills.length);
      document.getElementById("summary-copy").textContent = plan.summary;
      document.getElementById("gap-narrative").textContent = plan.gap_analysis.narrative;

      const gapRoot = document.getElementById("gap-pills");
      gapRoot.innerHTML = "";
      renderPills("gap-pills", plan.gap_analysis.matched_skills.slice(0, 4), "good");
      renderPills("gap-pills", plan.gap_analysis.missing_skills.slice(0, 4), "alert", true);

      const standoutRoot = document.getElementById("standout-list");
      standoutRoot.innerHTML = "";
      plan.standout_moves.forEach((move) => {
        const pill = document.createElement("div");
        pill.className = "pill";
        pill.style.width = "100%";
        pill.style.borderRadius = "16px";
        pill.style.padding = "12px 14px";
        pill.textContent = move;
        standoutRoot.appendChild(pill);
      });

      renderRoadmap(plan.roadmap);
      document.getElementById("capstone-title").textContent = plan.capstone.title;
      document.getElementById("capstone-pitch").textContent = plan.capstone.pitch;
      document.getElementById("capstone-outcomes").innerHTML = "<strong>Expected outcomes</strong><ul class='mini-list'>" +
        plan.capstone.outcomes.map((item) => `<li>${item}</li>`).join("") + "</ul>";
      renderSimpleList("capstone-milestones", plan.capstone.milestones);
      renderSimpleList("technical-focus", plan.interview_prep.technical_focus);
      renderSimpleList("behavioral-focus", plan.interview_prep.behavioral_focus);
      renderSimpleList("practice-prompts", plan.interview_prep.practice_prompts);
      renderResumeBullets(plan.resume_bullets);
      renderSkills(plan.skills);
      results.classList.add("visible");
      results.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    async function submitPlan(payload) {
      submitBtn.disabled = true;
      setStatus("Generating a competition-ready roadmap...");
      try {
        const response = await fetch("/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || data.error || "Unable to generate the plan.");
        }
        clearStatus();
        renderPlan(data);
      } catch (error) {
        setStatus(error.message || "Unable to generate the plan.", "error");
      } finally {
        submitBtn.disabled = false;
      }
    }

    document.getElementById("plan-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitPlan({
        company: companyInput.value,
        role: roleInput.value,
        job_url: jobUrlInput.value || null,
        job_text: jobTextInput.value || null,
        current_skills: asList(currentSkillsInput.value),
      });
    });

    document.getElementById("demo-btn").addEventListener("click", async () => {
      companyInput.value = "Stripe";
      roleInput.value = "Junior Software Engineer";
      currentSkillsInput.value = "Python, Git, SQL";
      jobUrlInput.value = "";
      jobTextInput.value = "We are hiring a Junior Software Engineer with experience in Python, SQL, REST APIs, Git, testing, AWS, and strong problem solving. You will build backend services, contribute to internal tools, collaborate across teams, write clean code, work with PostgreSQL, and apply data structures and algorithms in production settings.";
      await submitPlan({
        company: companyInput.value,
        role: roleInput.value,
        job_text: jobTextInput.value,
        current_skills: asList(currentSkillsInput.value),
      });
    });

    document.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        companyInput.value = chip.dataset.company || "";
        roleInput.value = chip.dataset.role || "";
        currentSkillsInput.value = chip.dataset.skills || "";
      });
    });
  </script>
</body>
</html>"""
