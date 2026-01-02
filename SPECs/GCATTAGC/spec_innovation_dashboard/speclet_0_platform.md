# SPEClet 0: Platform Infrastructure

**Version:** 1.0  
**Date:** 2025-11-03  
**SPEClet ID:** 0  
**Dependencies:** None (Foundation)  
**Blocks:** SPEClets 1, 2, 3, 4, 5 (all stage modules)

---

## ⚠️ SPEClet Notice

This is **SPEClet 0** of 7 in the Innovation Consultancy Dashboard project. This is an **experimental, project-internal** SPEClet implementation. See `SPECLET_ORCHESTRATION.md` for details.

---

## Goal

Create the foundational platform infrastructure for the Innovation Consultancy Dashboard, including authentication, database, routing, and base UI components that all stage modules will build upon.

---

## Software Stack & Architecture

### Deployment Type
- [x] Web Application (browser-based)

### Technology Stack
- **Backend:** Insforge BaaS (authentication, database, API)
- **Frontend:** React 18+ with Vite
- **Database:** Insforge managed PostgreSQL
- **UI Framework:** Tailwind CSS (rapid styling)
- **Routing:** React Router v6
- **State Management:** React Context API (simple, sufficient)
- **Build Tool:** Vite (fast development)

### User Interface Requirements
- **Primary users:** Innovation consultants (non-technical professionals)
- **Secondary users:** Business clients (end customers)
- **Interaction method:** Web browser, point-and-click navigation
- **Technical skill level:** None required (consumer-grade UX)
- **Accessibility requirements:** 
  - Clear navigation labels
  - Mobile-responsive (tablet/phone support)
  - Readable typography (16px minimum)
  - High contrast colours

### Deployment Requirements
- **Target environment:** Modern web browsers (Chrome, Firefox, Safari, Edge)
- **Installation method:** Access via URL (web-hosted)
- **Configuration needed:** Insforge API credentials (environment variables)
- **Startup process:** Navigate to URL, register/login

---

## Definition of Complete

### Primary Deliverable
- [ ] Deployed web application accessible via URL
- [ ] Working authentication (register, login, logout)
- [ ] Project creation and management functional
- [ ] Five-stage navigation implemented (Discovery, Define, Ideate, Prototype, Test)
- [ ] Data persists between sessions

### Quality Standards
- [ ] Mobile-responsive interface (works on tablets/phones)
- [ ] Secure authentication (Insforge managed)
- [ ] API endpoints documented for stage modules
- [ ] Database schema created and validated

### Verification Method
1. Create test user account
2. Create new project
3. Navigate through all 5 stages
4. Logout and login again
5. Verify project and stage data persists
6. Test on mobile device/browser

### Interface Contract (For Dependent SPEClets)

**This SPEClet MUST provide:**

1. **Authentication System**
   - User registration endpoint
   - Login/logout functionality
   - Session management
   - User-project ownership

2. **Database Schema**
   - `projects` table with fields: id, name, user_id, created_at, updated_at
   - `stage_data` table with fields: id, project_id, stage_name, data_json, updated_at
   - Stage names enum: "discovery", "define", "ideate", "prototype", "test"

3. **Base UI Components**
   - `Layout.jsx` - Main wrapper with navigation
   - `StageNav.jsx` - Five-stage tab navigation
   - `ProjectSelector.jsx` - Project switcher component
   - Responsive mobile layout

4. **API Endpoints**
   - `GET /api/projects` - List user's projects
   - `POST /api/projects` - Create new project
   - `GET /api/projects/:id` - Get project details
   - `GET /api/projects/:id/stage/:stage_name` - Fetch stage data
   - `POST /api/projects/:id/stage/:stage_name` - Save stage data
   - `POST /api/projects/:id/synthesis/:stage_name` - Trigger AI synthesis

5. **Routing Infrastructure**
   - `/` - Landing/welcome page
   - `/dashboard` - Project list view
   - `/project/:id/discovery` - Discovery stage view
   - `/project/:id/define` - Define stage view
   - `/project/:id/ideate` - Ideate stage view
   - `/project/:id/prototype` - Prototype stage view
   - `/project/:id/test` - Test stage view

---

## Definitions

- **goal:** Create foundational platform infrastructure
- **task[n]:** Discrete setup objective (Insforge, React, Database, UI, Deployment)
- **step[m]:** Concrete implementation action
- **backup[p]:** Alternative approach if step fails
- **critical_flag:** Step failure blocks platform foundation
- **mode:** Execution mode (dynamic default)
- **progress.json:** `progress_speclet_0_platform.json`

