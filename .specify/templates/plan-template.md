# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Integrated RAG Chatbot Compliance (50 points)
- [ ] RAG chatbot embedded using OpenAI Agents/ChatKit SDKs
- [ ] FastAPI backend implemented for chatbot functionality
- [ ] Neon Serverless Postgres with pgvector configured for embeddings
- [ ] Qdrant Cloud Free Tier used for vector storage
- [ ] Chatbot answers questions about book content
- [ ] Chatbot processes user-selected/highlighted text only
- [ ] Integration via sidebar widget or dedicated /chat page

### opencode Code Subagents Compliance (50 points)
- [ ] opencode CLI used as exclusive AI agent throughout project
- [ ] All mentions of "Claude" replaced with "opencode"
- [ ] Reusable opencode Code Subagents created and utilized
- [ ] Agent Skills implemented for repeatable tasks
- [ ] Consistent tooling maintained across development activities

### Authentication + Background Survey Compliance (50 points)
- [ ] Better Auth implemented for signup/signin functionality
- [ ] Custom signup form collects software/hardware background
- [ ] User profiles created and managed
- [ ] Background information stored for personalization use
- [ ] Authentication system integrated with Docusaurus

### Personalization Toggle Compliance (50 points)
- [ ] Per-chapter personalization buttons implemented
- [ ] Content adaptation based on user background
- [ ] Advanced modules shown for expert users
- [ ] Personalization toggle functional for logged-in users
- [ ] User preferences stored and applied consistently

### Urdu Translation Toggle Compliance (50 points)
- [ ] Per-chapter Urdu translation buttons implemented
- [ ] OpenAI API integrated for translation functionality
- [ ] Original English content preserved
- [ ] Translations provided as overlays or toggles
- [ ] Translation system functional for logged-in users

### Content Protection Compliance
- [ ] Existing /docs/ folder and all current files remain sacred and untouchable
- [ ] No changes to folder's files content and structure without explicit permission
- [ ] New chapter/module generation only with explicit human owner request

### Single Branch Discipline Compliance
- [ ] All AI work happens exclusively on opencode-ai branch
- [ ] Automatic checkout/create opencode-ai after every /sp.* command
- [ ] No other branches created, checked out, or referenced

### Git Discipline Compliance
- [ ] Automatic git add all changed files after every successful /sp.* command
- [ ] Descriptive commit messages generated automatically
- [ ] Automatic push to origin opencode-ai after every successful /sp.* command
- [ ] No auto-commit or auto-push without explicit confirmation

### opencode Exclusive Usage Compliance
- [ ] Every occurrence of "Claude" replaced with "opencode" in all templates
- [ ] Every occurrence of "Claude" replaced with "opencode" in all generated files
- [ ] No other AI agents mentioned or referenced anywhere

### Feature Scope Limitation Compliance
- [ ] No blog features implemented
- [ ] No multiplayer features implemented
- [ ] No payment features implemented
- [ ] No other features beyond mandatory scope implemented

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
