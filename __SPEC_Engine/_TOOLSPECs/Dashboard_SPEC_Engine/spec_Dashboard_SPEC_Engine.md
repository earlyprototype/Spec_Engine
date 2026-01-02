# Dashboard SPEC Engine

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Purpose:** Build a comprehensive web application dashboard that facilitates all key SPEC Engine features including DNA profile management, SPEC creation/management, parameter file editing, execution monitoring, and results visualisation

---

## Goal

Build a production-ready web application dashboard that enables users to interact with the SPEC Engine framework through a modern web interface, providing full functionality for managing DNA profiles, creating and editing SPECs, manually editing parameter files with validation, executing SPECs with real-time monitoring, and visualising results.

---

## Software Stack & Architecture

**Deployment Type:** Full-stack web application (client-server architecture)

**Frontend Stack:**
- **Framework:** React 18+ with TypeScript
- **UI Library:** Material-UI (MUI) v5 for modern component library
- **State Management:** Redux Toolkit for application state
- **Code Editor:** Monaco Editor (VS Code editor component) for TOML/Markdown editing
- **Real-time Updates:** WebSocket client for execution monitoring
- **Build Tool:** Vite for fast development and optimised builds
- **Styling:** CSS Modules + MUI theming system

**Backend Stack:**
- **Runtime:** Node.js 20 LTS with TypeScript
- **Framework:** Express.js for REST API
- **WebSocket:** Socket.io for real-time communication
- **File System:** fs-extra for enhanced file operations
- **Validation:** Zod for schema validation, TOML parser for parameter file validation
- **Process Management:** PM2 for production deployment
- **CORS:** cors middleware for security

**Database:**
- **Type:** File-based (SQLite) for execution history and metadata
- **Schema:** SPECs metadata, execution history, progress logs
- **ORM:** Prisma for type-safe database access

**Target Environment:**
- **Development:** localhost:3000 (frontend), localhost:5000 (backend)
- **Production:** Docker containerised deployment
- **OS Support:** Windows, macOS, Linux

**Packaging & Deployment:**
- **Frontend:** Static build served by Nginx or backend Express
- **Backend:** Standalone Node.js service
- **Container:** Docker Compose for full-stack deployment
- **Environment:** .env configuration for paths and settings

---

## Definition of Complete

What must exist and be verified:

- [ ] **Primary deliverable:** 
  - Production-ready web application with frontend and backend deployed
  - All six core features fully functional (DNA, SPECs, Editor, Execution, Progress, Results)
  - Application accessible via web browser with responsive UI

- [ ] **Quality standards met:** 
  - All UI components render correctly across desktop browsers (Chrome, Firefox, Edge)
  - Parameter file editor provides real-time validation and syntax highlighting
  - SPEC execution integrates with existing exe_[descriptor].md files
  - Real-time progress monitoring works without manual refresh
  - Data persistence works correctly (execution history, settings)
  - Error handling implemented for all user actions
  - UI follows SPEC Engine terminology and concepts consistently

- [ ] **Verification method:** 
  - Complete user workflow test: Create DNA → Create SPEC → Edit parameters → Execute → Monitor → View results
  - Parameter file validation correctly catches TOML syntax errors
  - Execution monitoring shows real-time progress updates
  - Application starts successfully via npm scripts or Docker
  - Responsive UI works on desktop screens (1920x1080 to 1366x768)

- [ ] **Build-specific requirements (Article XIV):**
  - Deployment artifact exists (Docker image or standalone package)
  - UI fully implemented (not placeholder or partial implementation)
  - Production-ready code (error handling, logging, validation)
  - Database migrations included for schema setup
  - README with setup, configuration, and usage instructions
  - Environment configuration template (.env.example)

---

## MCP Toolset

**This is a build goal - MCP tools typically not required for implementation.**

However, if research needed:
- **OPTIONAL:** github (for examining similar dashboard projects)
- **OPTIONAL:** tavily-search (for best practices research)

---

## Definitions

- **goal**: Build production-ready SPEC Engine dashboard web application
- **SPECLet[s]**: Work packages grouping related functionality
- **task[n]**: Discrete objectives within each SPECLet
- **step[m]**: Concrete implementation actions
- **backup[p]**: Alternative implementation approaches
- **critical_flag**: Boolean indicating whether step failure blocks goal achievement
- **mode**: Dynamic (autonomous with escalation when needed)
- **progress.json**: Structured log tracking implementation progress

---

## Components

Build requires creation of:

**Frontend Components:**
- Dashboard layout with navigation
- DNA Profile Manager (create, edit, view profiles)
- SPEC Manager (list, create, view SPECs)
- Parameter File Editor (Monaco editor with validation)
- Execution Controller (start, monitor SPECs)
- Progress Visualiser (real-time updates, task/step breakdown)
- Results Viewer (goal status, logs, completion verification)
- Settings panel (file paths, preferences)

