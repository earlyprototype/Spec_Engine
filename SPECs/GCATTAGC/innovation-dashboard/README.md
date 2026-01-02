# Innovation Consultancy Dashboard

**SPEClet 0: Platform Infrastructure**  
**Status:** Development Complete - Insforge Configuration Required  
**DNA Code:** GCATTAGC

---

## Project Overview

A web application to guide clients through the Design Thinking journey (Discovery → Define → Ideate → Prototype → Test) with AI-powered synthesis tools.

**Tech Stack:**
- Frontend: React 19 + TypeScript + Vite
- Backend: Insforge BaaS (Supabase-compatible)
- Styling: Tailwind CSS
- Routing: React Router v6

---

## Quick Start

### 1. Insforge Backend Setup

You need to configure your Insforge project with the required database schema.

#### A. Create Database Tables

Log into your Insforge console and run these SQL commands:

```sql
-- Projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_projects_user_id ON projects(user_id);

-- Stage data table
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

#### B. Enable Row Level Security

```sql
-- Projects RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own projects" ON projects
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own projects" ON projects
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own projects" ON projects
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own projects" ON projects
  FOR DELETE USING (auth.uid() = user_id);

-- Stage data RLS
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

#### C. Enable Authentication

1. Go to Authentication settings in Insforge
2. Enable **Email/Password** authentication
3. Configure email templates (optional for MVP)

#### D. Get API Credentials

1. Go to Project Settings → API
2. Copy your **Project URL**
3. Copy your **anon/public key**

### 2. Frontend Setup

#### A. Configure Environment

Create a `.env` file in the `frontend` directory:

```bash
cd frontend
```

Create `.env`:
```env
VITE_INSFORGE_URL=https://kb7k7cd9.us-east.insforge.app
VITE_INSFORGE_ANON_KEY=your-anon-key-here
VITE_GEMINI_API_KEY=your-gemini-api-key-here
```

Replace with your actual InsForge credentials from step 1D.
The Gemini API key is optional but required for AI synthesis features in Discovery, Ideate, and Prototype stages.

#### B. Install Dependencies (Already Done)

Dependencies are already installed. If you need to reinstall:

```bash
npm install
```

#### C. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

---

## Testing the Application

### 1. Register a User
1. Open `http://localhost:5173`
2. Click "Get Started" or "Register"
3. Enter email and password (min 8 characters)
4. Click "Register"

### 2. Sign In
1. After registration, sign in with your credentials

### 3. Create a Project
1. On the dashboard, enter a project name
2. Click "Create Project"
3. You'll be redirected to the Discovery stage

### 4. Navigate Stages
1. Use the stage tabs to move between:
   - Discovery
   - Define
   - Ideate
   - Prototype
   - Test
2. Enter notes in each stage
3. Click "Save" to persist data

### 5. Verify Data Persistence
1. Sign out
2. Sign back in
3. Open your project
4. Verify your stage notes are saved

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.tsx           # Main layout with navigation
│   │   └── ProtectedRoute.tsx   # Route authentication guard
│   ├── contexts/
│   │   └── AuthContext.tsx      # Authentication context/provider
│   ├── lib/
│   │   └── supabase.ts          # Supabase client configuration
│   ├── pages/
│   │   ├── Dashboard.tsx        # Project list view
│   │   ├── Landing.tsx          # Welcome page
│   │   ├── Login.tsx            # Login form
│   │   ├── Register.tsx         # Registration form
│   │   └── StageView.tsx        # Generic stage view (5 stages)
│   ├── App.tsx                  # Main app with routing
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles with Tailwind
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

---

## Features Implemented (SPEClet 0)

### Authentication System
- [x] User registration with email/password
- [x] Login/logout functionality
- [x] Session management
- [x] Protected routes
- [x] Authentication context

### Database Schema
- [x] `projects` table with user associations
- [x] `stage_data` table with JSONB storage
- [x] Row Level Security policies
- [x] Database indexes for performance

### Base UI Components
- [x] Layout with header and navigation
- [x] 5-stage tab navigation
- [x] Project selector/creator
- [x] Mobile-responsive design

### API Integration
- [x] Supabase/Insforge client configured
- [x] Project CRUD operations
- [x] Stage data save/load operations
- [x] User authentication APIs

### Routing Infrastructure
- [x] `/` - Landing page
- [x] `/login` - Login page
- [x] `/register` - Registration page
- [x] `/dashboard` - Project list
- [x] `/project/:id/discovery` - Discovery stage
- [x] `/project/:id/define` - Define stage
- [x] `/project/:id/ideate` - Ideate stage
- [x] `/project/:id/prototype` - Prototype stage
- [x] `/project/:id/test` - Test stage

---

## Interface Contract Status

**What SPEClet 0 Provides for SPEClets 1-5:**

- ✅ Authentication System
- ✅ Database Schema (projects + stage_data tables)
- ✅ Base UI Components (Layout, StageNav)
- ✅ API Endpoints (via Supabase client)
- ✅ Routing Infrastructure

**Dependencies Unblocked:**
- SPEClet 1 (Discovery Stage Module) - Ready
- SPEClet 2 (Define Stage Module) - Ready
- SPEClet 3 (Ideate Stage Module) - Ready
- SPEClet 4 (Prototype Stage Module) - Ready
- SPEClet 5 (Test Stage Module) - Ready

---

## Next Steps

### For Immediate Use:
1. Complete Insforge setup (run SQL commands above)
2. Add credentials to `.env` file
3. Start dev server and test the application

### For Production Deployment (Task 6):
1. Build production bundle: `npm run build`
2. Deploy to Vercel/Netlify
3. Configure environment variables in hosting platform
4. Test deployed application

### For SPEClet 1-5 Development:
Each stage module will enhance the placeholder `StageView` component with:
- Stage-specific data collection tools
- AI synthesis integration
- Rich text editors and form inputs
- Progress indicators

---

## Troubleshooting

### "Missing Supabase environment variables"
- Ensure `.env` file exists in `frontend/` directory
- Check that variable names match exactly: `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`
- Restart dev server after creating `.env`

### Database permission errors
- Verify RLS policies are created
- Check that authentication is enabled in Insforge
- Confirm user is signed in

### Cannot create projects
- Check database connection in browser console
- Verify `projects` table exists
- Ensure RLS policy for INSERT exists

---

## Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

---

**SPEClet 0: Platform Infrastructure - COMPLETE**

Ready for SPEClets 1-5 to build upon this foundation!