---

## Components

- Insforge BaaS backend (authentication, database, API)
- React frontend application
- Vite build system
- Tailwind CSS framework
- React Router navigation

---

## Constraints

- Must use Insforge for rapid prototyping (project preference)
- Mobile-responsive required (tablet/phone support)
- Non-technical user UX required (clear labels, simple navigation)
- Must establish interface contract for dependent SPEClets
- Authentication must be secure (managed by Insforge)

---

## Tasks and Steps

### Task [1]: Initialize Insforge Backend

**TOML Reference:** `tasks[id=1]` in parameters_speclet_0_platform.toml

- **Step [1.1]:** Create Insforge project and configure authentication
  - **Primary method:** Sign up for Insforge, create new project, enable email/password auth
  - **Backup [1]:** If Insforge unavailable, use Firebase as BaaS alternative
  - **Expected output:** Insforge project created with auth enabled, API credentials obtained
  - **Critical:** true
  - **Mode:** collaborative (requires account setup)

- **Step [1.2]:** Define database schema in Insforge
  - **Primary method:** Create `projects` and `stage_data` tables via Insforge console
  - **Backup [1]:** Use Insforge CLI or API to programmatically create schema
  - **Expected output:** Database tables created with correct fields and relationships
  - **Critical:** true
  - **Mode:** silent

- **Step [1.3]:** Configure API endpoints in Insforge
  - **Primary method:** Set up RESTful endpoints for projects and stage data
  - **Backup [1]:** Use Insforge auto-generated CRUD endpoints if manual setup complex
  - **Expected output:** API endpoints accessible and documented
  - **Critical:** true
  - **Mode:** silent

- **Step [1.4]:** Test backend connectivity and authentication
  - **Primary method:** Use Insforge API tester or Postman to verify endpoints
  - **Backup [1]:** Write simple Node.js test script to verify API
  - **Expected output:** All endpoints returning expected responses
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Backend operational, database schema created, API endpoints accessible
- **Logging:** Append to progress_speclet_0_platform.json

---

### Task [2]: Set Up React Frontend Application

**TOML Reference:** `tasks[id=2]` in parameters_speclet_0_platform.toml

- **Step [2.1]:** Initialize React project with Vite
  - **Primary method:** Run `npm create vite@latest frontend -- --template react`
  - **Backup [1]:** Use Create React App if Vite setup fails
  - **Expected output:** React project initialized with dev server running
  - **Critical:** true
  - **Mode:** silent

- **Step [2.2]:** Install dependencies (React Router, Tailwind CSS, Insforge SDK)
  - **Primary method:** `npm install react-router-dom tailwindcss @insforge/sdk`
  - **Backup [1]:** Install minimal dependencies first, add others incrementally
  - **Expected output:** All dependencies installed, package.json updated
  - **Critical:** true
  - **Mode:** silent

- **Step [2.3]:** Configure Tailwind CSS for styling
  - **Primary method:** Run `npx tailwindcss init`, configure tailwind.config.js
  - **Backup [1]:** Use CDN version of Tailwind if build setup complex
  - **Expected output:** Tailwind classes working in components
  - **Critical:** false (can use inline CSS temporarily)
  - **Mode:** silent

- **Step [2.4]:** Set up React Router with placeholder routes
  - **Primary method:** Create router configuration with 7 routes (dashboard + 5 stages + landing)
  - **Backup [1]:** Use simple conditional rendering if router setup complex
  - **Expected output:** Navigation between routes working
  - **Critical:** true
  - **Mode:** silent

- **Step [2.5]:** Configure Insforge SDK in React app
  - **Primary method:** Initialize Insforge client with API credentials, create auth context
  - **Backup [1]:** Use fetch API directly if SDK integration difficult
  - **Expected output:** Insforge SDK initialized, API calls working
  - **Critical:** true
  - **Mode:** silent

- **Verification:** React app running, routing functional, Insforge connected
- **Logging:** Append to progress_speclet_0_platform.json

---

### Task [3]: Implement Authentication Flow

**TOML Reference:** `tasks[id=3]` in parameters_speclet_0_platform.toml

- **Step [3.1]:** Create registration form component
  - **Primary method:** Build React form with email/password fields, validation
  - **Backup [1]:** Use simple HTML form if React form library complex
  - **Expected output:** Registration form rendering and capturing input
  - **Critical:** true
  - **Mode:** silent

