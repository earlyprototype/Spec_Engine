# SPEClet 6 – End-to-End Verification Checklist

Project: GCATTAGC | Phase: 3 | Date: ___

---

## Scope

Verify cross-stage integration, AI synthesis, export/reporting, deployment, and documentation.

---

## Pre-Requisites

- Deployed URL or local dev at http://localhost:5173
- Credentials for a test user
- Environment: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, optional `VITE_GEMINI_API_KEY`

---

## Steps

1. Authentication
   - [ ] Register or sign in successfully
   - [ ] Protected routes redirect unauthenticated users

2. Project Lifecycle
   - [ ] Create a project on Dashboard
   - [ ] Navigate Discovery → Test via tabs
   - [ ] Enter minimal data in each stage and save
   - [ ] Sign out/in and verify data persistence

3. Cross-Stage Summary
   - [ ] Open `/project/:id/summary`
   - [ ] Stage presence indicators reflect saved stages
   - [ ] Snapshot cards show content/"No Data" correctly

4. AI Synthesis
   - [ ] Click “Generate Cross-Stage Synthesis”
   - [ ] Succeeds (or shows actionable error if API key missing)

5. Export & Share
   - [ ] “Download Markdown” downloads a .md file
   - [ ] “Print / Save PDF” opens print dialog and saves a PDF
   - [ ] “Share” uses Web Share or falls back to clipboard/mailto

6. Mobile Responsive
   - [ ] Open on a phone and check layout (tabs, cards, actions)

7. Documentation
   - [ ] Consultant guide present and readable
   - [ ] Client guide present and readable
   - [ ] Deployment guide present and accurate

---

## Results

- Overall Status: PASSED | FAILED | PARTIAL
- Notes:
  - 
  - 

---

## Follow-Ups

- Issues found and owners:
  1) 
  2) 

---

End of Verification


