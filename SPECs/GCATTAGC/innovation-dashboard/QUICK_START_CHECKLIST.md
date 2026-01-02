# Quick Start Checklist - Innovation Dashboard

**Your 40-Minute Deployment Checklist**

Print this or keep it open while you work through deployment.

---

## Step 1: Configure Insforge (15 minutes)

### 1.1 Access Insforge Console
- [ ] Log into Insforge at your project URL
- [ ] Create new project: "Innovation Dashboard"
- [ ] Navigate to SQL Editor

### 1.2 Create Database Tables
- [ ] Open `INSFORGE_SETUP.md` in this folder
- [ ] Copy the "Create projects table" SQL
- [ ] Paste and execute in SQL Editor
- [ ] Verify success message
- [ ] Copy the "Create stage_data table" SQL
- [ ] Paste and execute in SQL Editor
- [ ] Verify success message

### 1.3 Apply Security Policies
- [ ] Copy all RLS policy SQL from `INSFORGE_SETUP.md`
- [ ] Paste and execute in SQL Editor
- [ ] Verify all policies created (should see 7 policies)

### 1.4 Enable Authentication
- [ ] Go to Authentication → Providers
- [ ] Enable "Email/Password" provider
- [ ] Set minimum password length: 8
- [ ] Save changes

### 1.5 Get API Credentials
- [ ] Go to Settings → API
- [ ] Copy Project URL (looks like: `https://xxxxx.supabase.co`)
- [ ] Write it here: `_______________________________`
- [ ] Copy anon/public key (long string starting with `eyJ`)
- [ ] Write first 10 characters here: `___________`

---

## Step 2: Configure Local Environment (5 minutes)

### 2.1 Create Environment File
- [ ] Open terminal/PowerShell
- [ ] Navigate to project:
  ```
  cd C:\Users\Fab2\Desktop\AI\Specs\SPECs\GCATTAGC\innovation-dashboard\frontend
  ```
- [ ] Create .env file:
  ```
  New-Item .env
  ```

### 2.2 Add Credentials
- [ ] Open `.env` file in editor
- [ ] Add this content (replace with your values):
  ```
  VITE_SUPABASE_URL=your-project-url-here
  VITE_SUPABASE_ANON_KEY=your-anon-key-here
  ```
- [ ] Save file
- [ ] Verify no typos in variable names

---

## Step 3: Test Locally (10 minutes)

### 3.1 Start Development Server
- [ ] In terminal (in frontend directory):
  ```
  npm run dev
  ```
- [ ] Open browser to: `http://localhost:5173`
- [ ] Verify landing page loads

### 3.2 Test Registration
- [ ] Click "Get Started" or "Register"
- [ ] Enter test email: `test@example.com`
- [ ] Enter password (min 8 chars): `test1234`
- [ ] Confirm password: `test1234`
- [ ] Click "Register"
- [ ] Verify redirected to login page

### 3.3 Test Login
- [ ] Enter email: `test@example.com`
- [ ] Enter password: `test1234`
- [ ] Click "Sign in"
- [ ] Verify redirected to dashboard

### 3.4 Test Project Management
- [ ] Enter project name: "Test Project"
- [ ] Click "Create Project"
- [ ] Verify redirected to Discovery stage

### 3.5 Test Stage Navigation
- [ ] Click "Define" tab
- [ ] Verify Define stage loads
- [ ] Click "Ideate" tab
- [ ] Verify Ideate stage loads
- [ ] Click "Prototype" tab
- [ ] Verify Prototype stage loads
- [ ] Click "Test" tab
- [ ] Verify Test stage loads
- [ ] Go back to "Discovery" tab

### 3.6 Test Data Persistence
- [ ] In Discovery stage, type some notes: "Test notes"
- [ ] Click "Save" button
- [ ] Verify "Last saved" time appears
- [ ] Click "Sign Out"
- [ ] Sign back in with same credentials
- [ ] Click on "Test Project"
- [ ] Verify your notes are still there

### 3.7 Stop Server
- [ ] Press `Ctrl+C` in terminal to stop dev server

---

## Step 4: Deploy to Vercel (10 minutes)

### 4.1 Install Vercel CLI (if not already installed)
- [ ] In terminal:
  ```
  npm install -g vercel
  ```
- [ ] Wait for installation

### 4.2 Deploy
- [ ] Make sure you're in frontend directory
- [ ] Run:
  ```
  vercel
  ```
- [ ] Answer prompts:
  - Link to existing project? **No**
  - Project name? **innovation-dashboard**
  - Directory? **.** (just press Enter)
  - Override settings? **No**

### 4.3 Add Environment Variables
- [ ] When prompted for environment variables, add:
  - Name: `VITE_SUPABASE_URL`
  - Value: Your Insforge URL
- [ ] Add second variable:
  - Name: `VITE_SUPABASE_ANON_KEY`
  - Value: Your Insforge anon key

### 4.4 Deploy to Production
- [ ] Run:
  ```
  vercel --prod
  ```
- [ ] Wait for deployment
- [ ] Copy the production URL shown
- [ ] Write it here: `_______________________________`

---

## Step 5: Verify Deployment (5 minutes)

### 5.1 Open Deployed App
- [ ] Open your production URL in browser
- [ ] Verify landing page loads

### 5.2 Test Full Workflow
- [ ] Register a new account (use different email)
- [ ] Sign in
- [ ] Create a project
- [ ] Navigate to all 5 stages
- [ ] Add notes in Discovery stage
- [ ] Save notes
- [ ] Sign out
- [ ] Sign back in
- [ ] Verify notes persisted

### 5.3 Test Mobile
- [ ] Open production URL on phone
- [ ] Verify responsive design works
- [ ] Test basic navigation

---

## Step 6: Mark Complete (2 minutes)

### 6.1 Update Progress
- [ ] Open `progress_speclet_0_platform.json`
- [ ] Change `"status": "deployment_ready"` to `"status": "completed"`
- [ ] Add completion timestamp
- [ ] Save file

### 6.2 Update Master Progress
- [ ] Open `progress_innovation_dashboard_MASTER.json`
- [ ] Find SPEClet 0 entry
- [ ] Change status to "completed"
- [ ] Add completion timestamp
- [ ] Update phase_1 status to "completed"
- [ ] Save file

---

## Troubleshooting

### "Missing environment variables"
- ✓ Check `.env` file exists in `frontend/` directory
- ✓ Check variable names are exactly: `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`
- ✓ Restart dev server after creating `.env`

### "permission denied for table projects"
- ✓ Verify RLS policies were created in Insforge
- ✓ Check SQL executed without errors
- ✓ Ensure you're signed in

### "relation projects does not exist"
- ✓ Verify CREATE TABLE commands executed successfully
- ✓ Check you're in correct Insforge project
- ✓ Refresh Insforge console

### Build fails on Vercel
- ✓ Verify environment variables are set in Vercel dashboard
- ✓ Check variable names don't have typos
- ✓ Trigger manual rebuild

---

## Success!

When all boxes are checked:
- ✅ SPEClet 0 is COMPLETE
- ✅ Platform foundation is live
- ✅ Ready to start SPEClet 1

---

## Next Steps

Execute `speclet_1_discovery.md` to build the Discovery stage module.

All 5 stage modules (SPEClets 1-5) are now unblocked!

---

**Total Time:** ~40 minutes  
**Difficulty:** Easy (just configuration)  
**Result:** Live Innovation Dashboard


