# Real-World Cloud Production Practice Rules

1. **Production Target:** All practical exercises must follow **real-world cloud production best practices** (AWS EKS, Azure AKS, GCP GKE), simulated locally using **`kind`** (upstream Kubernetes in Docker).
2. **No `docker run` / `docker compose` for Running Services:**
   - **NEVER** use `docker run` or `docker compose` to run applications, Nginx, databases, or monitoring tools.
   - **CI (GitHub Actions / Jenkins)** runs the pipeline, and **BuildKit** builds & pushes the OCI image inside it (daemonless/rootless in Kubernetes). Docker on the host is only the node runtime for `kind` and the local registry.
   - Everything (apps, NGINX Ingress Controller, Argo CD, Prometheus, Grafana, Loki, Secrets) runs **inside Kubernetes (`kind`)**, just like EKS/AKS/GKE.
3. **Polyglot Services:** Practice with all 3 services (`node-api`, `python-api`, `go-api`) inside `practical/01-production-docker/`.
4. **Locked-In Production Stack (No Confusing Menus of Alternatives):**
   - **Image Build & Push:** **BuildKit** (from `Dockerfile`s: multi-stage, non-root, minimal/distroless, `.dockerignore`)
   - **Kubernetes:** `kind` (multi-node upstream `k8s`)
   - **Ingress / Edge:** NGINX Ingress Controller + TLS
   - **Packaging:** Helm
   - **CD / GitOps:** Argo CD
   - **CI:** GitHub Actions / Jenkins (orchestrating the pipeline + BuildKit)
   - **Cloud & IaC:** Terraform + LocalStack (AWS)
   - **Config Management:** Ansible
   - **Observability:** Prometheus + Grafana + Loki
   - **Security & Secrets:** RBAC, NetworkPolicies, Pod Security Standards, Sealed Secrets / Vault
5. **Step-by-Step Rule:**
   - Work **strictly one step at a time**. Never jump ahead or combine multiple steps.
   - For every step, create or update files inside `/home/shumon/Documents/coding-practice/practical/`.
