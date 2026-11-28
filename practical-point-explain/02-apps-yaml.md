# `02-apps.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps/02-apps.yaml`

## Short Summary (TL;DR)
* **What this file does:** Deploys all 3 microservices (`node-api` on `:3000`, `python-api` on `:5000`, `go-api` on `:8080`) into `prod` using 1 shared tokenless `ServiceAccount` (`api-workload-sa`) plus a `Deployment` (`replicas: 2`, `RollingUpdate` with `maxUnavailable: 0` / `maxSurge: 1`, `restricted` securityContext, `readinessProbe` + `livenessProbe`), `ClusterIP` `Service`, and `PodDisruptionBudget` (`minAvailable: 1`) for each service.
* **Why it is needed:** Raw `Pod` manifests don't self-heal, don't load-balance, and cause downtime on updates. This file gives high availability, zero-downtime rollouts, node-upgrade protection, and container-level security.
* **Real-world production example:** An e-commerce backend running Node, Python, and Go APIs in EKS—when a new version is released or a worker node is drained for OS patching, traffic keeps flowing with zero dropped requests.

---

This file deploys all **3 microservices** (`node-api`, `python-api`, `go-api`) into the `prod` namespace using **10 Kubernetes resources**:
* 1 shared **`ServiceAccount`** (`api-workload-sa`)
* For each of the 3 services: a **`Deployment`**, a **`Service`**, and a **`PodDisruptionBudget` (PDB)**

---

## Block 1: `ServiceAccount` (`lines 1–6`)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-workload-sa
  namespace: prod
automountServiceAccountToken: false
```

* **`apiVersion: v1`** — Core stable Kubernetes API (`v1`).
* **`kind: ServiceAccount`** — `kind` = object type; `ServiceAccount` = an **identity for Pods** (just like a IAM user/role is an identity for humans/apps).
  * *Real-world production example:* In AWS EKS, a `ServiceAccount` lets a Pod assume an IAM Role to read an S3 bucket, or talk to the Kubernetes API.
* **`metadata:` / `name: api-workload-sa` / `namespace: prod`** — Names this identity `api-workload-sa` inside the `prod` namespace.
* **`automountServiceAccountToken: false`** — Tells Kubernetes **NOT** to mount a Kubernetes API auth token inside `/var/run/secrets/kubernetes.io/serviceaccount/token` in the Pod.
  * *Why it matters:* `node-api`, `python-api`, and `go-api` are web APIs—they never need to call the Kubernetes API.
  * *Real-world production example:* If an attacker breaks into your Node.js app, they cannot steal a mounted Kubernetes token to query or attack your cluster.
  * *Without it:* Kubernetes mounts the `default` ServiceAccount token into every Pod automatically.

---

## Block 2: `Deployment` (`lines 11–66` for `node-api`; same structure for `python-api` & `go-api`)

### Header & Metadata (`lines 11–17`)
* **`apiVersion: apps/v1`** — `Deployment` lives in the `apps` API group (`v1`), not core `v1`.
* **`kind: Deployment`** — Manages a group of identical Pods (handles scaling, self-healing if a Pod crashes, and zero-downtime updates).
  * *Real-world production example:* Never deploy bare `Pod` objects in production—if a node dies, a bare Pod is gone forever; a `Deployment` immediately recreates it on a healthy node.
* **`metadata.name: node-api`** & **`metadata.namespace: prod`** — Names the Deployment `node-api` inside `prod`.
* **`metadata.labels.app: node-api`** — Tags the Deployment itself with `app: node-api`.

### Replicas & Selector (`lines 18–22`)
* **`spec:`** — Desired state for this Deployment.
* **`replicas: 2`** — Always keep **2 copies (Pods)** running at the same time.
  * *Real-world production example:* Gives high availability—if 1 Pod crashes or a node restarts, the 2nd Pod keeps serving traffic with zero downtime.
* **`selector.matchLabels.app: node-api`** — Tells the Deployment: *"Manage all Pods that have the label `app: node-api`."* Must match `template.metadata.labels` below.

### Zero-Downtime Rollout Strategy (`lines 23–27`)
```yaml
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
```
* **`strategy.type: RollingUpdate`** — Replace old Pods gradually with new Pods instead of killing all Pods at once (`Recreate`).
* **`maxUnavailable: 0`** — **Zero Pods** are allowed to be down during an update (at least 2 healthy Pods must always remain).
* **`maxSurge: 1`** — Kubernetes may temporarily create **1 extra Pod** (total 3 Pods) during an update, wait until the new Pod passes its `readinessProbe`, and *only then* terminate 1 old Pod.
* *Real-world production example:* When deploying `node-api:1.0.1`, users experience **zero failed requests** during the release.

### Pod Template & Pod-Level Security (`lines 28–37`)
* **`template:`** — The blueprint used to create every Pod.
* **`template.metadata.labels.app: node-api`** — Labels each created Pod `app: node-api` so both the `Deployment` and `Service` can find it.
* **`template.spec.serviceAccountName: api-workload-sa`** — Attaches the token-disabled `ServiceAccount` from lines 1–6 to every Pod.
* **`securityContext:` (Pod-level)** — Security rules applied to the whole Pod (required by `enforce: restricted` in `01-namespace-and-security.yaml`):
  * **`runAsNonRoot: true`** — Rejects the container if its image tries to run as `uid=0` (`root`).
  * **`seccompProfile.type: RuntimeDefault`** — Enables the container runtime's default syscall filter (blocks dangerous Linux kernel calls).

### Container Spec (`lines 38–42`)
* **`containers:` / `- name: node-api`** — List of containers in the Pod (named `node-api`).
* **`image: localhost:5001/node-api:1.0.0`** — Pulls the exact pinned version `1.0.0` from your local `kind` registry (`localhost:5001`). *(In AWS/GCP, this would be `<account>.dkr.ecr.../node-api:1.0.0`.)*
* **`ports:` / `- containerPort: 3000`** — Documents that the app listens on port `3000` inside the container.

### Container-Level Security (`lines 43–47`)
* **`allowPrivilegeEscalation: false`** — Blocks processes from gaining extra privileges (e.g., via `setuid` binaries like `sudo`).
* **`readOnlyRootFilesystem: true`** — Locks the container's filesystem as read-only so attackers cannot write malware or edit files on disk.
* **`capabilities.drop: ["ALL"]`** — Strips all extra Linux kernel privileges (`NET_RAW`, `SYS_ADMIN`, etc.) from the container.

### Resource Requests & Limits (`lines 48–54`)
* **`requests:`** — Guaranteed minimum reserved for scheduling (`cpu: 50m` = 5% of 1 core; `memory: 64Mi`).
* **`limits:`** — Hard ceiling (`cpu: 200m` = 20% of 1 core; `memory: 128Mi` $\rightarrow$ `OOMKilled` if exceeded).
* *Why it matters:* Keeps Pods within `prod-quota` (`ResourceQuota`) and stops a memory leak from crashing the worker node.

### Health Probes (`lines 55–66`)
* **`readinessProbe:`** — Checks *"Is this Pod ready to receive user traffic?"*
  * **`httpGet: { path: /health, port: 3000 }`** — Sends `GET http://<pod-ip>:3000/health` (expects HTTP 200–399).
  * **`initialDelaySeconds: 3`** — Waits 3 seconds after container start before the first check.
  * **`periodSeconds: 5`** — Checks every 5 seconds.
  * *Real-world production example:* During a rolling update or heavy startup, traffic is NOT sent to the new Pod until `/health` returns `200 OK`.
