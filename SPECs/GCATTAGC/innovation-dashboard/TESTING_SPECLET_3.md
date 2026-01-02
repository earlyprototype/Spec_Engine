# SPEClet 3 (Ideate Stage) - Testing Guide

**Status:** Code Complete - Ready for Testing  
**Completed:** 2025-11-03  
**Requires:** Gemini API Key Configuration

---

## Pre-Testing Setup

### 1. Configure Gemini API Key

Follow the setup guide: `GEMINI_SETUP.md`

Quick setup:
```bash
# Add to frontend/.env file:
VITE_GEMINI_API_KEY=your-api-key-here
```

### 2. Start Development Server

```powershell
cd frontend
npm run dev
```

### 3. Access Application

Open browser to: `http://localhost:5173`

---

## Interface Contract Verification

### Required from SPEClet 0:
- ✅ Authentication system (login/register)
- ✅ Database schema (`stage_data` table)
- ✅ Layout component
- ✅ Routing infrastructure
- ✅ Mobile-responsive design

### Provided by SPEClet 3:
- ✅ `IdeateView` component at `/project/:projectId/ideate`
- ✅ Brainstorming canvas with sticky notes
- ✅ Drag & drop clustering
- ✅ AI-powered idea generation
- ✅ AI-powered clustering suggestions
- ✅ AI synthesis summary
- ✅ Idea evaluation matrix (2x2 Impact/Feasibility)
- ✅ Data persistence to `stage_data.data_json`

---

## Test Cases

### Test 1: Navigation & Access
**Purpose:** Verify routing and authentication

**Steps:**
1. Log into application
2. Open or create a project
3. Click "Ideate" tab in navigation
4. Verify IdeateView loads
5. Verify three tabs visible: Brainstorming Canvas, Evaluation Matrix, AI Synthesis

**Expected:**
- Page loads without errors
- All tabs are clickable
- Default tab is "Brainstorming Canvas"

---

### Test 2: Add Ideas (Brainstorming Canvas)
**Purpose:** Verify idea creation

**Steps:**
1. Navigate to Ideate stage
2. Ensure "Brainstorming Canvas" tab is active
3. Type "Idea 1" in input field
4. Click different colour buttons to change colour
5. Click "Add Idea" button
6. Repeat 5 times with different colours

**Expected:**
- Ideas appear in "Individual Ideas" section
- Each idea shows the selected colour
- Edit and Delete buttons visible on each idea
- Idea count updates correctly

---

### Test 3: Edit Ideas
**Purpose:** Verify inline editing

**Steps:**
1. Click "Edit" button on an idea
2. Modify the text
3. Click "Save"
4. Click "Edit" on another idea
5. Click "Cancel"

**Expected:**
- Textarea appears with current text
- Saving updates the idea content
- Cancelling discards changes
- Edited ideas remain in place

---

### Test 4: Delete Ideas
**Purpose:** Verify deletion

**Steps:**
1. Note current idea count
2. Click "Delete" on an idea
3. Verify idea removed

**Expected:**
- Idea disappears immediately
- Idea count decrements
- No errors in console

---

### Test 5: Clustering (Drag & Drop)
**Purpose:** Verify clustering functionality

**Steps:**
1. Create 4+ ideas
2. Drag one idea and drop it on another idea
3. Observe cluster creation
4. Edit cluster name
5. Add another idea to cluster
6. Remove an idea from cluster

**Expected:**
- Cluster section appears with default name "New Cluster"
- Both ideas appear in cluster
- Cluster name is editable
- Ideas can be removed from cluster
- Empty clusters are automatically deleted

---

### Test 6: Idea Evaluation
**Purpose:** Verify evaluation matrix

**Steps:**
1. Create 3+ ideas
2. Switch to "Evaluation Matrix" tab
3. Select an idea from dropdown
4. Move Feasibility slider (e.g., to 7)
5. Move Impact slider (e.g., to 8)
6. Click "Save Evaluation"
7. Repeat for multiple ideas with different scores

**Expected:**
- Selected idea appears in evaluation form
- Sliders update score display
- Ideas appear in correct matrix quadrant:
  - High Feasibility (≥5) + High Impact (≥5) = Quick Wins (Green)
  - Low Feasibility (<5) + High Impact (≥5) = Major Projects (Yellow)
  - High Feasibility (≥5) + Low Impact (<5) = Fill Ins (Blue)
  - Low Feasibility (<5) + Low Impact (<5) = Time Wasters (Red)

---

### Test 7: AI Generate Ideas
**Purpose:** Verify Gemini AI idea generation

**Prerequisites:** Gemini API key configured

**Steps:**
1. Switch to "AI Synthesis" tab
2. (Optional) Enter context in text area: "Building a mobile app for students"
3. Click "Generate Ideas" button
4. Wait for response
5. Review 5 generated ideas
6. Click "Add All to Canvas"
7. Switch to "Brainstorming Canvas" tab

**Expected:**
- Loading state shows "Generating..."
- 5 new ideas appear in green box
- Ideas are relevant to context (if provided)
- "Add All to Canvas" adds ideas to brainstorming canvas
- Ideas are marked with `ai-idea` prefix in statistics

---

### Test 8: AI Cluster Suggestions
**Purpose:** Verify AI clustering

**Prerequisites:** 
- Gemini API key configured
- At least 3 ideas created