**Backend Services:**
- REST API endpoints for CRUD operations
- File system service (read/write SPECs, DNA profiles, parameters)
- Validation service (TOML parsing, SPEC validation)
- Execution service (spawn exe_[descriptor].md processes)
- Progress monitoring service (watch progress.json files)
- WebSocket service (real-time progress broadcasts)

**Database Schema:**
- DNA profiles table (dna_code, settings, created_at)
- SPECs table (spec_id, name, descriptor, dna_code, status)
- Executions table (execution_id, spec_id, status, started_at, completed_at)
- Progress logs table (execution_id, task_id, step_id, status, timestamp)

**Configuration:**
- Environment variables (.env)
- Frontend config (API endpoints, WebSocket URL)
- Backend config (file paths, port, CORS origins)

**Machine-Readable Components:**  
See `[components]` section in parameters_Dashboard_SPEC_Engine.toml

---

## Constraints

- Must integrate with existing SPEC Engine file structure (respect __SPEC_Engine/ and SPECs/ directories)
- Cannot modify core SPEC Engine framework files (read-only access to _Constitution, _templates, etc.)
- Parameter file editing must preserve TOML structure and validate against SPEC Engine schema
- Execution must use existing exe_[descriptor].md files (not re-implement execution logic)
- UI terminology must match SPEC Engine documentation (Goal, Task, Step, SPECLet, DNA, etc.)
- Must support Windows file paths (user is on Windows)
- No deletion of SPEC files without confirmation dialogue
- Real-time updates should not overwhelm browser (throttle/debounce)

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dashboard_SPEC_Engine.toml:
- `respect_spec_engine_structure = true`
- `readonly_framework_files = true`
- `validate_toml_structure = true`
- `use_existing_executors = true`
- `match_engine_terminology = true`
- `support_windows_paths = true`

---

## User Stories

- As a **SPEC author**, I want to create and edit SPECs through a web interface so I don't need to manually create files
- As a **developer**, I want to edit parameter files with syntax highlighting and validation so I catch errors before execution
- As a **project manager**, I want to manage multiple DNA profiles through a dashboard so I can organise projects efficiently
- As a **operator**, I want to execute SPECs and monitor progress in real-time so I know what's happening without checking files manually
- As a **analyst**, I want to view execution history and results in a structured interface so I can review outcomes easily
- As a **system administrator**, I want to deploy the dashboard with Docker so setup is simplified and consistent

---

## SPECLet Structure

This is a complex multi-phase build goal requiring SPECLet organisation:

### SPECLet [1]: Platform Foundation
**Dependencies:** None  
**Parallel allowed:** Yes  
**Purpose:** Establish core infrastructure (backend API, database, file system integration)

**Tasks:**
- Task [1.1]: Set up backend API framework
- Task [1.2]: Configure database and schema
- Task [1.3]: Implement file system service

### SPECLet [2]: Frontend Foundation
**Dependencies:** platform_foundation  
**Parallel allowed:** Yes (can develop alongside backend)  
**Purpose:** Establish frontend architecture and routing

**Tasks:**
- Task [2.1]: Set up React application with TypeScript and Vite
- Task [2.2]: Implement dashboard layout and navigation
- Task [2.3]: Configure state management with Redux Toolkit

### SPECLet [3]: DNA Profile Management
**Dependencies:** platform_foundation, frontend_foundation  
**Parallel allowed:** No  
**Purpose:** Enable creation and management of DNA profiles

**Tasks:**
- Task [3.1]: Build DNA profile list view
- Task [3.2]: Implement DNA creation form
- Task [3.3]: Add DNA editing and viewing capabilities

### SPECLet [4]: SPEC Management
**Dependencies:** platform_foundation, frontend_foundation  
**Parallel allowed:** Yes (can develop alongside DNA management)  
**Purpose:** Enable browsing, creating, and viewing SPECs

**Tasks:**
- Task [4.1]: Build SPEC list view with filtering
- Task [4.2]: Implement SPEC creation interface
- Task [4.3]: Add SPEC detail viewer

### SPECLet [5]: Parameter File Editor
**Dependencies:** platform_foundation, frontend_foundation  
**Parallel allowed:** No  
**Purpose:** Provide advanced editor for parameter files with validation

**Tasks:**
- Task [5.1]: Integrate Monaco Editor component
- Task [5.2]: Implement TOML syntax validation
- Task [5.3]: Add save functionality with backup

### SPECLet [6]: Execution & Monitoring
**Dependencies:** All previous SPECLets  
**Parallel allowed:** No  
**Purpose:** Enable SPEC execution with real-time monitoring

**Tasks:**
- Task [6.1]: Implement execution service (backend)
- Task [6.2]: Build progress monitoring with WebSocket
- Task [6.3]: Create execution controller UI

### SPECLet [7]: Results Visualisation
**Dependencies:** execution_monitoring  
**Parallel allowed:** No  
**Purpose:** Display execution results and history

