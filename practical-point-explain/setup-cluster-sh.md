# `setup-cluster.sh` — Line-by-Line Explanation

Source file: `/home/shumon/Documents/coding-practice/practical/02-kind-cluster/setup-cluster.sh`

This script is **idempotent** (safe to run multiple times without breaking existing resources). It sets up a local OCI image registry (`localhost:5001`), creates the 3-node `kind` cluster, wires `containerd` on every node to use that registry, and documents the registry in Kubernetes.

---

## 1. Shebang & Strict Mode (`lines 1–2`)

```bash
#!/usr/bin/env bash
set -euo pipefail
```

* **`#!/usr/bin/env bash`** — Shebang: tells Linux to execute this file using `bash` found in your `$PATH`.
* **`set -euo pipefail`** — Bash strict mode:
  * **`-e`**: Exit immediately if any command returns a non-zero (error) status.
  * **`-u`**: Treat any unset/undefined variable as an error instead of expanding to an empty string.
  * **`-o pipefail`**: If any command in a pipeline (`cmd1 | cmd2`) fails, the whole pipeline fails (by default, Bash only checks the last command).

---

## 2. Configuration Variables (`lines 4–7`)

```bash
CLUSTER_NAME="prod-k8s"
REG_NAME="kind-registry"
REG_PORT="5001"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

* **`CLUSTER_NAME="prod-k8s"`** — Must match `name: prod-k8s` in `kind-config.yaml`.
* **`REG_NAME="kind-registry"`** — Docker container name for the local OCI/Docker registry.
* **`REG_PORT="5001"`** — Port on `localhost` where you push images (e.g., `localhost:5001/node-api:1.0.0`).
* **`SCRIPT_DIR=...`** — Resolves the **absolute folder path** where `setup-cluster.sh` is located.
  * **Why it matters:** Even if you run `./02-kind-cluster/setup-cluster.sh` from a different folder, `${SCRIPT_DIR}/kind-config.yaml` still finds `kind-config.yaml`.

---

## 3. Step 1: Start Local OCI Registry (`lines 9–15`)

```bash
if [ "$(docker inspect -f '{{.State.Running}}' "${REG_NAME}" 2>/dev/null || true)" != "true" ]; then
  echo "Starting local OCI registry (${REG_NAME} on localhost:${REG_PORT})..."
  docker run -d --restart=always -p "127.0.0.1:${REG_PORT}:5000" --network bridge --name "${REG_NAME}" registry:2
else
  echo "Local OCI registry (${REG_NAME}) is already running."
fi
```

* **`docker inspect -f '{{.State.Running}}' ... 2>/dev/null || true`** — Checks whether `kind-registry` is currently running.
  * `2>/dev/null`: Hides the "No such object" error if the container doesn't exist yet.
  * `|| true`: Prevents `set -e` from aborting the script when `docker inspect` fails on a fresh machine.
* **`docker run ... registry:2`** — Starts the official Docker Registry v2 container:
  * `-d`: Detached (background).
  * `--restart=always`: Automatically starts the registry again if Docker or your PC restarts.
  * `-p "127.0.0.1:${REG_PORT}:5000"`: Maps **only `127.0.0.1:5001`** (not `0.0.0.0`) to container port `5000`, so the registry is only reachable from your own machine.
  * `--network bridge`: Attaches it to Docker's default bridge network initially.
  * `--name "kind-registry"`: Gives it the fixed container name `kind-registry`.

---

## 4. Step 2: Create the Multi-Node `kind` Cluster (`lines 17–23`)

```bash
if ! kind get clusters | grep -qx "${CLUSTER_NAME}"; then
  echo "Creating kind cluster '${CLUSTER_NAME}' (1 control-plane + 2 workers)..."
  kind create cluster --config "${SCRIPT_DIR}/kind-config.yaml"
else
  echo "kind cluster '${CLUSTER_NAME}' already exists."