**Steps:**
1. Create 6+ diverse ideas
2. Switch to "AI Synthesis" tab
3. Click "Suggest Clusters" button
4. Wait for response
5. Review suggested clusters

**Expected:**
- Loading state shows "Clustering..."
- 2-4 clusters suggested
- Each cluster has a descriptive name
- Ideas are grouped logically
- Suggestions match your ideas (even if grouping differs from your expectation)

---

### Test 9: AI Synthesise
**Purpose:** Verify synthesis generation

**Prerequisites:**
- Gemini API key configured
- Multiple ideas created

**Steps:**
1. Create 5+ ideas
2. Switch to "AI Synthesis" tab
3. Click "Synthesise" button
4. Wait for response
5. Read synthesis summary

**Expected:**
- Loading state shows "Synthesizing..."
- Summary appears in purple box
- Summary identifies themes and patterns
- Suggests next steps
- Actionable recommendations provided

---

### Test 10: Data Persistence
**Purpose:** Verify auto-save and manual save

**Steps:**
1. Create 3 ideas
2. Note "Last saved" time
3. Click "Save Now" button at bottom
4. Verify "Last saved" time updates
5. Wait 30+ seconds
6. Verify "Last saved" time updates (auto-save)
7. Refresh the page
8. Navigate back to Ideate stage

**Expected:**
- Manual save updates timestamp
- Auto-save triggers every 30 seconds
- All ideas persist across page refresh
- Clusters persist
- Evaluations persist

---

### Test 11: Statistics
**Purpose:** Verify statistics tracking

**Steps:**
1. Switch to "AI Synthesis" tab
2. Scroll to "Ideation Statistics" section
3. Note counts

**Expected:**
- Total Ideas: Accurate count
- Evaluated: Count of ideas with evaluations
- Clustered: Count of ideas in clusters
- AI-Generated: Count of ideas from AI

---

### Test 12: Mobile Responsiveness
**Purpose:** Verify mobile layout

**Steps:**
1. Open browser DevTools
2. Toggle device emulation (mobile view)
3. Test all features in mobile view
4. Test tablet view

**Expected:**
- Layout adapts to smaller screens
- All buttons are accessible
- Text is readable
- Grid layouts collapse appropriately
- No horizontal scrolling

---

### Test 13: Error Handling (No API Key)
**Purpose:** Verify graceful degradation

**Steps:**
1. Remove `VITE_GEMINI_API_KEY` from .env
2. Restart dev server
3. Try AI features

**Expected:**
- Clear error message: "Gemini API key not configured"
- Instructions to add key
- Application doesn't crash
- Other features still work

---

### Test 14: Cross-Stage Data Access
**Purpose:** Verify data can be accessed by other stages

**Steps:**
1. Create and save ideas in Ideate stage
2. Navigate to another stage (e.g., Discovery)
3. Open browser DevTools Console
4. Run this code:
```javascript
const { data } = await supabase
  .from('stage_data')
  .select('*')
  .eq('stage_name', 'ideate')
  .single();
console.log(data);
```

**Expected:**
- Data structure visible in console
- `data_json` contains `ideas` and `clusters` arrays
- All data is properly formatted

---

## Known Issues / Limitations

### 1. Drag & Drop on Mobile
- Touch events not fully implemented
- Use manual clustering via edit mode

### 2. Canvas Positioning
- Grid layout (not freeform)
- `position` property stored but not used
- Future enhancement planned

### 3. AI Response Variability
- Gemini responses may vary
- Clustering suggestions are recommendations only
- Quality depends on context provided

---

## Troubleshooting

### Ideas not saving
**Check:**
- Console for errors
- Network tab for failed requests
- Authentication status
- Database permissions (RLS policies)

### AI features not working
**Check:**
- `.env` file has `VITE_GEMINI_API_KEY`
- API key is valid
- Dev server was restarted after adding key
- Internet connection active
- Not exceeding rate limits

### Drag & drop not working
**Try:**
- Different browser (Chrome/Edge recommended)
- Disable browser extensions
- Check console for JavaScript errors

---

## Success Criteria

### All Tests Pass ✅
- [ ] Navigation works
- [ ] Can create/edit/delete ideas
- [ ] Clustering works
- [ ] Evaluation matrix works
- [ ] AI generation works (with API key)
- [ ] AI clustering works (with API key)
- [ ] AI synthesis works (with API key)
- [ ] Data persists across refreshes
- [ ] Auto-save works
- [ ] Mobile responsive
- [ ] Error handling graceful
- [ ] Statistics accurate

### Interface Contract Satisfied ✅
- [ ] All required components delivered
- [ ] Integration with SPEClet 0 verified
- [ ] Data persistence working
- [ ] No linting errors

---

## Reporting Issues

If you find bugs, document:
1. **Steps to reproduce**
2. **Expected behaviour**
3. **Actual behaviour**
4. **Browser/device**
5. **Console errors** (if any)
6. **Screenshots** (if helpful)

---

## Next Steps After Testing

1. Document any bugs found
2. Test integration with other stages
3. Consider enhancements:
   - Freeform canvas positioning
   - Real-time collaboration
   - More AI features
   - Export functionality

---

**Testing Complete:** Mark SPEClet 3 as fully verified
**Next:** Continue with SPEClet 4 (Prototype) or SPEClet 5 (Test)


