# Pinterest-like Cloud Native Application

Cloud-native application inspired by Pinterest, built using:
- Python (FastAPI) microservices
- PostgreSQL
- Kubernetes + Helm
- Docker
- Prometheus + Grafana

## Status
## 🔐 Auth Service

Microserviciu dedicat autentificării utilizatorilor, realizat cu Python + FastAPI.

Funcționalități:
- înregistrare utilizator (/auth/register)
- autentificare utilizator (/auth/login)
- validare token JWT (/auth/me)
- endpoint de health check (/health)

Parolele sunt criptate folosind Argon2.
Bază de date: PostgreSQL rulat în Docker


Adminer pentru administrarea bazei de date
## AuthService porneste cu: 
docker run -p 8001:8001 \
  -e DATABASE_URL=... \
  -e JWT_SECRET=...
  auth-service:dev

## Team
- Constantin Radu
- Popescu Alexandra
- Vilcea Stefania
