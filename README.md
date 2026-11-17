# Auto Cloud AI

Phase 1 is a Flask-based cloud operations dashboard for the INT378 academic project. It includes a responsive server-rendered UI, authentication, SQLite/PostgreSQL-compatible persistence, CSRF protection, rate-limited AI endpoint scaffolding, and explicit unavailable-service states.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py run.py
```

Open `http://127.0.0.1:5000`. Register an account through the UI, or set
`DEMO_ADMIN_USERNAME`, `DEMO_ADMIN_EMAIL`, and `DEMO_ADMIN_PASSWORD` in `.env`
before the first start to create an administrator account.

Run tests with:

```powershell
pytest
```

External integrations are intentionally not faked in Phase 1. AWS, Gemini, Docker, Jenkins, security scanners, monitoring, and cost data will be added in later phases.

## Docker

Docker Compose runs the production Gunicorn container with PostgreSQL. SQLite
remains the default for local development.

1. Copy `.env.example` to `.env` and set a long random `SECRET_KEY` and
   `POSTGRES_PASSWORD`. Do not commit `.env`.
2. Build and start the services:

   ```powershell
   docker compose build
   docker compose up -d
   ```

3. Check service status and logs:

   ```powershell
   docker compose ps
   docker compose logs -f app
   ```

4. Verify the health endpoint and open the dashboard:

   ```powershell
   Invoke-RestMethod http://localhost:5000/health
   Start-Process http://localhost:5000
   ```

5. Stop the services without deleting the persistent PostgreSQL volume:

   ```powershell
   docker compose down
   ```

   To remove the database volume as well, use
   `docker compose down -v` (this deletes persisted data).

The `postgres_data` named volume preserves database data across container
restarts. The application and database communicate over the private
`autocloud` bridge network. Container logs are sent to stdout/stderr for
`docker compose logs`.

### Image tagging and Docker Hub

Tag a locally built image with your Docker Hub namespace, then log in and push
only when you are ready:

```powershell
docker build --target runtime -t autocloud-ai:latest .
docker tag autocloud-ai:latest YOUR_DOCKERHUB_USERNAME/autocloud-ai:1.0.0
docker tag autocloud-ai:latest YOUR_DOCKERHUB_USERNAME/autocloud-ai:latest
docker login
docker push YOUR_DOCKERHUB_USERNAME/autocloud-ai:1.0.0
docker push YOUR_DOCKERHUB_USERNAME/autocloud-ai:latest
```

Never put Docker Hub credentials, application secrets, or API keys in the
Dockerfile, Compose file, or source code.
