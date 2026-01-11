#!/usr/bin/env bash
set -euo pipefail

# -------------------------
# Config
# -------------------------
APP_NS="pinterest"
APP_RELEASE="pinterest"
APP_CHART="infra/helm/pinterest"

MON_NS="monitoring"
MON_RELEASE="monitoring"
MON_CHART="prometheus-community/kube-prometheus-stack"

# Set to 1 if you want the script to start Grafana port-forward automatically
AUTO_GRAFANA_PORT_FORWARD="${AUTO_GRAFANA_PORT_FORWARD:-0}"

SERVICES=(
  "auth-service"
  "pin-service"
  "board-service"
  "media-service"
  "user-service"
)

echo "==> 1) Starting minikube (if needed)..."
minikube start >/dev/null

echo "==> 2) Ensuring namespaces exist..."
kubectl get ns "${APP_NS}" >/dev/null 2>&1 || kubectl create ns "${APP_NS}"
kubectl get ns "${MON_NS}" >/dev/null 2>&1 || kubectl create ns "${MON_NS}"

echo "==> 3) Pointing Docker CLI to minikube docker daemon..."
eval "$(minikube -p minikube docker-env)"

echo "==> 4) Building service images inside minikube docker..."
for svc in "${SERVICES[@]}"; do
  echo "  -> Building ${svc}:latest"
  docker build -t "${svc}:latest" "./services/${svc}"
done

echo "==> 5) Deploy/Upgrade application Helm chart..."
helm lint "${APP_CHART}"
helm upgrade --install "${APP_RELEASE}" "${APP_CHART}" -n "${APP_NS}"

echo "==> 6) Rolling restart application deployments (ensure latest :latest is used)..."
kubectl rollout restart deployment -n "${APP_NS}" "${SERVICES[@]}"

echo "==> 7) Waiting for application deployments to become ready..."
for svc in "${SERVICES[@]}"; do
  kubectl rollout status deployment -n "${APP_NS}" "${svc}" --timeout=180s
done

echo "==> 8) Enabling metrics-server addon..."
minikube addons enable metrics-server >/dev/null || true

echo "==> 9) Waiting for metrics-server to be ready..."
# metrics-server name can vary slightly; best-effort wait
kubectl -n kube-system rollout status deploy/metrics-server --timeout=180s >/dev/null 2>&1 || true

echo "==> 10) Installing/Upgrading Prometheus+Grafana (kube-prometheus-stack)..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts >/dev/null 2>&1 || true
helm repo update >/dev/null

helm upgrade --install "${MON_RELEASE}" "${MON_CHART}" -n "${MON_NS}"

echo "==> 11) Waiting for Grafana service to exist..."
kubectl get svc -n "${MON_NS}" "${MON_RELEASE}-grafana" >/dev/null 2>&1 || \
  kubectl get svc -n "${MON_NS}" | grep -i grafana >/dev/null 2>&1 || true

echo
echo "==================== STATUS ===================="
echo "==> Pods in ${APP_NS}:"
kubectl get pods -n "${APP_NS}" -o wide

echo
echo "==> Services in ${APP_NS}:"
kubectl get svc -n "${APP_NS}"

echo
echo "==> Quick metrics checks (may take ~30-90s after first install):"
kubectl top nodes || true
kubectl top pods -n "${APP_NS}" || true

echo
echo "==> Monitoring namespace pods:"
kubectl get pods -n "${MON_NS}" -o wide

echo
echo "==================== ACCESS ===================="
echo "Swagger URLs (run and add /docs):"
echo "  minikube service auth-service  -n ${APP_NS} --url"
echo "  minikube service pin-service   -n ${APP_NS} --url"
echo "  minikube service board-service -n ${APP_NS} --url"
echo "  minikube service media-service -n ${APP_NS} --url"
echo "  minikube service user-service  -n ${APP_NS} --url"

echo
echo "Grafana access (recommended):"
echo "  kubectl -n ${MON_NS} port-forward svc/${MON_RELEASE}-grafana 3000:80"
echo "  then open: http://localhost:3000"
echo "Grafana admin password:"
echo "  kubectl get secret -n ${MON_NS} ${MON_RELEASE}-grafana -o jsonpath=\"{.data.admin-password}\" | base64 -d; echo"

if [[ "${AUTO_GRAFANA_PORT_FORWARD}" == "1" ]]; then
  echo
  echo "==> AUTO_GRAFANA_PORT_FORWARD=1 -> starting grafana port-forward on :3000 (Ctrl+C to stop)"
  kubectl -n "${MON_NS}" port-forward "svc/${MON_RELEASE}-grafana" 3000:80
else
  echo
  echo "Done. (Tip: set AUTO_GRAFANA_PORT_FORWARD=1 to auto port-forward Grafana.)"
fi
