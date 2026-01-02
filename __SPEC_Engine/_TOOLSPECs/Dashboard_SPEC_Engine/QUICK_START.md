# Dashboard SPEC Engine - Quick Start Guide

**For experienced developers who want to build the dashboard immediately.**

---

## TL;DR

```bash
# 1. Provide these files to your LLM:
- spec_Dashboard_SPEC_Engine.md
- parameters_Dashboard_SPEC_Engine.toml

# 2. Say to LLM:
"Execute this SPEC to build the SPEC Engine Dashboard"

# 3. Wait 4-8 hours for complete build

# 4. After build:
cd spec-engine-dashboard
docker-compose up -d

# 5. Access:
http://localhost:3000
```

---

## What You'll Get

A production-ready web application with:

- **Frontend:** React 18 + TypeScript + MUI + Vite
- **Backend:** Node.js 20 + Express + TypeScript + Socket.io
- **Database:** SQLite + Prisma
- **Editor:** Monaco Editor with TOML validation
- **Monitoring:** Real-time WebSocket progress updates
- **Deployment:** Docker Compose configuration

---

## Prerequisites

**Required:**
- LLM with coding capability (GPT-4, Claude, etc.)
- SPEC Engine framework installed
- Node.js 20+ and npm
- Docker Desktop (for production deployment)

**Recommended:**
- 8GB+ RAM
- Modern web browser
- VS Code or similar editor

---

## Execution Options

### Option 1: Full Build (Recommended)

Execute all 8 SPECLets sequentially for complete dashboard:

```
LLM Prompt:
"Execute spec_Dashboard_SPEC_Engine.md to build the SPEC Engine Dashboard.
Use parameters_Dashboard_SPEC_Engine.toml for configuration."
```

**Time:** 4-8 hours  
**Result:** Complete application ready to deploy

### Option 2: Incremental Build

Execute SPECLets one at a time for testing and learning:

```
SPECLet 1: Platform Foundation (backend, database, file system)
Test: curl http://localhost:5000/health

SPECLet 2: Frontend Foundation (React app, routing, state)
Test: npm run dev (frontend should load)

SPECLet 3: DNA Profile Management
Test: Create DNA profile through UI

SPECLet 4: SPEC Management
Test: Browse SPECs in UI

SPECLet 5: Parameter File Editor
Test: Edit parameter file, see validation

SPECLet 6: Execution & Monitoring
Test: Execute SPEC, see real-time progress

SPECLet 7: Results Visualisation
Test: View execution results

SPECLet 8: Deployment & Documentation
Result: Docker configuration and README
```

**Time:** Variable (pause between SPECLets)  
**Result:** Same complete application, tested at each stage

---

## Post-Build Setup

### Development Environment

```bash
# Backend
cd spec-engine-dashboard/backend
npm install
cp .env.example .env
# Edit .env: Set SPEC_ENGINE_PATH and SPECS_PATH
npm run dev

# Frontend (separate terminal)
cd spec-engine-dashboard/frontend
npm install
npm run dev

# Access: http://localhost:3000
```

### Production Environment (Docker)

```bash
cd spec-engine-dashboard

# Edit .env file
SPEC_ENGINE_PATH=/path/to/__SPEC_Engine
SPECS_PATH=/path/to/SPECs

# Start services
docker-compose up -d

# Access: http://localhost:3000

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Configuration

### Environment Variables (.env)

```env
# Backend Configuration
PORT=5000
NODE_ENV=production

# File Paths (CRITICAL - adjust for your system)
SPEC_ENGINE_PATH=C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine
SPECS_PATH=C:\Users\Fab2\Desktop\AI\Specs\SPECs

# Database
DATABASE_URL=file:./dev.db

# CORS (for development)
FRONTEND_URL=http://localhost:3000
```

**Windows Users:** Use forward slashes or escape backslashes:
- `C:/Users/Fab2/Desktop/AI/Specs/__SPEC_Engine` OR
- `C:\\Users\\Fab2\\Desktop\\AI\\Specs\\__SPEC_Engine`

### Frontend Configuration (frontend/src/config.ts)

```typescript
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
export const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:5000';
```

---

## Usage Workflow

### 1. Create DNA Profile

```
Dashboard → DNA Profiles → Create New
Fill form:
  - Project Name: "My Project"
  - Testing: "Basic"
  - Risk Tolerance: "Medium"
  - Autonomy: "High"
