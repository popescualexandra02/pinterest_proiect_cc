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


## 📌 Pin Service (Business Logic)

Pin Service este microserviciul principal de business logic al aplicației, responsabil de gestionarea pin-urilor (postări de tip Pinterest).

Funcționalități: creare pin (POST /pins), listare pin-uri (GET /pins), verificare stare serviciu (/health, /ready)

## Pin Service porneste cu:
docker run --rm -p 8002:8002 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5433/pinterest" \
  pin-service:dev

## Team
- Constantin Radu
- Popescu Alexandra
- Vilcea Stefania
