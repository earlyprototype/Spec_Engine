# Consultant User Guide – Innovation Consultancy Dashboard

Project: GCATTAGC | Audience: Consultants | Version: 1.0

---

## 1. Getting Started

1. Open the app URL (deployment) or run locally (see Deployment Guide).
2. Register or sign in.
3. Create a project on the Dashboard.

---

## 2. Workflow Overview (Design Thinking)

1. Discovery → capture research, observations, insights.
2. Define → frame problem (HMW), stakeholders, constraints/opportunities.
3. Ideate → brainstorm ideas, cluster, evaluate.
4. Prototype → document artefacts, test scenarios, success metrics, assumptions.
5. Test → collect feedback, analyse results, generate insights.
6. Summary → cross‑stage overview, AI synthesis, export/share.

---

## 3. Navigation

- Top tabs show stages plus Summary.
- A small dot next to a stage shows whether data exists for that stage.
- Use the Dashboard to switch projects.

---

## 4. Data Entry Tips

- Save regularly if a stage doesn’t auto‑save.
- Use concise bullets for faster synthesis.
- Prefer structured fields (scores, tags) where available.

---

## 5. Cross‑Stage Summary & Synthesis

- Go to Summary to view an aggregated journey.
- Click “Generate Cross‑Stage Synthesis” to create an executive summary, risks, and next actions.
- If the AI key is missing, you’ll be prompted to configure it.

---

## 6. Export & Share

- Download Markdown: creates a single report containing stage snapshots and AI synthesis.
- Print/Save PDF: use the browser print dialog to generate a PDF.
- Share: uses Web Share API when available; fallback copies the link or opens an email draft.

---

## 7. Best Practices

- Keep stage inputs tidy; synthesis quality reflects input quality.
- Use Summary before client reviews – it aligns language and highlights actionable next steps.
- After Test, regenerate synthesis to reflect the latest results.

---

## 8. Troubleshooting

- Can’t sign in? Verify Insforge auth is enabled; check environment variables.
- Missing data? Confirm you selected the correct project; re‑save the stage.
- AI errors? Check `VITE_GEMINI_API_KEY` is set; try again later.

---

## 9. Administration

- Environment: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, optional `VITE_GEMINI_API_KEY`.
- Deployment: See `innovation-dashboard/DEPLOYMENT_GUIDE.md` and `QUICK_START_CHECKLIST.md`.

---

## 10. Privacy & Security

- Only the anon key is used in the frontend; do not expose service-role keys.
- RLS policies restrict data to the owning user.

---

End of Guide


