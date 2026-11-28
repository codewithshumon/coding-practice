# Step 5: GitOps with Argo CD

Everything runs **inside `kind` Kubernetes**, pulling your Helm chart directly from GitHub (`https://github.com/codewithshumon/coding-practice.git`).

---

## 1. Push Your Helm Chart to GitHub First
Argo CD reads from your GitHub repo, so commit and push `practical/04-helm-packaging`:
```bash
cd /home/shumon/Documents/coding-practice
git add practical/
git commit -m "feat: add polyglot-api helm chart and argocd gitops manifests"
git push origin HEAD
```

---

## 2. Install Argo CD inside `kind`
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for Argo CD server & repo-server to be Ready (can take ~2 min)
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
kubectl get pods -n argocd
```

---

## 3. Get Admin Password & Open Argo CD UI
```bash
# Print initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Port-forward Argo CD UI in the background (or a separate terminal)
kubectl port-forward svc/argocd-server -n argocd 8081:443
```
Open **`https://localhost:8081`** in your browser -> Login with username **`admin`** and the password printed above.

---

## 4. Deploy Your App via GitOps (`Application`)
In another terminal:
```bash
cd /home/shumon/Documents/coding-practice/practical/05-argocd-gitops

# Create staging namespace with restricted Pod Security + TLS secret
kubectl create namespace staging --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace staging pod-security.kubernetes.io/enforce=restricted --overwrite

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/stg-tls.key -out /tmp/stg-tls.crt -subj "/CN=staging-api.localtest.me"
kubectl create secret tls staging-api-tls-secret -n staging \
  --key /tmp/stg-tls.key --cert /tmp/stg-tls.crt \
  --dry-run=client -o yaml | kubectl apply -f -
rm -f /tmp/stg-tls.key /tmp/stg-tls.crt

# Apply the Argo CD Application
kubectl apply -f argocd-app-staging.yaml
```

Watch Argo CD sync `staging`:
```bash
kubectl get applications -n argocd
kubectl get pods -n staging
```

---

## 5. Test Drift Detection & Self-Healing (Real GitOps!)
Manually scale `node-api` in `staging` (creating drift from Git):
```bash
kubectl scale deployment/node-api --replicas=4 -n staging
kubectl get pods -n staging
```
Wait ~10–30 seconds and run `kubectl get pods -n staging` again—**Argo CD will automatically scale it back down to `1` replica** to match Git (`selfHeal: true`)!

---

## Next
Tell me **"done"** once Argo CD shows `Synced` + `Healthy` and you've seen `selfHeal` revert manual drift, and we'll move to **Step 6: CI/CD with GitHub Actions + BuildKit**.
