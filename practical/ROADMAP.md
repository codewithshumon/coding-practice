# Senior DevOps Engineer — Real-World Cloud Production Roadmap

**Target:** AWS EKS / Azure AKS / GCP GKE production practices  
**Local Engine:** `kind` (upstream `k8s`) + Local Registry + LocalStack (AWS)  
**Strict Rules:**
- **No `docker run` or `docker compose` to run apps or services.**
- **CI (GitHub Actions / Jenkins)** runs the pipeline, and **BuildKit** builds & pushes the image inside it.
- Everything runs **inside Kubernetes (`kind`)** just like real cloud production.
- **One step at a time.**

---

## Steps

- [x] **Step 1: Production Container Images (`Dockerfile`s)** — Multi-stage, non-root, minimal/distroless images for `node-api`, `python-api`, `go-api`
- [x] **Step 2: Kubernetes (`kind`) Cluster + Local Registry** — Multi-node upstream `k8s` (`1 control-plane + 2 workers`) + local OCI registry (simulating ECR/ACR/Artifact Registry)
- [x] **Step 3: NGINX Ingress Controller + TLS + Production Primitives** — Deploy `node-api`, `python-api`, `go-api` in `kind` with NGINX Ingress, TLS, namespaces, RBAC, probes, resource limits, HPA, NetworkPolicy, PDB
- [x] **Step 4: Helm Packaging** — Production chart for the 3 services (`values-dev.yaml` / `values-prod.yaml`), upgrades & rollbacks
- [ ] **Step 5: GitOps with Argo CD** — Pull-based deployment in `kind`, auto-sync, self-heal, drift detection
- [ ] **Step 6: CI/CD with GitHub Actions / Jenkins + BuildKit** — Test, scan (Trivy), BuildKit build & push image, update GitOps repo
- [ ] **Step 7: Terraform + Cloud (AWS via LocalStack)** — Modular IaC, state management, IAM least privilege, VPC, EKS/AKS/GKE patterns
- [ ] **Step 8: Ansible** — Idempotent Linux hardening & config management
- [ ] **Step 9: Production Observability (Prometheus + Grafana + Loki)** — Running inside `kind` for metrics, alerts, and logs
- [ ] **Step 10: Secrets & Zero-Trust Security** — Sealed Secrets / Vault, TLS rotation, Pod Security Standards