**Tasks:**
- Task [7.1]: Build results viewer component
- Task [7.2]: Implement execution history browser
- Task [7.3]: Add completion verification display

### SPECLet [8]: Deployment & Documentation
**Dependencies:** All previous SPECLets  
**Parallel allowed:** No  
**Purpose:** Prepare for production deployment

**Tasks:**
- Task [8.1]: Create Docker configuration
- Task [8.2]: Write comprehensive README and setup guide
- Task [8.3]: Implement production build and optimisation

---

## Dependency Flow

```
platform_foundation
  ├──> frontend_foundation
  │      ├──> dna_profile_management
  │      ├──> spec_management (parallel with DNA)
  │      └──> parameter_file_editor
  │             └──> execution_monitoring
  │                    └──> results_visualisation
  │                           └──> deployment_documentation
```

**Execution Stages:**
1. Stage 1: platform_foundation, frontend_foundation (parallel)
2. Stage 2: dna_profile_management, spec_management (parallel after stage 1)
3. Stage 3: parameter_file_editor
4. Stage 4: execution_monitoring
5. Stage 5: results_visualisation
6. Stage 6: deployment_documentation

---

## SPECLet [1]: Platform Foundation

**Purpose:** Establish backend infrastructure  
**Dependencies:** None  
**Critical:** Yes (blocks all subsequent work)

### Task [1.1]: Set up backend API framework

**TOML Reference:** `speclets[id=1].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Create Express.js API server with TypeScript configuration

- **Step [1]:** Initialise Node.js project with TypeScript
  - **Primary method:** Create package.json, install Express, TypeScript, ts-node, @types/node, @types/express
  - **Expected output:** Backend project initialised with working TypeScript configuration
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Configure Express server with CORS and middleware
  - **Primary method:** Create src/server.ts, configure Express app with cors, express.json(), error handling
  - **Backup [1]:** If CORS issues during testing, use more permissive configuration for development
  - **Expected output:** Express server starting on port 5000 with middleware configured
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement basic route structure
  - **Primary method:** Create routes/ folder with dna.routes.ts, specs.routes.ts, execution.routes.ts, files.routes.ts
  - **Expected output:** Route handlers stubbed out with placeholder responses
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Set up environment configuration
  - **Primary method:** Install dotenv, create .env.example with SPEC_ENGINE_PATH, SPECS_PATH, PORT, DATABASE_URL
  - **Expected output:** Environment variables loading correctly, .env.example documented
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Server starts successfully, responds to health check endpoint
- **Logging:** Record backend setup in progress_Dashboard_SPEC_Engine.json

### Task [1.2]: Configure database and schema

**TOML Reference:** `speclets[id=1].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Set up SQLite database with Prisma ORM

- **Step [1]:** Install and configure Prisma
  - **Primary method:** Install @prisma/client and prisma, run prisma init with SQLite provider
  - **Expected output:** prisma/schema.prisma file created with datasource configured
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Define database schema
  - **Primary method:** Create models in schema.prisma: DnaProfile, Spec, Execution, ProgressLog
  - **Expected output:** Complete schema with relationships defined
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Run initial migration
  - **Primary method:** Execute prisma migrate dev to create database and tables
  - **Backup [1]:** If migration fails, debug schema syntax and retry
  - **Expected output:** SQLite database file created with all tables
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Create database service layer
  - **Primary method:** Create src/services/database.service.ts with PrismaClient instance and helper methods
  - **Expected output:** Database service exporting typed query methods
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Database connects successfully, can query tables
- **Logging:** Record database setup in progress

### Task [1.3]: Implement file system service

**TOML Reference:** `speclets[id=1].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Create service layer for reading/writing SPEC Engine files

- **Step [1]:** Install file system dependencies
  - **Primary method:** Install fs-extra for enhanced file operations
  - **Expected output:** fs-extra available for import
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create file path configuration
  - **Primary method:** Create src/config/paths.ts reading SPEC_ENGINE_PATH and SPECS_PATH from environment
  - **Backup [1]:** If environment variables not set, use default relative paths
  - **Expected output:** Path configuration module exporting all required paths
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement DNA profile file operations
  - **Primary method:** Create src/services/dna-files.service.ts with methods: listDnaProfiles(), readDnaProfile(), writeDnaProfile()
  - **Expected output:** Service can read/write project_constitution.toml files
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Implement SPEC file operations
  - **Primary method:** Create src/services/spec-files.service.ts with methods: listSpecs(), readSpec(), readParameters(), writeParameters()
  - **Expected output:** Service can read spec_*.md and parameters_*.toml files
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Implement progress file monitoring
  - **Primary method:** Create src/services/progress-monitor.service.ts with file watcher for progress_*.json files
  - **Expected output:** Service can watch and emit changes to progress files
  - **Critical:** false (monitoring is enhancement)
  - **Mode:** silent

- **Verification:** File operations work on test data, paths resolve correctly
- **Logging:** Record file service implementation in progress

---

## SPECLet [2]: Frontend Foundation

**Purpose:** Establish React application architecture  
**Dependencies:** None (can develop in parallel with backend)  
**Critical:** Yes (blocks all UI development)

### Task [2.1]: Set up React application with TypeScript and Vite

**TOML Reference:** `speclets[id=2].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Create frontend project structure

