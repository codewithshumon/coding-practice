# `templates/hpa.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/hpa.yaml`

## Short Summary (TL;DR)
* **What this file does:** Conditionally (`{{- if .Values.hpa.enabled }}`) loops over `.Values.services` to generate a `HorizontalPodAutoscaler` (`autoscaling/v2`) for every service, using `minReplicas`, `maxReplicas`, and `targetCPUUtilizationPercentage` from `values.yaml`.
* **Why it is needed:** Lets you turn autoscaling **off** in `dev` (`hpa.enabled: false`) to save resources and **on** in `prod` (`hpa.enabled: true`) across all services from a single template.
* **Real-world production example:** Using the same Helm chart in `values-dev.yaml` (fixed 1 Pod, no HPA) and `values-prod.yaml` (auto-scaling 2–10 Pods at 70% CPU during peak traffic).

---

```yaml
{{- if .Values.hpa.enabled }}
{{- range $name, $svc := .Values.services }}
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ $name }}-hpa
  labels:
    app: {{ $name }}
    {{- include "polyglot-api.labels" $ | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ $name }}
  minReplicas: {{ $.Values.hpa.minReplicas }}
  maxReplicas: {{ $.Values.hpa.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ $.Values.hpa.targetCPUUtilizationPercentage }}
{{- end }}
{{- end }}
```

---

## Line-by-Line Breakdown

### Line 1: `{{- if .Values.hpa.enabled }}`
* **`if .Values.hpa.enabled`** — A Helm **conditional (feature toggle)** checking `hpa.enabled` in `values.yaml`.
  * If `hpa.enabled: true`: Helm renders the HPA manifests.
  * If `hpa.enabled: false`: Helm skips this entire file and creates **0** HPA objects in Kubernetes.
* **Real-world production example:** In `values-dev.yaml`, teams set `hpa.enabled: false` (you only want 1 fixed Pod in dev to save money); in `values-prod.yaml`, they set `hpa.enabled: true` so production auto-scales under load.

### Line 2: `{{- range $name, $svc := .Values.services }}`
* **What it means:** Loops over every service (`node-api`, `python-api`, `go-api`) defined under `services:` in `values.yaml`.
* **Real-world production example:** Automatically creates 1 HPA per microservice (`node-api-hpa`, `python-api-hpa`, `go-api-hpa`) without duplicating YAML.

### Line 3: `---`
* **What it means:** YAML document separator before each generated `HorizontalPodAutoscaler`.

### Lines 4–5: `apiVersion: autoscaling/v2` / `kind: HorizontalPodAutoscaler`
* **`autoscaling/v2`:** Stable Kubernetes autoscaling API.
* **`HorizontalPodAutoscaler`:** Automatically scales the number of Pod replicas up or down based on CPU/memory metrics (requires Metrics Server).

### Lines 6–10: `metadata:`
* **`name: {{ $name }}-hpa`** — Generates `node-api-hpa`, `python-api-hpa`, `go-api-hpa`.
* **`labels:`**
  * **`app: {{ $name }}`** — Tags each HPA with its service name.
  * **`{{- include "polyglot-api.labels" $ | nindent 4 }}`** — Inserts standard Helm labels from `_helpers.tpl` using `$` (root context) and indents 4 spaces.

### Lines 11–15: `spec:` / `scaleTargetRef:`
* **`scaleTargetRef:`** — Tells HPA *which* Kubernetes workload to scale:
  * **`apiVersion: apps/v1`** & **`kind: Deployment`** — Target is a `Deployment`.
  * **`name: {{ $name }}`** — Matches `node-api`, `python-api`, `go-api` from `deployments.yaml`.

### Lines 16–17: `minReplicas` & `maxReplicas`
* **`minReplicas: {{ $.Values.hpa.minReplicas }}`** — Minimum Pod count (e.g., `2` in prod so high availability is always kept). Uses `$` because we are inside `range`.
* **`maxReplicas: {{ $.Values.hpa.maxReplicas }}`** — Maximum Pod count (e.g., `5` or `10`) to cap cloud costs and protect cluster capacity during traffic spikes/DDoS.

### Lines 18–24: `metrics:`
* **`- type: Resource`** / **`resource.name: cpu`** — Scales based on CPU usage.
* **`target.type: Utilization`** & **`averageUtilization: {{ $.Values.hpa.targetCPUUtilizationPercentage }}`** — Target average CPU percentage relative to `resources.requests.cpu` (e.g., `70` = scale up when average CPU > 70% of `requests.cpu`).

### Lines 25–26: `{{- end }}` / `{{- end }}`
* **Line 25 (`{{- end }}`):** Closes the `range $name, $svc := .Values.services` loop.
* **Line 26 (`{{- end }}`):** Closes the outer `if .Values.hpa.enabled` block.
