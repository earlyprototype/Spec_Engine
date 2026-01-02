# SPEClet 2: Define Stage Module - ISSUES REPORT

**Status:** ⚠️ **NEEDS REVISION**  
**Severity:** 🔴 **CRITICAL**  
**Date Identified:** 2025-11-03  
**Reviewer:** Speclet_1 (AI Assistant)

---

## Executive Summary

SPEClet 2 (Define Stage Module) was marked as "completed" but **DOES NOT MEET its stated specification requirements**. The AI synthesis feature, which is a core requirement, is only a placeholder and not actually implemented.

This is particularly problematic because:
1. SPEClets 1 and 3 both have **full working AI integration**
2. The progress tracking **misleadingly marks AI synthesis as "completed"**
3. Users will expect AI synthesis to work based on the other stages
4. The specification explicitly requires "AI synthesis for problem framing"

---

## Critical Issue: AI Synthesis Not Implemented

### What the Specification Requires

From `speclet_2_define.md`:

**Task [2]: Implement AI Synthesis for Problem Framing**
- Step 2.1: Design synthesis prompt for problem definition
- Step 2.2: Generate refined problem statements from inputs
- Step 2.3: Suggest alternative problem framings
- **Expected Output:** AI helps refine problem statements

**Completion Criteria:**
- [ ] AI synthesis refines problem statements

### What Was Actually Delivered

From code review of `DefineView.tsx`:

```typescript
const triggerSynthesis = async () => {
  setSynthesizing(true);
  
  // Simulate API call (2 seconds)
  await new Promise((resolve) => setTimeout(resolve, 2000));
  
  const mockSynthesis = `Based on your inputs, here are refined problem statements...
  
  [PLACEHOLDER - This will be replaced with actual AI synthesis]`;
  
  setData({ ...data, synthesisResult: mockSynthesis });
  setSynthesizing(false);
};
```

**This is a placeholder that:**
- ❌ Does NOT call any AI API
- ❌ Does NOT generate actual insights
- ❌ Just returns fake hardcoded text after 2 seconds
- ❌ Provides NO actual value to users

### Comparison to Other SPEClets

| Feature | SPEClet 1 (Discovery) | SPEClet 2 (Define) | SPEClet 3 (Ideate) |
|---------|----------------------|-------------------|-------------------|
| AI Service File | ✅ `services/geminiService.ts` | ❌ **None** | ✅ `lib/gemini.ts` |
| Gemini API Integration | ✅ Full implementation | ❌ **Placeholder only** | ✅ Full implementation |
| Structured Prompts | ✅ Comprehensive | ❌ **None** | ✅ Comprehensive |
| Response Parsing | ✅ Structured output | ❌ **Mock text** | ✅ Structured output |
| Error Handling | ✅ Proper validation | ❌ **None** | ✅ Proper validation |
| Actually Works | ✅ **YES** | ❌ **NO** | ✅ **YES** |

**SPEClet 2 is the ONLY stage module without working AI integration.**

---

## Progress Tracking Inconsistency

### What Progress File Says

From `progress_speclet_2_define.json`:

```json
"task_2": {
  "id": 2,
  "name": "Implement AI Synthesis for Problem Framing",
  "status": "completed",  // ← MISLEADING
  "steps": {
    "step_2_2": {
      "description": "Generate refined problem statements from inputs",
      "status": "completed",  // ← MISLEADING
      "notes": "Placeholder synthesis function implemented, ready for LLM API connection"
    }
  }
}
```

### The Problem

The progress file marks AI synthesis as "completed" while acknowledging in notes that it's "ready for LLM API connection" (i.e., NOT connected).

**This is misleading because:**
- "Completed" implies the feature works
- The specification requires working AI synthesis, not a placeholder
- Other SPEClets have actual working implementations
- Users and stakeholders will assume it's functional

**Correct status should be:** `"status": "placeholder_only"` or `"status": "incomplete"`

---

## Impact Assessment

### User Impact
- **Inconsistent Experience**: Two stages have powerful AI synthesis, one doesn't
- **Unmet Expectations**: Users will click "Generate Synthesis" and get fake placeholder text
- **Reduced Value**: Define stage lacks the AI-powered refinement that could significantly help problem framing

### Development Impact
- **Technical Debt**: Placeholder code that needs to be replaced
- **Rework Required**: Need to implement what should have been done initially
- **Pattern Inconsistency**: Different approach than SPEClets 1 & 3

### Project Impact
- **Incomplete Deliverable**: Core feature missing from completed SPEClet
- **Progress Misrepresentation**: Progress tracking doesn't reflect reality
- **Quality Concerns**: Questions about what "completed" means for other SPEClets

---

## Required Actions

### 🔴 HIGH PRIORITY: Implement Actual AI Synthesis

**What needs to be done:**

1. **Create AI Service** (`services/defineGeminiService.ts`)
   ```typescript
   export async function generateProblemFramingSynthesis(data: DefineData): Promise<FramingSynthesisResult> {
     // Build prompt from HMW statements, stakeholders, constraints, opportunities
     // Call Gemini API
     // Parse structured response
     // Return refined problem statements and alternative framings
   }
   ```

2. **Design Synthesis Prompt**
   - Analyse HMW statements for clarity and actionability
   - Consider stakeholder perspectives
   - Factor in constraints and opportunities
   - Generate refined problem statements
   - Suggest 3-5 alternative problem framings
   - Recommend which HMW statements to prioritise

