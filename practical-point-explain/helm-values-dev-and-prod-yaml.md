# `values-dev.yaml` & `values-prod.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source files:
* `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/values-dev.yaml`
* `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/values-prod.yaml`

## Short Summary (TL;DR)
* **What these files do:** They are **environment-specific override files** passed to Helm via `-f values-dev.yaml` or `-f values-prod.yaml`. Helm **deep-merges** only the fields listed here on top of the base `values.yaml` (which still provides `image`, `tag`, `port`, `path`, `resources`, `ingress.enabled`, and `ingress.className`).
* **Why they are needed:** You never want to maintain duplicate copies of Kubernetes templates for `dev` vs `prod`. With override files, **one Helm chart** deploys a lightweight, cheap setup in `dev` (`replicas: 1`, no HPA, no PDB, higher `limitRps: "50"`, `dev-api.localtest.me`) and a resilient, auto-scaling setup in `prod` (`replicas: 2`, HPA `2–5` at `70%` CPU, PDB `minAvailable: 1`, strict `limitRps: "10"`, `api.localtest.me`).
* **Real-world production example:** A CI/CD pipeline (GitHub Actions / Argo CD) deploys the exact same `polyglot-api` chart to `dev` (`helm upgrade --install ... -n dev -f values-dev.yaml`) and `prod` (`helm upgrade --install ... -n prod -f values-prod.yaml`), guaranteeing dev and prod share identical structure while tuning scale, domains, and safety controls per environment.

---

## Exact Files

### `values-dev.yaml`
```yaml
ingress:
  host: dev-api.localtest.me
  tlsSecretName: dev-api-tls-secret
  limitRps: "50"

pdb:
  enabled: false

hpa:
  enabled: false

services:
  node-api:
    replicas: 1
  python-api:
    replicas: 1
  go-api:
    replicas: 1
```

### `values-prod.yaml`
```yaml
ingress:
  host: api.localtest.me
  tlsSecretName: api-tls-secret
  limitRps: "10"

pdb:
  enabled: true
  minAvailable: 1

hpa:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70

services:
  node-api:
    replicas: 2
  python-api:
    replicas: 2
  go-api:
    replicas: 2
```

---

## Side-by-Side Comparison (`dev` vs `prod`)

| Setting | `values-dev.yaml` | `values-prod.yaml` | Why Different? |
| :--- | :--- | :--- | :--- |
| `ingress.host` | `dev-api.localtest.me` | `api.localtest.me` | Separate domain per environment |
| `ingress.tlsSecretName` | `dev-api-tls-secret` | `api-tls-secret` | Separate TLS certificate Secret per environment |
| `ingress.limitRps` | `"50"` | `"10"` | `dev` allows bursty load testing; `prod` enforces strict rate limiting |
| `pdb.enabled` | `false` | `true` (`minAvailable: 1`) | In `dev` (`replicas: 1`), a PDB would block node drains; `prod` needs HA |
| `hpa.enabled` | `false` | `true` (`2`–`5` @ `70%` CPU) | `dev` stays at 1 Pod to save cost; `prod` auto-scales under traffic |
| `services.*.replicas` | `1` | `2` | `dev` needs 1 copy; `prod` needs 2+ for zero-downtime & HA |

---

## Line-by-Line Breakdown

### 1. `ingress:` (`lines 1–4` in both files)
* **`host:`** — Overrides `.Values.ingress.host` in `templates/ingress.yaml` (`dev-api.localtest.me` vs `api.localtest.me`).
  * *Real-world production example:* `api.dev.company.com` vs `api.company.com`.
* **`tlsSecretName:`** — Overrides `.Values.ingress.tlsSecretName` (`dev-api-tls-secret` vs `api-tls-secret`). Each namespace/domain has its own TLS cert Secret.
* **`limitRps:`** — Overrides `.Values.ingress.limitRps` (`"50"` in dev so QA/load-tests aren't throttled easily vs `"10"` in prod to protect backend APIs).

### 2. `pdb:` (`lines 6–7` in dev; `lines 6–8` in prod)
* **`enabled: false` (`dev`)** — `templates/pdb.yaml` checks `{{- if .Values.pdb.enabled }}`, so **0** `PodDisruptionBudget` objects are created in `dev`.
  * *Why:* With `replicas: 1` in `dev`, a PDB with `minAvailable: 1` would make `kubectl drain` hang forever during node maintenance.
* **`enabled: true` + `minAvailable: 1` (`prod`)** — Creates `node-api-pdb`, `python-api-pdb`, and `go-api-pdb`, guaranteeing at least 1 Pod stays `Ready` during node upgrades.

### 3. `hpa:` (`lines 9–10` in dev; `lines 10–14` in prod)
* **`enabled: false` (`dev`)** — `templates/hpa.yaml` skips creating any `HorizontalPodAutoscaler` in `dev` (saves CPU/memory and keeps behavior predictable for debugging).
* **`enabled: true` (`prod`)** — Creates HPAs for all 3 services:
  * **`minReplicas: 2`:** Never drop below 2 Pods.
  * **`maxReplicas: 5`:** Cap at 5 Pods to protect cluster quota and cloud bill.
  * **`targetCPUUtilizationPercentage: 70`:** Scale up when average CPU exceeds 70% of `requests.cpu`.

### 4. `services:` (`lines 12–18` in dev; `lines 16–22` in prod)
* **`node-api.replicas` / `python-api.replicas` / `go-api.replicas`:**
  * **`1` in `dev`:** Minimal footprint (3 total Pods instead of 6).
  * **`2` in `prod`:** High availability across `prod-k8s-worker` and `prod-k8s-worker2` + zero-downtime rolling updates.
* **How deep-merging works:** Notice `image`, `tag`, `port`, `path`, and `resources` are **not** repeated here—Helm automatically keeps them from the base `values.yaml` and only overrides `replicas`!
