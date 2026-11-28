# `templates/deployments.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/deployments.yaml`

## Short Summary (TL;DR)
* **What this file does:** Uses a Helm `range` loop over `.Values.services` to dynamically generate hardened `Deployment` manifests for all microservices (`node-api`, `python-api`, `go-api`), injecting replicas, `image:tag`, ports, `toYaml` resources, `RollingUpdate` (`maxUnavailable: 0`, `maxSurge: 1`), `restricted` securityContext, and `/health` readiness/liveness probes from `values.yaml`.
* **Why it is needed:** Eliminates duplicating hundreds of lines of Deployment YAML across services and environments (`dev`/`staging`/`prod`), while letting CI/CD bump image tags with `--set` or separate `values-*.yaml` files.
* **Real-world production example:** A platform team maintains 1 Helm chart for 10 microservices; deploying a new release to `prod` is just `helm upgrade --set services.node-api.tag=1.0.5` with zero-downtime rolling updates.

---

Instead of copy-pasting 3 separate `Deployment` files (`node-api`, `python-api`, `go-api`), this single Helm template **loops over `.Values.services`** from `values.yaml` and generates all 3 `Deployment` manifests dynamically!

---

## Line-by-Line Breakdown

### Line 1: `{{- range $name, $svc := .Values.services }}`
* **`range`** — A Helm/Go template loop (like `for` in Python/JS) that iterates over a map or list.
* **`$name, $svc := .Values.services`** — Loops over every entry under `services:` in `values.yaml`:
  * **`$name`** receives the map key (`node-api`, `python-api`, `go-api`).
  * **`$svc`** receives that service's nested settings (`replicas`, `image`, `tag`, `port`, `resources`, etc.).
* **Real-world production example:** If your company adds a 4th microservice (`billing-api`), you only add 8 lines to `values.yaml`—you never duplicate Deployment YAML!

### Line 2: `---`
* **What it means:** YAML document separator printed at the start of each loop iteration, so the 3 generated `Deployment` objects are valid multi-document YAML.

### Lines 3–9: Header & Metadata
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ $name }}
  labels:
    app: {{ $name }}
    {{- include "polyglot-api.labels" $ | nindent 4 }}
```
* **`apiVersion: apps/v1`** & **`kind: Deployment`** — Standard Kubernetes Deployment resource.
* **`name: {{ $name }}`** — Renders `name: node-api`, `name: python-api`, `name: go-api`.
* **`app: {{ $name }}`** — Labels each Deployment with its service name.
* **`{{- include "polyglot-api.labels" $ | nindent 4 }}`** — Calls the helper template from `_helpers.tpl` and inserts the 3 standard Helm labels:
  * **Why `$` instead of `.`?** Inside a `range` loop, `.` changes to the current loop item. **`$` always points to the root Helm context** (which holds `.Release` and `.Chart`). Without `$`, `_helpers.tpl` would fail trying to read `.Release.Service`!
  * **`| nindent 4`** — Adds a **n**ewline and **indent**s every line of the output by **4 spaces** so it aligns cleanly under `labels:`.

### Lines 10–14: Replicas & Pod Selector
* **`replicas: {{ $svc.replicas }}`** — Pulls replica count from `values.yaml` (e.g., `1` in `dev`, `2` or `5` in `prod`).
* **`selector.matchLabels.app: {{ $name }}`** — Tells the Deployment to manage Pods labeled `app: node-api` (etc.).

### Lines 15–19: Zero-Downtime Rollout Strategy
* **`type: RollingUpdate`** / **`maxUnavailable: 0`** / **`maxSurge: 1`** — Replaces Pods one by one with zero downtime (spins up 1 new Pod, waits for `readinessProbe`, then stops 1 old Pod).

### Lines 20–29: Pod Template & Pod-Level Security
* **`template.metadata.labels.app: {{ $name }}`** — Labels each created Pod with its service name.
* **`serviceAccountName: {{ $.Release.Name }}-sa`** — Attaches the release-specific `ServiceAccount` (e.g., `prod-api-sa`).
  * Again, **`$.Release.Name`** uses `$` (root context) because we are inside `range`.
* **`securityContext:`** — `runAsNonRoot: true` + `seccompProfile.type: RuntimeDefault` (satisfies Pod Security `restricted`).

### Lines 30–34: Container Image & Port
* **`- name: {{ $name }}`** — Names the container (`node-api`, `python-api`, `go-api`).
* **`image: "{{ $svc.image }}:{{ $svc.tag }}"`** — Combines image repo and tag from `values.yaml` (e.g., `localhost:5001/node-api:1.0.0`).
  * *Real-world production example:* In CI/CD, you run `helm upgrade --set services.node-api.tag=1.0.5` to deploy a new version without editing YAML files!
* **`ports:` / `- containerPort: {{ $svc.port }}`** — Opens the service's port (`3000`, `5000`, `8080`).

### Lines 35–39: Container-Level Security
* **`allowPrivilegeEscalation: false`**, **`readOnlyRootFilesystem: true`**, **`capabilities.drop: ["ALL"]`** — Hardens every container against privilege escalation and disk tampering.

### Lines 40–41: Dynamic Resources Block
```yaml
          resources:
            {{- toYaml $svc.resources | nindent 12 }}
```
* **`toYaml $svc.resources`** — Converts the `resources:` dictionary from `values.yaml` (`requests` and `limits`) into raw YAML text.
* **`| nindent 12`** — Adds a newline and indents every line by **12 spaces** so it nests cleanly under `resources:`.
* *Real-world production example:* `values-dev.yaml` can give `go-api` `10m` CPU, while `values-prod.yaml` gives it `200m` CPU—using the exact same template.

### Lines 42–53: Health Probes
* **`readinessProbe`** (`path: /health`, `port: {{ $svc.port }}`, `initialDelaySeconds: 3`, `periodSeconds: 5`) — Controls when the Pod starts receiving traffic from its `Service`.
* **`livenessProbe`** (`path: /health`, `port: {{ $svc.port }}`, `initialDelaySeconds: 10`, `periodSeconds: 10`) — Restarts the container if `/health` keeps failing.

### Line 54: `{{- end }}`
* **What it means:** Closes the `range $name, $svc := .Values.services` loop (and `-` trims trailing whitespace).
