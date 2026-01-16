# Phase 0 Setup Instructions

## Important: Docker Desktop Requirement

**Before proceeding, you MUST start Docker Desktop!**

This project requires Docker Desktop to be running for PostgreSQL and Redis services.

### Steps to Complete Phase 0 Setup:

1. **Start Docker Desktop**
   - Open Docker Desktop application
   - Wait for Docker to fully start (icon should show "running")
   - You can verify Docker is running by opening a terminal and running: `docker ps`

2. **Start Infrastructure Services**
   ```bash
   cd infra/docker
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL 16 with pgvector extension (port 5432)
   - Redis 7 (port 6379)

3. **Verify Services are Running**
   ```bash
   docker ps
   ```

   You should see two containers:
   - `splay_postgres` (healthy)
   - `splay_redis` (healthy)

4. **Set Up Python Backend**
   ```bash
   cd apps/api

   # Create virtual environment
   python -m venv venv

   # Activate it
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

5. **Run Database Migrations**
   ```bash
   cd apps/api
   alembic upgrade head
   ```

   This will create all database tables with proper indexes and extensions.

6. **Verify Database Setup**
   ```bash
   # Connect to database
   psql postgresql://splay:splay_dev_pass@localhost:5432/splay_dev

   # Check tables exist
   \dt

   # Should show: users, subscriptions, products, scans, detected_items, item_matches

   # Check pgvector extension
   SELECT * FROM pg_extension WHERE extname = 'vector';

   # Exit psql
   \q
   ```

7. **Start API Server**
   ```bash
   cd apps/api
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Verify API is Working**
   - Open browser to http://localhost:8000/health
   - Should return: `{"status": "healthy", "environment": "development", "version": "1.0.0"}`
   - Check Swagger docs: http://localhost:8000/docs

9. **Create Phase 0 Complete Marker**
   ```bash
   # When all above steps pass, create marker file
   cd C:\Users\Shango\Documents\Code\project_130126_FurnitureFinder\Splay_cloco
   echo "Phase 0 complete" > .phase-0-complete
   ```

---

## Phase 0 Verification Checklist

- [ ] Docker Desktop running
- [ ] `docker ps` shows splay_postgres and splay_redis containers
- [ ] PostgreSQL accessible on port 5432
- [ ] Redis accessible on port 6379
- [ ] Python venv created and activated
- [ ] All Python dependencies installed
- [ ] Database migrations run successfully (`alembic upgrade head`)
- [ ] All 6 tables created (users, subscriptions, products, scans, detected_items, item_matches)
- [ ] pgvector extension enabled
- [ ] FastAPI server starts without errors
- [ ] Health check endpoint returns 200: http://localhost:8000/health
- [ ] Swagger UI accessible: http://localhost:8000/docs

---

## Troubleshooting

### "Docker daemon is not running"
**Solution:** Start Docker Desktop application and wait for it to fully start.

### "Port 5432 is already in use"
**Solution:** Stop any existing PostgreSQL instances or change the port in docker-compose.yml

### "Cannot connect to database"
**Solution:**
1. Check Docker containers are running: `docker ps`
2. Check PostgreSQL logs: `docker logs splay_postgres`
3. Restart containers: `cd infra/docker && docker-compose restart`

### "Module not found" errors when running uvicorn
**Solution:**
1. Make sure you're in the `apps/api` directory
2. Virtual environment is activated (you should see `(venv)` in your prompt)
3. Dependencies are installed: `pip install -r requirements.txt`

### Alembic migration fails
**Solution:**
1. Check database is accessible: `psql postgresql://splay:splay_dev_pass@localhost:5432/splay_dev`
2. If database doesn't exist, create it:
   ```bash
   docker exec -it splay_postgres psql -U splay -c "CREATE DATABASE splay_dev;"
   ```
3. Run migrations again: `alembic upgrade head`

---

## What's Included in Phase 0

✅ **Infrastructure:**
- Docker Compose configuration (PostgreSQL + Redis)
- Environment configuration (.env files)

✅ **Backend Foundation:**
- FastAPI application setup
- Settings and configuration management
- Database connection and session management

✅ **Database:**
- SQLAlchemy models (User, Subscription, Scan, DetectedItem, ItemMatch, Product)
- Initial Alembic migration (001_initial.py)
- pgvector extension for embedding storage
- All necessary indexes for query performance

✅ **Documentation:**
- README.md with quick start guide
- This setup instructions file
- Inline code documentation

---

## Next Steps (Phase 1)

Once Phase 0 is complete and verified, we'll proceed to Phase 1: Authentication

Phase 1 will add:
- User registration and login endpoints
- JWT token generation and validation
- Password hashing with bcrypt
- Frontend auth pages (login/register)
- Base UI components
- Stub providers for external services

Estimated time: 2-3 hours

---

## Need Help?

If you encounter any issues not covered in the Troubleshooting section:
1. Check the main README.md for additional resources
2. Review the detailed architecture documentation in `Documents/Documents_Claude_02_Master_forClaudeCodexAntigravity/`
3. Examine Docker container logs: `docker logs <container_name>`
