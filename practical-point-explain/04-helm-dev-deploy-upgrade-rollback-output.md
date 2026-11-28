# Helm `dev` Deploy, Verify, Upgrade & Rollback — Command & Output Explanation

## Short Summary (TL;DR)
* **What happened:** You idempotently created the `dev` namespace (enforcing Pod Security `restricted`), generated and stored a TLS Secret (`dev-api-tls-secret`), installed the `polyglot-api` Helm chart as release `polyglot-dev` (Revision `1`, all 3 Pods `1/1 Running`, `Ingress` active on `dev-api.localtest.me`), upgraded to Revision `2` (`node-api` scaled `1` $\rightarrow$ `2` Pods via `--set`), inspected `helm history` (`superseded` vs `deployed`), and rolled back to Revision `1` (scaling `node-api` cleanly back to `1` Pod).
* **Why it is needed:** Proves your Helm chart works end-to-end under strict `restricted` Pod Security in Kubernetes, and demonstrates zero-downtime scaling and instant revision-based rollback without editing any YAML files.
* **Real-world production example:** In production EKS/AKS/GKE, this is the exact workflow release engineers and CI/CD pipelines run to deploy a release, verify `1/1 Running` Pods + `Ingress`, inspect `helm history`, and execute `helm rollback <release> <rev>` within seconds if a bad release causes errors.

---

## Command-by-Command & Result Breakdown

### 1. Create `dev` Namespace Idempotently
```bash
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
```
* **Result:** `namespace/dev created`
* **What it does / What the result means:** `--dry-run=client -o yaml` generates the `Namespace` YAML locally without calling the Kubernetes API, then pipes (`|`) it to `kubectl apply -f -`, which creates `dev` (`namespace/dev created`).
* **Why it is needed:** Plain `kubectl create namespace dev` fails with `AlreadyExists` if run twice. Using `--dry-run=client -o yaml | kubectl apply -f -` makes the command **idempotent** (safe to re-run in scripts).
* **Real-world production example:** GitHub Actions or Jenkins bootstrap scripts run this before deploying a feature-branch preview environment (`pr-123`) so re-running a failed CI job never crashes on "namespace already exists."

---

### 2. Enforce Pod Security Standard (`restricted`)
```bash
kubectl label namespace dev pod-security.kubernetes.io/enforce=restricted --overwrite
```
* **Result:** `namespace/dev labeled`
* **What it does / What the result means:** Adds the `pod-security.kubernetes.io/enforce=restricted` label to the `dev` namespace (`namespace/dev labeled`), blocking any Pod that runs as `root` or lacks `seccompProfile` / `allowPrivilegeEscalation: false`.
* **Why it is needed:** Without `enforce=restricted` in `dev`, developers could test root containers locally and only discover security rejections when deploying to `prod`. `--overwrite` prevents errors if the label already exists.
* **Real-world production example:** Platform teams enforce `restricted` across `dev`, `staging`, and `prod` namespaces in EKS/GKE so security issues are caught early in `dev` ("shift-left security").

---

### 3. Create Dev Self-Signed TLS Certificate Secret
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/dev-tls.key -out /tmp/dev-tls.crt -subj "/CN=dev-api.localtest.me"
kubectl create secret tls dev-api-tls-secret -n dev \
  --key /tmp/dev-tls.key --cert /tmp/dev-tls.crt \
  --dry-run=client -o yaml | kubectl apply -f -
rm -f /tmp/dev-tls.key /tmp/dev-tls.crt
```
* **Result:** `secret/dev-api-tls-secret created`
* **What it does / What the result means:** `openssl` generates a 2048-bit RSA key (`-newkey rsa:2048`) and 365-day self-signed X.509 certificate (`-x509`) with no passphrase (`-nodes`) for `dev-api.localtest.me`; `kubectl` stores it idempotently as TLS Secret `dev-api-tls-secret` in `dev`; `rm -f` deletes the temp private key from `/tmp/`.
* **Why it is needed:** `values-dev.yaml` configures Ingress TLS using `tlsSecretName: dev-api-tls-secret`. Without this Secret, NGINX Ingress falls back to a fake default cert or fails TLS handshake.
* **Real-world production example:** In real cloud clusters, `cert-manager` automatically requests a Let's Encrypt or AWS ACM certificate and stores it in `dev-api-tls-secret`—locally we simulate that with `openssl` and delete the private key from disk immediately.

---

### 4. Install Helm Release (`polyglot-dev`)
```bash
helm upgrade --install polyglot-dev ./polyglot-api \
  -n dev \
  -f ./polyglot-api/values-dev.yaml
