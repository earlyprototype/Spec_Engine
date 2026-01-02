# SPEClet 2: Define Stage Module

**SPEClet ID:** 2 | **Dependencies:** [0] | **Phase:** 2  
**Date:** 2025-11-03

---

## Goal

Implement the Define stage module with problem framing tools, AI synthesis for problem statements, and interface for consultants to help clients articulate clear innovation challenges.

## Dependencies

**Requires SPEClet 0 to provide:**
- Platform foundation (auth, database, routing)
- API endpoints: `GET/POST /api/projects/:id/stage/define`
- Route: `/project/:id/define`

## Interface Contract

**This SPEClet MUST provide:**
- `DefineView.jsx` component
- Problem statement builder (How Might We statements)
- Stakeholder analysis tools
- AI synthesis for problem framing
- Progress indicators

---

## Tasks

### Task [1]: Build Define Data Collection Interface
- Step 1.1: Create problem statement builder (HMW format)
- Step 1.2: Create stakeholder mapping interface
- Step 1.3: Create constraints/opportunities capture
- Step 1.4: Implement auto-save to `stage_data` table
- **Expected Output:** Define forms functional, data saving

### Task [2]: Implement AI Synthesis for Problem Framing
- Step 2.1: Design synthesis prompt for problem definition
- Step 2.2: Generate refined problem statements from inputs
- Step 2.3: Suggest alternative problem framings
- **Expected Output:** AI helps refine problem statements

### Task [3]: Create Define Progress Dashboard
- Step 3.1: Show problem clarity score
- Step 3.2: Suggest improvements for problem definition
- **Expected Output:** Progress guidance for consultants

## Completion Criteria
- [ ] Problem framing tools collect structured data
- [ ] AI synthesis refines problem statements
- [ ] Mobile-responsive interface
- [ ] Integration with stage navigation

---

**Execution:** Use `exe_stage_module_template.md` with SPEClet ID = 2

