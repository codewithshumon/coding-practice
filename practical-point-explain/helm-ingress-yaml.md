# `templates/ingress.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/ingress.yaml`

## Short Summary (TL;DR)
* **What this file does:** Conditionally (`{{- if .Values.ingress.enabled }}`) creates 1 `Ingress` (`{{ .Release.Name }}-ingress`) with NGINX annotations (`rewrite-target: /$2`, `ssl-redirect: "true"`, `limit-rps` with `| quote`), TLS (`host` + `tlsSecretName`), and a `range` loop **inside `paths:`** that maps every service's `path` (`/node`, `/python`, `/go`) to its `Service` and `port`.
* **Why it is needed:** Allows `dev`, `staging`, and `prod` to use different domains, TLS secrets, and rate limits via `values.yaml`, while automatically adding new microservice routes to the single edge `Ingress`.
* **Real-world production example:** One chart deploys `api.staging.company.com` (with `limit-rps: "50"`) and `api.company.com` (with `limit-rps: "10"`) behind NGINX Ingress + Let's Encrypt TLS.

---

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-ingress
  labels:
    {{- include "polyglot-api.labels" . | nindent 4 }}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/limit-rps: {{ .Values.ingress.limitRps | quote }}
spec:
  ingressClassName: {{ .Values.ingress.className }}
  tls:
    - hosts:
        - {{ .Values.ingress.host }}
      secretName: {{ .Values.ingress.tlsSecretName }}
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          {{- range $name, $svc := .Values.services }}
          - path: {{ $svc.path }}(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: {{ $name }}
                port:
                  number: {{ $svc.port }}
          {{- end }}
{{- end }}
```

---

## Line-by-Line Breakdown

### Line 1: `{{- if .Values.ingress.enabled }}`
* **What it means:** Feature toggle from `values.yaml`. If `ingress.enabled: false` (e.g., for an internal-only cluster or unit test), Helm skips creating the `Ingress` completely.

### Lines 2–3: `apiVersion: networking.k8s.io/v1` / `kind: Ingress`
* Creates a standard Kubernetes `Ingress` (HTTP/HTTPS edge router).

### Lines 4–7: `metadata:` / `name` / `labels`
* **`name: {{ .Release.Name }}-ingress`** — Names the Ingress dynamically (e.g., `polyglot-api-ingress`). Uses `.` (not `$`) because we are at the top-level root scope, not inside a `range` loop yet.
* **`{{- include "polyglot-api.labels" . | nindent 4 }}`** — Inserts standard Helm labels from `_helpers.tpl`, indented 4 spaces.

### Lines 8–11: `annotations:`
* **`nginx.ingress.kubernetes.io/rewrite-target: /$2`** — Strips the path prefix (`/node`, `/python`, `/go`) before forwarding to the backend Service.
* **`nginx.ingress.kubernetes.io/ssl-redirect: "true"`** — Forces HTTP (`:80`) $\rightarrow$ HTTPS (`:443`) redirect.
* **`nginx.ingress.kubernetes.io/limit-rps: {{ .Values.ingress.limitRps | quote }}`** — Sets per-IP rate limiting (requests per second) from `values.yaml`.
  * **Why `| quote`?** In `values.yaml`, `limitRps` is a number (e.g., `10`). Kubernetes `annotations` **must be strings**, not numbers! `| quote` converts `10` $\rightarrow$ `"10"`.
  * **Without `| quote`:** Kubernetes rejects the manifest with an error because `10` is an integer instead of a string.

### Lines 12–17: `spec:` / `ingressClassName` / `tls`
* **`ingressClassName: {{ .Values.ingress.className }}`** — Selects the Ingress Controller (`nginx`, `alb`, `traefik`, etc.) from `values.yaml`.
* **`tls:`**
  * **`hosts:` / `- {{ .Values.ingress.host }}`** — Domain name from `values.yaml` (e.g., `api.localtest.me` locally, `api.staging.company.com` in staging, `api.company.com` in prod).
  * **`secretName: {{ .Values.ingress.tlsSecretName }}`** — Name of the TLS `Secret` (`api-tls-secret`) holding `tls.crt` and `tls.key`.

### Lines 18–21: `rules:` / `- host:` / `http:` / `paths:`
* **`host: {{ .Values.ingress.host }}`** — Routes incoming requests matching that domain name.

### Lines 22–30: Looping Inside `paths:`
```yaml
          {{- range $name, $svc := .Values.services }}
          - path: {{ $svc.path }}(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: {{ $name }}
                port:
                  number: {{ $svc.port }}
          {{- end }}
```
* **`range $name, $svc := .Values.services`** — Notice this `range` is **inside `paths:`** (unlike `deployments.yaml`, where `range` wrapped the whole resource)!
  * **Why?** We want **1 single `Ingress`** with **3 path entries**, not 3 separate `Ingress` objects.
* **`- path: {{ $svc.path }}(/|$)(.*)`** — Builds the regex path from `values.yaml` (e.g., `/node(/|$)(.*)`, `/python(/|$)(.*)`, `/go(/|$)(.*)`).
* **`pathType: ImplementationSpecific`** — Required for NGINX regex paths.
* **`backend.service.name: {{ $name }}`** & **`port.number: {{ $svc.port }}`** — Routes each path to the matching `Service` (`node-api:3000`, `python-api:5000`, `go-api:8080`).
* **Line 30 (`{{- end }}`):** Closes the `range` loop.

### Line 31: `{{- end }}`
* Closes the outer `if .Values.ingress.enabled` block.