```
* **Result:**
  ```text
  Release "polyglot-dev" does not exist. Installing it now.
  NAME: polyglot-dev
  LAST DEPLOYED: Sat Nov 28 23:10:57 2026
  NAMESPACE: dev
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None
  ```
* **What it does / What the result means:** `helm upgrade --install` saw no existing `polyglot-dev` release (`does not exist. Installing it now.`), rendered `./polyglot-api` merged with `values-dev.yaml`, and deployed Revision `1` (`STATUS: deployed`) in `dev`. `TEST SUITE: None` means no Helm test hooks exist yet.
* **Why it is needed:** `helm upgrade --install` is the single idempotent command that handles both first-time installation and future updates, while `-f values-dev.yaml` applies `dev`-specific settings (`replicas: 1`, no HPA/PDB).
* **Real-world production example:** Every CD pipeline (GitHub Actions, GitLab CI, Jenkins) uses `helm upgrade --install <release> <chart> -n <env> -f values-<env>.yaml` so the same pipeline step works on day 1 and day 100.

---

### 5. List Helm Releases in `dev`
```bash
helm list -n dev
```
* **Result:**
  ```text
  NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
  polyglot-dev    dev             1               2026-11-28 23:10:57.47920389 +0600 +06  deployed        polyglot-api-0.1.0      1.0.1
  ```
* **What it does / What the result means:** Shows all Helm releases in `dev`: `polyglot-dev` is at `REVISION: 1`, `STATUS: deployed`, using chart `polyglot-api-0.1.0` (`Chart.yaml` `version`) and `APP VERSION: 1.0.1` (`Chart.yaml` `appVersion`).
* **Why it is needed:** Confirms Helm's release state (`deployed` vs `failed` or `pending-upgrade`) and verifies which exact chart and app version are currently live.
* **Real-world production example:** During an incident, an engineer runs `helm list -A` to verify which chart version and app version are deployed across `dev`, `staging`, and `prod` namespaces.

---

### 6. Verify Pods & Ingress in `dev`
```bash
kubectl get pods,ingress -n dev
```
* **Result:**
  ```text
  NAME                              READY   STATUS    RESTARTS   AGE
  pod/go-api-77fbbff7f5-dbjns       1/1     Running   0          96s
  pod/node-api-7c7566545f-fg26h     1/1     Running   0          96s
  pod/python-api-77cbc8fb8c-x7npw   1/1     Running   0          96s

  NAME                                             CLASS   HOSTS                  ADDRESS     PORTS     AGE
  ingress.networking.k8s.io/polyglot-dev-ingress   nginx   dev-api.localtest.me   localhost   80, 443   96s
  ```
* **What it does / What the result means:** Confirms all 3 Pods (`go-api`, `node-api`, `python-api`, 1 replica each per `values-dev.yaml`) are `1/1 Running` with `0` restarts, and `polyglot-dev-ingress` (`CLASS: nginx`, `HOSTS: dev-api.localtest.me`) has an active `ADDRESS: localhost` on ports `80, 443`.
* **Why it is needed:** `helm install` succeeding only means YAML was submitted—checking `kubectl get pods,ingress` proves the containers actually started, passed `restricted` Pod Security + `/health` probes, and got picked up by NGINX Ingress.
* **Real-world production example:** Smoke-check step in a deployment pipeline right after `helm upgrade`, verifying Pods are `1/1 Running` and the cloud Load Balancer populated the Ingress `ADDRESS` before running integration tests.

---

### 7. Helm Upgrade (Scale `node-api` to 2 Replicas)
```bash
helm upgrade polyglot-dev ./polyglot-api -n dev -f ./polyglot-api/values-dev.yaml --set services.node-api.replicas=2
```
* **Result:**
  ```text
  Release "polyglot-dev" has been upgraded. Happy Helming!
  ...
  STATUS: deployed
  REVISION: 2
  ```
* **What it does / What the result means:** Upgrades `polyglot-dev` to `REVISION: 2` (`STATUS: deployed`), using `--set services.node-api.replicas=2` to override `replicas: 1` from `values-dev.yaml`.
* **Why it is needed:** `--set` has the highest precedence in Helm (`values.yaml` $\rightarrow$ `-f` $\rightarrow$ `--set`), allowing quick runtime overrides (like scaling or bumping a single image tag) without editing committed YAML files.
* **Real-world production example:** A CI pipeline builds `node-api:1.0.2` and runs `helm upgrade ... -f values-prod.yaml --set services.node-api.tag=1.0.2` to deploy only that new tag.

---

### 8. Verify Scaled Pods
```bash
kubectl get pods -n dev
```
* **Result:**
  ```text
  go-api-77fbbff7f5-dbjns       1/1     Running   0          2m27s
  node-api-7c7566545f-fg26h     1/1     Running   0          2m27s
  node-api-7c7566545f-xbfzg     1/1     Running   0          11s
  python-api-77cbc8fb8c-x7npw   1/1     Running   0          2m27s
  ```
* **What it does / What the result means:** Shows `node-api` now has **2** healthy Pods: the original `fg26h` (`2m27s` old, undisturbed) and the new `xbfzg` (`11s` old, `1/1 Running`), while `go-api` and `python-api` remained untouched.
* **Why it is needed:** Proves the Helm upgrade only changed what differed (`node-api` replicas) with **zero downtime** to existing Pods.
* **Real-world production example:** Before an expected marketing event or load test, an engineer scales a single bottleneck microservice without restarting unrelated services.

---

### 9. Inspect Helm Release History
```bash
helm history polyglot-dev -n dev
```
* **Result:**
  ```text
  REVISION        UPDATED                         STATUS          CHART                   APP VERSION     DESCRIPTION
  1               Sat Nov 28 23:10:57 2026        superseded      polyglot-api-0.1.0      1.0.1           Install complete
  2               Sat Nov 28 23:13:12 2026        deployed        polyglot-api-0.1.0      1.0.1           Upgrade complete
  ```
* **What it does / What the result means:** Lists every deployment revision stored by Helm: Revision `1` is now `superseded` (replaced by a newer revision, still stored for rollback) and Revision `2` is `deployed` (`Upgrade complete`).
* **Why it is needed:** Shows the exact audit trail of when changes happened and gives you the target revision number (`1`) to roll back to.
* **Real-world production example:** When latency spikes at 2:15 PM, an on-call engineer runs `helm history <release> -n prod` to see if a deployment happened at 2:13 PM and grabs the last known-good revision number.

---

### 10. Roll Back to Revision 1 & Verify
```bash
helm rollback polyglot-dev 1 -n dev
kubectl get pods -n dev
```
* **Result:**
  * `Rollback was a success! Happy Helming!`
  * `kubectl get pods -n dev` shows 3 Pods (`go-api`, 1 `node-api` `fg26h`, `python-api`)—the 2nd `node-api` Pod (`xbfzg`) was cleanly terminated.
* **What it does / What the result means:** Reverts `polyglot-dev` back to the exact manifests and values of Revision `1` (which Helm records as Revision `3` in history), scaling `node-api` back down to `1` Pod.
* **Why it is needed:** Provides a 1-command, instant recovery mechanism if an upgrade introduces a bug, bad config, or broken image tag—without needing to hunt down old Git commits or manually edit YAML.
* **Real-world production example:** If a bad production release causes HTTP 500 errors, the on-call engineer runs `helm rollback api-prod <last-good-rev> -n prod` to restore service in seconds while the team debugs offline.
