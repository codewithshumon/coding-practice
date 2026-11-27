# `kind` Cluster Creation & Verification Commands

## Commands

```bash
# Create the cluster + local registry
cd /home/shumon/Documents/coding-practice/practical/02-kind-cluster
chmod +x setup-cluster.sh
./setup-cluster.sh

# Verify the cluster
kubectl get nodes -o wide
kubectl get pods -A
curl -s http://localhost:5001/v2/_catalog
```

---

## Breakdown

### 1. `cd /home/shumon/Documents/coding-practice/practical/02-kind-cluster`
Changes your working directory to the `02-kind-cluster` folder where `setup-cluster.sh` and `kind-config.yaml` live.

### 2. `chmod +x setup-cluster.sh`
* **`chmod`** — Changes file permissions ("change mode").
* **`+x`** — Grants **execute** permission on `setup-cluster.sh`.
* **Without it:** Running `./setup-cluster.sh` fails with `Permission denied`.

### 3. `./setup-cluster.sh`
Runs `setup-cluster.sh` from the current directory (`./` tells the shell to run the local file instead of searching `$PATH`). This creates the 3-node `kind` cluster (`prod-k8s`) and starts the local OCI registry on port `5001`.

### 4. `kubectl get nodes -o wide`
* **`kubectl`** — The CLI tool for interacting with Kubernetes clusters.
* **`get nodes`** — Lists all nodes in the cluster (`prod-k8s-control-plane`, `prod-k8s-worker`, `prod-k8s-worker2`).
* **`-o wide`** — **Output: wide**. Displays extra columns (internal IP, OS image, kernel version, container runtime) in addition to `NAME`, `STATUS`, `ROLES`, `AGE`, and `VERSION`.

### 5. `kubectl get pods -A`
* **`get pods`** — Lists running Pods.
* **`-A`** (`--all-namespaces`) — Shows pods across **all namespaces**, not just `default`.
* **Without `-A`:** `kubectl get pods` only checks the `default` namespace, which is empty on a fresh cluster.
* **Core pods in `kube-system`:**
  * `kube-apiserver` — Central Kubernetes API server (`kubectl` talks to this).
  * `etcd` — Key-value database storing all cluster state.
  * `coredns` — Internal DNS server for service/pod name resolution.
  * `kube-proxy` — Manages network routing rules for Services.
  * `kindnet` — CNI networking plugin that connects pods across nodes.

### 6. `curl -s http://localhost:5001/v2/_catalog`
* **`curl -s`** — Sends a silent HTTP `GET` request (no progress bar).
* **`http://localhost:5001/v2/_catalog`** — Queries the Docker Registry v2 API `_catalog` endpoint on your local registry.
* **Expected output (`{"repositories":[]}`):** Confirms the local registry is running, reachable, and currently empty.