- **Step [1]:** Create Vite React TypeScript project
  - **Primary method:** Run npm create vite@latest frontend -- --template react-ts
  - **Expected output:** Frontend project created with TypeScript configuration
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Install core dependencies
  - **Primary method:** Install @mui/material, @mui/icons-material, @emotion/react, @emotion/styled, @reduxjs/toolkit, react-redux, react-router-dom, axios, socket.io-client
  - **Expected output:** All frontend dependencies installed
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Configure TypeScript and path aliases
  - **Primary method:** Update tsconfig.json with strict mode, path aliases (@components, @services, @store)
  - **Expected output:** TypeScript configuration with modern settings
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Set up Vite proxy for API calls
  - **Primary method:** Configure vite.config.ts with proxy to backend (localhost:5000)
  - **Expected output:** API calls proxied correctly during development
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Dev server starts, TypeScript compiles without errors
- **Logging:** Record frontend setup in progress

### Task [2.2]: Implement dashboard layout and navigation

**TOML Reference:** `speclets[id=2].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Create responsive dashboard shell with routing

- **Step [1]:** Create layout components
  - **Primary method:** Create src/components/layout/ with AppLayout, Sidebar, Header, MainContent components using MUI
  - **Expected output:** Responsive layout with collapsible sidebar
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Implement navigation structure
  - **Primary method:** Create navigation items: Dashboard Home, DNA Profiles, SPECs, Executions, Settings
  - **Expected output:** Sidebar navigation with icons and labels
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Configure React Router
  - **Primary method:** Set up BrowserRouter with routes for all major sections, create placeholder pages
  - **Expected output:** Routing working, navigation changes views
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Implement MUI theme customisation
  - **Primary method:** Create custom theme matching SPEC Engine aesthetics (professional, modern colour scheme)
  - **Expected output:** Consistent theming across application
  - **Critical:** false (default theme acceptable)
  - **Mode:** silent

- **Verification:** Navigation works, layout responsive, routes render correctly
- **Logging:** Record layout implementation in progress

### Task [2.3]: Configure state management with Redux Toolkit

**TOML Reference:** `speclets[id=2].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Set up centralised state management

- **Step [1]:** Create Redux store structure
  - **Primary method:** Create src/store/ with store.ts, configure Redux Toolkit store
  - **Expected output:** Redux store configured and provided to app
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create initial slices
  - **Primary method:** Create slices: dnaSlice (DNA profiles state), specsSlice (SPECs state), executionSlice (execution state)
  - **Expected output:** Slices with initial state, reducers, and actions
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Set up API service layer
  - **Primary method:** Create src/services/api.ts with axios instance and typed API methods
  - **Expected output:** API service with methods for all backend endpoints
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Implement Redux async thunks
  - **Primary method:** Create async thunks for data fetching (fetchDnaProfiles, fetchSpecs, startExecution, etc.)
  - **Expected output:** Async operations integrated with Redux slices
  - **Critical:** true
  - **Mode:** silent

- **Verification:** State management working, can dispatch actions and read state
- **Logging:** Record state management setup in progress

---

## SPECLet [3]: DNA Profile Management

**Purpose:** Enable DNA profile creation and management  
**Dependencies:** platform_foundation, frontend_foundation  
**Critical:** Yes (required for multi-project support)

### Task [3.1]: Build DNA profile list view

**TOML Reference:** `speclets[id=3].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Display all DNA profiles with metadata

- **Step [1]:** Create backend endpoint for listing DNA profiles
  - **Primary method:** Implement GET /api/dna endpoint returning list from database + file system
  - **Expected output:** API endpoint returning DNA profiles with dna_code, project name, settings
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build DnaList component
  - **Primary method:** Create src/pages/DnaProfiles/DnaList.tsx with MUI DataGrid or Table displaying profiles
  - **Expected output:** Table showing DNA profiles with search/filter capabilities
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Add profile actions
  - **Primary method:** Add action buttons: View, Edit, Create New
  - **Expected output:** Buttons navigate to appropriate views
  - **Critical:** true
  - **Mode:** silent

- **Verification:** DNA profiles display correctly, actions navigate properly
- **Logging:** Record DNA list implementation in progress

### Task [3.2]: Implement DNA creation form

**TOML Reference:** `speclets[id=3].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Allow users to create new DNA profiles through form

