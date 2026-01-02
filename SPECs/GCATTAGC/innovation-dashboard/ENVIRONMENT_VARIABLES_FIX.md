# Environment Variables Fix - InsForge Naming Correction

**Date:** 2025-11-07  
**Issue:** Naming inconsistency between backend platform (InsForge) and frontend environment variables (Supabase)  
**Status:** ✅ RESOLVED

---

## Problem Identified

The codebase was using `VITE_SUPABASE_*` environment variables despite using **InsForge** as the backend platform. While InsForge is Supabase-compatible (uses the same client library), the naming should reflect the actual platform being used.

---

## Changes Made

### 1. Frontend Client Configuration
**File:** `frontend/src/lib/supabase.ts`

**Before:**
```typescript
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error(
    'Missing Supabase environment variables. Please check your .env file.'
  );
}
```

**After:**
```typescript
const insforgeUrl = import.meta.env.VITE_INSFORGE_URL;
const insforgeAnonKey = import.meta.env.VITE_INSFORGE_ANON_KEY;

if (!insforgeUrl || !insforgeAnonKey) {
  throw new Error(
    'Missing InsForge environment variables. Please check your .env file and ensure VITE_INSFORGE_URL and VITE_INSFORGE_ANON_KEY are set.'
  );
}
```

### 2. Main README Documentation
**File:** `README.md`

**Before:**
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

**After:**
```env
VITE_INSFORGE_URL=https://lccl-pos-insforge-backend.onrender.com
VITE_INSFORGE_ANON_KEY=your-anon-key-here
```

### 3. Setup Documentation
**File:** `INSFORGE_SETUP.md`

Already correctly documented:
```env
VITE_INSFORGE_URL=<your-project-url>
VITE_INSFORGE_ANON_KEY=<your-anon-key>
```

---

## Required Environment Variables

Your frontend `.env` file should now contain:

```env
# InsForge Backend Configuration
VITE_INSFORGE_URL=https://kb7k7cd9.us-east.insforge.app
VITE_INSFORGE_ANON_KEY=your-anon-key-here

# Optional: Gemini AI for synthesis features (SPEClets 1, 3, 4)
VITE_GEMINI_API_KEY=your-gemini-api-key-here
```

---

## Why This Fix Matters

### 1. Clarity
- Environment variables now clearly indicate the backend platform
- Reduces confusion during setup and debugging
- Documentation matches implementation

### 2. Consistency
- Aligns with actual backend platform (InsForge)
- Matches MCP configuration which uses InsForge
- Consistent with project documentation

### 3. Maintainability
- Future developers immediately understand the platform
- Error messages accurately reference InsForge
- No mixed terminology between docs and code

---

## Migration Steps (If You Already Have .env)

If you already created a `.env` file with the old variable names:

### Option 1: Update Existing File
Open `frontend/.env` and rename the variables:

```diff
- VITE_SUPABASE_URL=https://lccl-pos-insforge-backend.onrender.com
- VITE_SUPABASE_ANON_KEY=ik_2j5yqIUfnvbgS9LTHKYoCWN7
+ VITE_INSFORGE_URL=https://lccl-pos-insforge-backend.onrender.com
+ VITE_INSFORGE_ANON_KEY=ik_2j5yqIUfnvbgS9LTHKYoCWN7
```

### Option 2: Create Fresh .env
Delete the old `.env` and create a new one with the correct variable names.

---

## Verification

After making these changes:

1. **Restart your development server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Check the console:**
   - No "Missing environment variables" errors
   - Application connects to InsForge successfully

3. **Test authentication:**
   - Register a new user
   - Login works
   - Data persists

---

## Impact on SPEClets

This change affects the foundation (SPEClet 0) that all other SPEClets depend on:

- ✅ **SPEClet 0:** Platform Infrastructure (updated)
- ✅ **SPEClet 1:** Discovery Stage (no changes needed - uses platform foundation)
- ✅ **SPEClet 2:** Define Stage (no changes needed - uses platform foundation)
- ✅ **SPEClet 3:** Ideate Stage (no changes needed - uses platform foundation)
- ✅ **SPEClet 4:** Prototype Stage (no changes needed - uses platform foundation)
- ✅ **SPEClet 5:** Test Stage (no changes needed - uses platform foundation)

All stage modules import the Supabase client from `lib/supabase.ts`, so they automatically benefit from this fix without requiring individual updates.

---

## Technical Notes

### Why Keep the File Named "supabase.ts"?

The file remains `supabase.ts` because:
1. InsForge uses the `@supabase/supabase-js` client library
2. The export is still called `supabase` for compatibility
3. All imports throughout the codebase reference this name
4. InsForge is fully Supabase-compatible at the API level

The key difference is the **environment variable names** which now correctly reflect your backend platform.

---

## Summary

✅ **Problem:** Environment variables used Supabase naming despite using InsForge  
✅ **Solution:** Updated variable names from `VITE_SUPABASE_*` to `VITE_INSFORGE_*`  
✅ **Impact:** Better clarity, consistency, and maintainability  
✅ **Action Required:** Update your `.env` file with the new variable names

---

**Status:** COMPLETE  
**Verified:** Environment variable naming now matches backend platform