- **Step [3.2]:** Implement registration logic with Insforge
  - **Primary method:** Call Insforge auth API to create user account
  - **Backup [1]:** Use Insforge SDK helper methods if direct API complex
  - **Expected output:** New users can register successfully, receive confirmation
  - **Critical:** true
  - **Mode:** silent

- **Step [3.3]:** Create login form component
  - **Primary method:** Build React login form with email/password
  - **Backup [1]:** Reuse registration form component with mode toggle
  - **Expected output:** Login form rendering and capturing credentials
  - **Critical:** true
  - **Mode:** silent

- **Step [3.4]:** Implement login/logout logic
  - **Primary method:** Call Insforge auth endpoints, store session token
  - **Backup [1]:** Use localStorage for session if Insforge session complex
  - **Expected output:** Users can login, logout, session persists across page refresh
  - **Critical:** true
  - **Mode:** silent

- **Step [3.5]:** Add authentication guards to routes
  - **Primary method:** Create ProtectedRoute component, redirect unauthenticated users
  - **Backup [1]:** Use conditional rendering in each route if guard component complex
  - **Expected output:** Unauthenticated users redirected to login
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Users can register, login, logout; protected routes working
- **Logging:** Append to progress_speclet_0_platform.json

---

### Task [4]: Build Project Management System

**TOML Reference:** `tasks[id=4]` in parameters_speclet_0_platform.toml

- **Step [4.1]:** Create project creation form component
  - **Primary method:** Build form with project name field, create button
  - **Expected output:** Form component rendering and capturing project name
  - **Critical:** true
  - **Mode:** silent

- **Step [4.2]:** Implement project creation API call
  - **Primary method:** POST to `/api/projects` with user_id and project name
  - **Backup [1]:** Use Insforge SDK create method if direct API complex
  - **Expected output:** New projects created in database, associated with user
  - **Critical:** true
  - **Mode:** silent

- **Step [4.3]:** Create project list/dashboard view
  - **Primary method:** Fetch user's projects, display in card grid layout
  - **Backup [1]:** Display as simple list if card layout complex
  - **Expected output:** Dashboard showing all user projects
  - **Critical:** true
  - **Mode:** silent

- **Step [4.4]:** Implement project selection functionality
  - **Primary method:** Store selected project in context, redirect to first stage
  - **Backup [1]:** Use URL params if context management complex
  - **Expected output:** Clicking project navigates to its Discovery stage
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Users can create projects, view project list, select projects
- **Logging:** Append to progress_speclet_0_platform.json

---

### Task [5]: Create Base UI Components and Stage Navigation

**TOML Reference:** `tasks[id=5]` in parameters_speclet_0_platform.toml

- **Step [5.1]:** Build Layout component with header and navigation
  - **Primary method:** Create Layout.jsx with logo, user menu, logout button
  - **Backup [1]:** Use minimal layout if complex design difficult
  - **Expected output:** Layout component wrapping all authenticated pages
  - **Critical:** false (can improve later)
  - **Mode:** silent

- **Step [5.2]:** Create StageNav component (5-stage tab navigation)
  - **Primary method:** Build horizontal tab navigation with 5 stages (Discovery→Define→Ideate→Prototype→Test)
  - **Backup [1]:** Use simple link list if tabs complex
  - **Expected output:** Stage navigation tabs rendering, active state showing
  - **Critical:** true
  - **Mode:** silent

- **Step [5.3]:** Implement stage routing and placeholder views
  - **Primary method:** Create 5 placeholder components (DiscoveryView, DefineView, etc.)
  - **Backup [1]:** Use single component with stage prop if separate files complex
  - **Expected output:** Each stage route rendering placeholder content
  - **Critical:** true
  - **Mode:** silent

- **Step [5.4]:** Add mobile-responsive styling
  - **Primary method:** Use Tailwind responsive classes (md:, lg:) for mobile layout
  - **Backup [1]:** Use CSS media queries if Tailwind approach complex
  - **Expected output:** Interface adapts to mobile/tablet screens
  - **Critical:** false (can improve later)
  - **Mode:** silent

- **Step [5.5]:** Implement stage data persistence structure
  - **Primary method:** Create API calls to save/load stage data to `stage_data` table
  - **Backup [1]:** Use localStorage temporarily if API integration complex
  - **Expected output:** Stage data saves to database, persists between sessions
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Stage navigation functional, data persistence working, mobile-responsive
- **Logging:** Append to progress_speclet_0_platform.json