- **Step [1]:** Create DNA creation backend endpoint
  - **Primary method:** Implement POST /api/dna endpoint that generates DNA code and creates project_constitution.toml
  - **Expected output:** API creates DNA directory and configuration file
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build DNA creation form
  - **Primary method:** Create src/pages/DnaProfiles/DnaCreate.tsx with form fields matching DNA_SPEC interview questions
  - **Expected output:** Form with fields for testing, risk, autonomy, custom tools, constraints
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement form validation
  - **Primary method:** Use React Hook Form with Zod schema validation
  - **Backup [1]:** If validation library causes issues, implement manual validation
  - **Expected output:** Form validates inputs before submission
  - **Critical:** false (basic validation acceptable)
  - **Mode:** silent

- **Step [4]:** Handle form submission
  - **Primary method:** Dispatch Redux action to create DNA profile, show success/error feedback
  - **Expected output:** DNA profile created, user redirected to profile list
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Can create DNA profile through form, files created correctly
- **Logging:** Record DNA creation feature in progress

### Task [3.3]: Add DNA editing and viewing capabilities

**TOML Reference:** `speclets[id=3].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Allow viewing and editing existing DNA profiles

- **Step [1]:** Create DNA view/edit backend endpoints
  - **Primary method:** Implement GET /api/dna/:dnaCode and PUT /api/dna/:dnaCode endpoints
  - **Expected output:** API can retrieve and update DNA configuration
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build DNA detail viewer
  - **Primary method:** Create src/pages/DnaProfiles/DnaDetail.tsx displaying all DNA settings in readable format
  - **Expected output:** Component shows DNA code, project name, all configuration settings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement DNA editing
  - **Primary method:** Add edit mode to DnaDetail with form for updating settings
  - **Expected output:** User can modify DNA settings and save changes
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Can view and edit DNA profiles, changes persist correctly
- **Logging:** Record DNA editing feature in progress

---

## SPECLet [4]: SPEC Management

**Purpose:** Enable browsing and managing SPECs  
**Dependencies:** platform_foundation, frontend_foundation  
**Critical:** Yes (core dashboard functionality)

### Task [4.1]: Build SPEC list view with filtering

**TOML Reference:** `speclets[id=4].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Display all SPECs across DNA profiles

- **Step [1]:** Create backend endpoint for listing SPECs
  - **Primary method:** Implement GET /api/specs endpoint scanning file system for all spec_*.md files
  - **Expected output:** API returns list of SPECs with metadata (descriptor, DNA code, goal, status)
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build SpecList component
  - **Primary method:** Create src/pages/Specs/SpecList.tsx with table/grid view of SPECs
  - **Expected output:** Table showing SPEC name, DNA, goal, last executed, status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement filtering and search
  - **Primary method:** Add filter controls for DNA profile, status (completed/pending), search by name/goal
  - **Expected output:** Users can filter and search SPEC list
  - **Critical:** false (nice to have)
  - **Mode:** silent

- **Verification:** SPECs display correctly, filtering works
- **Logging:** Record SPEC list implementation in progress

### Task [4.2]: Implement SPEC creation interface

**TOML Reference:** `speclets[id=4].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Provide UI for creating new SPECs (simplified version, not full Commander)

- **Step [1]:** Create SPEC creation backend endpoint
  - **Primary method:** Implement POST /api/specs endpoint that creates spec_*.md, parameters_*.toml from template
  - **Expected output:** API creates SPEC files in appropriate DNA folder
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build SPEC creation form
  - **Primary method:** Create src/pages/Specs/SpecCreate.tsx with basic form (descriptor, DNA code, goal, software stack)
  - **Expected output:** Form for creating simple SPEC from template
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Handle SPEC file generation
  - **Primary method:** Form submission triggers API call, backend generates files from templates
  - **Expected output:** New SPEC files created, user redirected to SPEC detail
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Can create basic SPEC through UI, files created correctly
- **Logging:** Record SPEC creation feature in progress

### Task [4.3]: Add SPEC detail viewer

**TOML Reference:** `speclets[id=4].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Display SPEC details including goal, tasks, completion criteria

- **Step [1]:** Create SPEC detail backend endpoint
  - **Primary method:** Implement GET /api/specs/:specId endpoint reading spec_*.md and parsing structure
  - **Expected output:** API returns parsed SPEC data (goal, tasks, steps, completion criteria)
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build SpecDetail component
  - **Primary method:** Create src/pages/Specs/SpecDetail.tsx displaying SPEC information in structured format
  - **Expected output:** Component shows goal, tasks breakdown, definition of complete, software stack
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Add action buttons
  - **Primary method:** Add buttons: Edit Parameters, Execute SPEC, View Progress, View Results
  - **Expected output:** Buttons navigate to appropriate features
  - **Critical:** true
  - **Mode:** silent

- **Verification:** SPEC details display correctly, navigation works
- **Logging:** Record SPEC detail viewer in progress

---

## SPECLet [5]: Parameter File Editor

**Purpose:** Provide advanced TOML editor with validation  
**Dependencies:** platform_foundation, frontend_foundation  
**Critical:** Yes (key requirement - manual editing before execution)

### Task [5.1]: Integrate Monaco Editor component

