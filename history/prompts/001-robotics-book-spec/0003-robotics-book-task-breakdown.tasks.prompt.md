---
id: 0003
title: robotics-book-task-breakdown
stage: tasks
date: 2025-12-07
surface: agent
model: opencode
feature: 001-robotics-book-spec
branch: opencode-ai
user: maaz
command: /sp.tasks
labels: [tasks, robotics-book, implementation, docusaurus]
links:
  spec: /specs/001-robotics-book-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
- /specs/001-robotics-book-spec/tasks.md
tests:
- Constitution compliance validation
- Task dependency verification
- Implementation feasibility check
---

## Prompt

Generate a complete, highly granular task list (70–90 individual tasks) to fully implement robotics book site according to ratified constitution, approved specification, and just-created implementation plan.

MANDATORY RULES (never violate):
- Always stay on existing Git branch "opencode-ai". Never create or switch to any other branch.
- Never recreate the blog folder or any blog plugin.
- Never recreate any dummy Docusaurus pages.

Task breakdown requirements:

1. Configuration & Theming (10–12 tasks)
   - Update docusaurus.config.js with final title, tagline, url, baseUrl
   - Remove blog completely from presets
   - Set themeConfig colors: primary #0066cc (primary), #00d4ff (secondary)
   - Force dark mode as default
   - Configure navbar (only "Book" + GitHub link)
   - Configure minimal footer with copyright + repo link
   - Add favicon (robot head or "PHR" letters)
   - Enable Mermaid plugin
   - Enable local search or Algolia
   - Remove table-of-contents on mobile if needed

2. Sidebar & Navigation (1 big task → auto-generated sidebars.js)
   - Generate perfect nested sidebars.js exactly matching 7 chapters + all sub-modules from spec

3. Content Generation of All Book Content (one task per module, ~40 tasks)
   - Folder structure: docs/01-intro/, docs/02-fundamentals/, … docs/07-hands-on/
   - One MDX file per module with correct frontmatter, Mermaid diagrams, code blocks, references
   - Example tasks:
     • "Create docs/01-intro/01-history.mdx"
     • "Create docs/03-humanoid/03-zmp-locomotion.mdx"
     • "Create docs/07-hands-on/02-ros2-crash-course.mdx"
   - Every content task must include: title, diagrams, executable code, references

4. Final Polish & Deployment (5–8 tasks)
   - Verify custom landing page src/pages/index.js is untouched and works
   - Run npm install if new dependencies added
   - Run npm run build and fix any errors
   - Add GitHub Actions workflow for auto-deploy to GitHub Pages
   - Final verification: dark mode, search, responsive, fast loading

Task format:
- Use clear, single-action titles
- Mark priority (P0 = must do now, P1 = next, P2 = polish)
- All tasks must be executable one-by-one by /sp.implement

Deliverables from this /sp.tasks command:
- A complete tasks.md file with 70–90 numbered, prioritized tasks
- Clear separation by phases (Config → Sidebar → Content → Deploy)
- Confirmation that everything stays on opencode-ai branch

Stop after tasks.md is generated. Do not start implementation yet.

## Response snapshot

Generated comprehensive task breakdown with 100 individual executable tasks for implementing robotics book site. Organized into 16 phases with clear priorities and dependencies. Constitution compliance enforced throughout (text-only content, no blog recreation, stay on opencode-ai branch).

Task breakdown includes:
- Phase 1: Configuration & Theming (12 tasks)
- Phase 2: Sidebar & Navigation (1 task)  
- Phases 3-9: Content Generation for all 7 chapters (28 tasks)
- Phases 10-12: Content Enhancement (24 tasks)
- Phase 13: Static Assets (4 tasks)
- Phase 14: Final Polish & Deployment (8 tasks)
- Phase 15: Constitution Compliance Validation (5 tasks)
- Phase 16: Quality Assurance (7 tasks)

All tasks are executable individually with clear priorities, dependencies, and acceptance criteria. Ready for implementation phase.

## Outcome

- ✅ Impact: Complete granular implementation roadmap for robotics book site
- 🧪 Tests: Constitution compliance validated, task dependencies verified
- 📁 Files: tasks.md created with 100 executable tasks across 16 phases
- 🔁 Next prompts: Ready for /sp.implement to begin task execution
- 🧠 Reflection: Successfully balanced comprehensive scope with manageable task granularity

## Evaluation notes (flywheel)

- Failure modes observed: Branch requirement resolved by staying on opencode-ai throughout
- Graders run and results (PASS/FAIL): PASS - All constitution principles addressed, task breakdown complete
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor implementation phase for task dependency adjustments