# 🚀 Splay - Quick Start (No Docker!)

I've adapted the entire application to work without Docker! Everything runs with just Python.

## ✅ What's Ready Now

- **Authentication API** - Register & Login with JWT tokens
- **SQLite Database** - No Docker needed
- **Test Page** - Beautiful HTML interface to test the API

## 🎯 Get Started in 3 Steps

### Step 1: Run Setup
```bash
cd C:\Users\Shango\Documents\Code\project_130126_FurnitureFinder\Splay_cloco
setup.bat
```

This will:
- Create Python virtual environment
- Install all dependencies
- Set up SQLite database
- Run migrations

**Expected time:** 2-3 minutes

### Step 2: Start the Server
```bash
cd C:\Users\Shango\Documents\Code\project_130126_FurnitureFinder\Splay_cloco\apps\api
venv\Scripts\activate
python run.py
```

You should see:
```
==================================================
 Splay API Server
==================================================

Environment: development
Database: SQLite (no Docker needed!)

Starting server...
→ API: http://0.0.0.0:8000
→ Docs: http://localhost:8000/docs

Press CTRL+C to stop
==================================================
```

### Step 3: Open Test Page

**Double-click this file:**
```
C:\Users\Shango\Documents\Code\project_130126_FurnitureFinder\Splay_cloco\test-page.html
```

Or open in your browser:
- **Test Page**: `file:///C:/Users/Shango/Documents/Code/project_130126_FurnitureFinder/Splay_cloco/test-page.html`

## 🧪 Test the API

### Option 1: Use the Test Page (Recommended)
1. Open `test-page.html` in your browser
2. Fill in name, email, password (or use defaults)
3. Click "Register" to create an account
4. Click "Login" to authenticate
5. See the response with JWT tokens!

### Option 2: Use Browser
- **API Home**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Option 3: Use curl
```bash
# Health check
curl http://localhost:8000/health

# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test1234!\",\"name\":\"Test User\"}"

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test1234!\"}"
```

## 📁 Project Files

```
Splay_cloco/
├── START_HERE.md          ← You are here
├── NO-DOCKER-README.md    ← Detailed docs
├── test-page.html         ← Test interface
├── setup.bat              ← Setup script
└── apps/
    └── api/
        ├── run.py         ← Start server
        ├── splay.db       ← SQLite database (created automatically)
        └── app/
            ├── main.py    ← FastAPI app
            ├── models/    ← Database models
            ├── routes/    ← API endpoints
            └── services/  ← Business logic
```

## ✨ What Works Right Now

✅ **Authentication**
- POST `/auth/register` - Create new account
- POST `/auth/login` - Get JWT tokens
- JWT token generation (15min expiry)
- Password hashing with bcrypt

✅ **Infrastructure**
- SQLite database
- Alembic migrations
- FastAPI with automatic docs
- CORS enabled

## 🚧 Coming Next (Phase 2)

- Upload room photos
- AI furniture detection (stubbed)
- Product matching
- Results with clickable items

## 🛠️ Troubleshooting

### "Python not found"
Install Python 3.11+ from https://www.python.org/downloads/

### "setup.bat doesn't work"
Run commands manually:
```bash
cd apps\api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

### "Port 8000 already in use"
Change port in `apps/api/app/settings.py`:
```python
api_port: int = 8001
```

### "Cannot connect to API"
Make sure the server is running (`python run.py`)

## 📚 Learn More

- **NO-DOCKER-README.md** - Complete documentation
- **README.md** - Original project overview
- **Swagger Docs** - http://localhost:8000/docs - Interactive API documentation

## 💡 Pro Tips

1. **Swagger UI** is your friend - http://localhost:8000/docs lets you test all endpoints
2. **Keep the server running** - Don't close the terminal where `python run.py` is running
3. **Check the test page** - It has a prettier interface than curl commands

## 🎉 Success Criteria

You'll know everything is working when:
1. ✅ `setup.bat` completes without errors
2. ✅ Server starts with "Starting server..."
3. ✅ http://localhost:8000/health returns `{"status": "healthy"}`
4. ✅ Test page shows "✅ API is running!"
5. ✅ Registration creates a user and returns tokens

---

**Need help?** Check NO-DOCKER-README.md for detailed troubleshooting!
