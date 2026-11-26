#!/usr/bin/env bash
set -euo pipefail

CLUSTER_NAME="prod-k8s"
REG_NAME="kind-registry"
REG_PORT="5001"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Start local OCI registry (simulates AWS ECR / Azure ACR / GCP Artifact Registry)
if [ "$(docker inspect -f '{{.State.Running}}' "${REG_NAME}" 2>/dev/null || true)" != "true" ]; then
  echo "Starting local OCI registry (${REG_NAME} on localhost:${REG_PORT})..."
  docker run -d --restart=always -p "127.0.0.1:${REG_PORT}:5000" --network bridge --name "${REG_NAME}" registry:2
else
  echo "Local OCI registry (${REG_NAME}) is already running."
fi

# 2. Create multi-node kind cluster if it doesn't exist
if ! kind get clusters | grep -qx "${CLUSTER_NAME}"; then
  echo "Creating kind cluster '${CLUSTER_NAME}' (1 control-plane + 2 workers)..."
  kind create cluster --config "${SCRIPT_DIR}/kind-config.yaml"
else
  echo "kind cluster '${CLUSTER_NAME}' already exists."
fi

# 3. Configure containerd on every node to route localhost:5001 -> kind-registry:5000
REGISTRY_DIR="/etc/containerd/certs.d/localhost:${REG_PORT}"
for node in $(kind get nodes --name "${CLUSTER_NAME}"); do
  docker exec "${node}" mkdir -p "${REGISTRY_DIR}"
  cat <<EOF | docker exec -i "${node}" tee "${REGISTRY_DIR}/hosts.toml" >/dev/null
[host."http://${REG_NAME}:5000"]
EOF
done

# 4. Connect registry to the kind Docker network
if [ "$(docker inspect -f='{{json .NetworkSettings.Networks.kind}}' "${REG_NAME}")" = "null" ]; then
  docker network connect "kind" "${REG_NAME}"
fi

# 5. Document local registry inside kube-public (standard KEP-1755)
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

echo ""
echo "Done! Cluster status:"
kubectl get nodes -o wide
