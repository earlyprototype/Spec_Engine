# SPEClet 1: Discovery Stage Module

**SPEClet ID:** 1 | **Dependencies:** [0] | **Phase:** 2  
**Date:** 2025-11-03

---

## Goal

Implement the Discovery stage module with information collection tools, AI synthesis capabilities, and user-friendly interface for innovation consultants to guide clients through discovery activities.

## Dependencies

**Requires SPEClet 0 to provide:**
- Authentication system
- Database with `stage_data` table
- `Layout` and `StageNav` components
- API endpoints: `GET/POST /api/projects/:id/stage/discovery`
- Route: `/project/:id/discovery`

## Interface Contract

**This SPEClet MUST provide:**
- `DiscoveryView.jsx` component (replaces placeholder from SPEClet 0)
- Discovery data collection forms (user research, observations, insights)
- AI synthesis integration (analyzes discovery data, generates insights)
- Progress indicators for consultants

---

## Tasks

### Task [1]: Build Discovery Data Collection Interface
- Step 1.1: Create form for user research inputs (interviews, surveys)
- Step 1.2: Create observation logging interface (field notes, photos)
- Step 1.3: Create insights capture form (patterns, themes)
- Step 1.4: Implement auto-save to `stage_data` table
- **Expected Output:** Discovery forms functional, data saving to database

### Task [2]: Implement AI Synthesis for Discovery
- Step 2.1: Design synthesis prompt for discovery data
- Step 2.2: Integrate LLM API call (OpenAI/Anthropic/local)
- Step 2.3: Display synthesized insights to user
- Step 2.4: Allow user to refine/edit synthesis output
- **Expected Output:** AI synthesis generates useful discovery insights

### Task [3]: Create Discovery Progress Dashboard
- Step 3.1: Build completeness indicators (% of forms filled)
- Step 3.2: Add suggested next actions for consultant
- Step 3.3: Create visual summary of discovery data
- **Expected Output:** Progress dashboard helps consultants track discovery phase

## Completion Criteria
- [ ] Discovery forms collect user research, observations, insights
- [ ] Data persists to database via API
- [ ] AI synthesis analyzes discovery data and presents insights
- [ ] Mobile-responsive interface
- [ ] Integration with `StageNav` from SPEClet 0

---

**Execution:** Use `exe_stage_module_template.md` with SPEClet ID = 1

