# Dashboard SPEC Engine - README

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Type:** TOOLSPEC (Specialised SPEC for SPEC Engine ecosystem)

---

## Overview

The Dashboard SPEC Engine is a comprehensive specification for building a production-ready web application dashboard that provides a modern graphical interface for the SPEC Engine framework. This TOOLSPEC enables developers to create a full-stack web application that facilitates all key SPEC Engine features.

**What this SPEC builds:**
- Full-stack web application (React + TypeScript + Node.js + Express)
- DNA Profile management interface
- SPEC creation and management system
- Advanced parameter file editor with Monaco Editor
- Real-time SPEC execution monitoring via WebSocket
- Progress visualisation dashboard
- Results and execution history browser
- Docker containerised deployment

---

## Why This TOOLSPEC Exists

The SPEC Engine is a powerful framework for structured LLM-driven goal achievement, but it currently requires:
- Manual file creation and editing
- Command-line execution
- Manual monitoring of progress.json files
- File system navigation to review results

This TOOLSPEC addresses those limitations by providing:
1. **Graphical Interface:** Web-based dashboard for all SPEC Engine operations
2. **Parameter Editing:** Monaco Editor integration with TOML validation
3. **Real-time Monitoring:** Live progress updates during SPEC execution
4. **Centralised Management:** All DNA profiles and SPECs in one place
5. **Execution History:** Browse and compare past executions
6. **User-Friendly:** Modern UI following Material Design principles

---

## What You Get

### Frontend Application (React + TypeScript + Vite)
- Dashboard home with overview statistics
- DNA Profile Manager (create, edit, view, delete profiles)
- SPEC Browser with filtering and search
- SPEC Detail Viewer showing goal, tasks, completion criteria
- Parameter File Editor with syntax highlighting and validation
- Execution Controller with mode selection
- Progress Monitor with real-time updates
- Results Viewer with completion verification
- Settings panel for configuration

### Backend API (Node.js + Express + TypeScript)
- REST API for all CRUD operations
- File system integration (reads/writes SPEC Engine files)
- TOML validation service
- Execution service (spawns exe_*.md processes)
- WebSocket server for real-time progress broadcasting
- Progress file monitoring with file watchers

### Database (SQLite + Prisma)
- DNA profiles metadata
- SPECs metadata and relationships
- Execution history tracking
- Progress logs for analytics

### Deployment
- Docker Compose configuration
- Multi-stage Dockerfiles for optimised images
- Environment configuration templates
- Production-ready build optimisation

---

## Key Features

### 1. DNA Profile Management
- Create DNA profiles through guided form (matches DNA_SPEC interview)
- View all profiles with project metadata
- Edit existing profile settings
- Automatic DNA code generation (8-character A/T/G/C sequence)

### 2. SPEC Management
- Browse all SPECs across DNA profiles
- Filter and search by name, DNA, goal, status
- View detailed SPEC information (goal, tasks, steps, software stack)
- Create simple SPECs from templates (simplified Commander interface)

### 3. Parameter File Editor (KEY REQUIREMENT)
- Monaco Editor integration (full VS Code editor experience)
- TOML syntax highlighting
- Real-time validation with error display
- SPEC Engine schema validation
- Automatic backup before save
- Unsaved changes warning
- Keyboard shortcuts (Ctrl+S to save)

### 4. SPEC Execution
- Execute SPECs directly from dashboard
- Select execution mode (Silent, Dynamic, Collaborative)
- Real-time progress monitoring via WebSocket
- Task/step breakdown visualisation
- Status indicators for each step
- Execution logs capture

### 5. Progress Monitoring
- Real-time updates without manual refresh
- Visual progress indicators (task/step level)
- File watcher monitoring progress_*.json files
- WebSocket broadcasting for instant updates
- Reconnection logic for network resilience

