# TrustVault — Secure Document Sharing

A Flask application demonstrating authenticated users, server-enforced document permissions, private file storage and an audit trail.

## Features
- Owner registration; admin accounts are created through a protected CLI command.
- Password hashing and server-side login sessions.
- Private uploads stored outside the public `static` directory.
- Read and edit permissions; owners/admins can share and revoke access.
- Server-side authorization on download, rename, delete and permission changes.
- Audit records for logins, uploads, downloads, permission changes and denied actions.
- CSRF protection on forms; 10 MB upload limit and extension allowlist.

## Run locally
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Create an admin
Set environment variables (do not commit credentials):
- `ADMIN_USERNAME`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD` (12+ characters)
Then run:
```bash
flask --app app create-admin
```
The admin account is not available through public registration.

## Tests
```bash
pytest -q
```

## Production deployment
Set a strong random `SECRET_KEY`, a persistent `DATABASE_URL` (PostgreSQL recommended), `COOKIE_SECURE=true`, and a persistent private upload volume mounted to the configured `UPLOAD_FOLDER` (or adapt the path for your host). Run with:
```bash
gunicorn app:app
```
Do not use the development secret, SQLite on ephemeral storage, or local ephemeral uploads for production. Configure HTTPS. Back up the database and private upload volume.

## Security notes / limitations
- The allowlist checks extensions, not malware. Production deployments should add antivirus scanning and content-type/signature validation.
- Audit logs are application-level records; production should export them to append-only storage and restrict database access.
- This starter is a compact assessment implementation, not a certified secure document-management product.
