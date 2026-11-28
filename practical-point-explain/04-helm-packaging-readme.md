# `04-helm-packaging/README.md` — Line-by-Line & Flag-by-Flag Explanation

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/README.md`

## Short Summary (TL;DR)
* **What this file does:** Walks through the complete Helm lifecycle for the `polyglot-api` chart: installing `helm`, validating/rendering templates (`helm lint`, `helm template`), idempotently preparing the `dev` namespace + TLS secret + `restricted` Pod Security label, deploying with `helm upgrade --install -f values-dev.yaml`, testing HTTPS endpoints, and practicing live upgrades (`--set`) and instant rollbacks (`helm rollback`).
* **Why it is needed:** Shows how one reusable Helm chart replaces raw environment-specific YAML files and teaches safe production workflows—validating before applying (`lint`/`template`), idempotent scripting (`--dry-run=client -o yaml | kubectl apply -f -`), and zero-panic rollbacks (`helm history` + `helm rollback`).
* **Real-world production example:** This exact sequence (`helm lint` $\rightarrow$ `helm template` $\rightarrow$ `helm upgrade --install -f values-prod.yaml --set ...` $\rightarrow$ `helm rollback` on failure) is what GitHub Actions / Jenkins CI pipelines run when deploying microservices to AWS EKS, Azure AKS, or GCP GKE.

---

## Step 1: Install `helm` (`lines 7–11`)

```bash
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

