# Gemini Pro 2.5 API Setup Guide

**SPEClet 3: Ideate Stage Module**  
**AI Synthesis Configuration**

---

## Overview

The Ideate stage uses Google's Gemini Pro 2.5 API to provide AI-powered features:
- Generate creative ideas based on context
- Suggest idea clustering by themes
- Synthesise brainstorming sessions into actionable insights

---

## Prerequisites

You need a Google AI Studio API key to use Gemini Pro 2.5.

---

## Step 1: Get Your Gemini API Key

### 1.1 Visit Google AI Studio
1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account

### 1.2 Create API Key
1. Click "Create API Key"
2. Select a Google Cloud project (or create a new one)
3. Click "Create API Key in existing project" or "Create API Key"
4. Copy the generated API key (starts with `AIza...`)

### 1.3 Important Notes
- Keep your API key secure and never commit it to version control
- The API key is free to use with rate limits
- See pricing at: [https://ai.google.dev/pricing](https://ai.google.dev/pricing)

---

## Step 2: Configure Your Application

### 2.1 Add to Environment Variables

Open your `.env` file in the `frontend/` directory and add:

```env
VITE_GEMINI_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with your actual API key from Step 1.

### 2.2 Complete .env Example

Your `.env` file should now look like:

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VITE_GEMINI_API_KEY=AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2.3 Restart Development Server

If your dev server is running, restart it to load the new environment variable:

```powershell
# Stop the server (Ctrl+C)
# Then restart
npm run dev
```

---

## Step 3: Test AI Features

### 3.1 Access Ideate Stage
1. Log into your Innovation Dashboard
2. Open a project
3. Navigate to the "Ideate" tab

### 3.2 Test Each AI Feature

**Generate Ideas:**
1. Click "AI Synthesis" tab
2. (Optional) Add context in the text area
3. Click "Generate Ideas" button
4. Wait for 5 AI-generated ideas
5. Click "Add All to Canvas"

**Suggest Clusters:**
1. Create at least 3 ideas on the Brainstorming Canvas
2. Go to "AI Synthesis" tab
3. Click "Suggest Clusters" button
4. Review AI clustering suggestions

**Synthesize:**
1. Create several ideas on the Brainstorming Canvas
2. Go to "AI Synthesis" tab
3. Click "Synthesize" button
4. Read the AI-generated synthesis summary

---

## Troubleshooting

### "Gemini API key not configured"

**Cause:** Environment variable not set or not loaded

**Fix:**
1. Verify `.env` file exists in `frontend/` directory
2. Check variable name is exactly: `VITE_GEMINI_API_KEY`
3. Ensure no extra spaces around the `=` sign
4. Restart dev server after adding the key

### "API request failed" or 403 Error

**Cause:** Invalid API key or quota exceeded

**Fix:**
1. Verify API key is correct (no extra characters)
2. Check API key hasn't been revoked in Google AI Studio
3. Verify you haven't exceeded free tier limits
4. Try creating a new API key

### "Failed to parse AI response"

**Cause:** Gemini returned unexpected format

**Fix:**
- This is usually temporary
- Try the operation again
- If it persists, check your internet connection

### Rate Limit Errors

**Cause:** Too many requests in short time

**Fix:**
- Wait a few seconds between requests
- Free tier has rate limits
- Consider upgrading if you need higher limits

---

## API Usage & Costs

### Free Tier (As of 2025)
- 60 requests per minute
- 1,500 requests per day
- Free for development and testing

### Paid Tier
- If you need higher limits, enable billing in Google Cloud
- Pay only for what you use
- See current pricing: [https://ai.google.dev/pricing](https://ai.google.dev/pricing)

---

## Security Best Practices

### Do NOT:
- ❌ Commit `.env` file to git
- ❌ Share your API key publicly
- ❌ Include API key in screenshots
- ❌ Store API key in frontend code

### Do:
- ✅ Use environment variables
- ✅ Add `.env` to `.gitignore`
- ✅ Regenerate key if accidentally exposed
- ✅ Use separate keys for development/production

---

## Production Deployment

### For Vercel Deployment:

When deploying to Vercel, add the environment variable:

```bash
vercel env add VITE_GEMINI_API_KEY
```

Or via Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add new variable:
   - Name: `VITE_GEMINI_API_KEY`
   - Value: Your API key
   - Environment: Production (or all)

---

## Alternative: Using a Backend Proxy (Recommended for Production)

For production applications, consider proxying Gemini API calls through your backend:

**Benefits:**
- Keep API key secure on server
- Add rate limiting
- Monitor usage
- Add caching

**Implementation:**
1. Create backend endpoint: `/api/ai/generate`
2. Store `GEMINI_API_KEY` in backend environment only
3. Update frontend to call your backend instead of Gemini directly
4. Backend forwards requests to Gemini API

---

## Support

**Gemini API Documentation:**
- [https://ai.google.dev/tutorials/get_started_web](https://ai.google.dev/tutorials/get_started_web)

**Google AI Studio:**
- [https://makersuite.google.com/](https://makersuite.google.com/)

---

**Status:** Ready for AI-powered ideation

**Next:** Test all three AI features in the Ideate stage


