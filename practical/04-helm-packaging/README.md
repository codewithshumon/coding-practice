# Step 4: Helm Packaging (Multi-Environment Chart)

Instead of duplicating YAML for `dev`, `staging`, and `prod`, we packaged all 3 services (`node-api`, `python-api`, `go-api`) into one reusable Helm chart: `polyglot-api/`.

---

## 1. Install `helm` (if not installed)
```bash
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

---

## 2. Lint & Dry-Run Render (Validate Before Deploying)
```bash
cd /home/shumon/Documents/coding-practice/practical/04-helm-packaging

helm lint ./polyglot-api -f ./polyglot-api/values-dev.yaml
helm lint ./polyglot-api -f ./polyglot-api/values-prod.yaml

# Preview exact Kubernetes YAML that Helm generates for dev
helm template polyglot-dev ./polyglot-api -f ./polyglot-api/values-dev.yaml | head -n 45
```

---

## 3. Deploy to `dev` Namespace via Helm
```bash
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace dev pod-security.kubernetes.io/enforce=restricted --overwrite

# Create dev TLS secret
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/dev-tls.key -out /tmp/dev-tls.crt -subj "/CN=dev-api.localtest.me"
kubectl create secret tls dev-api-tls-secret -n dev \
  --key /tmp/dev-tls.key --cert /tmp/dev-tls.crt \
  --dry-run=client -o yaml | kubectl apply -f -
rm -f /tmp/dev-tls.key /tmp/dev-tls.crt

# Install / Upgrade release
helm upgrade --install polyglot-dev ./polyglot-api \
  -n dev \
  -f ./polyglot-api/values-dev.yaml
```

---

## 4. Verify & Test `dev` Endpoints
```bash
helm list -n dev
kubectl get pods,ingress -n dev

curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 https://dev-api.localtest.me/node
curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 https://dev-api.localtest.me/python
curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 https://dev-api.localtest.me/go
```

---

## 5. Practice Helm Upgrade & Rollback
```bash
# Upgrade: scale node-api to 2 replicas in dev
helm upgrade polyglot-dev ./polyglot-api -n dev -f ./polyglot-api/values-dev.yaml --set services.node-api.replicas=2
kubectl get pods -n dev

# Check release history & rollback to revision 1
helm history polyglot-dev -n dev
helm rollback polyglot-dev 1 -n dev
kubectl get pods -n dev
```

---

## Next
Tell me **"done"** once you've tested `helm upgrade` and `helm rollback`, and we'll move to **Step 5: GitOps with Argo CD**.
