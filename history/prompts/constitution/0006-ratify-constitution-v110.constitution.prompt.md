---
id: 0006
title: "Ratify Constitution v1.1.0"
stage: constitution
date: 2025-12-10
surface: opencode
model: opencode-cli
feature: none
branch: opencode-ai
user: maaz
command: /sp.constitution
labels: [constitution, ratification, v110, mandatory-scope]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - /.specify/memory/constitution.md
  - /.specify/templates/plan-template.md
  - /.specify/templates/spec-template.md
  - /.specify/templates/tasks-template.md
tests:
  - Constitution compliance validation
  - Template alignment verification
  - Mandatory scope coverage check
---

## Prompt

Ratify the final constitution v1.1.0 for the Docusaurus book "Physical and Humanoid Robotics: From Fundamentals to Advanced Applications" on 2025-12-10. This completely overrides every previous version.

MANDATORY SCOPE (only these features are allowed):


1. Integrated RAG Chatbot (50 bonus points)  
   The published book MUST embed a fully functional Retrieval-Augmented Generation (RAG) chatbot using:
   - OpenAI Agents / ChatKit SDKs
   - FastAPI backend
   - Neon Serverless Postgres + pgvector
   - Qdrant Cloud Free Tier
   The chatbot answers questions about the book content and can use only the text the user currently selects/highlights.

2. opencode Code Subagents & Reusable Skills (50 bonus points)  
   Participants earn 50 bonus points by creating and using reusable opencode Code Subagents and Agent Skills throughout the project (replace every mention of "Claude" with "opencode").

3. Authentication + Background Survey (50 bonus points)  
   Implement signup/signin with Better Auth[](https://www.better-auth.com/). At signup, ask users about their software and hardware background to enable personalization.

4. Personalization Toggle per Chapter (50 bonus points)  
   Logged-in users can press a button at the start of each chapter to personalize content based on their background.

5. Urdu Translation Toggle per Chapter (50 bonus points)  
   Logged-in users can press a button at the start of each chapter to instantly translate the entire chapter into Urdu using OpenAI API.

STRICT RULES:

- The existing /docs/ folder and all its current files are sacred and untouchable until the human owner explicitly requests new chapter/module generation in a future spec.
- Don't change the folder's files content and structure. 
- All AI work happens exclusively on branch opencode-ai.
- After every successful /sp.* command: automatically checkout/create opencode-ai, git add all changed files, commit with descriptive message, push to origin opencode-ai.
- Replace every occurrence of "Claude" with "opencode" in all templates and generated files.
- No other features (blog, multiplayer, payments, etc.) are allowed.

Governance:
- Human owner has final authority
- Amendments only via new /sp.constitution with justification
- Semantic versioning: this is v1.1.0 (MINOR – added the four bonus features above)

Tech stack locked: Docusaurus 2+, MDX, Mermaid, FastAPI, Neon, Qdrant, Better Auth, OpenAI API.

Generate full Sync Impact Report as HTML comment. Set RATIFICATION_DATE: 2025-12-10, LAST_AMENDED_DATE: 2025-12-10. Remove every bracketed placeholder. 

## Response snapshot

Constitution v1.1.0 ratified successfully with complete mandatory scope override. Updated constitution.md and all template files to align with new requirements:

**Key Changes Made:**
- Complete override of previous constitution (v2.2.0 → v1.1.0)
- Added 5 mandatory features with 50-point bonuses each
- Implemented strict governance rules (content protection, single branch, git discipline)
- Updated all templates (plan, spec, tasks) with new requirements
- Replaced all "Claude" references with "opencode"

**Files Updated:**
- /.specify/memory/constitution.md (complete rewrite)
- /.specify/templates/plan-template.md (updated compliance sections)
- /.specify/templates/spec-template.md (updated requirements sections)
- /.specify/templates/tasks-template.md (updated task examples)

**Sync Impact Report Generated** showing version change and template updates.

## Outcome

- ✅ Impact: Constitution v1.1.0 ratified with complete mandatory scope override
- 🧪 Tests: Constitution compliance validation passed, template alignment verified
- 📁 Files: 4 files updated (constitution.md + 3 templates)
- 🔁 Next prompts: /sp.specify to create new feature specification based on v1.1.0
- 🧠 Reflection: Complete governance reset with focused bonus-point-driven scope

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution override completed successfully
- Graders run and results (PASS/FAIL): PASS - All mandatory requirements captured
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create new specification based on v1.1.0 requirements