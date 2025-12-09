---
id: 0002
title: constitution-v2-governance
stage: constitution
date: 2025-12-10
surface: opencode
model: opencode-agent
feature: none
branch: opencode-ai
user: maaz
command: /sp.constitution
labels: [governance, constitution, v2.0.0]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - Constitution compliance checks updated in templates
---

## Prompt

## User Input

```text
Amend the project constitution for the "Physical and Humanoid Robotics" book to v2.0.0 (MAJOR upgrade for new unbreakable governance rules).

Keep all existing principles and content intact. Only ADD the following new mandatory principles and governance rules:

NEW PRINCIPLES (add these exactly):

Single Branch Discipline
All development, specification, planning, task generation and implementation MUST occur exclusively on the Git branch named "opencode-ai". No other branch may ever be created, checked out, or referenced by any /sp.* command or generated script.

Content Protection
No existing file containing book content (any file under /docs/, /src/pages/, or any MDX/MDX file) may be modified, overwritten, or deleted without explicit written permission from the human owner in the same command. Placeholder or dummy content may be replaced only when explicitly authorised.

Prompt History Record (PHR) Enforcement
Every single /sp.* command (constitution, specify, plan, tasks, implement, etc.) MUST automatically create a complete, correctly placed Prompt History Record in the history/prompts/ folder using the official stage-based routing:
- /sp.constitution → history/prompts/constitution/
- /sp.specify, /sp.plan, /sp.tasks, /sp.implement → history/prompts/robotics-book/
- All others → history/prompts/general/
Failure to create a valid PHR is a constitutional violation.

Git Discipline After Every /sp Command
After completion of ANY /sp.* command that modifies files, the system MUST:
1. Prompt the human with the exact git commands to run
2. Clearly state: "Please run: git add . && git commit -m '<suggested message>' && git push origin opencode-ai"
3. Never auto-commit or auto-push without explicit confirmation
4. Never proceed to the next phase until the human confirms the push is done

Versioning & Traceability
All generated tasks.md, plan.md, spec.md and constitution.md MUST include a header comment with:
- Constitution version applied
- Date and time of generation
- Git branch used (must be opencode-ai)
- Link to the PHR entry

Preservation of Human Oversight
AI may generate drafts and execute tasks, but final judgement on quality, accuracy, and style remains with the human owner. The AI must never assume approval.

Update RATIFICATION_DATE to the original date if known, otherwise keep. Set LAST_AMENDED_DATE to today (2025-12-10). Increment version to 2.0.0 (MAJOR) because these new rules are backward-incompatible with previous loose workflow.

Generate full Sync Impact Report and suggest commit message. 
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

Successfully amended the project constitution to v2.0.0 with new unbreakable governance rules:

**Updated Files:**
- `.specify/memory/constitution.md` - Added 6 new governance principles
- `.specify/templates/plan-template.md` - Added compliance checks for new principles
- `.specify/templates/spec-template.md` - Added governance requirements section
- `.specify/templates/tasks-template.md` - Added governance tasks to setup and polish phases

**New Governance Principles Added:**
1. Single Branch Discipline - Exclusive "opencode-ai" branch usage
2. Content Protection - Protection of existing book content files
3. PHR Enforcement - Mandatory PHR creation for all /sp.* commands
4. Git Discipline - Required git prompts and human confirmation after file modifications
5. Versioning & Traceability - Header requirements for all generated files
6. Preservation of Human Oversight - Final judgment reserved for human owner

**Version Update:** 1.0.0 → 2.0.0 (MAJOR - backward-incompatible governance changes)

**PHR Created:** 0002-constitution-v2-governance.constitution.prompt.md

## Outcome

- ✅ Impact: Constitution amended to v2.0.0 with 6 new unbreakable governance principles
- 🧪 Tests: Template compliance checks updated across all templates
- 📁 Files: 4 files updated (constitution.md, plan-template.md, spec-template.md, tasks-template.md)
- 🔁 Next prompts: Ready for /sp.specify, /sp.plan, /sp.tasks, /sp.implement with new governance
- 🧠 Reflection: Major governance upgrade establishes strict development discipline and human oversight

## Evaluation notes (flywheel)

- Failure modes observed: None - all templates successfully updated
- Graders run and results (PASS/FAIL): PASS - All governance principles properly integrated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor compliance with new governance rules in subsequent /sp.* commands