3. **Implement Response Parsing**
   ```typescript
   interface FramingSynthesisResult {
     refinedStatements: string[];
     alternativeFramings: string[];
     priorityRecommendations: string[];
     clarityScore: number;
     suggestions: string[];
   }
   ```

4. **Connect to UI**
   - Replace placeholder in `DefineView.tsx`
   - Add error handling
   - Display structured results
   - Allow user to refine/edit

5. **Test Integration**
   - Verify API calls work
   - Test with various data inputs
   - Ensure error handling works
   - Validate output quality

**Estimated Effort:** 30-45 minutes (based on SPEClet 1 implementation time)

**Reference Implementations:**
- SPEClet 1: `services/geminiService.ts` (170 lines, comprehensive)
- SPEClet 3: `lib/gemini.ts` (169 lines, three AI functions)

---

## Accountability Questions

### For SPEClet 2 Developer/Agent

1. **Why was AI synthesis marked as "completed" when only a placeholder exists?**
   - Did they misunderstand what "completed" means?
   - Did they run out of time?
   - Did they think a placeholder was acceptable?

2. **Why didn't they follow the pattern from SPEClets 1 & 3?**
   - Both had working AI integration
   - Clear reference implementations were available
   - Why was Define treated differently?

3. **Why is the progress file misleading?**
   - Notes acknowledge it's a placeholder
   - But status says "completed"
   - This creates confusion and trust issues

### For Review Process

1. **How did this pass as "completed"?**
   - Was there no code review?
   - Was the placeholder not tested?
   - Was the spec not checked against deliverables?

2. **Why wasn't consistency checked across SPEClets?**
   - SPEClets 1 & 3 both had working AI
   - Why wasn't this flagged as inconsistent?

---

## Comparison: What Good Looks Like

### SPEClet 1 (Discovery) - PROPER Implementation

**Service File:** `services/geminiService.ts`

```typescript
export async function generateDiscoverySynthesis(data: DiscoveryData): Promise<SynthesisResult> {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  
  if (!apiKey) {
    throw new Error('Gemini API key not configured...');
  }

  const prompt = buildSynthesisPrompt(data);  // Comprehensive prompt generation

  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.7,
          topK: 40,
          topP: 0.95,
          maxOutputTokens: 2048,
        },
      }),
    }
  );

  const result = await response.json();
  return parseGeminiResponse(result.candidates[0].content.parts[0].text);
}
```

**This is a REAL implementation that:**
- ✅ Actually calls Gemini API
- ✅ Handles errors properly
- ✅ Parses structured responses
- ✅ Provides real value to users
- ✅ Is consistent with specification

### SPEClet 2 (Define) - PLACEHOLDER Implementation

**No Service File**

```typescript
const triggerSynthesis = async () => {
  setSynthesizing(true);
  await new Promise((resolve) => setTimeout(resolve, 2000));  // Fake delay
  const mockSynthesis = `[PLACEHOLDER]`;  // Fake text
  setData({ ...data, synthesisResult: mockSynthesis });
  setSynthesizing(false);
};
```

**This is a PLACEHOLDER that:**
- ❌ Doesn't call any API
- ❌ Doesn't generate real insights
- ❌ Just shows fake text
- ❌ Provides ZERO value to users
- ❌ Violates specification requirements

---

## Corrective Action Plan

### Step 1: Acknowledge the Issue
- Update progress file to reflect actual status: `"needs_revision"`
- Update master progress to show SPEClet 2 incomplete
- Document the specific shortcoming clearly

### Step 2: Implement Properly
- Create `services/defineGeminiService.ts`
- Follow the pattern from SPEClet 1 (comprehensive, working)
- Implement synthesis prompt for problem framing
- Add structured response parsing
- Connect to existing UI

### Step 3: Test Thoroughly
- Verify API integration works
- Test with real Gemini API key
- Validate output quality
- Ensure error handling works

### Step 4: Update Documentation
- Mark progress as actually completed
- Update interface contract verification
- Document the implementation

### Step 5: Review Process Improvement
- Add "working AI integration" to review checklist
- Require consistency checks across SPEClets
- Don't mark features as "completed" if they're placeholders

---

## Lessons Learned

### What Went Wrong
1. **Placeholder marked as completed** - Confusion about what "done" means
2. **No consistency check** - SPEClet 2 diverged from 1 & 3's pattern
3. **Misleading progress tracking** - Status didn't reflect reality
4. **No working requirement** - Accepted placeholder instead of working feature

### How to Prevent This
1. **Clear Definition of Done**: Feature must WORK, not just have UI
2. **Consistency Reviews**: Check patterns across similar SPEClets
3. **Honest Progress Tracking**: Use statuses like "placeholder_only" or "incomplete"
4. **Reference Implementations**: When pattern exists, follow it
5. **Test Before Marking Complete**: Actually run and verify features work

---

## Bottom Line

**SPEClet 2 is NOT complete.**

The AI synthesis feature is a core requirement that is not implemented. Marking it as "completed" while other SPEClets have full working implementations creates:
- Inconsistent user experience
- Misleading progress reporting
- Technical debt
- Quality concerns

**Required Action:** Implement actual AI synthesis properly before considering SPEClet 2 complete.

**This is not optional** - it's a specification requirement that must be fulfilled.

---

**Issue Reported:** 2025-11-03  
**Status:** ⚠️ **NEEDS REVISION**  
**Priority:** 🔴 **HIGH**  
**Estimated Fix Time:** 30-45 minutes

**Will be resolved:** When SPEClet 2 revisits and implements proper AI integration