---

### Task [6]: Deploy Platform and Verify Interface Contract

**TOML Reference:** `tasks[id=6]` in parameters_speclet_0_platform.toml

- **Step [6.1]:** Configure production build settings
  - **Primary method:** Set environment variables for production Insforge credentials
  - **Backup [1]:** Use .env file if environment variable setup complex
  - **Expected output:** Production config ready, no hardcoded credentials
  - **Critical:** true
  - **Mode:** silent

- **Step [6.2]:** Build production bundle
  - **Primary method:** Run `npm run build` to create optimized bundle
  - **Backup [1]:** Use development build temporarily if production build fails
  - **Expected output:** Optimized production files in dist/ folder
  - **Critical:** true
  - **Mode:** silent

- **Step [6.3]:** Deploy to web hosting (Vercel/Netlify/Insforge hosting)
  - **Primary method:** Deploy via Vercel CLI or GitHub integration
  - **Backup [1]:** Use Netlify if Vercel deployment fails
  - **Backup [2]:** Use Insforge hosting if both external hosts fail
  - **Expected output:** Application accessible via public URL
  - **Critical:** true
  - **Mode:** silent

- **Step [6.4]:** Verify interface contract deliverables
  - **Primary method:** Test all required endpoints, components, and functionality
  - **Expected output:** Checklist confirming all interface contract items delivered
  - **Critical:** true
  - **Mode:** collaborative (requires systematic verification)

- **Step [6.5]:** Create local deployment documentation
  - **Primary method:** Write README with setup instructions, environment config
  - **Backup [1]:** Create simple SETUP.md if comprehensive README complex
  - **Expected output:** Documentation enabling local development setup
  - **Critical:** false (nice to have)
  - **Mode:** silent

- **Verification:** Application deployed, all interface contract items delivered, documentation complete
- **Logging:** Append to progress_speclet_0_platform.json

---

## Interface Contract Verification Checklist

Before marking SPEClet 0 complete, verify these deliverables exist:

### Authentication System
- [ ] User registration working
- [ ] Login/logout functional
- [ ] Session management active
- [ ] User-project associations stored

### Database Schema
- [ ] `projects` table created with correct fields
- [ ] `stage_data` table created with correct fields
- [ ] Foreign keys and relationships correct
- [ ] Test data can be saved/retrieved

### Base UI Components
- [ ] `Layout.jsx` exists and functional
- [ ] `StageNav.jsx` exists with 5 stages
- [ ] `ProjectSelector.jsx` exists
- [ ] Mobile-responsive styling applied

### API Endpoints
- [ ] `GET /api/projects` returns user projects
- [ ] `POST /api/projects` creates new project
- [ ] `GET /api/projects/:id` returns project details
- [ ] `GET /api/projects/:id/stage/:stage_name` returns stage data
- [ ] `POST /api/projects/:id/stage/:stage_name` saves stage data
- [ ] `POST /api/projects/:id/synthesis/:stage_name` endpoint exists (placeholder OK)

### Routing Infrastructure
- [ ] `/` landing page exists
- [ ] `/dashboard` project list working
- [ ] `/project/:id/discovery` route exists
- [ ] `/project/:id/define` route exists
- [ ] `/project/:id/ideate` route exists
- [ ] `/project/:id/prototype` route exists
- [ ] `/project/:id/test` route exists

### Deployment
- [ ] Application accessible via URL
- [ ] Local deployment instructions documented

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (speclet_0_platform.md) must maintain perfect alignment with its companion file (parameters_speclet_0_platform.toml).

**Bridging Requirements:**
1. Each task in this file has corresponding `[[tasks]]` entry in TOML with matching ID
2. Each step has corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file match `expected_output` fields in TOML
4. Critical flags align between both files

---

## Instructions for LLM Executor

1. This is SPEClet 0 - the **foundation** for the entire project
2. **All other SPEClets depend on this** - verify interface contract thoroughly
3. Execute tasks sequentially (1→2→3→4→5→6)
4. Log all progress to `progress_speclet_0_platform.json`
5. After completion, update `progress_innovation_dashboard_MASTER.json`:
   - Mark SPEClet 0 as "completed"
   - Update phase_1_foundation status to "completed"
   - Enable phase_2_stages for execution
6. Verify all interface contract items before marking complete
7. Use Dynamic mode (collaborative escalation on failures)
8. Insforge setup (Step 1.1) requires human account creation

---

**End of SPEClet 0 Specification**


