# Pinterest-like Cloud Native Application

Cloud-native application inspired by Pinterest, built using:
- Python (FastAPI) microservices
- PostgreSQL
- Kubernetes + Helm
- Docker
- Prometheus + Grafana

## 🧩 Prezentare arhitectura

Aplicatia este deployata ca un set de microservicii independente, care ruleaza intr-un cluster Kubernetes.
Fiecare microserviciu este impachetat ca imagine Docker si este deployat folosind chart-uri Helm.

Componentele de infrastructura (PostgreSQL, Adminer, Portainer, stack-ul de monitoring) sunt, de asemenea, gestionate prin Kubernetes.
Configuratia aplicatiei este transmisa prin variabile de mediu si valori Helm.

Persistenta datelor pentru PostgreSQL este asigurata printr-un PersistentVolumeClaim (PVC).
Monitoring-ul este realizat folosind metrics-server, Prometheus si Grafana.

## Status
## 🔐 Auth Service

Microserviciu dedicat autentificarii utilizatorilor, realizat cu Python + FastAPI.

Parolele sunt criptate folosind Argon2.
Adminer pentru administrarea bazei de date.

Pornire (Docker):

```bash
docker run --rm -p 8001:8001 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5433/pinterest" \
  -e JWT_SECRET="dev-secret" \
  -e JWT_EXP_MINUTES="60" \
  auth-service:dev
```

## 📌 Pin Service (Business Logic)

Microserviciul principal de business logic al aplicatiei, responsabil de gestionarea pin-urilor (postari de tip Pinterest).

Pentru testare locala, user-ul este transmis prin header:

```
X-User-Id: <id>
```

Pornire (Docker):

```bash
docker run --rm -p 8002:8002 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5433/pinterest" \
  pin-service:dev
```

## 🗂️ Board Service

Microserviciu pentru gestionarea board-urilor (colectii de pin-uri).

Pentru testare locala, user-ul este transmis prin header:

```
X-User-Id: <id>
```

Pornire (Docker):

```bash
docker run --rm -p 8003:8003 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5433/pinterest" \
  board-service:dev
```

## 🖼️ Media Service

Microserviciu utilitar pentru incarcarea si servirea fisierelor media (imagini).
Pin-service pastreaza doar image_url, iar media-service gestioneaza upload-ul.

Pornire (Docker):

```bash
docker run --rm -p 8005:8005 \
  media-service:dev
```

Exemplu utilizare:

uploadezi imagine in media-service → primesti path (ex: /media/abc.jpg)

creezi pin in pin-service cu:
image_url = http://localhost:8005/media/abc.jpg

## 👤 User Service

Microserviciu pentru profilul utilizatorului (separat de autentificare).

Pornire (Docker):

```bash
docker run --rm -p 8004:8004 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5433/pinterest" \
  user-service:dev
```

## ☁️ Kubernetes + Helm Deployment

### Prerequisites

- Docker
- Minikube
- kubectl
- Helm

### 🚀 Pornire aplicatie in Kubernetes (Minikube)

#### 1️⃣ Pornire Minikube

```bash
minikube start
```

#### 2️⃣ Creare namespace

```bash
kubectl create namespace pinterest
```

#### 3️⃣ Conectare Docker la Minikube

```bash
eval $(minikube -p minikube docker-env)
```

### 🐳 Build imagini Docker (in Minikube)

```bash
docker build -t auth-service:latest  ./services/auth-service
docker build -t pin-service:latest   ./services/pin-service
docker build -t board-service:latest ./services/board-service
docker build -t media-service:latest ./services/media-service
docker build -t user-service:latest  ./services/user-service
```

### ⚙️ Deploy aplicatie cu Helm

```bash
helm lint infra/helm/pinterest
helm upgrade --install pinterest infra/helm/pinterest -n pinterest
```

Verificare:

```bash
kubectl get pods -n pinterest
kubectl get svc -n pinterest
```

### 🔍 Testare servicii (Swagger + health)

```bash
minikube service auth-service  -n pinterest --url
minikube service pin-service   -n pinterest --url
minikube service board-service -n pinterest --url
minikube service media-service -n pinterest --url
minikube service user-service  -n pinterest --url
```

### 💾 Persistenta bazei de date (PVC)

PostgreSQL foloseste un PersistentVolumeClaim:

```bash
kubectl get pvc -n pinterest
```

Datele sunt pastrate la restartul podului.

### 📊 Monitoring (Metrics Server + Prometheus + Grafana)

#### Metrics Server

```bash
minikube addons enable metrics-server
kubectl top pods -n pinterest
kubectl top nodes
```

#### Prometheus + Grafana

```bash
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring
```

Acces Grafana:

```bash
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80
```

Parola admin:

```bash
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d; echo
```

Dashboard-uri utilizate:

- Kubernetes / Compute Resources / Node
- Kubernetes / Compute Resources / Pod

### 🛠️ Admin Tools

#### Adminer (DB UI)

```bash
minikube service adminer -n pinterest --url
```

#### Portainer (Cluster UI)

```bash
minikube service portainer -n pinterest --url
```

## Team
- Constantin Radu
- Popescu Alexandra
- Vilcea Stefania
