# Helm `dev` Deploy, Verify, Upgrade & Rollback — Command & Output Explanation

## Short Summary (TL;DR)
* **What happened:** You idempotently created the `dev` namespace (enforcing Pod Security `restricted`), generated and stored a TLS Secret (`dev-api-tls-secret`), installed the `polyglot-api` Helm chart as release `polyglot-dev` (Revision `1`, all 3 Pods `1/1 Running`, `Ingress` active on `dev-api.localtest.me`), upgraded to Revision `2` (`node-api` scaled `1` $\rightarrow$ `2` Pods via `--set`), inspected `helm history` (`superseded` vs `deployed`), and rolled back to Revision `1` (scaling `node-api` cleanly back to `1` Pod).
* **Why it is needed:** Proves your Helm chart works end-to-end under strict `restricted` Pod Security in Kubernetes, and demonstrates zero-downtime scaling and instant revision-based rollback without touching any YAML files.
* **Real-world production example:** In production EKS/AKS/GKE, this is the exact workflow used by release engineers and CI/CD pipelines to deploy a release, verify `1/1 Running` Pods + `Ingress` address, inspect `helm history`, and run `helm rollback <release> <rev>` within seconds if a bad release causes errors.

---

## Command-by-Command & Result Breakdown

### 1. Create `dev` Namespace Idempotently
```bash
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
```
* **Result:** `namespace/dev created`
* **What it means:** `--dry-run=client -o yaml` generated the Namespace YAML locally without calling the API server, and `kubectl apply -f -` created `dev`. Running it again later would safely say `namespace/dev unchanged` instead of failing.

---

### 2. Enforce Pod Security Standard (`restricted`)
```bash
kubectl label namespace dev pod-security.kubernetes.io/enforce=restricted --overwrite
```
* **Result:** `namespace/dev labeled`
* **What it means:** Attached the `restricted` Pod Security Standard label to `dev`, blocking any container running as `root` or without `seccompProfile` / `allowPrivilegeEscalation: false`. `--overwrite` ensures re-runs won't fail.

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
* **What it means:**
  * `openssl` generated a 2048-bit RSA key + 365-day self-signed X.509 cert (`....+++...`) for `dev-api.localtest.me` without a passphrase (`-nodes`).
  * `kubectl create secret tls ... --dry-run=client -o yaml | kubectl apply -f -` stored it idempotently in `dev` as `dev-api-tls-secret` (matching `values-dev.yaml`).
  * `rm -f` deleted the temporary private key from `/tmp/`.

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
* **What each line means:**
  * `Release "polyglot-dev" does not exist. Installing it now.` — `helm upgrade --install` saw no existing release in `dev`, so it performed a fresh install.
  * `STATUS: deployed` — All Kubernetes resources (`ServiceAccount`, 3 `Deployment`s, 3 `Service`s, `Ingress`) were accepted and applied.
  * `REVISION: 1` — First version stored in Helm's release history (saved as a Kubernetes `Secret` in `dev`).
  * `TEST SUITE: None` — No `helm test` hook Pods are defined in `templates/tests/`.

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
* **What it means:** Confirms release `polyglot-dev` is at Revision `1`, `deployed` using chart `polyglot-api-0.1.0` (`Chart.yaml` `version`) and `APP VERSION` `1.0.1` (`Chart.yaml` `appVersion`).

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
* **What it means:**
  * All 3 Pods (`go-api`, `node-api`, `python-api`) are **`1/1 Running`** with `0` restarts—meaning `tag: "1.0.1"` passed `restricted` Pod Security and `/health` readiness probes!
  * Only 1 Pod per service (3 total) because `values-dev.yaml` sets `replicas: 1`.
  * `polyglot-dev-ingress` has `CLASS: nginx`, `HOSTS: dev-api.localtest.me`, `ADDRESS: localhost`, and `PORTS: 80, 443`.

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
* **What it means:** `--set services.node-api.replicas=2` overrode `replicas: 1` from `values-dev.yaml`, creating **Revision 2** without changing any files on disk.

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
* **What it means:** Notice `node-api` now has **2 Pods**: the original `fg26h` (`2m27s` old, untouched!) and the brand-new `xbfzg` (`11s` old, `1/1 Running`). Zero downtime!

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
* **What it means:**
  * Revision 1's status changed from `deployed` $\rightarrow$ **`superseded`** (replaced by a newer revision, but still saved in Helm history so you can roll back to it).
  * Revision 2 is currently **`deployed`**.

---

### 10. Roll Back to Revision 1 & Verify
```bash
helm rollback polyglot-dev 1 -n dev
kubectl get pods -n dev
```
* **Result:**
  * `Rollback was a success! Happy Helming!`
  * `kubectl get pods -n dev` now shows only **1** `node-api` Pod (`fg26h`, `3m28s`)—the extra Pod (`xbfzg`) from Revision 2 was cleanly terminated!
* **Important Helm detail:** Rolling back to Revision 1 actually records a **Revision 3** (`Rollback to 1`) in `helm history`, so your full audit trail is preserved.
