# `05-argocd-gitops/README.md` — Line-by-Line & Flag-by-Flag Explanation

Source file: `/home/shumon/Documents/coding-practice/practical/05-argocd-gitops/README.md`

## Short Summary (TL;DR)
* **What this file does:** Walks through setting up **GitOps with Argo CD** inside `kind`: pushing your Helm chart to GitHub (`git push`), installing Argo CD in the `argocd` namespace, extracting the initial `admin` password (`jsonpath` + `base64 -d`) and opening the Argo CD UI (`kubectl port-forward ... 8081:443`), preparing the `staging` namespace (`restricted` PSS + `staging-api-tls-secret`), applying `argocd-app-staging.yaml` so Argo CD syncs `staging` from GitHub, and testing **self-healing** (`kubectl scale ... --replicas=4` automatically reverted to `1` by Argo CD).
* **Why it is needed:** Teaches pull-based GitOps deployment—where Kubernetes pulls its desired state from Git instead of engineers/CI pushing directly with `kubectl`/`helm`—and proves drift detection + automatic self-healing works live.
* **Real-world production example:** In real EKS/AKS/GKE production clusters, platform teams install Argo CD once, lock down manual `kubectl` write access, and let Argo CD continuously sync every `git push` across `staging` and `prod` while automatically reverting any manual configuration drift.

---

## Step 1: Push Your Helm Chart to GitHub First (`lines 7–14`)

```bash
cd /home/shumon/Documents/coding-practice
git add practical/
git commit -m "feat: add polyglot-api helm chart and argocd gitops manifests"
git push origin HEAD
```

* **What it does:** Stages all files under `practical/`, creates a commit, and pushes your current local branch (`HEAD`) to `origin` on GitHub.
* **Why it is needed:** Argo CD runs inside the Kubernetes cluster and reads the Helm chart directly from `https://github.com/codewithshumon/coding-practice.git`—not from your local laptop folder. If you don't push first, Argo CD fails with `path not found` in Git.
* **Real-world production example:** Every GitOps workflow requires changes to be committed and pushed to Git first (usually via a reviewed Pull Request) before Argo CD can deploy them.

---

## Step 2: Install Argo CD inside `kind` (`lines 20–29`)

```bash
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for Argo CD server to be Ready (image pull takes ~2-3 min on first install)
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
kubectl get pods -n argocd
```

* **`kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -`**
  * **What it does:** Idempotently creates the dedicated `argocd` namespace where Argo CD's control-plane components will run (safe to re-run if `argocd` already exists).
  * **Why it is needed:** Plain `kubectl create namespace argocd` fails with `AlreadyExists` on re-runs; `--dry-run=client -o yaml | kubectl apply -f -` prevents that while keeping Argo CD's pods, CRDs, and secrets isolated from app namespaces (`dev`, `staging`, `prod`).
  * **Real-world production example:** Every production cluster bootstrap script creates platform namespaces (`argocd`, `ingress-nginx`, `monitoring`) idempotently.
* **`kubectl apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`**
  * **What it does:** Downloads and installs Argo CD's official `stable` manifest (API server, repo-server, application-controller, Redis, Dex, and `Application`/`AppProject` CRDs) into `argocd` using **Server-Side Apply (`--server-side`)** and **`--force-conflicts`**.
  * **Why it is needed:**
    * **`--server-side`:** Argo CD's CRD (`applicationsets.argoproj.io` / `applications.argoproj.io`) is larger than **262,144 bytes (256 KB)**. Regular client-side `kubectl apply` tries to save the entire YAML inside `metadata.annotations["kubectl.kubernetes.io/last-applied-configuration"]` and **crashes with `Too long: may not be more than 262144 bytes`**. Server-Side Apply lets the API server handle field-level merging without that annotation!
    * **`--force-conflicts`:** Automatically resolves field-ownership conflicts if any Argo CD CRDs or manifests were previously applied client-side or by another tool.
  * **Real-world production example:** Modern Helm/Argo CD/Crossplane/Prometheus Operator CRD installs in EKS/GKE always use `--server-side --force-conflicts` because large OpenAPI schemas in CRDs routinely exceed Kubernetes' 256 KB annotation limit.
* **`kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s`**
  * **What it does:** Pauses until the `argocd-server` Pod passes its readiness probe (up to 5 minutes for first-time image pulls), then `kubectl get pods -n argocd` shows all Argo CD pods running.
  * **Why it is needed:** Prevents running `port-forward` or `get secret` before Argo CD finishes starting up.
  * **Real-world production example:** Standard automation gate in cluster bootstrap scripts (Terraform/Bash) before configuring Argo CD apps.