### 6. Results Visualisation
- Goal achievement status (ACHIEVED/PARTIAL/NOT ACHIEVED)
- Completion verification display
- Post-execution analysis insights
- Execution history browser
- Filter by SPEC, date, status
- Execution comparison view

---

## Technology Stack

### Frontend
| Technology | Purpose | Why |
|------------|---------|-----|
| React 18+ | UI framework | Industry standard, component-based |
| TypeScript | Type safety | Prevents bugs, better DX |
| Vite | Build tool | Fast dev server, optimised builds |
| Material-UI v5 | Component library | Professional, accessible, themeable |
| Redux Toolkit | State management | Centralised state, easy async handling |
| Monaco Editor | Code editor | VS Code quality editing |
| Socket.io Client | WebSocket | Real-time updates |
| React Router | Routing | SPA navigation |

### Backend
| Technology | Purpose | Why |
|------------|---------|-----|
| Node.js 20 LTS | Runtime | Stable, modern features |
| Express.js | API framework | Simple, flexible, well-documented |
| TypeScript | Type safety | Shared types with frontend |
| Socket.io | WebSocket server | Real-time bidirectional communication |
| fs-extra | File operations | Enhanced file system utilities |
| Prisma | ORM | Type-safe database access |
| Zod | Validation | Schema validation |

### Database
| Technology | Purpose | Why |
|------------|---------|-----|
| SQLite | Database | File-based, zero-configuration, portable |
| Prisma | ORM | Type-safe queries, migrations |

### Deployment
| Technology | Purpose | Why |
|------------|---------|-----|
| Docker | Containerisation | Consistent deployment |
| Docker Compose | Orchestration | Multi-container management |
| Nginx | Static serving | Efficient frontend delivery |
| PM2 | Process management | Production process management |

---

## How This SPEC Works

### SPECLet Architecture
This SPEC uses the SPECLet abstraction layer for complex multi-phase organisation:

```
1. Platform Foundation (backend API, database, file system)
   ├─> 2. Frontend Foundation (React app, routing, state)
   │      ├─> 3. DNA Profile Management
   │      ├─> 4. SPEC Management (parallel with DNA)
   │      └─> 5. Parameter File Editor
   │             └─> 6. Execution & Monitoring
   │                    └─> 7. Results Visualisation
   │                           └─> 8. Deployment & Documentation
```

**Total:** 8 SPECLets, 24 Tasks, ~95 Steps

### Execution Flow
1. **Platform Foundation** establishes backend infrastructure
2. **Frontend Foundation** builds React application shell
3. **DNA & SPEC Management** run in parallel (independent features)
4. **Parameter Editor** requires foundation from previous SPECLets
5. **Execution & Monitoring** integrates all previous work
6. **Results Visualisation** builds on execution features
7. **Deployment & Documentation** finalises production readiness

### Critical Steps
- Approximately 60% of steps marked as critical (constitutional compliance)
- Critical steps block goal achievement if failed
- Non-critical steps logged but allow continuation

---

## Prerequisites

Before executing this SPEC, ensure you have:

### Required
- **LLM with coding capability** (GPT-4, Claude, etc.)
- **SPEC Engine framework** installed and functional
- **Node.js 20 LTS or later** for backend development
- **npm or yarn** for package management
- **Git** for version control (recommended)

### Recommended
- **Docker Desktop** for containerised deployment
- **VS Code** or similar editor for development review
- **Modern web browser** (Chrome, Firefox, Edge) for testing
- **Minimum 8GB RAM** for running full stack locally

### File System Access
The dashboard must have:
- **Read access** to `__SPEC_Engine/` directory (framework files)
- **Read/Write access** to `SPECs/` directory (DNA profiles, SPECs, parameters)
- **File system permissions** appropriate for your OS

---

## How to Use This TOOLSPEC

### Option 1: Direct Execution (Recommended for experienced users)

If you're familiar with SPEC execution and want the full dashboard:

