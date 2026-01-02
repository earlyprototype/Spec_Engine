# Deployment Guide - Innovation Consultancy Dashboard

**Status:** Ready for Deployment  
**SPEClet:** 0 (Platform Infrastructure)  
**Last Updated:** 2025-11-03

---

## Prerequisites Checklist

Before deploying, ensure you have:

- [x] Insforge account (confirmed)
- [ ] Insforge project configured with database schema
- [ ] Vercel or Netlify account (for hosting)
- [ ] Git repository (optional but recommended)

---

## Step 1: Configure Insforge Backend (15 minutes)

### A. Access Insforge Console

1. Log into your Insforge account
2. Create a new project: **"Innovation Dashboard"**
3. Navigate to the **SQL Editor**

### B. Execute Database Schema

Copy and paste this SQL into the Insforge SQL Editor and execute:

```sql
-- Create projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_projects_user_id ON projects(user_id);

-- Create stage_data table
CREATE TABLE stage_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  stage_name VARCHAR(50) NOT NULL CHECK (stage_name IN ('discovery', 'define', 'ideate', 'prototype', 'test')),
  data_json JSONB NOT NULL DEFAULT '{}',
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(project_id, stage_name)
);

CREATE INDEX idx_stage_data_project_id ON stage_data(project_id);
CREATE INDEX idx_stage_data_stage_name ON stage_data(stage_name);
```

### C. Enable Row Level Security

Execute this SQL to protect user data:

```sql
-- Enable RLS on projects
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own projects" ON projects
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own projects" ON projects
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own projects" ON projects
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own projects" ON projects
  FOR DELETE USING (auth.uid() = user_id);

-- Enable RLS on stage_data
ALTER TABLE stage_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own stage data" ON stage_data
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM projects 
      WHERE projects.id = stage_data.project_id 
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can create own stage data" ON stage_data
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM projects 
      WHERE projects.id = stage_data.project_id 
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update own stage data" ON stage_data
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM projects 
      WHERE projects.id = stage_data.project_id 
      AND projects.user_id = auth.uid()
    )
  );
```

### D. Enable Authentication

1. Go to **Authentication** → **Providers** in Insforge console
2. Enable **Email/Password** provider
3. Set minimum password length to 8 characters
4. Email confirmation: Optional for MVP (can enable later)

### E. Get API Credentials

1. Go to **Settings** → **API**
2. Copy your **Project URL** (looks like `https://xxxxx.supabase.co`)
3. Copy your **anon/public key** (long string starting with `eyJ...`)

---

## Step 2: Configure Frontend Environment (2 minutes)

### Local Development

1. Navigate to the frontend directory:
```bash
cd SPECs/GCATTAGC/innovation-dashboard/frontend
```

2. Create `.env` file:
```bash
# Windows PowerShell
New-Item .env
```

3. Add your Insforge credentials to `.env`:
```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

Replace with actual values from Step 1E.

### Test Locally

```bash
npm run dev
```

Open `http://localhost:5173` and:
1. Register a new account
2. Create a test project
3. Navigate through the 5 stages
4. Add some notes and save
5. Sign out and sign back in
6. Verify data persists

---

## Step 3: Deploy to Vercel (Recommended - 10 minutes)

### A. Prepare Git Repository (Optional)

```bash
cd SPECs/GCATTAGC/innovation-dashboard
git init
git add .
git commit -m "Initial commit - SPEClet 0 complete"
```

Push to GitHub/GitLab if desired.

### B. Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Navigate to frontend:
```bash
cd frontend
```

3. Deploy:
```bash
vercel
```

4. Follow the prompts:
   - Link to existing project? **No**
   - Project name: **innovation-dashboard**
   - Directory: **.**
   - Override settings? **No**

5. Add environment variables when prompted:
   - `VITE_SUPABASE_URL`: Your Insforge URL
   - `VITE_SUPABASE_ANON_KEY`: Your Insforge anon key

6. Deploy to production:
```bash
vercel --prod
```

