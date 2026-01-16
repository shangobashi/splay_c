# Splay - Quick Start (NO DOCKER NEEDED!)

Since Docker is not available on your system, I've adapted the entire app to work with SQLite and in-memory processing. **Everything runs with just Python!**

## Super Quick Start (3 steps)

### Step 1: Run Setup
```bash
setup.bat
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Set up the SQLite database
- Run migrations

### Step 2: Start the Server
```bash
cd apps\api
venv\Scripts\activate
python run.py
```

### Step 3: Test the App
Open your browser to:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## What Changed from the Original Design?

**Original (with Docker):**
- PostgreSQL with pgvector extension
- Redis for job queue
- Worker process for async scanning

**Adapted (no Docker):**
- ✅ SQLite database (built into Python)
- ✅ In-memory vector operations with numpy
- ✅ Synchronous scan processing (no queue needed)
- ✅ Everything works locally!

## Project Structure

```
Splay_cloco/
├── apps/
│   └── api/              # FastAPI backend
│       ├── app/
│       │   ├── models/   # Database models (SQLite)
│       │   ├── routes/   # API endpoints
│       │   ├── services/ # Business logic
│       │   └── main.py   # FastAPI app
│       ├── alembic/      # Database migrations
│       ├── venv/         # Virtual environment (created by setup.bat)
│       ├── splay.db      # SQLite database (created automatically)
│       └── run.py        # Development server
└── setup.bat             # One-click setup script
```

## API Endpoints (Current)

### Health Check
```bash
GET http://localhost:8000/health
```

### Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Coming Soon (Phase 1)
- POST `/auth/register` - Create account
- POST `/auth/login` - Get JWT token
- POST `/scans` - Upload room photo
- GET `/scans/:id` - View results

## Development

### Restart the Server
```bash
# Press CTRL+C to stop
# Then run again:
python run.py
```

### View Database
```bash
# Install DB Browser for SQLite (optional)
# Or use command line:
sqlite3 splay.db
.tables
.schema users
.quit
```

### Reset Database
```bash
# Delete the database file
del splay.db

# Re-run migrations
alembic upgrade head
```

## Troubleshooting

### "Python not found"
- Install Python 3.11+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### "Cannot find module 'app'"
- Make sure you're in the `apps/api` directory
- Make sure virtual environment is activated: `venv\Scripts\activate`

### Port 8000 already in use
- Kill the process using port 8000
- Or change the port in `app/settings.py`: `api_port: int = 8001`

### Migration errors
- Delete `splay.db` and run `alembic upgrade head` again

## Next Steps

Once the API is running, I'll add:
1. **Authentication** - Register/login endpoints
2. **Scan Upload** - Upload room photos
3. **Product Matching** - AI furniture detection
4. **Frontend** - Simple HTML test page

You'll be able to test everything locally without Docker! 🎉