```
1. Provide spec_Dashboard_SPEC_Engine.md to your LLM
2. Provide parameters_Dashboard_SPEC_Engine.toml to your LLM
3. Say: "Execute this SPEC to build the SPEC Engine Dashboard"
4. LLM will proceed with all 8 SPECLets sequentially
```

The LLM will:
- Set up backend infrastructure
- Build frontend application
- Implement all features
- Create Docker configuration
- Write deployment documentation

**Expected time:** 4-8 hours (depending on LLM speed)

### Option 2: Commander-Assisted Generation

If you want customisation or a different approach:

```
1. Provide __SPEC_Engine/_Commander_SPEC/Spec_Commander.md to your LLM
2. Say: "Create a SPEC for building a web dashboard for the SPEC Engine framework with parameter editing, execution monitoring, and results visualisation"
3. Commander will interview you and generate a custom SPEC
4. Review and approve the generated SPEC
5. Execute the custom SPEC
```

This allows you to:
- Modify technology stack
- Adjust features
- Change architecture
- Customise deployment

### Option 3: Incremental Execution (For learning or low-resource scenarios)

Execute one SPECLet at a time:

```
1. Start with SPECLet 1 (Platform Foundation)
2. Test backend API works
3. Move to SPECLet 2 (Frontend Foundation)
4. Test frontend shell works
5. Continue through remaining SPECLets
```

This allows:
- Testing at each stage
- Lower memory requirements per execution
- Learning the codebase incrementally
- Easier debugging

---

## What Gets Built

After execution, you'll have:

### Directory Structure
```
spec-engine-dashboard/
├── backend/
│   ├── src/
│   │   ├── server.ts
│   │   ├── routes/
│   │   ├── services/
│   │   ├── config/
│   │   └── prisma/
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
├── DEPLOYMENT.md
└── API.md
```

### Running the Application

**Development:**
```bash
# Terminal 1 - Backend
cd backend
npm install
npm run dev

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev

# Access: http://localhost:3000
```

**Production (Docker):**
```bash
docker-compose up -d

# Access: http://localhost:3000
```

### Using the Dashboard

1. **Create DNA Profile:** Navigate to DNA Profiles → Create New → Fill form → Save
2. **Browse SPECs:** Navigate to SPECs → View all SPECs across profiles
3. **Edit Parameters:** Click on SPEC → Edit Parameters → Monaco editor opens → Make changes → Save
4. **Execute SPEC:** Click on SPEC → Execute → Select mode → Start → Monitor progress
5. **View Results:** After execution → View Results → See completion verification and analysis

---

## Key Requirements Satisfied

This SPEC satisfies all user requirements:

1. **Web App Dashboard:** Full-stack application with modern UI
2. **All Key Features:** DNA, SPECs, editing, execution, monitoring, results
3. **Manual Parameter Editing:** Monaco Editor with validation (KEY REQUIREMENT)
4. **Real-time Monitoring:** WebSocket updates during execution
5. **Production-Ready:** Docker deployment, documentation, error handling

---

## Constitutional Compliance

This SPEC adheres to SPEC Engine Constitution:

- **Article I (North Star):** Singular goal - build dashboard
- **Article II (Hierarchy):** SPECLets → Tasks → Steps properly structured
- **Article III (Bridging):** spec.md and parameters.toml synchronised
- **Article VI (Critical Balance):** ~60% critical steps
- **Article VII (Genuine Backups):** Alternative approaches, not retries
- **Article IX (Execution Modes):** Dynamic mode with escalation
- **Article XIV (Completeness):** All build requirements defined

---

## Limitations & Trade-offs

### What This Dashboard IS
- Production-ready web interface for SPEC Engine
- Full CRUD operations for DNA and SPECs
- Advanced parameter editing with validation
- Real-time execution monitoring
- Docker-deployable application

### What This Dashboard IS NOT
- Full Commander replacement (simplified SPEC creation only)
- Multi-user system with authentication (single-user focused)
- Cloud-hosted SaaS (self-hosted application)
- Mobile app (desktop web interface)

