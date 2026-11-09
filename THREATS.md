# Threat model — TrustVault

## Assets
Private document contents, user credentials, role assignments, document permissions, and audit records.

## Trust boundaries
Browser-to-Flask HTTP requests; authenticated user-to-document authorization; application-to-database; application-to-private upload storage; deployment environment variables and persistent volumes.

## Threats and mitigations
| Threat | Mitigation | Verification |
|---|---|---|
| Unauthenticated user downloads a document | `login_required` and server-side access check | Request download without login; expect redirect to login |
| Logged-in user guesses another document ID (IDOR) | `get_document_access` checks owner/admin/explicit permission on every download | Login as unrelated user and request known ID; expect 403 |
| Viewer edits or deletes a document | Edit permission checked on rename; delete restricted to owner/admin | POST rename/delete as viewer; expect 403 |
| User self-assigns admin role | Public registration always assigns `owner`; admin created by CLI environment variables | Register with a `role=admin` form field; account remains owner |
| CSRF changes permissions or deletes files | Flask-WTF CSRF protection on POST forms | Submit POST without CSRF token; expect 400 |
| Path traversal in upload name | `secure_filename` plus random server-generated storage name | Upload `../../secret.txt`; stored name is generated |
| Oversized or disallowed upload | 10 MB request limit and extension allowlist | Upload >10 MB or `.exe`; request rejected |
| Permission revoked but access persists | Every document request re-queries current permission | Revoke, then request download; expect 403 |
| Audit evidence altered by ordinary user | No user-facing audit mutation route | Inspect routes; only audit creation occurs internally |
| Password database disclosure | Werkzeug password hashing | Verify database stores `password_hash`, not plaintext |

## Residual risks
Extension allowlists do not detect malicious content. Production needs malware scanning, strict proxy configuration, database backups, append-only external audit storage, rate limiting, and secure secret management. The test suite is a baseline and should be expanded before production use.