fi
```

* **`kind get clusters | grep -qx "${CLUSTER_NAME}"`** — Checks if `prod-k8s` already exists:
  * `-q`: Quiet (no output, just exit code 0 if found, 1 if not).
  * `-x`: Exact full-line match (so `prod-k8s-2` wouldn't falsely match `prod-k8s`).
* **`kind create cluster --config "${SCRIPT_DIR}/kind-config.yaml"`** — Reads `kind-config.yaml` and creates the 3 node containers (`prod-k8s-control-plane`, `prod-k8s-worker`, `prod-k8s-worker2`) and configures your `kubectl` context.

---

## 5. Step 3: Configure `containerd` on Every Node (`lines 25–32`)

```bash
REGISTRY_DIR="/etc/containerd/certs.d/localhost:${REG_PORT}"
for node in $(kind get nodes --name "${CLUSTER_NAME}"); do
  docker exec "${node}" mkdir -p "${REGISTRY_DIR}"
  cat <<EOF | docker exec -i "${node}" tee "${REGISTRY_DIR}/hosts.toml" >/dev/null
[host."http://${REG_NAME}:5000"]
EOF
done
```

* **`for node in $(kind get nodes --name "${CLUSTER_NAME}")`** — Loops through all 3 node containers.
* **`docker exec "${node}" mkdir -p "${REGISTRY_DIR}"`** — Creates `/etc/containerd/certs.d/localhost:5001` inside each node.
* **`cat <<EOF | docker exec -i "${node}" tee "${REGISTRY_DIR}/hosts.toml" >/dev/null`** — Writes `hosts.toml` inside each node:
  ```toml
  [host."http://kind-registry:5000"]
  ```
  * **Why `-i` on `docker exec`?** Keeps standard input (`stdin`) open so the piped heredoc (`<<EOF ... EOF`) can be written into `tee`.
  * **Why `>/dev/null`?** `tee` prints to both the file and stdout; redirecting stdout to `/dev/null` keeps terminal output clean.
  * **Why this is needed:** From **your host**, you push to `localhost:5001`. Inside a **kind node**, `localhost` means the node itself—not your host! This tells `containerd` on each node: *"When a Pod asks for `localhost:5001/...`, actually pull from `http://kind-registry:5000` over plain HTTP."*

---

## 6. Step 4: Connect Registry to the `kind` Docker Network (`lines 34–37`)

```bash
if [ "$(docker inspect -f='{{json .NetworkSettings.Networks.kind}}' "${REG_NAME}")" = "null" ]; then
  docker network connect "kind" "${REG_NAME}"
fi
```

* **`docker inspect -f='{{json .NetworkSettings.Networks.kind}}' "${REG_NAME}"`** — Checks if `kind-registry` is attached to the `kind` Docker network. If not, `docker inspect` prints `null`.
* **`docker network connect "kind" "${REG_NAME}"`** — Connects `kind-registry` to the `kind` network so all 3 Kubernetes nodes can reach `http://kind-registry:5000` by container name (Docker DNS).
* **Without this:** The nodes and registry would be on separate Docker networks and image pulls would fail with connection/DNS errors.

---

## 7. Step 5: Document Registry in Kubernetes (`lines 39–50`)

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:${REG_PORT}"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF
```

* **`kubectl apply -f -`** — Reads the YAML from standard input (`-`) and creates/updates a `ConfigMap` in Kubernetes.
* **`local-registry-hosting` in `kube-public`** — Follows the official Kubernetes standard (**KEP-1755**). It advertises `localhost:5001` so tools like Tilt, Skaffold, or IDE plugins automatically know a local registry is available.

---

## 8. Final Status Output (`lines 52–54`)

```bash
echo ""
echo "Done! Cluster status:"
kubectl get nodes -o wide
```

Prints a blank line, a `"Done! Cluster status:"` message, and runs `kubectl get nodes -o wide` so you immediately see all 3 nodes (`prod-k8s-control-plane`, `prod-k8s-worker`, `prod-k8s-worker2`) in `Ready` state.