### Architectural Decisions

**File-based Database (SQLite):**
- **Pro:** Simple, no server, portable, sufficient for use case
- **Con:** Not suitable for high concurrency or large scale
- **Rationale:** SPEC Engine is typically single-user or small team

**Monaco Editor (heavy bundle):**
- **Pro:** Full VS Code experience, TOML support, validation
- **Con:** Large bundle size (~10MB)
- **Rationale:** Core requirement - quality editing worth the size

**WebSocket for Progress:**
- **Pro:** Real-time updates, no polling overhead
- **Con:** More complex than REST, connection management
- **Rationale:** Better UX, more efficient than polling

**Docker Deployment:**
- **Pro:** Consistent environment, easy setup
- **Con:** Requires Docker installation
- **Rationale:** Modern best practice, simplifies dependencies

---

## Maintenance & Extension

### After Build Completion

**Test thoroughly:**
1. Create DNA profile through form
2. Create SPEC through simplified interface
3. Edit parameter file, introduce errors, verify validation
4. Execute SPEC, verify real-time progress updates
5. View results, check completion verification

**Potential Enhancements:**
- User authentication for multi-user scenarios
- Dark mode support
- Keyboard shortcuts throughout UI
- Advanced SPEC comparison analytics
- Export execution reports as PDF
- Integration with version control (Git)
- LLM provider switching (use different LLMs for execution)

### Troubleshooting

**Backend won't start:**
- Check Node.js version (20+ required)
- Verify .env configuration
- Check database file permissions
- Review console logs for errors

**Frontend build fails:**
- Clear node_modules, reinstall dependencies
- Check TypeScript errors
- Verify Vite configuration
- Check for port conflicts

**WebSocket not connecting:**
- Verify backend Socket.io running
- Check firewall settings
- Review CORS configuration
- Test with polling fallback

**Parameter validation not working:**
- Check TOML parser installation
- Verify backend endpoint responding
- Review browser network tab
- Test validation endpoint directly

---

## Related Documents

- **spec_Dashboard_SPEC_Engine.md:** Human-readable specification (THIS TOOLSPEC)
- **parameters_Dashboard_SPEC_Engine.toml:** Machine-readable configuration
- **QUICK_START.md:** Fast-track guide for experienced developers
- **__SPEC_Engine/README.md:** SPEC Engine framework documentation
- **__SPEC_Engine/GETTING_STARTED.md:** SPEC Engine beginner tutorial

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-02 | Initial TOOLSPEC creation |

---

## Questions?

**Where is the executor (exe_*.md)?**
- For TOOLSPECs, the spec and parameters files are sufficient
- Provide both to your LLM and say "Execute this SPEC"
- LLM will follow the SPEC Engine execution principles automatically

**Can I modify this SPEC before execution?**
- Yes! Edit spec_Dashboard_SPEC_Engine.md and/or parameters_Dashboard_SPEC_Engine.toml
- Common modifications: technology stack, features to exclude, deployment approach
- Ensure spec.md and parameters.toml stay synchronised (Article III)

**How long will execution take?**
- Estimated 4-8 hours for complete build
- Depends on LLM speed, token limits, complexity
- Can pause and resume between SPECLets

**What if execution fails partway through?**
- Review progress_Dashboard_SPEC_Engine.json to see what completed
- Identify failed task/step
- Fix underlying issue (missing dependencies, file permissions, etc.)
- Resume from failed SPECLet or restart

**Can I deploy this alongside existing SPEC Engine projects?**
- Yes! Dashboard integrates with existing __SPEC_Engine/ and SPECs/ directories
- Configure paths in .env to point to your SPEC Engine installation
- Dashboard operates on existing DNA profiles and SPECs

---

**Ready to build?** Provide spec_Dashboard_SPEC_Engine.md and parameters_Dashboard_SPEC_Engine.toml to your LLM and say "Execute this SPEC".