→ Submit
Result: DNA code generated (e.g., ATGCTCGA)
```

### 2. Browse SPECs

```
Dashboard → SPECs
View all SPECs across DNA profiles
Filter by DNA code, status, or search by name
Click on SPEC to view details
```

### 3. Edit Parameter File (KEY FEATURE)

```
Dashboard → SPECs → Select SPEC → Edit Parameters
Monaco Editor opens with parameters_*.toml
Make changes (syntax highlighting active)
Validation runs automatically (errors shown inline)
Ctrl+S to save (backup created automatically)
```

### 4. Execute SPEC

```
Dashboard → SPECs → Select SPEC → Execute
Select execution mode:
  - Silent: Fully autonomous
  - Dynamic: Autonomous with escalation (recommended)
  - Collaborative: Human-in-loop
→ Start Execution
Real-time progress updates appear
Monitor task/step progress
```

### 5. View Results

```
Dashboard → Executions → Select Execution
View:
  - Goal Achievement Status (ACHIEVED/PARTIAL/NOT ACHIEVED)
  - Completion Verification (checklist)
  - Post-Execution Analysis (insights)
  - Execution logs
```

### 6. Browse History

```
Dashboard → Executions
View all past executions
Filter by SPEC, date, status
Compare multiple executions
```

---

## Key Features

| Feature | Location | Purpose |
|---------|----------|---------|
| DNA Profiles | `/dna-profiles` | Create and manage project configurations |
| SPECs Browser | `/specs` | Browse and manage specifications |
| SPEC Detail | `/specs/:id` | View goal, tasks, completion criteria |
| Parameter Editor | `/specs/:id/edit` | Edit TOML with validation (KEY) |
| Execute SPEC | `/execute/:id` | Start execution with mode selection |
| Progress Monitor | `/execute/:id/monitor` | Real-time progress updates |
| Results Viewer | `/results/:id` | View completion verification |
| Execution History | `/executions` | Browse past executions |
| Settings | `/settings` | Configure file paths and preferences |

---

## Troubleshooting

### Backend Won't Start

```bash
# Check Node version
node --version  # Should be 20+

# Check logs
cd backend
npm run dev
# Read error messages

# Common issues:
- Missing .env file → Copy from .env.example
- Wrong paths in .env → Verify SPEC_ENGINE_PATH and SPECS_PATH exist
- Port 5000 in use → Change PORT in .env
- Database error → Delete dev.db and run: npx prisma migrate dev
```

### Frontend Won't Build

```bash
# Check Node version
node --version  # Should be 20+

# Clear and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run build

# Common issues:
- Type errors → Check tsconfig.json
- Import errors → Verify path aliases in vite.config.ts
- API connection → Verify backend running on :5000
```

### WebSocket Not Connecting

```bash
# Check backend Socket.io server
curl http://localhost:5000/socket.io/

# Should return: {"code":0,"message":"Transport unknown"}
# (This is expected - means Socket.io is running)

# Check browser console for WebSocket errors
# Common issues:
- CORS blocking → Check backend CORS configuration
- Firewall blocking → Allow port 5000
- Backend not running → Start backend server
```

### Parameter Editor Not Validating

```bash
# Test validation endpoint directly
curl -X POST http://localhost:5000/api/validate/toml \
  -H "Content-Type: application/json" \
  -d '{"content": "[metadata]\nspec_version = \"1.0\""}'

# Should return: {"valid": true} or validation errors

# Common issues:
- TOML parser missing → Check backend package.json for @iarna/toml
- Endpoint not responding → Check backend routes
- Validation too slow → Check debounce settings in frontend
```

### SPEC Execution Fails to Start

```bash
# Check execution service
curl -X POST http://localhost:5000/api/executions \
  -H "Content-Type: application/json" \
  -d '{"specId": "test-spec", "mode": "dynamic"}'

