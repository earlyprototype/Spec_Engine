# Insforge Backend Setup Guide

**Project:** Innovation Consultancy Dashboard  
**SPEClet 0 - Task 1: Initialize Insforge Backend**

---

## Required Insforge Configuration

### Database Schema

#### Table 1: `projects`
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
```

#### Table 2: `stage_data`
```sql
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

---

## API Endpoints to Configure

### Projects API
- `GET /api/projects` - List user's projects
- `POST /api/projects` - Create new project
- `GET /api/projects/:id` - Get project details
- `DELETE /api/projects/:id` - Delete project (optional)

### Stage Data API
- `GET /api/projects/:id/stage/:stage_name` - Get stage data
- `POST /api/projects/:id/stage/:stage_name` - Save stage data
- `PUT /api/projects/:id/stage/:stage_name` - Update stage data

### AI Synthesis API (Placeholder for now)
- `POST /api/projects/:id/synthesis/:stage_name` - Trigger AI synthesis

---

## Authentication Configuration

Enable **Email/Password Authentication** with:
- Email verification (optional for MVP)
- Password minimum length: 8 characters
- Session management enabled
- JWT tokens for API authentication

---

## Row Level Security (RLS) Policies

### Projects Table
```sql
-- Users can only read their own projects
CREATE POLICY "Users can read own projects" ON projects
  FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own projects
CREATE POLICY "Users can create own projects" ON projects
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own projects
CREATE POLICY "Users can update own projects" ON projects
  FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own projects
CREATE POLICY "Users can delete own projects" ON projects
  FOR DELETE USING (auth.uid() = user_id);

-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
```

### Stage Data Table
```sql
-- Users can only access stage data for their projects
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

-- Enable RLS
ALTER TABLE stage_data ENABLE ROW LEVEL SECURITY;
```

---

## Required Environment Variables

After Insforge setup, you'll need:

```env
VITE_INSFORGE_URL=<your-project-url>
VITE_INSFORGE_ANON_KEY=<your-anon-key>
```

---

## Setup Steps in Insforge Console

1. Log into your Insforge account
2. Create new project: "Innovation Dashboard"
3. Navigate to SQL Editor
4. Execute the database schema SQL (tables above)
5. Execute the RLS policies SQL
6. Navigate to Authentication settings
7. Enable Email/Password authentication
8. Copy your Project URL and Anon Key
9. Provide these to the frontend application

---

## Setup Status

✅ **COMPLETED** - Backend fully configured on 2025-11-07

**What was implemented:**
1. ✅ `projects` table created with proper schema
2. ✅ `stage_data` table created with proper schema
3. ✅ Foreign key relationships established (users → projects → stage_data)
4. ✅ Row Level Security (RLS) enabled on both tables
5. ✅ All RLS policies implemented for user data isolation
6. ✅ Indexes created for optimised queries
7. ✅ OAuth authentication configured (GitHub + Google)

**Backend URL:** https://lccl-pos-insforge-backend.onrender.com

**Next Steps:**
1. Configure environment variables in your frontend application
2. Install InsForge SDK: `npm install @insforge/sdk@latest`
3. Begin frontend development using the SDK

---

**Status:** ✅ Setup Complete