**TOML Reference:** `speclets[id=5].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Embed VS Code editor component for file editing

- **Step [1]:** Install Monaco Editor
  - **Primary method:** Install @monaco-editor/react package
  - **Expected output:** Monaco Editor dependency available
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create ParameterEditor component
  - **Primary method:** Create src/components/ParameterEditor/ParameterEditor.tsx wrapping Monaco Editor
  - **Expected output:** Component renders editor with TOML syntax highlighting
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Configure TOML language support
  - **Primary method:** Register TOML language with Monaco, configure syntax highlighting rules
  - **Backup [1]:** If TOML support limited, use INI or similar syntax as fallback
  - **Expected output:** TOML files display with proper syntax highlighting
  - **Critical:** false (basic highlighting acceptable)
  - **Mode:** silent

- **Step [4]:** Implement editor preferences
  - **Primary method:** Add settings: theme (light/dark), font size, line numbers, minimap
  - **Expected output:** Editor preferences customisable by user
  - **Critical:** false (default settings acceptable)
  - **Mode:** silent

- **Verification:** Monaco Editor renders, TOML highlighting works
- **Logging:** Record editor integration in progress

### Task [5.2]: Implement TOML syntax validation

**TOML Reference:** `speclets[id=5].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Validate TOML syntax and SPEC Engine schema compliance

- **Step [1]:** Install TOML parser
  - **Primary method:** Install @iarna/toml or smol-toml for TOML parsing
  - **Expected output:** TOML parser available in backend
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create validation backend endpoint
  - **Primary method:** Implement POST /api/validate/toml endpoint that parses and validates TOML structure
  - **Expected output:** API returns validation result with errors/warnings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement real-time validation in editor
  - **Primary method:** Add onChange handler that debounces and calls validation endpoint
  - **Expected output:** Validation errors shown in editor with line numbers
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Add SPEC Engine schema validation
  - **Primary method:** Validate TOML contains required sections: metadata, goal, tasks, steps
  - **Expected output:** Schema validation catches missing required fields
  - **Critical:** false (syntax validation more critical)
  - **Mode:** silent

- **Verification:** Validation catches TOML syntax errors, displays them in editor
- **Logging:** Record validation implementation in progress

### Task [5.3]: Add save functionality with backup

**TOML Reference:** `speclets[id=5].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Enable saving edited parameters with automatic backup

- **Step [1]:** Create parameter save backend endpoint
  - **Primary method:** Implement PUT /api/specs/:specId/parameters endpoint that writes to parameters_*.toml
  - **Expected output:** API saves edited TOML to file
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Implement automatic backup before save
  - **Primary method:** Backend creates backup copy in .backups/ folder with timestamp before overwriting
  - **Expected output:** Original file backed up before each save
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Add save UI controls
  - **Primary method:** Add Save button with keyboard shortcut (Ctrl+S), show save status indicator
  - **Expected output:** User can save file, receives confirmation feedback
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Implement unsaved changes warning
  - **Primary method:** Track dirty state, show warning dialog if user navigates away with unsaved changes
  - **Expected output:** User prompted before losing unsaved edits
  - **Critical:** false (nice to have)
  - **Mode:** silent

- **Verification:** Can save parameter files, backups created, validation prevents saving invalid TOML
- **Logging:** Record save functionality in progress

---

## SPECLet [6]: Execution & Monitoring

**Purpose:** Enable SPEC execution with real-time progress monitoring  
**Dependencies:** All previous SPECLets  
**Critical:** Yes (core functionality)

### Task [6.1]: Implement execution service (backend)

**TOML Reference:** `speclets[id=6].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Backend service to spawn and manage SPEC execution

- **Step [1]:** Install process management dependencies
  - **Primary method:** Install child_process utilities for spawning LLM processes
  - **Expected output:** Process spawning available
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create execution service
  - **Primary method:** Create src/services/execution.service.ts with methods: startExecution(), stopExecution(), getExecutionStatus()
  - **Expected output:** Service can spawn exe_*.md execution and track process
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement execution endpoint
  - **Primary method:** Create POST /api/executions endpoint that starts SPEC execution, returns execution_id
  - **Expected output:** API starts execution and returns tracking ID
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Handle execution lifecycle
  - **Primary method:** Track execution state (pending, running, completed, failed), update database
  - **Expected output:** Execution records created and updated in database
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Implement execution log capture
  - **Primary method:** Capture stdout/stderr from execution process, store in database or file
  - **Expected output:** Execution logs available for viewing
  - **Critical:** false (progress monitoring more critical)
  - **Mode:** silent

- **Verification:** Can start SPEC execution via API, execution tracked correctly
- **Logging:** Record execution service in progress

### Task [6.2]: Build progress monitoring with WebSocket

