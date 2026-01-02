# SPEClet 3: Ideate Stage - Quick Reference Card

**Status:** ✅ COMPLETE | **Route:** `/project/:projectId/ideate`

---

## What It Does

Provides consultants with a complete brainstorming and idea management workspace featuring visual sticky notes, AI-powered idea generation, and strategic prioritisation.

---

## Three Main Tools

### 1. Brainstorming Canvas
**Purpose:** Capture and organise ideas visually

**Features:**
- Add colourful sticky notes (6 colours)
- Edit/delete ideas inline
- Drag ideas to create clusters
- Name and organise clusters

**Use When:** Initial brainstorming, ideation sessions

---

### 2. Evaluation Matrix
**Purpose:** Prioritise ideas strategically

**Framework:**
- Quick Wins (High Impact, Easy) → Do First
- Major Projects (High Impact, Hard) → Plan Carefully
- Fill Ins (Low Impact, Easy) → If Time Allows
- Time Wasters (Low Impact, Hard) → Avoid

**Use When:** Need to decide what to prototype

---

### 3. AI Synthesis
**Purpose:** Generate and analyse ideas with AI

**Three Actions:**
1. **Generate Ideas** - AI creates 5 new ideas
2. **Suggest Clusters** - AI groups similar ideas
3. **Synthesise** - AI summarises session + next steps

**Use When:** Need inspiration or want to analyse patterns

---

## Quick Start

```bash
# 1. Setup Gemini API (one-time)
# Get key: https://makersuite.google.com/app/apikey
# Add to frontend/.env:
VITE_GEMINI_API_KEY=your-key

# 2. Start dev server
npm run dev

# 3. Navigate
# Login → Project → Ideate tab
```

---

## Data Structure

```typescript
// Saved to: stage_data.data_json
{
  ideas: [
    {
      id: string,
      content: string,
      color: string,
      clusterId?: string,
      evaluation?: { feasibility: 1-10, impact: 1-10 }
    }
  ],
  clusters: [
    { id: string, name: string, ideaIds: string[] }
  ]
}
```

---

## Common Workflows

### Workflow 1: Solo Brainstorm
1. Add 10-20 ideas (different colours)
2. Click "AI Synthesis" → "Generate Ideas" for more
3. Drag similar ideas together to cluster
4. Switch to "Evaluation Matrix"
5. Rate each idea
6. Focus on Quick Wins quadrant

### Workflow 2: Team Session
1. Share screen, navigate to Ideate
2. Capture team ideas on sticky notes
3. Use colours to categorise (e.g., by theme)
4. Create clusters by dragging
5. Vote/discuss evaluation scores
6. Use AI Synthesis for summary

### Workflow 3: AI-Assisted
1. Add problem context in AI Synthesis tab
2. Generate ideas with AI
3. Add all to canvas
4. Add your own ideas too
5. Request AI clustering suggestions
6. Request AI synthesis for summary
7. Evaluate top ideas

---

## Tips & Tricks

### Colours
Use colours intentionally:
- Yellow = User-focused ideas
- Blue = Technical ideas
- Green = Business ideas
- Pink = Creative/wild ideas
- Purple = Process improvements
- Orange = Quick wins

### Clustering
- Drag one idea onto another to auto-cluster
- Clusters auto-delete when empty
- Name clusters clearly (e.g., "Mobile Features")

### Evaluation
- Be honest about feasibility
- Consider resources, time, complexity
- High impact = significant value/differentiation
- Focus on Quick Wins first, Major Projects second

### AI Tips
- Provide context for better AI ideas
- Generate ideas multiple times for variety
- Use clustering suggestions as inspiration
- Synthesis is great for reports/documentation

---

## Files Reference

| File | Purpose |
|------|---------|
| `SPECLET_3_SUMMARY.md` | Executive summary |
| `SPECLET_3_COMPLETION.md` | Full completion report |
| `GEMINI_SETUP.md` | API key setup guide |
| `TESTING_SPECLET_3.md` | Testing procedures |
| `SPECLET_3_QUICK_REFERENCE.md` | This file |

---

## Troubleshooting

### "Gemini API key not configured"
→ Add `VITE_GEMINI_API_KEY` to `.env`, restart server

### Ideas not saving
→ Check console errors, verify authentication, check network tab

### Drag-drop not working
→ Try Chrome/Edge, disable extensions, check console

### AI taking too long
→ Normal for first request, check internet, verify API key valid

---

## Statistics Bar

Located in AI Synthesis tab:
- **Total Ideas** - All ideas created
- **Evaluated** - Ideas with feasibility/impact scores
- **Clustered** - Ideas in clusters
- **AI-Generated** - Ideas from AI (useful for tracking)

---

## Integration with Other Stages

### From Define Stage
Import "How Might We" statements as idea prompts

### To Prototype Stage
Export Quick Wins as prototype candidates

### From AI Synthesis
Use synthesis summary in final project report

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Add idea | Type + Enter |
| Edit idea | Click "Edit" button |
| Save edit | Button only |
| Delete idea | Button only |

*Note: More shortcuts could be added in future*

---

## Data Persistence

- **Auto-save:** Every 30 seconds
- **Manual save:** Click "Save Now" at bottom
- **Load:** Automatic on page load
- **Storage:** Supabase `stage_data` table

---

## Mobile Usage

**Works Best:**
- Adding ideas
- Editing ideas
- Viewing evaluation matrix
- AI synthesis

**Limited:**
- Drag-and-drop (touch events)
- Use manual clustering workarounds

---

## API Costs

**Gemini Free Tier:**
- 60 requests/minute
- 1,500 requests/day
- Free forever (as of 2025)

**Typical Usage:**
- Generate Ideas: 1 request
- Suggest Clusters: 1 request
- Synthesise: 1 request
- ~3 requests per session

**Well within free limits for normal use**

---

## Success Indicators

You're using it effectively when:
- ✅ Generated 15+ ideas per session
- ✅ Created 2-4 meaningful clusters
- ✅ Evaluated all ideas on matrix
- ✅ Identified 3-5 Quick Wins
- ✅ Used AI for inspiration/validation
- ✅ Have clear synthesis summary
- ✅ Ready to move to Prototype stage

---

## What's Next?

After completing Ideate:
1. Review Quick Wins from evaluation matrix
2. Read AI synthesis summary
3. Select 2-3 ideas to prototype
4. Navigate to **Prototype stage** (SPEClet 4)
5. Reference Ideate data for context

---

## Support

**Documentation:**
- Setup: `GEMINI_SETUP.md`
- Testing: `TESTING_SPECLET_3.md`
- Details: `SPECLET_3_COMPLETION.md`

**Questions:** Review docs or report bugs with steps to reproduce

---

**Remember:** Ideation is divergent thinking. Generate quantity first, evaluate quality later. Use AI for inspiration, not as a replacement for human creativity.

---

✅ **SPEClet 3 Complete & Ready to Use**