---

## Step 3: Get Admin Password & Open Argo CD UI (`lines 30–38`)

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

kubectl port-forward svc/argocd-server -n argocd 8081:443
```

* **`kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo`**
  * **What it does:**
    * Fetches the auto-generated Secret `argocd-initial-admin-secret`.
    * `-o jsonpath="{.data.password}"` extracts *only* the `password` field (which Kubernetes stores base64-encoded).
    * `| base64 -d` decodes the base64 text into the plain password.
    * `; echo` prints a clean newline so your shell prompt doesn't stick to the end of the password.
  * **Why it is needed:** You need the generated `admin` password to log into the Argo CD Web UI or `argocd` CLI.
  * **Real-world production example:** In production, admins log in once with this initial password, configure SSO (GitHub/Okta/Google), and then **delete** `argocd-initial-admin-secret` for security.
* **`kubectl port-forward svc/argocd-server -n argocd 8081:443`**
  * **What it does:** Creates a secure local tunnel from `https://localhost:8081` on your machine directly to port `443` of the `argocd-server` `Service` inside `kind` (`8081` is used so it doesn't collide with NGINX Ingress on `443`).
  * **Why it is needed:** `argocd-server` is a `ClusterIP` Service (not exposed externally); `port-forward` lets you open the Argo CD UI safely without creating an Ingress first.
  * **Real-world production example:** Engineers use `kubectl port-forward` for temporary private access to internal dashboards (Argo CD, Prometheus, Grafana) without exposing them to the public internet.

---

## Step 4: Deploy Your App via GitOps (`lines 42–66`)

```bash
cd /home/shumon/Documents/coding-practice/practical/05-argocd-gitops

kubectl create namespace staging --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace staging pod-security.kubernetes.io/enforce=restricted --overwrite

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/stg-tls.key -out /tmp/stg-tls.crt -subj "/CN=staging-api.localtest.me"
kubectl create secret tls staging-api-tls-secret -n staging \
  --key /tmp/stg-tls.key --cert /tmp/stg-tls.crt \
  --dry-run=client -o yaml | kubectl apply -f -
rm -f /tmp/stg-tls.key /tmp/stg-tls.crt

kubectl apply -f argocd-app-staging.yaml
```
* **What it does:** Idempotently creates `staging`, enforces `restricted` Pod Security, creates `staging-api-tls-secret` for `staging-api.localtest.me`, and applies `argocd-app-staging.yaml` so Argo CD pulls the Helm chart from GitHub and deploys it to `staging`.
* **Why it is needed:** Notice you did **NOT** run `helm install`! You only gave Argo CD the `Application` manifest, and Argo CD handles rendering and syncing the Helm chart into `staging`.
* **Real-world production example:** Using an "App of Apps" pattern, a platform team applies one root `Application` and Argo CD automatically provisions and syncs every microservice in `staging` and `prod`.

```bash
kubectl get applications -n argocd
kubectl get pods -n staging
```
* **What it does:** Checks Argo CD's `SYNC STATUS` (`Synced`) and `HEALTH STATUS` (`Healthy`), and verifies the 3 API Pods (`go-api`, `node-api`, `python-api`) are `1/1 Running` in `staging`.
* **Why it is needed:** Confirms Argo CD successfully cloned GitHub, rendered Helm, and deployed healthy Pods.
* **Real-world production example:** Standard verification check in GitOps dashboards or CLI scripts.

---

## Step 5: Test Drift Detection & Self-Healing (`lines 70–76`)

```bash
kubectl scale deployment/node-api --replicas=4 -n staging
kubectl get pods -n staging
```

* **What it does:** Manually scales `node-api` up to 4 Pods (creating **configuration drift** because Git `values-dev.yaml` says `replicas: 1`). Within ~10–30 seconds, Argo CD detects `OutOfSync` and **automatically scales `node-api` back down to `1` replica** because `selfHeal: true` is enabled in `argocd-app-staging.yaml`.
* **Why it is needed:** Proves your cluster is truly **GitOps-controlled**: Git always wins over manual `kubectl` changes.
* **Real-world production example:** If an engineer makes an emergency `kubectl edit` or `kubectl scale` during an incident and forgets to update Git, `selfHeal: true` prevents undocumented "snowflake" configuration from lingering in production.
