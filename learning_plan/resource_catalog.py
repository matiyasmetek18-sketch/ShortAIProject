from __future__ import annotations

from typing import Dict, List
from urllib.parse import quote_plus

from .models import Resource


RESOURCE_CATALOG: Dict[str, dict] = {
    "Python": {
        "category": "Programming Language",
        "estimated_time": "2-3 weeks",
        "resources": [
            ("Python Official Tutorial", "https://docs.python.org/3/tutorial/", "documentation"),
            ("freeCodeCamp Python Course", "https://www.youtube.com/watch?v=eWRfhZUzrAc", "video"),
        ],
        "exercises": [
            "Build a CLI that reads and filters JSON data.",
            "Solve 20 beginner scripting problems involving files, loops, and functions.",
        ],
    },
    "Java": {
        "category": "Programming Language",
        "estimated_time": "2-3 weeks",
        "resources": [
            ("Dev.java Learn", "https://dev.java/learn/", "documentation"),
            ("Helsinki Java Programming MOOC", "https://java-programming.mooc.fi/", "course"),
        ],
        "exercises": [
            "Build a small REST API or console app in Java.",
            "Practice object-oriented design with classes for a library or task manager.",
        ],
    },
    "JavaScript": {
        "category": "Programming Language",
        "estimated_time": "2 weeks",
        "resources": [
            ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "documentation"),
            ("JavaScript.info", "https://javascript.info/", "tutorial"),
        ],
        "exercises": [
            "Create a browser app with form validation and API calls.",
            "Implement array, object, and async programming exercises.",
        ],
    },
    "TypeScript": {
        "category": "Programming Language",
        "estimated_time": "1 week",
        "resources": [
            ("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html", "documentation"),
            ("Total TypeScript Beginner Concepts", "https://www.totaltypescript.com/tutorials/beginners-typescript", "tutorial"),
        ],
        "exercises": [
            "Convert a JavaScript project to TypeScript with strict mode enabled.",
            "Model API request and response types for a small app.",
        ],
    },
    "React": {
        "category": "Frontend Framework",
        "estimated_time": "1-2 weeks",
        "resources": [
            ("React Learn", "https://react.dev/learn", "documentation"),
            ("Scrimba Learn React for Free", "https://scrimba.com/learn/learnreact", "course"),
        ],
        "exercises": [
            "Build a dashboard that fetches and filters API data.",
            "Create a multi-step form with validation and reusable components.",
        ],
    },
    "SQL": {
        "category": "Database",
        "estimated_time": "1 week",
        "resources": [
            ("SQLBolt", "https://sqlbolt.com/", "tutorial"),
            ("PostgreSQL Tutorial", "https://www.postgresqltutorial.com/", "tutorial"),
        ],
        "exercises": [
            "Design a schema for a simple product catalog and write CRUD queries.",
            "Solve 25 SQL practice questions involving joins and aggregations.",
        ],
    },
    "PostgreSQL": {
        "category": "Database",
        "estimated_time": "4-6 days",
        "resources": [
            ("PostgreSQL Documentation", "https://www.postgresql.org/docs/", "documentation"),
            ("PostgreSQL Tutorial", "https://www.postgresqltutorial.com/", "tutorial"),
        ],
        "exercises": [
            "Create tables, indexes, and migrations for a sample app.",
            "Profile a slow query and improve it with indexing.",
        ],
    },
    "Git": {
        "category": "Developer Tooling",
        "estimated_time": "2-3 days",
        "resources": [
            ("Pro Git", "https://git-scm.com/book/en/v2", "book"),
            ("Learn Git Branching", "https://learngitbranching.js.org/", "interactive"),
        ],
        "exercises": [
            "Practice branching, rebasing, resolving conflicts, and pull-request workflows.",
            "Track a personal project using feature branches and clear commits.",
        ],
    },
    "Docker": {
        "category": "Developer Tooling",
        "estimated_time": "3-5 days",
        "resources": [
            ("Docker Overview", "https://docs.docker.com/get-started/docker-overview/", "documentation"),
            ("Docker Curriculum", "https://docker-curriculum.com/", "tutorial"),
        ],
        "exercises": [
            "Containerize a web app with a database dependency.",
            "Write a `docker-compose.yml` file for a local development stack.",
        ],
    },
    "REST APIs": {
        "category": "Backend Concept",
        "estimated_time": "4-5 days",
        "resources": [
            ("MDN Web APIs and HTTP", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Client-Server_overview", "documentation"),
            ("Build a REST API with FastAPI", "https://fastapi.tiangolo.com/tutorial/", "tutorial"),
        ],
        "exercises": [
            "Design and build CRUD endpoints for a small product or note service.",
            "Add validation, pagination, and error handling to an API.",
        ],
    },
    "Data Structures": {
        "category": "Computer Science",
        "estimated_time": "1-2 weeks",
        "resources": [
            ("Open Data Structures", "https://opendatastructures.org/", "book"),
            ("Abdul Bari Data Structures Playlist", "https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ", "video"),
        ],
        "exercises": [
            "Implement arrays, linked lists, stacks, queues, trees, and hash maps.",
            "Solve 20 practice problems focused on choosing the right structure.",
        ],
    },
    "Algorithms": {
        "category": "Computer Science",
        "estimated_time": "1-2 weeks",
        "resources": [
            ("MIT OpenCourseWare Intro to Algorithms", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/", "course"),
            ("NeetCode Roadmap", "https://neetcode.io/roadmap", "practice"),
        ],
        "exercises": [
            "Practice sorting, searching, recursion, graph traversal, and dynamic programming.",
            "Solve 3-5 algorithm problems per week and write explanations for each solution.",
        ],
    },
    "Testing": {
        "category": "Software Engineering Practice",
        "estimated_time": "4-5 days",
        "resources": [
            ("Testing Library Docs", "https://testing-library.com/docs/", "documentation"),
            ("pytest Getting Started", "https://docs.pytest.org/en/stable/getting-started.html", "documentation"),
        ],
        "exercises": [
            "Add unit and integration tests to a personal project.",
            "Write tests for edge cases, failures, and input validation.",
        ],
    },
    "System Design": {
        "category": "Architecture",
        "estimated_time": "1 week",
        "resources": [
            ("System Design Primer", "https://github.com/donnemartin/system-design-primer", "github"),
            ("ByteByteGo YouTube Channel", "https://www.youtube.com/@ByteByteGo", "video"),
        ],
        "exercises": [
            "Design a URL shortener or notification service and explain tradeoffs.",
            "Draw component diagrams for a scalable web application.",
        ],
    },
    "Linux": {
        "category": "Developer Tooling",
        "estimated_time": "3-4 days",
        "resources": [
            ("The Linux Command Line", "https://linuxcommand.org/tlcl.php", "book"),
            ("Linux Journey", "https://linuxjourney.com/", "tutorial"),
        ],
        "exercises": [
            "Navigate the shell, manage files, and automate tasks with Bash.",
            "Deploy a sample app to a Linux VM or container.",
        ],
    },
    "AWS": {
        "category": "Cloud",
        "estimated_time": "1 week",
        "resources": [
            ("AWS Skill Builder Free Resources", "https://skillbuilder.aws/", "course"),
            ("AWS Documentation", "https://docs.aws.amazon.com/", "documentation"),
        ],
        "exercises": [
            "Deploy a static site and a small API using free-tier eligible services.",
            "Learn IAM basics, storage, and compute by building a small deployment flow.",
        ],
    },
    "CI/CD": {
        "category": "Developer Tooling",
        "estimated_time": "3-4 days",
        "resources": [
            ("GitHub Actions Docs", "https://docs.github.com/en/actions", "documentation"),
            ("Continuous Delivery with GitHub Actions", "https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions", "tutorial"),
        ],
        "exercises": [
            "Create a pipeline that runs tests and linting on every pull request.",
            "Add deployment automation for a small demo app.",
        ],
    },
}


def resource_bundle(skill: str) -> dict:
    entry = RESOURCE_CATALOG.get(skill)
    if entry:
        return entry
    fallback_url = f"https://www.google.com/search?q={quote_plus(skill + ' free tutorial official documentation')}"
    youtube_url = f"https://www.youtube.com/results?search_query={quote_plus(skill + ' tutorial')}"
    return {
        "category": "Role-Specific Skill",
        "estimated_time": "4-7 days",
        "resources": [
            (f"{skill} official docs or free tutorial search", fallback_url, "search"),
            (f"{skill} YouTube tutorial search", youtube_url, "video"),
        ],
        "exercises": [
            f"Build a small proof-of-concept that uses {skill} in a realistic workflow.",
            f"Write a short project README explaining how and when to use {skill}.",
        ],
    }


def to_resources(skill: str) -> List[Resource]:
    bundle = resource_bundle(skill)
    return [
        Resource(title=title, url=url, kind=kind, estimated_time=bundle["estimated_time"])
        for title, url, kind in bundle["resources"]
    ]
