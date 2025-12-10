<!--
Sync Impact Report:
- Version change: 2.2.0 → 1.1.0 (MAJOR - complete override with new mandatory scope)
- Modified principles: All previous principles replaced with new mandatory scope
- Added sections: Integrated RAG Chatbot (50 points), opencode Code Subagents (50 points), Authentication + Background Survey (50 points), Personalization Toggle (50 points), Urdu Translation Toggle (50 points)
- Removed sections: All previous core principles and governance sections
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md - all updated with new requirements
- Follow-up TODOs: None
-->

# Physical and Humanoid Robotics Book Constitution

## Mandatory Scope

### Integrated RAG Chatbot (50 bonus points)
The published book MUST embed a fully functional Retrieval-Augmented Generation (RAG) chatbot using:
- OpenAI Agents / ChatKit SDKs
- FastAPI backend
- Neon Serverless Postgres + pgvector
- Qdrant Cloud Free Tier
The chatbot answers questions about the book content and can use only the text the user currently selects/highlights.

### opencode Code Subagents & Reusable Skills (50 bonus points)
Participants earn 50 bonus points by creating and using reusable opencode Code Subagents and Agent Skills throughout the project (replace every mention of "Claude" with "opencode").

### Authentication + Background Survey (50 bonus points)
Implement signup/signin with Better Auth. At signup, ask users about their software and hardware background to enable personalization.

### Personalization Toggle per Chapter (50 bonus points)
Logged-in users can press a button at the start of each chapter to personalize content based on their background.

### Urdu Translation Toggle per Chapter (50 bonus points)
Logged-in users can press a button at the start of each chapter to instantly translate the entire chapter into Urdu using OpenAI API.

## Strict Rules

### Content Protection
The existing /docs/ folder and all its current files are sacred and untouchable until the human owner explicitly requests new chapter/module generation in a future spec. Don't change the folder's files content and structure.

### Single Branch Discipline
All AI work happens exclusively on branch opencode-ai.

### Git Discipline After Every /sp Command
After every successful /sp.* command: automatically checkout/create opencode-ai, git add all changed files, commit with descriptive message, push to origin opencode-ai.

### opencode Exclusive Usage
Replace every occurrence of "Claude" with "opencode" in all templates and generated files.

### Feature Scope Limitation
No other features (blog, multiplayer, payments, etc.) are allowed.

## Governance

### Human Authority
Human owner has final authority.

### Amendment Process
Amendments only via new /sp.constitution with justification.

### Versioning
Semantic versioning: this is v1.1.0 (MINOR – added the four bonus features above).

## Tech Stack

### Locked Technologies
- Docusaurus 2+, MDX, Mermaid
- FastAPI, Neon, Qdrant
- Better Auth, OpenAI API

**Version**: 1.1.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10