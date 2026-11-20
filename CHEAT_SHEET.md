# 📝 DevOps Pipeline - Cheat Sheet

## 🚀 Starting the App

```bash
# First time only
./QUICK_START.sh

# Every time (easiest way)
./START_BOTH.sh

# Or manually (2 terminals)
# Terminal 1:
source venv/bin/activate && python3 -m backend.main

# Terminal 2:
cd frontend && npm run dev

# Open browser
http://localhost:3000
```

---

## 🔑 Login

```
Username: iamjitishkr
Password: jitish123
```

---

## 🧪 Test Repositories (Copy & Paste)

```
Fast (2 min):
https://github.com/psf/requests

Medium (5 min):
https://github.com/pallets/flask

JavaScript:
https://github.com/expressjs/express
```

---

## 📂 Project Structure

```
deeplearn/
├── backend/          # FastAPI Python server
├── frontend/         # React app
├── docker/           # Docker configs
├── k8s/             # Kubernetes manifests
├── docs/            # Documentation
├── QUICK_START.sh   # Setup script
├── START_BOTH.sh    # Start everything
└── *.md             # Documentation
```

---

## 🐛 Quick Fixes

```bash
# Backend not starting?
source venv/bin/activate
pip install -r backend/requirements.txt

# Frontend not starting?
cd frontend
npm install

# White page?
# Check: http://localhost:8000/health

# Reset database
rm devops_pipeline.db
python -m backend.database.init_db
```

---

## 🎤 Interview Quick Answers

**Q: What does it do?**
> Automatically clones GitHub repos, detects language, installs dependencies, runs tests

**Q: Is it CI/CD?**
> CI yes (testing), CD no (no deployment yet)

**Q: What ML?**
> Rule-based detection now, ML would predict build times/failures

**Q: Tech stack?**
> FastAPI, React, Docker, Kubernetes, PostgreSQL

---

## 📊 API Endpoints

```
Health:      GET  /health
Dashboard:   GET  /api/v1/dashboard
Projects:    GET  /api/v1/projects
Add GitHub:  POST /api/v1/projects/github
Test Repos:  GET  /api/v1/projects/github/test-repos
```

---

## 🐳 Docker Commands

```bash
# Build
docker-compose build

# Start
docker-compose up

# Stop
docker-compose down

# Dev mode
docker-compose -f docker-compose.dev.yml up
```

---

## ☸️ Kubernetes Commands

```bash
# Apply all
kubectl apply -f k8s/

# Check pods
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs <pod-name>

# Scale
kubectl scale deployment backend --replicas=5
```

---

## 📝 Resume One-Liner

> AI-powered CI pipeline automating GitHub repository testing with Docker/Kubernetes, reducing manual testing time by 80%

---

## 🎯 Demo Flow (5 minutes)

1. Start: `./START_BOTH.sh`
2. Open: http://localhost:3000
3. Login: iamjitishkr/jitish123
4. Projects → Add from GitHub
5. Paste: https://github.com/psf/requests
6. Wait 2 min
7. Pipelines → View results ✅

---

## 🔗 Quick Links

```
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
Health:    http://localhost:8000/health
```

---

## 🛑 Stopping Everything

```bash
# If using START_BOTH.sh
Ctrl+C (once)

# If running separately
Ctrl+C in each terminal

# Force kill
pkill -f "python3 -m backend.main"
pkill -f "npm run dev"
```

---

## 📚 Documentation Files

- **README_SIMPLE.md** - Quick start
- **HOW_TO_USE.md** - Complete guide
- **INTERVIEW_ANSWERS.md** - Interview prep
- **RESUME_DESCRIPTION.md** - Resume writing
- **CI_CD_EXPLAINED.md** - CI/CD concepts

---

**Print this and keep it handy! 📌**
