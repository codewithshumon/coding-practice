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

---

## Detailed Breakdown of Your Actual Output

### 1. Registry Output
```json
{"repositories":[]}
```
* Your `kind-registry` container is alive and responding on `localhost:5001`.
* `"repositories":[]` is an empty list because no Docker/OCI images have been pushed to `localhost:5001` yet.

---

### 2. `kubectl get nodes -o wide` Output
```text
NAME                     STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION      CONTAINER-RUNTIME
prod-k8s-control-plane   Ready    control-plane   14m   v1.32.2   172.31.0.4    <none>        Debian GNU/Linux 12 (bookworm)   7.2.15+kali-amd64   containerd://2.0.2
prod-k8s-worker          Ready    <none>          14m   v1.32.2   172.31.0.2    <none>        Debian GNU/Linux 12 (bookworm)   7.2.15+kali-amd64   containerd://2.0.2
prod-k8s-worker2         Ready    <none>          14m   v1.32.2   172.31.0.3    <none>        Debian GNU/Linux 12 (bookworm)   7.2.15+kali-amd64   containerd://2.0.2
```

Every column explained:
* **`NAME`** — The 3 node names auto-generated from `name: prod-k8s` + roles in `kind-config.yaml`.
* **`STATUS` (`Ready`)** — All 3 nodes are healthy, connected to the control plane, and ready to accept Pods.
* **`ROLES`** — `control-plane` manages the cluster; `<none>` simply means standard worker node (Kubernetes leaves worker roles blank by default).
* **`AGE` (`14m`)** — Created 14 minutes ago.
* **`VERSION` (`v1.32.2`)** — Kubernetes version running on every node (`kubelet`).
* **`INTERNAL-IP` (`172.31.0.2`, `.3`, `.4`)** — Private IPs assigned on the `kind` Docker bridge network so nodes can talk to each other.
* **`EXTERNAL-IP` (`<none>`)** — No public cloud IP because this is a local `kind` cluster (on AWS/GCP/Azure, nodes can have public IPs).
* **`OS-IMAGE` (`Debian GNU/Linux 12 (bookworm)`)** — The Linux OS inside the `kind` node container image.
* **`KERNEL-VERSION` (`7.2.15+kali-amd64`)** — Shared from your host machine's Linux kernel (containers share the host kernel).
* **`CONTAINER-RUNTIME` (`containerd://2.0.2`)** — The engine inside each node that pulls images and runs containers.

---

### 3. `kubectl get pods -A` Output

#### Columns:
* **`NAMESPACE`** — Logical group isolating resources (`kube-system` for K8s core, `local-path-storage` for storage).
* **`NAME`** — Unique Pod name. Control-plane pods end with `-prod-k8s-control-plane`; Deployment/DaemonSet pods have random suffixes (like `-gljz8`).
* **`READY` (`1/1`)** — `1` out of `1` container inside the Pod is healthy and passing readiness checks.
* **`STATUS` (`Running`)** — All Pods are actively running.
* **`RESTARTS` (`0`)** — Zero crashes! (High restart counts indicate crash loops.)
* **`AGE` (`14m`)** — Running continuously since cluster creation.

#### Every Pod Explained:
1. **`coredns` (2 pods in `kube-system`)** — Internal DNS server for the cluster. Lets Pods find Services by name (e.g., `node-api.default.svc.cluster.local`). Runs 2 replicas for high availability.
2. **`etcd-prod-k8s-control-plane` (1 pod)** — The cluster's key-value database storing all Kubernetes state (Deployments, Secrets, ConfigMaps, Pod statuses).
3. **`kube-apiserver-prod-k8s-control-plane` (1 pod)** — The front door/API brain of Kubernetes. Every `kubectl` command and internal component talks to this.
4. **`kube-controller-manager-prod-k8s-control-plane` (1 pod)** — Background control loops that keep actual state matching desired state (e.g., if a Deployment wants 3 replicas and 1 dies, it creates a replacement).
5. **`kube-scheduler-prod-k8s-control-plane` (1 pod)** — Decides which node (`worker` or `worker2`) a new Pod should run on based on CPU/memory and labels.
6. **`kindnet` (3 pods in `kube-system`)** — A **DaemonSet** (1 Pod per node $\times$ 3 nodes). It is the CNI networking plugin that gives every Pod its own IP and routes traffic between nodes.
7. **`kube-proxy` (3 pods in `kube-system`)** — Also a **DaemonSet** (1 Pod per node $\times$ 3 nodes). Maintains network/iptables rules on every node so Kubernetes `Service` IPs route to the right backend Pods.
8. **`local-path-provisioner` (1 pod in `local-path-storage`)** — Automatically creates `PersistentVolume` storage on the host/node disk whenever an app requests a `PersistentVolumeClaim` (e.g., for databases or logs).

