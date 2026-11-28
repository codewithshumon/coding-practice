# `templates/pdb.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/pdb.yaml`

```yaml
{{- if .Values.pdb.enabled }}
{{- range $name, $svc := .Values.services }}
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ $name }}-pdb
  labels:
    app: {{ $name }}
    {{- include "polyglot-api.labels" $ | nindent 4 }}
spec:
  minAvailable: {{ $.Values.pdb.minAvailable }}
  selector:
    matchLabels:
      app: {{ $name }}
{{- end }}
{{- end }}
```

---

## Line-by-Line Breakdown

### Line 1: `{{- if .Values.pdb.enabled }}`
* **What it means:** Feature toggle from `values.yaml`.
  * If `pdb.enabled: true`, Helm creates a `PodDisruptionBudget` for each service.
  * If `pdb.enabled: false`, Helm skips this entire file.
* **Real-world production example:** In `values-dev.yaml` (where apps often run with `replicas: 1`), teams set `pdb.enabled: false` because a PDB with `minAvailable: 1` on a 1-replica app would **block** cluster upgrades (`kubectl drain` would hang forever). In `values-prod.yaml` (where `replicas >= 2`), `pdb.enabled: true` protects availability.

### Line 2: `{{- range $name, $svc := .Values.services }}`
* **What it means:** Loops over every service (`node-api`, `python-api`, `go-api`) in `values.yaml`, generating 1 PDB per service (`node-api-pdb`, `python-api-pdb`, `go-api-pdb`).

### Line 3: `---`
* **What it means:** YAML document separator before each generated `PodDisruptionBudget`.

### Lines 4–5: `apiVersion: policy/v1` / `kind: PodDisruptionBudget`
* **`policy/v1`:** Stable Kubernetes policy API group.
* **`PodDisruptionBudget` (PDB):** Protects your application during **voluntary disruptions** (node OS upgrades, `kubectl drain`, cluster autoscaler scale-downs).

### Lines 6–10: `metadata:`
* **`name: {{ $name }}-pdb`** — Names each PDB `node-api-pdb`, `python-api-pdb`, `go-api-pdb`.
* **`labels:`**
  * **`app: {{ $name }}`** — Tags the PDB with the service name.
  * **`{{- include "polyglot-api.labels" $ | nindent 4 }}`** — Inserts standard Helm labels from `_helpers.tpl` using `$` (root context, since we are inside `range`) and indents 4 spaces.

### Lines 11–15: `spec:`
* **`minAvailable: {{ $.Values.pdb.minAvailable }}`** — Minimum number of Pods that must stay `Ready` at all times during voluntary disruptions (e.g., `1`). Uses `$` because we are inside `range`.
  * *Real-world production example:* During an EKS/GKE worker node upgrade, Kubernetes drains one node at a time and refuses to evict the last healthy `node-api` Pod until another replica is `Ready` on a healthy node.
* **`selector.matchLabels.app: {{ $name }}`** — Tells the PDB which Pods it protects (all Pods with `app: node-api`, `app: python-api`, or `app: go-api`).

### Lines 16–17: `{{- end }}` / `{{- end }}`
* **Line 16 (`{{- end }}`):** Closes the `range` loop.
* **Line 17 (`{{- end }}`):** Closes the `if .Values.pdb.enabled` conditional.
