# SPEC Engine Dashboard - Deployment Guide

**Version:** 1.0  
**Last Updated:** 2 January 2026

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Deployment](#development-deployment)
3. [Production Deployment (Docker)](#production-deployment-docker)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)

---

## Prerequisites

### Required
- **Node.js 20+ LTS** ([Download](https://nodejs.org/))
- **npm 10+** (comes with Node.js)
- **SPEC Engine** installed and configured

### For Docker Deployment
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose** (included with Docker Desktop)

### System Requirements
- **RAM:** Minimum 4GB, recommended 8GB+
- **Disk Space:** 2GB for application + dependencies
- **OS:** Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)

---

## Development Deployment

Perfect for development, testing, and making code changes.

### Step 1: Install Backend

```bash
cd spec-engine-dashboard/backend

# Install dependencies
npm install

# Create .env file
copy env.example.txt .env  # Windows
# or
cp env.example.txt .env    # macOS/Linux

# Edit .env - SET YOUR PATHS!
# SPEC_ENGINE_PATH=C:/Users/Fab2/Desktop/AI/Specs/__SPEC_Engine
# SPECS_PATH=C:/Users/Fab2/Desktop/AI/Specs/SPECs
```

### Step 2: Initialize Database

```bash
# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev --name init

# (Optional) Seed with example data
# npx prisma db seed
```

### Step 3: Start Backend

```bash
npm run dev
```

Backend will start on **http://localhost:5000**

Test: Open http://localhost:5000/health - should return `{"status":"ok"}`

### Step 4: Install Frontend

```bash
# Open new terminal
cd spec-engine-dashboard/frontend

# Install dependencies
npm install
```

### Step 5: Start Frontend

```bash
npm run dev
```

Frontend will start on **http://localhost:3000**

### Step 6: Access Dashboard

Open browser: **http://localhost:3000**

You should see the SPEC Engine Dashboard with navigation sidebar.

---

## Production Deployment (Docker)

Recommended for production use, simpler setup, consistent environment.

### Step 1: Configure Environment

Edit `docker-compose.yml` to set your SPEC Engine paths:

```yaml
environment:
  - SPEC_ENGINE_PATH=/spec-engine/__SPEC_Engine
  - SPECS_PATH=/spec-engine/SPECs

volumes:
  # CHANGE THESE PATHS for your system:
  - C:/Users/Fab2/Desktop/AI/Specs/__SPEC_Engine:/spec-engine/__SPEC_Engine:ro
  - C:/Users/Fab2/Desktop/AI/Specs/SPECs:/spec-engine/SPECs:rw
```

**Windows Users:** Use forward slashes or escape backslashes:
- `C:/Users/YourName/Desktop/AI/Specs/__SPEC_Engine` ✅
- `C:\\Users\\YourName\\Desktop\\AI\\Specs\\__SPEC_Engine` ✅
- `C:\Users\YourName\Desktop\AI\Specs\__SPEC_Engine` ❌

### Step 2: Build Images

```bash
cd spec-engine-dashboard

# Build all images
docker-compose build

# This takes 5-10 minutes on first build
```

### Step 3: Start Services

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Step 4: Access Dashboard

Open browser: **http://localhost:3000**

### Step 5: Verify Health

```bash
# Check backend health
curl http://localhost:5000/health

# Should return: {"status":"ok","timestamp":"...","service":"spec-engine-dashboard-backend"}
```

### Managing Docker Deployment

```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d

# Remove everything (including volumes)
docker-compose down -v
```

---

## Configuration

### Backend Configuration (.env)

```env
# Server
PORT=5000
NODE_ENV=production

# SPEC Engine Paths (REQUIRED)
SPEC_ENGINE_PATH=/path/to/__SPEC_Engine
SPECS_PATH=/path/to/SPECs

# Database
DATABASE_URL=file:./dev.db

# CORS
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=info
```

### Frontend Configuration

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:5000
VITE_WS_URL=http://localhost:5000
```

### Docker Volumes

The dashboard needs access to your SPEC Engine files:

**Read-only access:**
- `__SPEC_Engine/` - Framework files (constitution, templates, etc.)

**Read-write access:**
- `SPECs/` - DNA profiles, SPECs, parameters, progress files

**Volume Configuration:**
```yaml
volumes:
  - /host/path/__SPEC_Engine:/container/path/__SPEC_Engine:ro
  - /host/path/SPECs:/container/path/SPECs:rw
```

`:ro` = read-only  
`:rw` = read-write

---

## Troubleshooting

### Backend Won't Start

**Error: "Cannot find module"**
```bash
# Solution: Reinstall dependencies
cd backend
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 5000 already in use"**
```bash
# Solution: Change port in .env
PORT=5001

# Or kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

**Error: "Prisma Client not generated"**
```bash
# Solution: Generate Prisma client
npx prisma generate

# If still failing, run migration
npx prisma migrate dev
```

**Error: "SPEC_ENGINE_PATH not found"**
```bash
# Solution: Check .env file has correct paths
cat .env  # Linux/Mac
type .env # Windows

# Verify paths exist
ls C:/Users/Fab2/Desktop/AI/Specs/__SPEC_Engine
```

### Frontend Won't Start

**Error: "Failed to resolve import"**
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Solution: Change port in vite.config.ts
server: {
  port: 3001,
  ...
}
```

**Error: "Cannot connect to backend"**
```bash
# Solution: Verify backend is running
curl http://localhost:5000/health

# Check Vite proxy configuration in vite.config.ts
# Verify VITE_API_URL in .env matches backend
```

### Docker Issues

**Error: "Cannot connect to Docker daemon"**
```bash
# Solution: Start Docker Desktop
# Windows: Open Docker Desktop application
# Linux: sudo systemctl start docker
```

**Error: "Volume mount failed"**
```bash
# Solution: Check Docker Desktop settings
# Windows: Settings → Resources → File Sharing
# Add the drive containing your SPEC Engine files (C:, D:, etc.)
```

**Error: "Container exits immediately"**
```bash
# Solution: Check container logs
docker-compose logs backend
docker-compose logs frontend

# Common causes:
# - Invalid .env configuration
# - Missing volume mounts
# - Port conflicts
```

**Error: "Cannot access mounted volumes"**
```bash
# Solution: Verify paths in docker-compose.yml
# Test container can see files:
docker-compose exec backend ls /spec-engine/__SPEC_Engine
docker-compose exec backend ls /spec-engine/SPECs

# If empty, check volume mount syntax
```

### WebSocket Not Connecting

**Check 1: Backend Socket.io Running**
```bash
curl http://localhost:5000/socket.io/
# Should return: {"code":0,"message":"Transport unknown"}
```

**Check 2: CORS Configuration**
```bash
# Verify FRONTEND_URL in backend .env matches actual frontend URL
FRONTEND_URL=http://localhost:3000
```

**Check 3: Browser Console**
```
Open DevTools → Console → Look for WebSocket errors
Common errors:
- "WebSocket connection failed" → Backend not running
- "CORS error" → CORS misconfigured
- "404 on /socket.io/" → Socket.io not initialized
```

### Database Issues

**Error: "Table does not exist"**
```bash
# Solution: Run migrations
cd backend
npx prisma migrate dev
```

**Error: "Database locked"**
```bash
# Solution: Close other connections to database
# Delete dev.db-journal file if it exists
rm dev.db-journal
```

**Reset Database:**
```bash
# Delete database and recreate
rm dev.db dev.db-journal
npx prisma migrate dev --name init
```

---

## Maintenance

### Updating Dependencies

```bash
# Check for updates
npm outdated

# Update dependencies
npm update

# Or update to latest
npm install package-name@latest
```

### Database Backups

```bash
# Backup SQLite database
cp backend/dev.db backend/dev.db.backup

# Docker environment
docker-compose exec backend cp /app/data/prod.db /app/data/prod.db.backup
```

### Logs

**Development:**
```bash
# Backend logs: stdout in terminal
# Frontend logs: browser console
```

**Docker:**
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Save logs to file
docker-compose logs > logs.txt
```

### Performance Monitoring

**Backend:**
```bash
# Check memory usage
docker stats spec-dashboard-backend

# Check response times
curl -w "@-" http://localhost:5000/health <<'EOF'
\ntime_total: %{time_total}\n
EOF
```

**Frontend:**
```bash
# Check bundle size
cd frontend
npm run build
# Check dist/ folder size

# Analyze bundle
npm install -g vite-bundle-visualizer
npx vite-bundle-visualizer
```

---

## Scaling & Performance

### Horizontal Scaling (Not Recommended)

This dashboard is designed for **single-user or small team** use.

For high-scale deployments:
1. Replace SQLite with PostgreSQL
2. Add authentication and authorization
3. Implement connection pooling
4. Add caching layer (Redis)
5. Use load balancer for multiple instances

### Performance Optimization

**Backend:**
- Enable Gzip compression
- Implement caching for file operations
- Use connection pooling
- Add rate limiting

**Frontend:**
- Enable code splitting (already configured)
- Lazy load Monaco Editor
- Implement virtual scrolling for large lists
- Add service worker for offline support

---

## Security Checklist

- [ ] Change default ports if exposed to internet
- [ ] Add authentication (JWT or session-based)
- [ ] Use HTTPS (add reverse proxy with SSL)
- [ ] Restrict CORS origins
- [ ] Add rate limiting
- [ ] Implement input validation
- [ ] Add audit logging
- [ ] Regular dependency updates
- [ ] Use secrets management for sensitive configs

---

## Backup & Recovery

### Full Backup

```bash
# Backup database
cp backend/dev.db backups/dev.db.$(date +%Y%m%d)

# Backup SPEC files (handled by SPEC Engine)
# Dashboard doesn't modify framework files

# Backup configuration
cp backend/.env backups/.env.$(date +%Y%m%d)
cp docker-compose.yml backups/docker-compose.yml.$(date +%Y%m%d)
```

### Recovery

```bash
# Restore database
cp backups/dev.db.20260102 backend/dev.db

# Restart services
docker-compose restart backend
```

---

## Monitoring

### Health Checks

```bash
# Backend
curl http://localhost:5000/health

# Frontend
curl http://localhost:3000/

# Docker health status
docker-compose ps
```

### Set Up Monitoring (Optional)

1. **Prometheus + Grafana:**
   - Add `/metrics` endpoint to backend
   - Scrape metrics with Prometheus
   - Visualize in Grafana

2. **Log Aggregation:**
   - Use ELK stack (Elasticsearch, Logstash, Kibana)
   - Or use Loki for lighter alternative

3. **Uptime Monitoring:**
   - UptimeRobot, Pingdom, or similar
   - Monitor health check endpoints

---

## Production Checklist

Before deploying to production:

- [ ] Environment variables configured correctly
- [ ] SPEC Engine paths accessible from container
- [ ] Database migrations run successfully
- [ ] Health checks passing
- [ ] CORS configured for production domain
- [ ] Error handling tested
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Documentation reviewed
- [ ] End-to-end workflow tested

---

## Support

For issues or questions:

1. Check logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost:5000/health`
3. Check this guide's troubleshooting section
4. Review README.md for architecture details
5. Consult SPEC Engine documentation

---

**Deployment guide complete. The dashboard is now production-ready!**
