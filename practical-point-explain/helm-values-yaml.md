# `values.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/values.yaml`

## Short Summary (TL;DR)
* **What this file does:** Provides the **default configuration values** (`.Values`) for the entire `polyglot-api` Helm chart—controlling `ingress` (`enabled`, `className`, `host`, `tlsSecretName`, `limitRps`), `pdb` (`enabled`, `minAvailable`), `hpa` (`enabled`, `minReplicas`, `maxReplicas`, `targetCPUUtilizationPercentage`), and the `services` map (`node-api`, `python-api`, `go-api` with `image`, `tag`, `port`, `path`, `replicas`, and `resources`).
* **Why it is needed:** Templates in `templates/` (`deployments.yaml`, `services.yaml`, `ingress.yaml`, `hpa.yaml`, `pdb.yaml`) are generic blueprints with placeholders like `{{ .Values.ingress.host }}` and `{{ $svc.tag }}`. `values.yaml` supplies the baseline defaults so `helm install` works out-of-the-box, while `-f values-dev.yaml`, `-f values-prod.yaml`, or `--set` only need to override what differs.
* **Real-world production example:** In CI/CD, `values.yaml` holds safe production-ready defaults, `-f values-prod.yaml` tunes environment-specific hosts/replicas, and GitHub Actions/Jenkins runs `helm upgrade --install ... --set services.node-api.tag=1.0.2` on every new build—Helm merges them in order: `values.yaml` $\rightarrow$ `-f` file $\rightarrow$ `--set` (highest priority).

---

## Exact File

```yaml
ingress:
  enabled: true
  className: nginx
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
    image: localhost:5001/node-api
    tag: "1.0.1"
    port: 3000
    path: /node
    replicas: 2
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 128Mi

  python-api:
    image: localhost:5001/python-api
    tag: "1.0.1"
    port: 5000
    path: /python
    replicas: 2
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 128Mi

  go-api:
    image: localhost:5001/go-api
    tag: "1.0.0"
    port: 8080
    path: /go
    replicas: 2
    resources:
      requests:
        cpu: 25m
        memory: 32Mi
      limits:
        cpu: 100m
        memory: 64Mi
```

---

## Line-by-Line Breakdown

### 1. `ingress:` (`lines 1–6`)
Feeds `.Values.ingress.*` in `templates/ingress.yaml`:
* **`enabled: true`** (`line 2`) — Turns on `Ingress` rendering by default (`{{- if .Values.ingress.enabled }}`).
* **`className: nginx`** (`line 3`) — Sets `spec.ingressClassName: nginx` so NGINX Ingress Controller handles routing.
* **`host: api.localtest.me`** (`line 4`) — Default domain for TLS and HTTP routing rules.
* **`tlsSecretName: api-tls-secret`** (`line 5`) — Kubernetes TLS `Secret` name holding `tls.crt` and `tls.key`.
* **`limitRps: "10"`** (`line 6`) — Default per-IP rate limit (`10` req/sec), quoted as a string for NGINX annotations.

### 2. `pdb:` (`lines 8–10`)
Feeds `.Values.pdb.*` in `templates/pdb.yaml`:
* **`enabled: true`** (`line 9`) — Enables `PodDisruptionBudget` creation for all services by default.
* **`minAvailable: 1`** (`line 10`) — Guarantees at least 1 Pod per service remains `Ready` during voluntary node drains/upgrades.

### 3. `hpa:` (`lines 12–16`)
Feeds `.Values.hpa.*` in `templates/hpa.yaml`:
* **`enabled: true`** (`line 13`) — Enables `HorizontalPodAutoscaler` creation for all services by default.
* **`minReplicas: 2`** (`line 14`) — Minimum Pod count (high availability floor).
* **`maxReplicas: 5`** (`line 15`) — Maximum Pod count (cost & quota ceiling).
* **`targetCPUUtilizationPercentage: 70`** (`line 16`) — Scales up when average CPU usage exceeds 70% of `requests.cpu`.

### 4. `services:` (`lines 18–59`)
A map of microservices looped over by `range $name, $svc := .Values.services` in `deployments.yaml`, `services.yaml`, `ingress.yaml`, `hpa.yaml`, and `pdb.yaml`:

* **Key (`node-api` / `python-api` / `go-api`)** — Becomes `$name` (used for `Deployment`, `Service`, `HPA`, `PDB`, and container names).
* **`image:`** — Container registry + image repository (e.g., `localhost:5001/node-api`; in AWS production: `<account>.dkr.ecr.../node-api`).
* **`tag:`** — Pinned image version (`"1.0.1"` for `node-api` & `python-api`, `"1.0.0"` for `go-api`), quoted so YAML doesn't misparse numeric-looking tags.
* **`port:`** — Used in 4 places across templates: `containerPort`, readiness/liveness probe `port`, `Service` `port`/`targetPort`, and `Ingress` backend `port.number`.
* **`path:`** — URL prefix in `ingress.yaml` (`/node`, `/python`, `/go`), combined with `(/|$)(.*)`.
* **`replicas:`** — Default Pod replica count (`2` for HA).
* **`resources:`** — Rendered via `toYaml` in `deployments.yaml`:
  * `node-api` & `python-api`: `requests` (`50m` CPU, `64Mi` RAM) / `limits` (`200m` CPU, `128Mi` RAM).
  * `go-api`: `requests` (`25m` CPU, `32Mi` RAM) / `limits` (`100m` CPU, `64Mi` RAM) — half the footprint because compiled Go binaries are lightweight.