### C. Alternative: Deploy via Vercel Web Interface

1. Go to [vercel.com](https://vercel.com)
2. Click **Add New** → **Project**
3. Import your Git repository (or upload manually)
4. Configure project:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
6. Click **Deploy**

---

## Step 4: Deploy to Netlify (Alternative - 10 minutes)

### Via Netlify CLI

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Navigate to frontend:
```bash
cd frontend
```

3. Build the project:
```bash
npm run build
```

4. Deploy:
```bash
netlify deploy --prod
```

5. Follow prompts and specify:
   - **Publish directory:** `dist`

6. Add environment variables via Netlify dashboard:
   - Go to **Site settings** → **Environment variables**
   - Add `VITE_SUPABASE_URL`
   - Add `VITE_SUPABASE_ANON_KEY`

7. Trigger rebuild after adding variables

### Via Netlify Web Interface

1. Go to [netlify.com](https://netlify.com)
2. Drag and drop the `frontend/dist` folder
3. Add environment variables via site settings
4. Rebuild and deploy

---

## Step 5: Verify Deployment (5 minutes)

### Test Checklist

Visit your deployed URL and verify:

- [ ] Landing page loads correctly
- [ ] Can register a new user
- [ ] Can sign in
- [ ] Dashboard loads and displays
- [ ] Can create a new project
- [ ] Can navigate to all 5 stages:
  - [ ] Discovery
  - [ ] Define
  - [ ] Ideate
  - [ ] Prototype
  - [ ] Test
- [ ] Can save stage notes
- [ ] Can sign out
- [ ] Can sign back in
- [ ] Saved data persists
- [ ] Mobile responsive (test on phone)

---

## Step 6: Update Progress Tracking

After successful deployment, mark SPEClet 0 as complete:

1. Update `progress_speclet_0_platform.json`:
   - Set `status: "completed"`
   - Add `completed_at` timestamp

2. Update `progress_innovation_dashboard_MASTER.json`:
   - Mark SPEClet 0 as `"completed"`
   - Update Phase 1 status to `"completed"`
   - Enable Phase 2 for execution

---

## Troubleshooting

### Build Fails

**Error:** Missing environment variables
- **Solution:** Ensure `.env` file exists with correct variable names

**Error:** TypeScript compilation errors
- **Solution:** Run `npm run build` locally first to catch errors

### Authentication Issues

**Error:** "Invalid API key"
- **Solution:** Verify anon key is correct and hasn't been regenerated

**Error:** Users can't register
- **Solution:** Check that Email/Password auth is enabled in Insforge

### Database Errors

**Error:** "permission denied for table projects"
- **Solution:** Verify RLS policies were created correctly

**Error:** "relation projects does not exist"
- **Solution:** Execute database schema SQL in Insforge

### Deployment Platform Issues

**Vercel:**
- Ensure build command is `npm run build`
- Verify output directory is `dist`
- Check environment variables are set

**Netlify:**
- Ensure publish directory is `dist`
- Environment variables must be prefixed with `VITE_`
- May need to trigger manual rebuild after adding env vars

---

## Post-Deployment

### Security Checklist

- [ ] `.env` file is in `.gitignore` (already done)
- [ ] No credentials in git history
- [ ] RLS policies active
- [ ] Only anon key used (not service role key)

### Next Steps

Once SPEClet 0 is deployed and verified:

1. Mark SPEClet 0 as **COMPLETE**
2. Update master progress tracker
3. Begin SPEClet 1 (Discovery Stage Module)
4. Continue with SPEClets 2-5
5. Finish with SPEClet 6 (Integration & Final Deployment)

---

## Quick Reference

### Local Development
```bash
cd frontend
npm run dev
# http://localhost:5173
```

### Build
```bash
npm run build
# Output: dist/
```

### Environment Variables
```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJxxx...
```

### Deploy Commands
```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

---

**Ready to deploy! Follow the steps above and your Innovation Dashboard will be live.**