**TOML Reference:** `speclets[id=6].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Real-time progress updates via WebSocket

- **Step [1]:** Configure Socket.io on backend
  - **Primary method:** Install socket.io, set up WebSocket server on Express
  - **Expected output:** WebSocket server running on backend
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Implement progress file watcher
  - **Primary method:** Use fs.watch or chokidar to watch progress_*.json files, emit changes via WebSocket
  - **Expected output:** Progress updates broadcast when files change
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Create WebSocket client in frontend
  - **Primary method:** Use socket.io-client to connect to backend WebSocket
  - **Expected output:** Frontend receives real-time progress updates
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Implement reconnection logic
  - **Primary method:** Handle WebSocket disconnections, auto-reconnect with exponential backoff
  - **Backup [1]:** If WebSocket unreliable, fall back to polling progress endpoint
  - **Expected output:** Connection resilient to network issues
  - **Critical:** false (polling is acceptable backup)
  - **Mode:** silent

- **Verification:** Real-time updates work, progress changes visible immediately
- **Logging:** Record WebSocket implementation in progress

### Task [6.3]: Create execution controller UI

**TOML Reference:** `speclets[id=6].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** UI for starting execution and monitoring progress

- **Step [1]:** Build execution control panel
  - **Primary method:** Create src/pages/Execution/ExecutionControl.tsx with mode selection and start button
  - **Expected output:** UI allows selecting execution mode (Silent/Dynamic/Collaborative) and starting execution
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Implement progress visualisation
  - **Primary method:** Create ProgressMonitor component displaying task/step breakdown with status indicators
  - **Expected output:** Visual representation of execution progress (tasks, steps, status)
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Add real-time progress updates
  - **Primary method:** Connect ProgressMonitor to WebSocket, update UI when progress events received
  - **Expected output:** Progress UI updates in real-time without manual refresh
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Implement execution controls
  - **Primary method:** Add buttons: Stop Execution, View Logs, View Full Progress (open progress.json)
  - **Expected output:** User can control and inspect running execution
  - **Critical:** false (stop functionality nice to have)
  - **Mode:** silent

- **Verification:** Can start execution from UI, see real-time progress updates
- **Logging:** Record execution UI in progress

---

## SPECLet [7]: Results Visualisation

**Purpose:** Display execution results and history  
**Dependencies:** execution_monitoring  
**Critical:** Yes (users need to see outcomes)

### Task [7.1]: Build results viewer component

**TOML Reference:** `speclets[id=7].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Display execution outcome and completion verification

- **Step [1]:** Create results backend endpoint
  - **Primary method:** Implement GET /api/executions/:executionId/results reading progress_*.json and parsing completion data
  - **Expected output:** API returns goal achievement status, completion verification, post-execution analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build ResultsViewer component
  - **Primary method:** Create src/pages/Results/ResultsViewer.tsx displaying goal status (ACHIEVED/PARTIAL/NOT ACHIEVED)
  - **Expected output:** Component shows outcome with visual indicator (success/warning/error)
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Display completion verification
  - **Primary method:** Show verification checklist with status (primary deliverable, quality standards, verification method)
  - **Expected output:** User sees which completion criteria passed/failed
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Show post-execution analysis
  - **Primary method:** Display failure patterns, backup effectiveness, constitutional compliance score
  - **Expected output:** Analysis section shows insights from execution
  - **Critical:** false (core outcome more critical)
  - **Mode:** silent

- **Verification:** Results display correctly, outcome clear
- **Logging:** Record results viewer in progress

### Task [7.2]: Implement execution history browser

**TOML Reference:** `speclets[id=7].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Browse past executions with filtering

- **Step [1]:** Create execution history endpoint
  - **Primary method:** Implement GET /api/executions endpoint querying database for past executions
  - **Expected output:** API returns list of executions with metadata (spec, status, duration, timestamp)
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Build ExecutionHistory component
  - **Primary method:** Create src/pages/Results/ExecutionHistory.tsx with table of past executions
  - **Expected output:** Table showing execution history with filtering by SPEC, date, status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Add execution comparison
  - **Primary method:** Allow selecting multiple executions to compare outcomes
  - **Expected output:** Side-by-side comparison of execution results
  - **Critical:** false (nice to have)
  - **Mode:** silent

- **Verification:** Can browse execution history, filter and sort works
- **Logging:** Record history browser in progress

### Task [7.3]: Add completion verification display

**TOML Reference:** `speclets[id=7].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Detailed view of completion criteria verification

- **Step [1]:** Create verification detail component
  - **Primary method:** Create CompletionVerification component showing each criterion with pass/fail status
  - **Expected output:** Component displays universal checks and build-specific verification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Add drill-down to verification details
  - **Primary method:** Allow expanding each criterion to see details (e.g., which files verified, what tests passed)
  - **Expected output:** User can see granular verification information
  - **Critical:** false (summary is sufficient)
  - **Mode:** silent

- **Verification:** Verification display shows accurate completion criteria status
- **Logging:** Record verification display in progress

---

## SPECLet [8]: Deployment & Documentation

**Purpose:** Prepare application for production deployment  
**Dependencies:** All previous SPECLets  
**Critical:** Yes (required for delivery)

### Task [8.1]: Create Docker configuration

**TOML Reference:** `speclets[id=8].tasks[id=1]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Containerise application for easy deployment

