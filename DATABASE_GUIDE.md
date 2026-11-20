# 📊 Database & Storage - Complete Guide

## 🔑 NEW Login Credentials

```
Username: iamjitishkr
Password: jitish123
```

---

## 💾 Where Everything is Stored

### 1. **Database File (SQLite)**

**Location:**
```
/Users/jitishkumar/Desktop/amazonsde/deeplearn/devops_pipeline.db
```

**What it stores:**
- ✅ Users (username, password, email)
- ✅ Projects (GitHub repos you added)
- ✅ Builds (test history, pass/fail status)
- ✅ Build metrics (lines of code, test coverage)
- ✅ ML models data
- ✅ Anomaly logs

**NOT stored in database:**
- ❌ Cloned GitHub repositories (temporary files)
- ❌ Test output logs (stored in memory)
- ❌ Downloaded code files

---

### 2. **Cloned Repositories (Temporary)**

**Location:**
```
/tmp/ai_devops_XXXXXXXX/
```

**Example:**
```
/tmp/ai_devops_abc123/
├── README.md
├── setup.py
├── requirements.txt
└── tests/
    └── test_main.py
```

**Important:**
- 🗑️ **Auto-deleted** after tests complete
- ⏱️ **Temporary** - don't look for them later!
- 💾 Only test **results** are saved to database

**How it works:**
```
Step 1: Clone to /tmp/ai_devops_xyz123/
Step 2: Run tests
Step 3: Save results to database
Step 4: DELETE /tmp/ai_devops_xyz123/ ← Cleaned up!
```

---

### 3. **Log Files**

**Location:**
```
/Users/jitishkumar/Desktop/amazonsde/deeplearn/logs/app.log
```

**What it contains:**
- API requests
- Error messages
- System events

---

### 4. **Workspace Files**

**Location:**
```
/Users/jitishkumar/Desktop/amazonsde/deeplearn/workspaces/
```

**Purpose:**
- Build artifacts
- Temporary build files
- (Currently not heavily used)

---

### 5. **ML Models**

**Location:**
```
/Users/jitishkumar/Desktop/amazonsde/deeplearn/ai-engine/models/
```

**What it stores:**
- Trained machine learning models
- Model weights
- Prediction data

---

### 6. **Uploads**

**Location:**
```
/Users/jitishkumar/Desktop/amazonsde/deeplearn/uploads/
```

**Purpose:**
- File uploads
- Artifacts
- (Currently not used)

---

## 🔄 How to Reset Database

### Method 1: Delete and Recreate (Easiest)

```bash
cd /Users/jitishkumar/Desktop/amazonsde/deeplearn

# Step 1: Delete old database
rm devops_pipeline.db

# Step 2: Recreate with new credentials
source venv/bin/activate
python -m backend.database.init_db
```

**Result:**
- ✅ New database created
- ✅ New username: `iamjitishkr`
- ✅ New password: `jitish123`
- ✅ Sample projects and builds recreated

---

### Method 2: Manual SQL Update (Advanced)

```bash
# Install sqlite3 tool
brew install sqlite3  # macOS

# Open database
sqlite3 devops_pipeline.db

# View current users
SELECT * FROM users;

# Update username and password
UPDATE users 
SET username = 'iamjitishkr', 
    email = 'iamjitishkr@devops.com',
    full_name = 'Jitish Kumar'
WHERE username = 'iamjitishkr';

# Exit
.quit
```

**To update password:**
```python
# You need to generate password hash first
python3 << EOF
from backend.utils.auth import get_password_hash
print(get_password_hash("jitish123"))
EOF

# Copy the hash, then in sqlite:
UPDATE users 
SET hashed_password = '<paste_hash_here>'
WHERE username = 'iamjitishkr';
```

---

## 📂 Complete File Structure

```
deeplearn/
├── devops_pipeline.db          ← Main database file (SQLite)
│
├── backend/
│   ├── database/
│   │   ├── init_db.py         ← Database initialization script
│   │   └── base.py            ← Database connection config
│   └── config.py              ← All settings (database path, etc.)
│
├── workspaces/                 ← Build workspaces (auto-created)
├── uploads/                    ← File uploads (auto-created)
├── logs/
│   └── app.log                ← Application logs
│
├── ai-engine/
│   └── models/                ← ML model files
│
└── /tmp/ai_devops_*/          ← Temporary cloned repos (auto-deleted)
```

---

## 🎯 What Gets Stored Where

### User Login

**When you login:**
```
1. Frontend sends: username + password
2. Backend checks: devops_pipeline.db → users table
3. If match: Generate JWT token
4. Token stored: Browser memory (not on disk)
```

**Database table:**
```sql
users
├── id: 1
├── username: iamjitishkr
├── email: iamjitishkr@devops-pipeline.com
├── hashed_password: $2b$12$xxxxxxxxxxx (encrypted!)
├── full_name: Jitish Kumar
└── is_active: true
```

---

### Adding GitHub Repository

**When you add `https://github.com/pallets/flask`:**

**Step 1: Save project info**
```sql
projects
├── id: 4
├── name: flask
├── description: Python web framework
├── repository_url: https://github.com/pallets/flask
├── owner_id: 1 (your user ID)
├── language: Python
└── created_at: 2024-01-15
```

**Step 2: Clone temporarily**
```
/tmp/ai_devops_abc123/
└── (entire flask repository)
```

**Step 3: Run tests**
```
Inside /tmp/ai_devops_abc123/:
$ pytest --verbose

Results:
- 125 tests passed
- 0 tests failed
- Duration: 45.2 seconds
```