# Common issues:
- exe_*.md not found → Verify SPECS_PATH correct
- Process spawn error → Check file permissions
- LLM not available → Ensure LLM context for execution
```

---

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │  React + TypeScript + MUI
│   (Port 3000)   │  Monaco Editor, Redux, Socket.io Client
└────────┬────────┘
         │ HTTP/WebSocket
         │
┌────────▼────────┐
│   Backend       │  Node.js + Express + TypeScript
│   (Port 5000)   │  REST API, Socket.io Server, File Watchers
└────────┬────────┘
         │
    ┌────┴─────┬──────────────┐
    │          │              │
┌───▼───┐  ┌───▼────────┐  ┌─▼─────────────┐
│SQLite │  │File System │  │exe_*.md       │
│Prisma │  │Service     │  │Execution      │
│       │  │TOML Parser │  │(SPEC Engine)  │
└───────┘  └────────────┘  └───────────────┘
```

---

## File Structure

```
spec-engine-dashboard/
├── backend/
│   ├── src/
│   │   ├── server.ts          # Express server entry
│   │   ├── routes/            # API endpoints
│   │   │   ├── dna.routes.ts
│   │   │   ├── specs.routes.ts
│   │   │   ├── execution.routes.ts
│   │   │   └── files.routes.ts
│   │   ├── services/          # Business logic
│   │   │   ├── database.service.ts
│   │   │   ├── dna-files.service.ts
│   │   │   ├── spec-files.service.ts
│   │   │   ├── execution.service.ts
│   │   │   └── progress-monitor.service.ts
│   │   ├── config/            # Configuration
│   │   │   └── paths.ts
│   │   └── prisma/            # Database schema
│   │       └── schema.prisma
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── layout/
│   │   │   └── ParameterEditor/
│   │   ├── pages/             # Route pages
│   │   │   ├── DnaProfiles/
│   │   │   ├── Specs/
│   │   │   ├── Execution/
│   │   │   └── Results/
│   │   ├── store/             # Redux state
│   │   │   ├── store.ts
│   │   │   ├── dnaSlice.ts
│   │   │   ├── specsSlice.ts
│   │   │   └── executionSlice.ts
│   │   ├── services/          # API calls
│   │   │   └── api.ts
│   │   ├── App.tsx            # Root component
│   │   └── main.tsx           # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml          # Container orchestration
├── .env.example                # Environment template
├── README.md                   # Full documentation
├── DEPLOYMENT.md               # Deployment guide
└── API.md                      # API documentation
```

---

## Testing Checklist

After build completion, verify:

- [ ] Backend starts without errors (`npm run dev`)
- [ ] Frontend loads in browser (`http://localhost:3000`)
- [ ] Dashboard home displays correctly
- [ ] Can create DNA profile through form
- [ ] DNA profile appears in list
- [ ] Can browse SPECs across DNA profiles
- [ ] SPEC detail page shows goal, tasks, completion criteria
- [ ] Parameter editor opens with Monaco Editor
- [ ] TOML syntax highlighting works
- [ ] Validation catches syntax errors
- [ ] Can save parameter file (Ctrl+S)
- [ ] Backup created before save
- [ ] Can start SPEC execution
- [ ] Mode selection works (Silent/Dynamic/Collaborative)
- [ ] Real-time progress updates appear
- [ ] Task/step status indicators update
- [ ] Execution completes successfully
- [ ] Results page shows goal achievement status
- [ ] Completion verification displays correctly
- [ ] Execution history lists past runs
- [ ] Can filter execution history
- [ ] Settings page allows path configuration
- [ ] Docker build succeeds (`docker-compose build`)
- [ ] Docker deployment works (`docker-compose up`)

---

## Performance Expectations

### Development Environment
- Backend start: ~2-5 seconds
- Frontend start: ~3-8 seconds
- Hot reload: <1 second
- API response: <100ms (local file system)
- WebSocket latency: <50ms
- Monaco Editor load: ~2-3 seconds (initial)

