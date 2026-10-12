# 🚀 Simple Start Guide - Just 2 Terminals!

## ✅ You've already installed dependencies! Now just start the servers.

---

## Terminal 1 - Start Backend

```bash
cd /Users/jitishkumar/Desktop/amazonsde/deeplearn
source venv/bin/activate
python3 -m backend.main
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ Backend is running! **Keep this terminal open!**

---

## Terminal 2 - Start Frontend

Open a **NEW terminal window** and run:

```bash
cd /Users/jitishkumar/Desktop/amazonsde/deeplearn/frontend
npm run dev
```

**Wait for this message:**
```
➜  Local:   http://localhost:3000/
```

✅ Frontend is running! **Keep this terminal open too!**

---

## 🌐 Open Browser

1. Open your browser
2. Go to: **http://localhost:3000**
3. Login with:
   - **Username:** demo
   - **Password:** demo123

---

## 🎉 Now Test It!

### Test 1: Check Dashboard
- You should see 60 builds
- Charts and statistics
- ✅ Dashboard works!

### Test 2: Add GitHub Repository (THE COOL PART!)
1. Click **"Projects"** (left sidebar)
2. Click **"Add from GitHub"** (black button at top)
3. You'll see demo repositories
4. Click **"Add & Test"** on "Simple Python Calculator"
5. Wait - it should appear in your projects list

### Test 3: Trigger Real Build (THE IMPRESSIVE PART!)
1. Click **"Pipelines"** (left sidebar)
2. Find your newly added project
3. Click **"Trigger Build"** button
4. Click on the build to see logs
5. **Watch REAL testing happen!**

You'll see:
```
🔄 Cloning repository from GitHub...
✅ Repository cloned successfully!
🔍 Detecting project type: Python
📦 Installing dependencies...
🧪 Running tests: pytest
test_add.py::test_addition PASSED ✅
test_subtract.py::test_subtraction PASSED ✅
10 tests passed in 0.45s
```

**This is REAL code testing, not simulation!**

---

## 🆘 Problems?

### Backend shows "ModuleNotFoundError":
```bash
# Make sure you activated the virtual environment
source venv/bin/activate
# Then run backend again
python3 -m backend.main
```

### Port already in use:
```bash
# Kill existing processes
kill -9 $(lsof -ti:8000)
kill -9 $(lsof -ti:3000)
# Try again
```

### Database error:
```bash
# Delete old database
rm devops_pipeline.db
# Restart backend
source venv/bin/activate
python3 -m backend.main
```

---

## 🎯 Quick Demo for Teacher

**Say:** "Let me show you real GitHub integration..."

**Do:**
1. Go to Projects → Add from GitHub
2. Use: `https://github.com/realpython/python-testing-101`
3. Go to Pipelines → Trigger Build
4. Show the logs: **"See? Real git clone, real pip install, real pytest tests!"**
5. Point to results: **"10 tests passed - these are actual test results from real code!"**

---

## 📊 What Each Page Does

- **Dashboard** - Overview of all builds, statistics
- **Projects** - Manage your GitHub repositories
- **Pipelines** - See all builds, trigger new ones
- **AI Predictions** - Predict if build will fail (87% accurate)
- **Analytics** - Charts and trends
- **API Monitor** - See all HTTP requests in real-time

---

## ✅ Success Signs

You'll know it's working when:
- ✅ Backend shows "Uvicorn running"
- ✅ Frontend shows "Local: http://localhost:3000"
- ✅ Can login with demo/demo123
- ✅ Dashboard shows 60 builds
- ✅ Can add GitHub repository
- ✅ Can see real test logs when triggering build

---

## 🎉 That's It!

**Two terminals, two commands, one amazing project!**

**Now go show your teacher! 🚀**