* **`curl -fsSL <URL> | bash`** — Downloads and runs the official Helm 3 installer script:
  * `-f` (`--fail`): Fail silently on HTTP errors (don't pipe a `404` HTML page into `bash`).
  * `-s` (`--silent`): Hide progress bar.
  * `-S` (`--show-error`): Still print an error if `-s` is on and `-f` fails.
  * `-L` (`--location`): Follow HTTP redirects.
* **`helm version`** — Confirms Helm v3 is installed and prints its version.

---

## Step 2: Lint & Dry-Run Render (`lines 15–24`)

```bash
cd /home/shumon/Documents/coding-practice/practical/04-helm-packaging

helm lint ./polyglot-api -f ./polyglot-api/values-dev.yaml
helm lint ./polyglot-api -f ./polyglot-api/values-prod.yaml

helm template polyglot-dev ./polyglot-api -f ./polyglot-api/values-dev.yaml | head -n 45
```

* **`helm lint ./polyglot-api -f ./polyglot-api/values-dev.yaml`** — Checks `Chart.yaml`, `values.yaml`, and all `templates/*.yaml` for syntax errors, missing required fields, or broken Go-template logic **for both `dev` and `prod` value overrides** before touching Kubernetes.
* **`helm template polyglot-dev ./polyglot-api -f ./polyglot-api/values-dev.yaml`** — Renders the final Kubernetes YAML **locally on your screen** without connecting to any cluster (like a dry-run preview).
  * `polyglot-dev`: Simulated release name (populates `.Release.Name`).
  * `| head -n 45`: Shows only the first 45 lines so your terminal isn't flooded.
  * *Real-world production example:* CI pull-request checks run `helm lint` + `helm template` so broken templates are caught before merge.

---

## Step 3: Deploy to `dev` Namespace via Helm (`lines 28–45`)

### A. Idempotent Namespace Creation + Pod Security Label
```bash
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace dev pod-security.kubernetes.io/enforce=restricted --overwrite
```
* **`--dry-run=client -o yaml | kubectl apply -f -`** — Classic Kubernetes **idempotency trick**:
  * `kubectl create namespace dev` normally **fails** if `dev` already exists.
  * Adding `--dry-run=client -o yaml` tells `kubectl` *not* to create it yet—just print the YAML locally, then pipe (`|`) it to `kubectl apply -f -`, which safely creates it if missing or leaves it unchanged if it already exists!
* **`kubectl label namespace dev pod-security.kubernetes.io/enforce=restricted --overwrite`** — Enforces Kubernetes' strictest `restricted` Pod Security Standard on `dev`; `--overwrite` updates the label cleanly if it already exists.

### B. Dev TLS Certificate Secret (Idempotent)
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/dev-tls.key -out /tmp/dev-tls.crt -subj "/CN=dev-api.localtest.me"
kubectl create secret tls dev-api-tls-secret -n dev \
  --key /tmp/dev-tls.key --cert /tmp/dev-tls.crt \
  --dry-run=client -o yaml | kubectl apply -f -
rm -f /tmp/dev-tls.key /tmp/dev-tls.crt
```
* Generates a self-signed TLS cert for `dev-api.localtest.me` (matches `values-dev.yaml`), creates/updates `dev-api-tls-secret` idempotently using `--dry-run=client -o yaml | kubectl apply -f -`, and deletes the temp key from `/tmp/`.

### C. Install / Upgrade Release
```bash
helm upgrade --install polyglot-dev ./polyglot-api \
  -n dev \
  -f ./polyglot-api/values-dev.yaml
```
* **`helm upgrade --install`** — Another **idempotent** production command:
  * If release `polyglot-dev` doesn't exist yet $\rightarrow$ **installs** it (Revision 1).
  * If `polyglot-dev` already exists $\rightarrow$ **upgrades** it (Revision 2, 3, ...).
* **`polyglot-dev`** — Release name (creates `polyglot-dev-sa`, `polyglot-dev-ingress`, etc.).
* **`./polyglot-api`** — Local chart directory.
* **`-n dev`** — Target namespace (`dev`).
* **`-f ./polyglot-api/values-dev.yaml`** — Overrides `values.yaml` with `dev` settings (`replicas: 1`, `hpa.enabled: false`, `pdb.enabled: false`, `dev-api.localtest.me`).

---

## Step 4: Verify & Test `dev` Endpoints (`lines 49–57`)

```bash
helm list -n dev
kubectl get pods,ingress -n dev

curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 https://dev-api.localtest.me/node
curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 https://dev-api.localtest.me/python
curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 https://dev-api.localtest.me/go
```

* **`helm list -n dev`** — Lists installed Helm releases in `dev`, showing `REVISION`, `STATUS` (`deployed`), `CHART` (`polyglot-api-0.1.0`), and `APP VERSION` (`1.0.1`).
* **`kubectl get pods,ingress -n dev`** — Verifies all 3 Pods (`1/1 Running`) and `polyglot-dev-ingress` (`dev-api.localtest.me`).
* **`curl -sk --resolve dev-api.localtest.me:443:127.0.0.1 ...`** — Tests HTTPS routing for all 3 endpoints on `dev-api.localtest.me` without needing `/etc/hosts`.

---

## Step 5: Practice Helm Upgrade & Rollback (`lines 61–71`)

```bash
helm upgrade polyglot-dev ./polyglot-api -n dev -f ./polyglot-api/values-dev.yaml --set services.node-api.replicas=2
kubectl get pods -n dev

helm history polyglot-dev -n dev
helm rollback polyglot-dev 1 -n dev
kubectl get pods -n dev
```

* **`helm upgrade ... --set services.node-api.replicas=2`** — Creates **Revision 2**, overriding `replicas` to `2` on the command line (`--set` has the highest priority, beating `values.yaml` and `-f values-dev.yaml`). `node-api` scales from 1 $\rightarrow$ 2 Pods.
* **`helm history polyglot-dev -n dev`** — Shows all revisions (`1`, `2`, ...) with timestamps, statuses, and descriptions.
* **`helm rollback polyglot-dev 1 -n dev`** — Instantly reverts `polyglot-dev` back to **Revision 1** (which creates **Revision 3** in history!), scaling `node-api` back down to 1 Pod.
  * *Real-world production example:* If a bad release breaks production, `helm rollback <release> <prev-rev>` restores the exact previous templates, config, and image tags in seconds.
