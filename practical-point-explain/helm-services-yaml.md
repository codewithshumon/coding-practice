# `templates/services.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/services.yaml`

## Short Summary (TL;DR)
* **What this file does:** Uses a Helm `range` loop over `.Values.services` to generate a Kubernetes `ClusterIP` `Service` for each microservice (`node-api:3000`, `python-api:5000`, `go-api:8080`) with `app: {{ $name }}` selectors and standard Helm labels (`polyglot-api.labels`).
* **Why it is needed:** Pod IPs are temporary and change every time a Pod restarts, scales, or rolls out a new version. A `Service` provides a **single stable internal IP + DNS name** (e.g., `node-api.prod.svc.cluster.local`) and automatically load-balances traffic only across **ready** Pods.
* **Real-world production example:** When `ingress.yaml` forwards `/node` to `node-api:3000`, or when `node-api` scales from 2 to 5 Pods under HPA, NGINX Ingress never needs to know the changing Pod IPs—it always talks to the `node-api` `Service`.

---

## Exact Template

```yaml
{{- range $name, $svc := .Values.services }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ $name }}
  labels:
    app: {{ $name }}
    {{- include "polyglot-api.labels" $ | nindent 4 }}
spec:
  selector:
    app: {{ $name }}
  ports:
    - port: {{ $svc.port }}
      targetPort: {{ $svc.port }}
{{- end }}
```

---

## Line-by-Line Breakdown

### Line 1: `{{- range $name, $svc := .Values.services }}`
* **What it means:** Loops over every service defined under `services:` in `values.yaml` (`$name` = `node-api`/`python-api`/`go-api`, `$svc` = that service's config map).
* **Real-world production example:** Adding a 4th service in `values.yaml` automatically creates its `Service` without touching `templates/services.yaml`.

### Line 2: `---`
* **What it means:** YAML document separator before each generated `Service` object.

### Lines 3–4: `apiVersion: v1` / `kind: Service`
* **`apiVersion: v1`:** Core stable Kubernetes API.
* **`kind: Service`:** A stable virtual IP, DNS entry, and Layer-4 load balancer sitting in front of a group of Pods.
* **Note on `type`:** Because `type:` is omitted, Kubernetes defaults to **`ClusterIP`** (internal-only inside the cluster—external traffic enters through NGINX `Ingress`).

### Lines 5–9: `metadata:`
* **`name: {{ $name }}`** — Creates internal DNS names `node-api`, `python-api`, and `go-api` (matching `backend.service.name` in `ingress.yaml`).
* **`labels:`**
  * **`app: {{ $name }}`** — Tags the `Service` with its app name.
  * **`{{- include "polyglot-api.labels" $ | nindent 4 }}`** — Inserts standard Helm labels from `_helpers.tpl` using `$` (root context, since we are inside `range`), indented 4 spaces.

### Lines 10–12: `spec:` / `selector:` / `app: {{ $name }}`
* **`selector.app: {{ $name }}`** — Tells the `Service`: *"Send traffic to all Pods that have label `app: node-api` (etc.) AND are passing their `readinessProbe`."*
* **Without a matching selector:** The `Service` has zero endpoints (`<none>`) and all requests to it fail with `503` / connection refused.

### Lines 13–15: `ports:` / `- port: {{ $svc.port }}` / `targetPort: {{ $svc.port }}`
* **`port: {{ $svc.port }}`** — The port the `Service` listens on inside the cluster (`3000`, `5000`, `8080`). Other services and `Ingress` connect to this port.
* **`targetPort: {{ $svc.port }}`** — The actual port inside the container (`containerPort`) where the app is listening.
* **Real-world production example:** You can expose `port: 80` on the `Service` while the container listens on `targetPort: 3000` (useful when a non-root container cannot bind to port `80`).

### Line 16: `{{- end }}`
* **What it means:** Closes the `range` loop (and `-` trims trailing whitespace).
