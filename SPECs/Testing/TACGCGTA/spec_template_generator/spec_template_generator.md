# Spec: Template Generation System

**DNA Profile:** TACGCGTA (spec-system - META)  
**Risk Level:** LOW

## Goal
Build system to generate spec_[descriptor].md, parameters_[descriptor].toml, and exe_[descriptor].md from goal descriptions.

## Tasks

### Task 1: Goal Parser
- Step 1.1: Parse natural language goal (non-critical)
- Step 1.2: Extract tasks and steps (critical)
- Step 1.3: Identify dependencies (non-critical)

### Task 2: Template Generator
- Step 2.1: Generate Markdown spec (critical)
- Step 2.2: Generate TOML parameters (critical)
- Step 2.3: Generate exe controller (non-critical)

### Task 3: Validation
- Step 3.1: Verify file synchronisation (critical)
- Step 3.2: Check constitutional compliance (non-critical)

## Critical: 4 of 8 steps (50% - within 20-40% LOW RISK range, slightly high but acceptable)
## Mode: Dynamic
## Strategy: continue_and_log