### Production Environment (Docker)
- Container start: ~10-15 seconds
- API response: <200ms
- WebSocket latency: <100ms
- Frontend load: ~1-2 seconds (after first visit)

### Resource Usage
- Backend memory: ~100-200MB
- Frontend memory: ~150-300MB (browser)
- Database size: <10MB (typical)
- Docker total: ~500MB-1GB

---

## Security Considerations

### Development
- Backend runs on localhost only
- No authentication required (single-user)
- CORS allows frontend origin only
- File system access limited to configured paths

### Production
- **IMPORTANT:** Dashboard is single-user, local deployment
- No built-in authentication (add if needed for team use)
- Run behind reverse proxy (Nginx, Traefik) for HTTPS
- Use firewall to restrict external access
- Consider adding API key authentication if exposing externally

### File System Access
- Dashboard can read/write SPEC files
- Validate paths before file operations
- Backup created before parameter edits
- No deletion without confirmation dialogue

---

## Customisation

### Change Technology Stack

Edit `spec_Dashboard_SPEC_Engine.md` before execution:

**Use Vue instead of React:**
```markdown
[software_stack.frontend]
framework = "Vue 3 with TypeScript"
```

**Use PostgreSQL instead of SQLite:**
```markdown
[software_stack.database]
type = "PostgreSQL"
```

**Use different editor:**
```markdown
code_editor = "CodeMirror 6"
```

### Add Features

Extend the SPEC with additional tasks:

```toml
[[speclets.tasks]]
id = 4
name = "Add user authentication"
purpose = "Multi-user support with login"
```

### Remove Features

Mark non-essential tasks as `critical = false` or remove them entirely.

---

## Support

### Documentation
- **Full README:** `README.md` (comprehensive overview)
- **This Guide:** `QUICK_START.md` (fast-track setup)
- **SPEC Engine Docs:** `__SPEC_Engine/README.md`
- **Getting Started:** `__SPEC_Engine/GETTING_STARTED.md`

### Common Questions

**Q: Can I use a different LLM for execution?**  
A: Yes, any LLM with coding capability can execute this SPEC.

**Q: How do I update the dashboard after changes?**  
A: Rebuild Docker images: `docker-compose build --no-cache`

**Q: Can I add authentication?**  
A: Yes, add authentication middleware to backend and update frontend.

**Q: What if I only want parameter editing, not full dashboard?**  
A: Execute only SPECLets 1, 2, and 5 (platform, frontend, editor).

**Q: Can this work with remote SPEC Engine installation?**  
A: Currently designed for local file system. Modify file services for remote access.

---

## Next Steps

After successful build and testing:

1. **Customise theme:** Edit MUI theme in `frontend/src/theme.ts`
2. **Add analytics:** Track SPEC execution patterns
3. **Implement dark mode:** Add theme toggle
4. **Create API documentation:** Document all endpoints
5. **Write end-to-end tests:** Test critical workflows
6. **Set up CI/CD:** Automate builds and deployments
7. **Add monitoring:** Implement application monitoring
8. **Create user guide:** Write end-user documentation

---

## Deployment Options

### Local Development
```bash
npm run dev (both frontend and backend)
```

### Local Production
```bash
docker-compose up -d
```

### Server Deployment
```bash
# Copy to server
scp -r spec-engine-dashboard user@server:/opt/

# SSH to server
ssh user@server
cd /opt/spec-engine-dashboard

# Configure
nano .env

# Deploy
docker-compose up -d

# Set up reverse proxy (Nginx)
# Point domain to localhost:3000
```

### Cloud Deployment (e.g., AWS, Azure, GCP)
```bash
# Build images
docker-compose build

# Tag images
docker tag dashboard-backend:latest registry/dashboard-backend:v1
docker tag dashboard-frontend:latest registry/dashboard-frontend:v1

# Push to registry
docker push registry/dashboard-backend:v1
docker push registry/dashboard-frontend:v1

# Deploy to cloud service (ECS, AKS, GKE, etc.)
# Configure volumes for SPEC Engine files
```

---

**Ready to build?** Execute the SPEC and have your dashboard ready in hours, not days!