* **`livenessProbe:`** — Checks *"Is this Pod still alive or frozen/deadlocked?"*
  * **`httpGet: { path: /health, port: 3000 }`** — Hits `/health` on port `3000`.
  * **`initialDelaySeconds: 10`** — Waits 10 seconds before first check.
  * **`periodSeconds: 10`** — Checks every 10 seconds. If it fails repeatedly (default 3 times), Kubernetes **restarts** the container.

---

## Block 3: `Service` (`lines 68–78`)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: node-api
  namespace: prod
spec:
  selector:
    app: node-api
  ports:
    - port: 3000
      targetPort: 3000
```

* **`apiVersion: v1`** & **`kind: Service`** — Gives your Pods a **single stable internal IP and DNS name** (`node-api.prod.svc.cluster.local`) and load-balances across all ready Pods.
  * *Why it matters:* Pod IPs change every time a Pod restarts or updates; `Service` never changes.
* **`metadata.name: node-api`** & **`metadata.namespace: prod`** — Creates DNS name `node-api` inside `prod`.
* **`spec.selector.app: node-api`** — Routes traffic to all **ready** Pods with label `app: node-api`.
* **`ports:`**
  * **`port: 3000`** — The port other cluster components (like NGINX Ingress) connect to on the `Service`.
  * **`targetPort: 3000`** — The port the container is actually listening on inside the Pod.
* *(Note: `type` is omitted, so it defaults to `ClusterIP`—internal-only, reachable inside the cluster via Ingress.)*

---

## Block 4: `PodDisruptionBudget` (`lines 80–89`)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: node-api-pdb
  namespace: prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: node-api
```

* **`apiVersion: policy/v1`** & **`kind: PodDisruptionBudget`** (PDB) — Protects your app during **voluntary disruptions** (like `kubectl drain` for node OS upgrades or cluster autoscaler scaling down a node).
* **`metadata.name: node-api-pdb`** & **`metadata.namespace: prod`** — Names the PDB and places it in `prod`.
* **`spec.minAvailable: 1`** — Guarantees that **at least 1 Pod** of `node-api` must stay up and ready at all times.
  * *Real-world production example:* If AWS/GKE upgrades both worker nodes at once, Kubernetes refuses to drain the 2nd node until a healthy `node-api` Pod is running elsewhere—preventing accidental outages during maintenance.
* **`spec.selector.matchLabels.app: node-api`** — Applies this protection to Pods labeled `app: node-api`.

---

## Block 5: All 3 Services Compared (`lines 8–255`)

All 3 services use the exact same hardening (`api-workload-sa`, `replicas: 2`, `RollingUpdate` with `maxUnavailable: 0` / `maxSurge: 1`, `restricted` securityContext, `ClusterIP` Service, and `PDB` with `minAvailable: 1`). Here are the service-specific values:

| Service | Lines | Image | Port (`containerPort` / `port` / `targetPort`) | Requests (CPU / RAM) | Limits (CPU / RAM) | Readiness (`initial` / `period`) | Liveness (`initial` / `period`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`node-api`** | `8–90` | `localhost:5001/node-api:1.0.0` | `3000` | `50m` / `64Mi` | `200m` / `128Mi` | `3s` / `5s` | `10s` / `10s` |
| **`python-api`** | `91–173` | `localhost:5001/python-api:1.0.0` | `5000` | `50m` / `64Mi` | `200m` / `128Mi` | `3s` / `5s` | `10s` / `10s` |
| **`go-api`** | `174–255` | `localhost:5001/go-api:1.0.0` | `8080` | `25m` / `32Mi` | `100m` / `64Mi` | `2s` / `5s` | `5s` / `10s` |

*(Notice `go-api` uses half the CPU/RAM and shorter probe delays because compiled Go binaries start faster and use less memory than Node.js or Python!)*
