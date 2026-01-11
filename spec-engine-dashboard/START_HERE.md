# SPEC Engine Dashboard - Start Here

**Status:** ✅ Build Complete - Ready to Run  
**Date:** 2 January 2026

---

## Quick Start (5 Minutes)

### Step 1: Restart Frontend (Ctrl+C in terminal, then restart)

The missing configuration files have been created. Restart the dev server:

```powershell
# In the terminal where you ran npm run dev, press Ctrl+C to stop
# Then restart:
cd spec-engine-dashboard/frontend
npm run dev
```

You should see:
```
VITE v5.4.21  ready in XXXX ms
➜  Local:   http://localhost:3000/
```

### Step 2: Start Backend (New Terminal)

```powershell
cd spec-engine-dashboard/backend

# Install dependencies
npm install

# Create .env file (copy from example)
echo "PORT=5000
NODE_ENV=development
SPEC_ENGINE_PATH=C:/Users/Fab2/Desktop/AI/Specs/__SPEC_Engine
SPECS_PATH=C:/Users/Fab2/Desktop/AI/Specs/SPECs
DATABASE_URL=file:./dev.db
FRONTEND_URL=http://localhost:3000" > .env

# Initialize database
npx prisma generate
npx prisma migrate dev --name init

# Start server
npm run dev
```

Backend will start on **http://localhost:5000**

### Step 3: Access Dashboard

Open browser: **http://localhost:3000**

You should see the SPEC Engine Dashboard!

---

## What You Can Do Now

### 1. Create DNA Profile
- Click "DNA Profiles" in sidebar
- Click "Create DNA Profile"
- Fill out form (project name, preferences)
- Save - a unique DNA code will be generated

### 2. Create SPEC
- Click "SPECs" in sidebar
- Click "Create SPEC"
- Select DNA profile, enter descriptor and goal
- Save - files created in SPECs directory

### 3. Edit Parameters (KEY FEATURE)
- Find your SPEC in the list
- Click edit icon
- Monaco Editor opens with TOML syntax highlighting
- Edit the parameters file
- Validation runs as you type
- Press Ctrl+S to save (backup created automatically)

### 4. Execute SPEC
- Click play icon on your SPEC
- Select execution mode (Dynamic recommended)
- Click "Start Execution"
- Monitor page shows real-time progress

### 5. View Results
- After execution completes
- View goal achievement status
- See completion verification
- Review post-execution analysis

---

## Troubleshooting

### Frontend Still Won't Start After Restart

**If you still see errors:**

1. **Stop the dev server** (Ctrl+C)

2. **Check files exist:**
```powershell
ls spec-engine-dashboard/frontend/tsconfig.node.json
ls spec-engine-dashboard/frontend/index.html
```

3. **Restart Vite:**
```powershell
cd spec-engine-dashboard/frontend
npm run dev
```

### Backend Errors

**If Prisma migration fails:**
```powershell
cd spec-engine-dashboard/backend
rm dev.db dev.db-journal
npx prisma migrate dev --name init
```

**If ports already in use:**
```powershell
# Check what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Browser Shows White Screen

1. Check browser console (F12) for errors
2. Verify backend is running (http://localhost:5000/health)
3. Check terminal for TypeScript errors
4. Try hard refresh (Ctrl+Shift+R)

---

## Complete Application Architecture

```
SPEC Engine Dashboard (http://localhost:3000)
│
├── Backend (http://localhost:5000)
│   ├── Express API (REST endpoints)
│   ├── Socket.io (WebSocket server)
│   ├── SQLite Database (Prisma ORM)
│   ├── File System Services
│   │   ├── DNA profile management
│   │   ├── SPEC file operations
│   │   └── Progress monitoring (chokidar)
│   └── Execution Service (spawn exe_*.md)
│
├── Frontend (React + TypeScript)
│   ├── Material-UI Components
│   ├── Redux State Management
│   ├── Monaco Editor (parameter editing)
│   ├── Socket.io Client (real-time updates)
│   └── React Router (navigation)
│
└── SPEC Engine Integration
    ├── Reads: __SPEC_Engine/ (read-only)
    └── Reads/Writes: SPECs/ (DNA, parameters, progress)
```

---

## All Features Implemented

### DNA Profile Management ✅
- List all DNA profiles with stats
- Create new profiles with auto-generated codes
- View/edit profile settings
- Navigate to SPECs under each DNA

### SPEC Management ✅
- Browse all SPECs across DNA profiles
- Filter by DNA code, status, search
- Create simple SPECs from template
- View SPEC details (goal, tasks)
- Navigate to edit/execute

### Parameter Editor ✅ (KEY REQUIREMENT)
- Monaco Editor with TOML syntax
- Real-time validation (debounced)
- Auto-backup before save
- Ctrl+S keyboard shortcut
- Unsaved changes warning

### Execution & Monitoring ✅
- Select execution mode (Silent/Dynamic/Collaborative)
- Start SPEC execution
- Real-time progress via WebSocket
- Task/step status display
- Progress bars

### Results Visualisation ✅
- Goal achievement status (ACHIEVED/PARTIAL/NOT ACHIEVED)
- Completion verification checklist
- Post-execution analysis
- Execution history with filtering

### Deployment ✅
- Docker Compose configuration
- Multi-stage Docker builds
- Nginx for frontend serving
- Volume mounts for SPEC Engine files

---

## Documentation

- **README.md** - Complete overview and architecture
- **DEPLOYMENT.md** - Deployment guide (dev + Docker)
- **API.md** - Complete API documentation
- **COMPLETION_VERIFICATION.md** - Verification of all requirements
- **EXECUTION_COMPLETE.md** - Build summary
- **This File** - Quick start guide

---

## Next Steps After Starting

1. **Create your first DNA profile** (DNA Profiles → Create)
2. **Create a test SPEC** (SPECs → Create)
3. **Try editing parameters** (click edit icon on SPEC)
4. **Test the workflow** (Execute → Monitor → View Results)

---

## Getting Help

**Application not loading?**
- Check both backend and frontend terminals for errors
- Verify Node.js version: `node --version` (should be 20+)
- See DEPLOYMENT.md troubleshooting section

**Features not working?**
- Check browser console (F12) for errors
- Verify API calls in Network tab
- Check backend console for server errors

**Docker deployment?**
- See DEPLOYMENT.md for complete Docker guide
- Adjust paths in docker-compose.yml for your system

---

**The SPEC Engine Dashboard is ready! Access it at http://localhost:3000 after both servers start.**
