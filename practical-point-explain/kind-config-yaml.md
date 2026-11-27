# `kind-config.yaml` — Line-by-Line Explanation

Source file: `/home/shumon/Documents/coding-practice/practical/02-kind-cluster/kind-config.yaml`

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: prod-k8s

# Allow containerd on all K8s nodes to pull from our local OCI registry (localhost:5001)
containerdConfigPatches:
  - |-
    [plugins."io.containerd.grpc.v1.cri".registry]
      config_path = "/etc/containerd/certs.d"

nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP

  - role: worker
  - role: worker
```

---

## Section-by-Section Breakdown

### 1. Cluster Identity (`lines 1–3`)
* **`kind: Cluster`** — Tells the `kind` CLI that this YAML file defines a Kubernetes cluster.
* **`apiVersion: kind.x-k8s.io/v1alpha4`** — Specifies the `kind` configuration schema version (`v1alpha4` is the standard version).
* **`name: prod-k8s`** — Names the cluster `prod-k8s`.
  * **Why it matters:** Your nodes are named `prod-k8s-control-plane`, `prod-k8s-worker`, and `prod-k8s-worker2`, and your `kubectl` context becomes `kind-prod-k8s`.
  * **Without it:** `kind` defaults the cluster name to `kind`.

---

### 2. Local Container Registry Support (`lines 5–9`)
* **`containerdConfigPatches`** — `kind` uses **containerd** (not Docker Engine) inside each Kubernetes node to pull and run images. This injects custom TOML configuration into containerd on every node.
* **`|-`** — YAML syntax for a multi-line string block (preserves newlines, strips the final trailing newline).
* **`[plugins."io.containerd.grpc.v1.cri".registry]`** — Targets containerd's CRI (Container Runtime Interface) registry settings.
* **`config_path = "/etc/containerd/certs.d"`** — Tells containerd to read per-registry configuration files from `/etc/containerd/certs.d` inside each node.
  * **Why it matters:** `setup-cluster.sh` places a `hosts.toml` file in `/etc/containerd/certs.d/localhost:5001/` on each node so Kubernetes pods can pull images from your local registry (`localhost:5001/...`) over plain HTTP.
  * **Without it:** containerd ignores `/etc/containerd/certs.d` and fails to pull images from `localhost:5001`.

---

### 3. Cluster Nodes (`line 11`)
* **`nodes:`** — Lists every node (each running as a Docker container on your host) that forms the Kubernetes cluster.

---

### 4. Control-Plane Node (`lines 12–25`)
* **`- role: control-plane`** — Creates 1 control-plane (master) node running Kubernetes' core control components (`kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`).

#### A. Node Label for Ingress (`lines 13–18`)
* **`kubeadmConfigPatches`** — Passes custom configuration to `kubeadm` (the tool `kind` uses to bootstrap Kubernetes inside the node).
* **`kind: InitConfiguration`** — Applies these settings during control-plane initialization.
* **`nodeRegistration.kubeletExtraArgs`** — Passes extra flags to `kubelet` (the node agent).
* **`node-labels: "ingress-ready=true"`** — Attaches the label `ingress-ready=true` to the control-plane node.
  * **Why it matters:** When installing an Ingress Controller (like NGINX Ingress) in `kind`, its `nodeSelector` looks for `ingress-ready: "true"` so the Ingress Controller pod lands on **this** node—the one with ports `80` and `443` mapped to your host.

#### B. Port Mappings (`lines 19–25`)
* **`extraPortMappings`** — Forwards ports from your host machine (`hostPort`) into the control-plane node container (`containerPort`).
* **`80 -> 80` (TCP)** — Forwards HTTP traffic from `http://localhost` on your machine to port `80` inside the control-plane node.
* **`443 -> 443` (TCP)** — Forwards HTTPS traffic from `https://localhost` on your machine to port `443` inside the control-plane node.
* **Without it:** Your Ingress Controller inside Kubernetes would not be reachable from your browser or `curl` on `localhost`.

---

### 5. Worker Nodes (`lines 27–28`)
* **`- role: worker`** (listed twice) — Adds 2 worker nodes (`prod-k8s-worker` and `prod-k8s-worker2`) dedicated to running your application pods (`node-api`, `python-api`, `go-api`, etc.), simulating a realistic multi-node production cluster.

---

## How Do You Know You Have Those 3 Nodes?

### 1. Where the 3 nodes are defined & created in the files
You do **not** type the names `prod-k8s-control-plane`, `prod-k8s-worker`, or `prod-k8s-worker2` manually anywhere. Instead:
1. **Defined in `kind-config.yaml` (`lines 11–28`):** Each `- role:` entry under `nodes:` creates one node:
   * Line 12: `- role: control-plane` → `prod-k8s-control-plane`
   * Line 27: `- role: worker` → `prod-k8s-worker`
   * Line 28: `- role: worker` → `prod-k8s-worker2`
   `kind` automatically builds those names from `name: prod-k8s` (line 3) + the role name (and adds `2`, `3`, ... for extra nodes of the same role).
2. **Created in `setup-cluster.sh` (`line 20`):**
   ```bash
   kind create cluster --config "${SCRIPT_DIR}/kind-config.yaml"
   ```
   This command reads `kind-config.yaml` and actually creates those 3 Docker containers/nodes.

### 2. By checking live (after creating the cluster)
* **Kubernetes:** `kubectl get nodes`
* **kind CLI:** `kind get nodes --name prod-k8s`
* **Docker (each node is a Docker container):** `docker ps --filter "name=prod-k8s"`