- **Step [1]:** Create backend Dockerfile
  - **Primary method:** Write Dockerfile for Node.js backend with multi-stage build (build + production)
  - **Expected output:** Backend Dockerfile building working image
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create frontend Dockerfile
  - **Primary method:** Write Dockerfile for frontend with Nginx serving static build
  - **Expected output:** Frontend Dockerfile building working image
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Create Docker Compose configuration
  - **Primary method:** Write docker-compose.yml orchestrating backend, frontend, database
  - **Expected output:** docker-compose up starts complete application stack
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Add volume configuration for SPEC Engine files
  - **Primary method:** Configure volumes to mount __SPEC_Engine/ and SPECs/ directories
  - **Expected output:** Container accesses host file system for SPEC files
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Application starts via Docker Compose, all features work in container
- **Logging:** Record Docker configuration in progress

### Task [8.2]: Write comprehensive README and setup guide

**TOML Reference:** `speclets[id=8].tasks[id=2]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Document installation, configuration, and usage

- **Step [1]:** Create main README.md
  - **Primary method:** Write README with sections: Overview, Features, Requirements, Installation, Configuration, Usage
  - **Expected output:** Comprehensive README documenting entire application
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Document environment configuration
  - **Primary method:** Create .env.example with all required variables documented
  - **Expected output:** Users know how to configure application
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Write deployment guide
  - **Primary method:** Create DEPLOYMENT.md with instructions for Docker, standalone, and development setup
  - **Expected output:** Clear deployment instructions for different scenarios
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Create API documentation
  - **Primary method:** Document all API endpoints with request/response examples
  - **Expected output:** API.md file with complete endpoint documentation
  - **Critical:** false (nice to have)
  - **Mode:** silent

- **Verification:** Documentation is clear, setup instructions work when followed
- **Logging:** Record documentation in progress

### Task [8.3]: Implement production build and optimisation

**TOML Reference:** `speclets[id=8].tasks[id=3]` in parameters_Dashboard_SPEC_Engine.toml  
**Purpose:** Optimise application for production deployment

- **Step [1]:** Configure frontend production build
  - **Primary method:** Optimise Vite build configuration (minification, tree-shaking, code splitting)
  - **Expected output:** Frontend builds to optimised static assets
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Implement backend production settings
  - **Primary method:** Add production mode configuration (logging, error handling, security headers)
  - **Expected output:** Backend runs efficiently in production mode
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Add health check endpoints
  - **Primary method:** Implement /health and /ready endpoints for monitoring
  - **Expected output:** Monitoring systems can check application health
  - **Critical:** false (nice to have)
  - **Mode:** silent

- **Step [4]:** Implement logging
  - **Primary method:** Add structured logging with Winston or Pino
  - **Expected output:** Production logs are structured and queryable
  - **Critical:** false (console logs acceptable)
  - **Mode:** silent

- **Verification:** Production build works, application runs efficiently
- **Logging:** Record production optimisation in progress

---

## Post-Execution Analysis

After all SPECLets complete, verify:

### Universal Checks
- Primary deliverable exists: Web application deployed and accessible
- Quality standards met: All features functional, UI responsive, validation working
- Verification method passed: Complete workflow test successful (DNA → SPEC → Edit → Execute → Monitor → Results)

### Build-Specific Verification (Article XIV)
- Deployment artifact exists: Docker image or standalone package ready
- UI fully implemented: All six core features working (not placeholders)
- Production-ready: Error handling, logging, validation in place
- Database migrations: Schema setup automated
- Documentation: README with setup instructions exists
- Environment configuration: .env.example provided

### Compliance Review
- Article I (North Star): Goal singular - build dashboard for SPEC Engine
- Article II (Hierarchy): SPECLets, tasks, steps all within recommended ranges
- Article VI (Critical balance): Critical steps appropriately flagged
- Article XIV (Completeness): All build requirements satisfied

---

## Recommendations

### If Goal ACHIEVED
- Consider enhancements: Dark mode, keyboard shortcuts, advanced filtering
- Add analytics: Track SPEC execution patterns, success rates
- Implement user authentication for multi-user scenarios
- Add backup/restore functionality for SPEC configurations

### If Goal PARTIAL
- Review which features incomplete
- Prioritise core functionality over enhancements
- Document known limitations in README

### If Goal NOT ACHIEVED
- Identify blocking issues (execution service, WebSocket, editor integration)
- Review architectural decisions
- Consider simpler alternatives for failed components

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-02 | Initial SPEC creation for SPEC Engine Dashboard |

---

**This SPEC is ready for execution.** Provide `exe_Dashboard_SPEC_Engine.md` to executor agent when ready to begin development.
