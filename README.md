# Splay - Shop The Room

AI-powered "Shazam for furniture" app that transforms room photos into shoppable furniture catalogs.

## Project Overview

**Splay** helps users discover and purchase furniture by uploading inspiration photos. The app uses AI to detect furniture items and matches them to purchasable products from multiple retailers.

### Core Features
- 📸 Upload room photos (device, gallery, camera, URL)
- 🤖 AI-powered furniture detection with bounding boxes
- 🔍 Product matching via visual similarity search
- 🛍️ One-click shopping via affiliate links
- 💰 Monetization: 3 free scans/month, $29/month for unlimited

### Tech Stack
- **Frontend Web:** Next.js 14, Tailwind CSS, Zustand
- **Backend:** Python 3.11+ with FastAPI 0.109+
- **Database:** PostgreSQL 16 with pgvector
- **Cache/Queue:** Redis 7, RQ (Redis Queue)
- **Storage:** AWS S3 (local filesystem for MVP)

---

## Quick Start

### Prerequisites

1. **Docker Desktop** - Install from https://www.docker.com/products/docker-desktop/
   - Required for PostgreSQL and Redis
   - Make sure Docker Desktop is running before proceeding

2. **Python 3.11+** - Check with `python --version`

3. **Node.js 20+** - Check with `node --version`

### Step 1: Start Infrastructure

```bash
# Navigate to docker directory
cd infra/docker

# Start PostgreSQL and Redis
docker-compose up -d

# Verify containers are running
docker ps
```

You should see:
- `splay_postgres` on port 5432
- `splay_redis` on port 6379

### Step 2: Set Up Backend

```bash
# Navigate to API directory
cd apps/api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed database with sample products (will be added in Phase 0)
# python app/scripts/seed_products.py

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Step 3: Set Up Frontend (Coming in Phase 1)

```bash
# Navigate to web directory
cd apps/web

# Install dependencies
npm install

# Start development server
npm run dev
```

The web app will be available at http://localhost:3000

---

## Project Structure

```
Splay_cloco/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── alembic/      # Database migrations
│   │   ├── app/
│   │   │   ├── models/   # SQLAlchemy models
│   │   │   ├── routes/   # API endpoints
│   │   │   ├── services/ # Business logic
│   │   │   ├── providers/# External services (vision, storage)
│   │   │   ├── middleware/# Auth, error handling
│   │   │   ├── database.py
│   │   │   ├── main.py   # FastAPI app
│   │   │   └── settings.py
│   │   ├── tests/
│   │   └── requirements.txt
│   ├── worker/           # RQ worker service (Phase 2)
│   └── web/              # Next.js frontend (Phase 1)
├── packages/
│   └── matching_core/    # Shared matching logic (Phase 2)
├── infra/
│   └── docker/           # Docker Compose setup
│       ├── docker-compose.yml
│       ├── .env
│       └── .env.example
└── scripts/              # Build/deploy scripts
```

---

## Development Workflow

### Phase 0: ✅ Infrastructure (CURRENT)
- [x] Docker Compose setup
- [x] Database models
- [x] Initial migration
- [ ] Start Docker
- [ ] Run migrations
- [ ] Seed products
- [ ] Verify API health check

### Phase 1: Authentication (NEXT)
- [ ] Auth service (JWT, password hashing)
- [ ] Auth endpoints (register, login, refresh)
- [ ] Frontend auth pages
- [ ] Base UI components

### Phase 2: Core Features
- [ ] Image upload
- [ ] Worker processing
- [ ] Product matching
- [ ] Results display

### Phase 3: Monetization
- [ ] Scan limits
- [ ] Paywall
- [ ] Affiliate tracking

### Phase 4: Polish
- [ ] Error handling
- [ ] Loading states
- [ ] Testing (80%+ coverage)
- [ ] CI/CD

---

## API Endpoints (Phase 0 Complete)

### Health Check
```bash
curl http://localhost:8000/health
```

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Database Management

### Run Migrations
```bash
cd apps/api
alembic upgrade head
```

### Create New Migration
```bash
cd apps/api
alembic revision --autogenerate -m "Description of changes"
```

### Rollback Migration
```bash
cd apps/api
alembic downgrade -1
```

### View Migration History
```bash
cd apps/api
alembic history
```

### Connect to Database
```bash
# Using psql
psql postgresql://splay:splay_dev_pass@localhost:5432/splay_dev

# Using Docker
docker exec -it splay_postgres psql -U splay -d splay_dev
```

---

## Testing

### Backend Tests
```bash
cd apps/api
pytest --cov=app --cov-report=term-missing
```

### Frontend Tests
```bash
cd apps/web
npm test
```

### Integration Tests
```bash
cd apps/api
pytest tests/integration/
```

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://splay:splay_dev_pass@localhost:5432/splay_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT (CHANGE IN PRODUCTION!)
JWT_SECRET=your-secret-key-change-in-production

# Storage
STORAGE_TYPE=local
STORAGE_PATH=./storage

# Environment
ENVIRONMENT=development
```

---

## Troubleshooting

### Docker Not Starting
```bash
# Check if Docker Desktop is running
docker ps

# Restart Docker Desktop
# Windows: Right-click Docker icon → Restart
# macOS: Click Docker icon → Restart

# Check Docker Compose logs
cd infra/docker
docker-compose logs
```

### Database Connection Errors
```bash
# Verify PostgreSQL is running
docker ps | grep splay_postgres

# Check database logs
docker logs splay_postgres

# Restart PostgreSQL
cd infra/docker
docker-compose restart postgres
```

### Migration Errors
```bash
# Reset database (WARNING: Destroys all data!)
cd infra/docker
docker-compose down -v
docker-compose up -d
cd ../../apps/api
alembic upgrade head
```

### Port Already in Use
```bash
# Find process using port 8000 (Windows)
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in settings.py
API_PORT=8001
```

---

## Contributing

### Code Style

**Backend (Python):**
- Follow PEP 8
- Use Black for formatting: `black app/`
- Use isort for imports: `isort app/`
- Type hints required: `mypy app/ --strict`
- Max line length: 120 characters

**Frontend (TypeScript):**
- ESLint configuration
- Prettier for formatting
- TypeScript strict mode
- No `any` types

### Commit Messages

Format: `<type>(<scope>): <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```bash
feat(auth): implement JWT token refresh
fix(scan): handle upload errors gracefully
docs(api): update endpoint documentation
```

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [pgvector](https://github.com/pgvector/pgvector)

### Project Documentation
- See `Documents/Documents_Claude_02_Master_forClaudeCodexAntigravity/` for complete specifications
- **PRD:** `02_PRD.md`
- **Architecture:** `03_SYSTEM_ARCHITECTURE.md`
- **API Spec:** `04_API_SPECIFICATION.md`
- **Database:** `05_DATABASE_SCHEMA.md`

---

## License

Proprietary - All rights reserved

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review project documentation in `Documents/`
3. Check existing GitHub issues
4. Contact the development team

---

**Current Status:** Phase 0 Complete ✅ - Infrastructure set up, ready for Phase 1 (Authentication)
