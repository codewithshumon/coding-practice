# Step 3: NGINX Ingress Controller + TLS + Production K8s Primitives

Everything runs **inside `kind` Kubernetes** (just like EKS / AKS / GKE).

---

## 1. Build & Push All 3 Images to Your Local OCI Registry (`localhost:5001`)

```bash
cd /home/shumon/Documents/coding-practice/practical/01-production-docker
docker buildx build --network=host -t localhost:5001/node-api:1.0.0 --push ./node-api
docker buildx build --network=host -t localhost:5001/python-api:1.0.0 --push ./python-api
docker buildx build --network=host -t localhost:5001/go-api:1.0.0 --push ./go-api

curl -s http://localhost:5001/v2/_catalog
```

---

## 2. Install NGINX Ingress Controller inside `kind`

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Wait until NGINX Ingress Pod is Ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

---

## 3. Apply Production Namespace, Security, Apps, TLS & HPA

```bash
cd /home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps

# Apply namespace + Pod Security 'restricted' + ResourceQuota + NetworkPolicy
kubectl apply -f 01-namespace-and-security.yaml

# Create TLS certificate secret for Ingress
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=api.localtest.me"
kubectl create secret tls api-tls-secret \
  --namespace prod \
  --key /tmp/tls.key --cert /tmp/tls.crt
rm -f /tmp/tls.key /tmp/tls.crt

# Deploy all 3 apps + Ingress + HPA + RBAC
kubectl apply -f 02-apps.yaml
kubectl apply -f 03-ingress-tls.yaml
kubectl apply -f 04-hpa-and-rbac.yaml
```

---

## 4. Verify Pods, Nodes & Ingress

```bash
kubectl get pods -n prod -o wide
kubectl get ingress -n prod
kubectl get pdb,hpa -n prod
```

Notice how Pods are spread across `prod-k8s-worker` and `prod-k8s-worker2`!

---

## 5. Test HTTPS Routing & Load Balancing via NGINX Ingress

```bash
curl -sk --resolve api.localtest.me:443:127.0.0.1 https://api.localtest.me/node
curl -sk --resolve api.localtest.me:443:127.0.0.1 https://api.localtest.me/python
curl -sk --resolve api.localtest.me:443:127.0.0.1 https://api.localtest.me/go
```

Run `/node` twice in a row—watch `"hostname"` switch between the 2 Pod replicas!

---

## Next

Tell me **"done"** once all 3 endpoints respond over HTTPS, and we'll move to **Step 4: Helm Packaging**.
