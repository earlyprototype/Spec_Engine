# GEMINI Context: SPEC Engine & Podcast Website Project

## 1. Project Overview

This directory contains the **SPEC Engine**, a constitutional framework for guiding Large Language Models (LLMs) to achieve complex goals through structured, executable specifications. It also contains active project directories (like `TGACGTCA`) generated and managed by this engine.

**Core Philosophy:**
*   **Goal-Driven:** Every Spec has a single "North Star" goal.
*   **Constitutional:** Governed by immutable rules (Articles I-XIV) to ensure reliability and safety.
*   **Dual-File Architecture:** Specs consist of human-readable Markdown (`spec_*.md`) for intent and machine-readable TOML (`parameters_*.toml`) for structure, plus an execution controller (`exe_*.md`).

## 2. Directory Structure

### Framework Core (`__SPEC_Engine/`)
*   **`_Constitution/`**: Governance rules (`constitution.md`) and design philosophy.
*   **`_Commander_SPEC/`**: The "Master Spec" (`Spec_Commander.md`) used to generate new Specs.
*   **`_templates/`**: Blueprints for Spec generation (`Spec_template.md`, `parameters_template.toml`, `exe_template.md`).
*   **`_tools/`**: Catalog of MCP (Model Context Protocol) tools for autonomous integration.
*   **`_DNA/`**: Project configuration generator (`DNA_SPEC.md`).

### Active Projects (`SPECs/`)
Projects are organized by 8-character "DNA Codes" (e.g., `TGACGTCA`).

*   **`TGACGTCA/`**: **Project: Podcast Website**
    *   `project_constitution.toml`: Project-specific configuration (Risk: Moderate, Stack: Next.js).
    *   `podcast-website/`: The actual source code for the Next.js application.
    *   `chats/`: Logs of LLM interactions.
    *   `error_logs/`: Troubleshooting records.

## 3. Core Workflows

### A. Creating a New Spec (The "Commander" Flow)
1.  **Open:** `__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`.
2.  **Input:** Provide a clear, singular goal (e.g., "Build a CLI tool for file analysis").
3.  **Process:** The Commander will:
    *   Analyze the goal.
    *   Recommend MCP tools.
    *   Draft a structure (Tasks -> Steps).
    *   Generate the 3 Spec files in `SPECs/[DNA_CODE]/[descriptor]/`.

### B. Executing a Spec
1.  **Open:** The generated `exe_[descriptor].md` file (e.g., `SPECs/TGACGTCA/spec_podcast/exe_podcast.md`).
2.  **Run:** Follow the instructions in the controller file.
3.  **Monitor:** Check `progress_[descriptor].json` for real-time status and error propagation.

## 4. Current Context: Podcast Website (`TGACGTCA`)

**DNA Code:** `TGACGTCA`
**Goal:** Deploy a production podcast website with episode listings, audio playback, and admin panel.

### Tech Stack
*   **Framework:** Next.js 16 (App Router)
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS 4, shadcn/ui (Radix UI + Lucide React)
*   **State/Form:** React Hook Form, Zod
*   **Backend Strategy:** "Insforge" (BaaS preferred for rapid deployment)

### Key Commands (in `TGACGTCA/podcast-website/`)
*   `npm run dev`: Start development server.
*   `npm run build`: Build for production.
*   `npm start`: Start production server.
*   `npm run lint`: Run ESLint.

## 5. Development Conventions

*   **Modification:** Do not manually edit generated Spec files (`spec_*.md`, `parameters_*.toml`) unless necessary. Use the Commander to regenerate or strictly follow the "Bridging" rules to keep them in sync.
*   **Validation:** All Specs must pass "Pre-flight Validation" (Constitutional compliance) before execution.
*   **Error Handling:** The system uses "Error Propagation" — downstream steps are aware of upstream failures.
*   **Modes:**
    *   **Dynamic (Default):** Autonomous with intelligent escalation.
    *   **Silent:** Fully autonomous (use with caution).
    *   **Collaborative:** Human-in-the-loop for every critical decision.

## 6. Future Direction: V3.0 Biological Framework (Proposed)

**Philosophy:** Moving from "Mechanical Construction" to "Organic Growth".
*   **Immune System:** Divergence is not just failure, but an antigen. The system learns "antibodies" (prevention rules) from every error.
*   **Epigenetics:** The SPEC is a genome (potential); the Environment determines the phenotype (expression). The same DNA behaves differently in "Prototype" vs "Production" contexts.
*   **Morphogenesis:** Instead of prescriptive steps, Specs define "Growth Rules" and "Attractors". The architecture emerges from exploring the environment (e.g., "If file system exists -> grow browser; if not -> grow CRUD").

**Status:** Proposal Phase. See `@_structureNewProposal.md`.
