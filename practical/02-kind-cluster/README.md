# Step 2: `kind` Multi-Node Kubernetes Cluster + Local OCI Registry

This sets up a **3-node upstream Kubernetes (`k8s`) cluster** (`1 control-plane + 2 workers`) and a **local OCI registry (`localhost:5001`)** that simulates **AWS ECR / Azure ACR / GCP Artifact Registry**.

---

## 1. Install `kind` and `kubectl` (if not installed)

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm -f kubectl

# Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.27.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Verify both:

```bash
kubectl version --client
kind version
```

---

## 2. Create the Cluster + Local Registry

```bash
cd /home/shumon/Documents/coding-practice/practical/02-kind-cluster
chmod +x setup-cluster.sh
./setup-cluster.sh
```

---

## 3. Verify Your Cluster

```bash
kubectl get nodes -o wide
kubectl get pods -A
curl -s http://localhost:5001/v2/_catalog
```

You should see:

- **3 nodes** (`prod-k8s-control-plane`, `prod-k8s-worker`, `prod-k8s-worker2`) all in `Ready` state.
- Core K8s system pods (`coredns`, `etcd`, `kube-apiserver`, `kube-proxy`, `kindnet`) running in `kube-system`.
- `{"repositories":[]}` from `localhost:5001`.

---

## Next

Tell me **"done"** once all 3 nodes are `Ready`, and we'll move to **Step 3: NGINX Ingress Controller + TLS + Deploying `node-api`, `python-api`, `go-api`**.
