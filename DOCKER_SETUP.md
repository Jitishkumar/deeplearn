# 🐳 Docker Setup - Production-Ready AI DevOps Pipeline

## 🚀 Quick Start (30 seconds!)

```bash
# Clone and enter the project
git clone <your-repo-url>
cd deeplearn

# Start the entire system with ONE command!
docker-compose -f docker-compose.dev.yml up -d

# That's it! 🎉
```

**Access your application:**
- 🎨 **Frontend:** http://localhost:3000
- 🚀 **Backend API:** http://localhost:8000
- 📚 **API Docs:** http://localhost:8000/docs
- 📊 **Monitoring:** http://localhost:9090
- 💚 **Health Check:** http://localhost:8000/health

---

## 📦 What's Inside Your Docker Setup?

### 🏗️ Architecture Overview:
```
🐳 Docker Container Ecosystem
├── 🎨 Frontend Container (React + Nginx)
├── 🚀 Backend Container (FastAPI + AI Engine)  
├── 🗄️ Database Container (PostgreSQL)
└── 📊 Monitoring Container (System Status)
```

### 🔧 Container Details:

#### 🎨 Frontend Container:
- **Base:** Node.js 18 Alpine (Build) → Nginx Alpine (Serve)
- **Size:** ~50MB (optimized!)
- **Features:** Multi-stage build, gzip compression, security headers
- **Health Check:** HTTP ping every 30s

#### 🚀 Backend Container:
- **Base:** Python 3.13 Slim
- **Size:** ~800MB (includes ML libraries)
- **Features:** Real GitHub integration, actual testing, AI predictions
- **Health Check:** FastAPI health endpoint

#### 🗄️ Database Container:
- **Base:** PostgreSQL 15 Alpine
- **Size:** ~200MB
- **Features:** Production-ready, persistent storage, health checks

---

## 🎯 Two Deployment Modes

### 🛠️ Development Mode (SQLite - Easy Demo)
```bash
# Uses SQLite database (great for presentations!)
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down
```

### 🏢 Production Mode (PostgreSQL - Real World)
```bash
# Uses PostgreSQL database (production-ready!)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔧 Useful Docker Commands

### 📊 System Management:
```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View system resource usage
docker stats

# View container logs
docker logs ai-devops-backend -f
docker logs ai-devops-frontend -f
```

### 🔄 Container Operations:
```bash
# Restart a single service
docker-compose restart backend

# Rebuild a container (after code changes)
docker-compose build backend
docker-compose up -d backend

# Execute commands inside containers
docker exec -it ai-devops-backend bash
docker exec -it ai-devops-frontend sh
```

### 🧹 Cleanup:
```bash
# Stop and remove all containers
docker-compose down

# Remove containers + volumes (DESTRUCTIVE!)
docker-compose down -v

# Clean up unused Docker resources
docker system prune -f

# Remove all stopped containers
docker container prune -f
```

---

## 🔍 Troubleshooting Guide

### ❌ Common Issues & Solutions:

#### 1. **Port Already in Use**
```bash
Error: port is already allocated

# Solution: Change ports in docker-compose.yml
ports:
  - "3001:3000"  # Frontend on 3001 instead
  - "8001:8000"  # Backend on 8001 instead
```

#### 2. **Container Won't Start**
```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend

# Rebuild the container
docker-compose build backend
docker-compose up -d backend
```

#### 3. **Database Connection Issues**
```bash
# Make sure database is healthy
docker-compose ps

# Reset the database
docker-compose down -v
docker-compose up -d
```

#### 4. **Out of Disk Space**
```bash
# Clean up Docker resources
docker system prune -a -f

# Remove unused volumes
docker volume prune -f
```

---

## 🌟 Production Deployment Tips

### 🚀 Deploy to Cloud:
1. **AWS ECS:** Use `docker-compose.yml` with ECS CLI
2. **Google Cloud Run:** Build images and deploy
3. **DigitalOcean Apps:** Connect GitHub repo directly
4. **Heroku:** Use `heroku.yml` configuration

### 🔒 Security Best Practices:
- ✅ Non-root users in containers
- ✅ Health checks configured
- ✅ Resource limits set
- ✅ Secrets via environment variables
- ✅ Security headers in nginx

### 📊 Monitoring & Scaling:
```bash
# Scale services horizontally
docker-compose up -d --scale backend=3

# View resource usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Set resource limits in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

## 🎓 For Your Final Year Presentation

### 🗣️ What to Say to Professors:

> **"I've containerized the entire application using Docker, which means:**
> - **Consistent environments:** Runs identically on any system
> - **Production ready:** Same containers go from dev to production
> - **Easy deployment:** One command starts the entire system
> - **Scalable architecture:** Can handle increased load
> - **Industry standard:** Used by Netflix, Google, Amazon"

### 📈 Impressive Stats to Mention:
- ✅ **Multi-container architecture** (4 services)
- ✅ **Multi-stage builds** (optimized images)
- ✅ **Health checks** (production monitoring)
- ✅ **Non-root security** (security best practices)
- ✅ **Volume persistence** (data survives restarts)
- ✅ **Network isolation** (secure communication)

### 🎯 Demo Script:
1. **Show docker-compose.yml:** "Here's my infrastructure as code"
2. **Run `docker-compose up -d`:** "Entire system starts in 30 seconds"
3. **Show `docker ps`:** "All services running and healthy"
4. **Open monitoring dashboard:** "Real-time system monitoring"
5. **Show logs:** "Centralized logging for debugging"

---

## 🔧 Environment Variables

### 📝 Backend (.env):
```bash
DATABASE_URL=postgresql://devops_user:secure_password_2024@database:5432/devops_pipeline
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=False
WORKSPACE_PATH=/app/workspaces
```

### 📝 Frontend (.env):
```bash
VITE_API_URL=http://localhost:8000
```

---

## 🎉 Success Indicators

### ✅ Everything Working When You See:
- All containers show "healthy" status
- Frontend loads at http://localhost:3000
- Backend API docs at http://localhost:8000/docs
- Health check returns 200 at http://localhost:8000/health
- Monitoring dashboard at http://localhost:9090
- No error logs in `docker-compose logs`

### 🎯 Your Project is Now:
- ✅ **Production Ready** - Can deploy anywhere
- ✅ **Scalable** - Can handle more users
- ✅ **Maintainable** - Easy to update and debug
- ✅ **Professional** - Industry-standard practices
- ✅ **Impressive** - Shows advanced DevOps skills

**Congratulations! You now have a containerized, production-ready AI DevOps pipeline! 🚀**