**Step 4: Save results to database**
```sql
builds
├── id: 101
├── project_id: 4
├── status: SUCCESS
├── duration: 45.2
├── created_at: 2024-01-15 10:30:00
└── branch: main
```

```sql
build_metrics
├── build_id: 101
├── test_count: 125
├── test_passed: 125
├── test_failed: 0
├── lines_of_code: 15000
└── test_coverage: 92.5
```

**Step 5: Delete temporary files**
```bash
rm -rf /tmp/ai_devops_abc123/
```

**What's LEFT after test completes:**
- ✅ Project info in database
- ✅ Build results in database
- ✅ Test metrics in database
- ❌ Cloned code is DELETED (saved space!)

---

## 🔍 Viewing Database Contents

### Method 1: Using SQLite Browser (GUI)

```bash
# Install DB Browser for SQLite
brew install --cask db-browser-for-sqlite

# Open database
open devops_pipeline.db
```

### Method 2: Command Line

```bash
cd /Users/jitishkumar/Desktop/amazonsde/deeplearn

# Open database
sqlite3 devops_pipeline.db

# List all tables
.tables

# View users
SELECT * FROM users;

# View projects
SELECT * FROM projects;

# View builds
SELECT * FROM builds;

# View latest 10 builds
SELECT id, project_id, status, duration, created_at 
FROM builds 
ORDER BY created_at DESC 
LIMIT 10;

# Exit
.quit
```

### Method 3: Python Script

```python
import sqlite3

# Connect
conn = sqlite3.connect('devops_pipeline.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Users:", users)

# Get all projects
cursor.execute("SELECT * FROM projects")
projects = cursor.fetchall()
print("Projects:", projects)

# Get build statistics
cursor.execute("""
    SELECT status, COUNT(*) 
    FROM builds 
    GROUP BY status
""")
stats = cursor.fetchall()
print("Build stats:", stats)

conn.close()
```

---

## 🛠️ Common Database Operations

### 1. **Change Username/Password**

```bash
# Delete old database
rm devops_pipeline.db

# Edit init_db.py (already done for you!)
# username = "iamjitishkr"
# password = "jitish123"

# Recreate database
python -m backend.database.init_db
```

---

### 2. **Reset Everything (Fresh Start)**

```bash
# Delete database
rm devops_pipeline.db

# Delete workspaces
rm -rf workspaces/*

# Delete logs
rm -rf logs/*

# Recreate database
python -m backend.database.init_db

# Restart backend
python -m backend.main
```

---

### 3. **Backup Database**

```bash
# Create backup
cp devops_pipeline.db devops_pipeline.db.backup

# With timestamp
cp devops_pipeline.db devops_pipeline_$(date +%Y%m%d_%H%M%S).db
```

---

### 4. **Restore Database**

```bash
# Restore from backup
cp devops_pipeline.db.backup devops_pipeline.db

# Or from specific backup
cp devops_pipeline_20240115_103000.db devops_pipeline.db
```

---

### 5. **View Database Size**

```bash
ls -lh devops_pipeline.db

# Typical sizes:
# - Fresh database: ~100 KB
# - After 10 projects: ~500 KB
# - After 100 builds: ~2 MB
```

---

## 🧹 Cleanup Commands

### Clean Temporary Files

```bash
# Remove all temp clones
rm -rf /tmp/ai_devops_*

# Check disk space
du -sh /tmp/ai_devops_*
```

### Clean Logs

```bash
# Clear logs
> logs/app.log

# Or delete logs folder
rm -rf logs/
mkdir logs
```

### Clean Workspaces

```bash
rm -rf workspaces/*
```

---

## 🔐 Security Notes

### Password Storage

**❌ NOT stored in plain text:**
```
Password: jitish123
```

**✅ Stored as hash:**
```
$2b$12$xQzI9b5yK3N.pL2vM8r7.uH1vW6jF9tG2kP4nE8hL5wR3qO7sD1mC
```

**How it works:**
```python
# When you register/create user:
hashed = bcrypt.hash("jitish123")
database.save(hashed)

# When you login:
user_input = "jitish123"
db_hash = database.get_hash()
if bcrypt.verify(user_input, db_hash):
    print("Login successful!")
```

**Important:**
- Cannot reverse the hash to get original password
- Even if someone steals database, they can't get your password!

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    repository_url VARCHAR,
    language VARCHAR,
    owner_id INTEGER REFERENCES users(id),
    total_builds INTEGER DEFAULT 0,
    success_rate FLOAT DEFAULT 0,
    created_at TIMESTAMP
);
```

### Builds Table
```sql
CREATE TABLE builds (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    status VARCHAR NOT NULL,
    branch VARCHAR DEFAULT 'main',
    commit_hash VARCHAR,
    duration FLOAT,
    error_message TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

## 🎯 Summary

### ✅ What IS Stored:
- User accounts (username, email, hashed password)
- Project metadata (name, URL, language)
- Build history (status, duration, timestamp)
- Test results (passed, failed, coverage)
- ML model data

### ❌ What is NOT Stored:
- Cloned repository files (temporary, deleted after tests)
- Plain text passwords (only encrypted hashes)
- Large log files (kept separate in logs/ folder)

### 📍 Key Locations:
```bash
# Database
/Users/jitishkumar/Desktop/amazonsde/deeplearn/devops_pipeline.db

# Temporary clones
/tmp/ai_devops_*/

# Logs
/Users/jitishkumar/Desktop/amazonsde/deeplearn/logs/app.log
```

### 🔄 Reset Database:
```bash
rm devops_pipeline.db
python -m backend.database.init_db
```

### 🔑 New Login:
```
Username: iamjitishkr
Password: jitish123
```

---

**All set! Your database is ready with the new credentials!** 🎉
