# FastAPI Notes App

This is a sample **FastAPI** application featuring:

- User registration and login with JWT tokens
- CRUD for notes (create, read, delete)
- SQLite database via SQLAlchemy
- Simple static frontend (Vanilla JS)
- Dockerfile with non-root user
- CI/CD via GitHub Actions deploying to Google Cloud Run

## Prerequisites

- Python 3.11+
- Docker
- Google Cloud SDK (`gcloud`)
- GitHub repository with secrets:
  - `GCP_PROJECT_ID`
  - `GCP_SA_KEY`

## Local Setup

1. Clone repo and `cd fastapi-notes-app`
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `uvicorn app.main:app --reload`
4. Open `http://127.0.0.1:8000` in browser

## Google Cloud Run Deployment

1. Authenticate: `gcloud auth login` + `gcloud config set project YOUR_PROJECT_ID`
2. Build and deploy via GitHub Actions on push to `main` branch

## Creating secret

```bash
python - << 'EOF'
import secrets
print(secrets.token_urlsafe(32))
EOF
```

---
