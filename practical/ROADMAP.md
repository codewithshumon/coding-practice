# Senior DevOps Engineer — Production-Grade Local Practice Roadmap

**Environment:** Kali Linux (12 threads, 15 GiB RAM) + Docker + `kind` (upstream K8s) + LocalStack (AWS)  
**Rule:** Strictly one step at a time. Each step has its own folder/files inside `practical/`.

---

## Steps

- [x] **Step 1: Production Docker** — Multi-stage builds, non-root user, minimal image, `.dockerignore`, healthchecks, resource limits, Trivy image scan
- [ ] **Step 2: Linux & Nginx Production Reverse Proxy** — TLS/SSL termination, security headers, rate limiting, upstream health, log & port debugging
- [ ] **Step 3: Kubernetes (`kind`) Production Primitives** — Multi-node upstream `k8s`, NGINX Ingress, Namespaces, RBAC, probes, resource requests/limits, HPA, NetworkPolicy, PDB
- [ ] **Step 4: Helm Packaging** — Production chart structure, `values-dev.yaml` vs `values-prod.yaml`, rollbacks
- [ ] **Step 5: GitOps with Argo CD** — Pull-based deployment, auto-sync, self-heal, drift detection, App-of-Apps
- [ ] **Step 6: CI/CD Pipeline** — Lint, unit/integration tests, container scan, build & tag, GitOps manifest update (`act` / GitHub Actions / Jenkins)
- [ ] **Step 7: Terraform + Cloud (AWS via LocalStack, plus Azure & GCP mapping)** — Modular IaC, state management, IAM least privilege, VPC/networking, managed K8s (EKS / AKS / GKE)
- [ ] **Step 8: Ansible Configuration Management** — Idempotent playbooks, roles, Linux hardening against local container targets
- [ ] **Step 9: Production Observability (Prometheus, Grafana, Loki)** — Metrics, dashboards, alerting rules, centralized logging
- [ ] **Step 10: Secrets & Zero-Trust Security** — HashiCorp Vault / Sealed Secrets, JWT/OAuth2 flow, TLS rotation
