# `templates/_helpers.tpl` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/_helpers.tpl`

## Short Summary (TL;DR)
* **What this file does:** Defines a reusable Helm named template (`"polyglot-api.labels"`) that outputs 3 standard Kubernetes/Helm labels: `app.kubernetes.io/managed-by`, `helm.sh/chart`, and `app.kubernetes.io/instance`. The `_` filename prefix tells Helm it is a helper partial, not a K8s manifest.
* **Why it is needed:** Avoids copy-pasting identical metadata labels across every template file (`Deployment`, `Service`, `Ingress`, `HPA`, `PDB`) and keeps chart/release tracking consistent.
* **Real-world production example:** In a cluster managed by Helm, Terraform, and Argo CD, `managed-by: Helm` + `helm.sh/chart` lets on-call engineers immediately see which chart version owns a resource and prevents accidental manual `kubectl edit` changes.

---

```gotemplate
{{- define "polyglot-api.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
```

---

## First: Why is the file named `_helpers.tpl`?

* **Leading underscore (`_`)** — In Helm, any file inside `templates/` starting with `_` (like `_helpers.tpl`) is **NOT** rendered as a standalone Kubernetes YAML manifest. Instead, it holds reusable template snippets (like functions/partials) that other templates call.
  * *Without `_`*: Helm would try to send the file to `kubectl`/Kubernetes API as a YAML resource and fail.
* **`.tpl` extension** — Stands for **Go template** file (not pure YAML).

---

## Line-by-Line Breakdown

### Line 1: `{{- define "polyglot-api.labels" -}}`
* **`{{ ... }}`** — Helm/Go template delimiters (everything inside is evaluated by Helm, not literal YAML).
* **`{{-` and `-}}`** — The `-` trims whitespace/newlines before and after the tag so you don't get ugly blank lines in the final rendered YAML.
* **`define "polyglot-api.labels"`** — Declares a reusable named template block called `"polyglot-api.labels"`.
* **Real-world production example:** Instead of copy-pasting the same 3 metadata labels into 10 files (`Deployment`, `Service`, `Ingress`, `HPA`, `PDB`, `ServiceAccount`), you define them once here and call them everywhere with `{{- include "polyglot-api.labels" . | nindent 4 }}`.

---

### Line 2: `app.kubernetes.io/managed-by: {{ .Release.Service }}`
* **Key (`app.kubernetes.io/managed-by`):** A Kubernetes recommended standard label showing *which tool* manages this resource.
* **Value (`{{ .Release.Service }}`):** Built-in Helm variable that always evaluates to **`Helm`** when deployed with `helm install` / `helm upgrade`.
* **Real-world production example:** In a production cluster with Terraform, Argo CD, and Helm all creating resources, `app.kubernetes.io/managed-by: Helm` immediately tells engineers (and tools like Lens/Datadog) not to manually edit this object with `kubectl edit` because Helm owns it.

---

### Line 3: `helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}`
* **Key (`helm.sh/chart`):** Standard Helm label recording the exact chart name and version that created the resource.
* **Values:**
  * **`{{ .Chart.Name }}`** — Reads `name:` from `Chart.yaml` (e.g., `polyglot-api`).
  * **`{{ .Chart.Version }}`** — Reads `version:` from `Chart.yaml` (e.g., `0.1.0` or `1.2.0`).
  * Combined output: `helm.sh/chart: polyglot-api-0.1.0`.
* **Real-world production example:** During an outage, an on-call engineer runs `kubectl get deploy -n prod --show-labels` and instantly sees which exact Helm chart version (`polyglot-api-1.2.0`) is running in production.

---

### Line 4: `app.kubernetes.io/instance: {{ .Release.Name }}`
* **Key (`app.kubernetes.io/instance`):** Standard Kubernetes label identifying a specific deployment/installation instance of the application.
* **Value (`{{ .Release.Name }}`):** The release name you pass to `helm install <RELEASE_NAME> ...` (e.g., `prod-api` or `staging-api`).
* **Real-world production example:** If you install the same chart twice in a cluster—once as `helm install payments-api` and once as `helm install orders-api`—this label keeps their resources distinguishable (`kubectl get pods -l app.kubernetes.io/instance=payments-api`).

---

### Line 5: `{{- end -}}`
* **What it means:** Closes the `define "polyglot-api.labels"` block, with `{{-` and `-}}` trimming extra whitespace/newlines.

---

## What the Rendered Output Looks Like

When another template calls `{{- include "polyglot-api.labels" . | nindent 4 }}` (assuming `helm install my-api ./polyglot-api`), Helm renders:

```yaml
    app.kubernetes.io/managed-by: Helm
    helm.sh/chart: polyglot-api-0.1.0
    app.kubernetes.io/instance: my-api
```
