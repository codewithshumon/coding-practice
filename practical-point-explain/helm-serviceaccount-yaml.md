# `templates/serviceaccount.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/templates/serviceaccount.yaml`

## Short Summary (TL;DR)
* **What this file does:** Creates a dedicated, release-scoped Kubernetes `ServiceAccount` (`{{ .Release.Name }}-sa`) with `automountServiceAccountToken: false` and attaches standard Helm labels (`polyglot-api.labels`), which all Pods in `deployments.yaml` use via `serviceAccountName: {{ $.Release.Name }}-sa`.
* **Why it is needed:** By default, Kubernetes mounts the `default` ServiceAccount's API token into every Pod at `/var/run/secrets/kubernetes.io/serviceaccount/token`. Since web APIs (`node-api`, `python-api`, `go-api`) don't need to call the Kubernetes API, disabling token automounting follows least-privilege security and limits blast radius if an app is compromised.
* **Real-world production example:** In a production EKS/GKE cluster, an app with a Remote Code Execution (RCE) or path-traversal bug cannot read `/var/run/secrets/kubernetes.io/serviceaccount/token` to probe or attack the Kubernetes API—and if you later install the same chart twice (`payments` and `orders`), each release gets its own isolated `payments-sa` and `orders-sa`.

---

## Exact Template

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ .Release.Name }}-sa
  labels:
    {{- include "polyglot-api.labels" . | nindent 4 }}
automountServiceAccountToken: false
```

---

## Line-by-Line Breakdown

### Line 1: `apiVersion: v1`
* **What `apiVersion` means:** Tells Kubernetes which API schema version to use to validate this resource.
* **What `v1` means:** The core, stable Kubernetes API (where `ServiceAccount`, `Pod`, `Service`, and `Namespace` live).

### Line 2: `kind: ServiceAccount`
* **What `kind` means:** The type of Kubernetes object to create.
* **What `ServiceAccount` means:** A **Pod identity** inside Kubernetes (similar to an IAM role/user for an application instead of a human).
* **Real-world production example:** Every microservice or Helm release gets its own dedicated `ServiceAccount` instead of sharing `default`, so permissions, audits, and cloud IAM bindings (e.g., AWS IRSA / GCP Workload Identity) stay cleanly separated.

### Line 3: `metadata:`
* **What `metadata` means:** Identifying information about the object (`name`, `labels`, `annotations`).

### Line 4: `  name: {{ .Release.Name }}-sa`
* **What `name` means:** The unique name of this `ServiceAccount` inside the release's namespace.
* **What `{{ .Release.Name }}-sa` means:** Uses the Helm release name + `-sa` (e.g., `polyglot-api-sa`, `staging-api-sa`). Matches `serviceAccountName: {{ $.Release.Name }}-sa` in `deployments.yaml`.
* **Without `{{ .Release.Name }}`:** Installing the same Helm chart twice in the same namespace would fail with an `already exists` conflict.

### Lines 5–6: `  labels:` / `    {{- include "polyglot-api.labels" . | nindent 4 }}`
* **What it means:** Inserts the 3 standard Helm labels (`managed-by`, `helm.sh/chart`, `instance`) from `_helpers.tpl`, indented 4 spaces under `labels:`. (Uses `.` because we are at the root Helm context, not inside a `range` loop.)

### Line 7: `automountServiceAccountToken: false`
* **What `automountServiceAccountToken` means:** Controls whether Kubernetes automatically mounts a JWT API token inside Pods that use this `ServiceAccount`.
* **What `false` means:** **Do NOT mount** any Kubernetes API token into the Pod's filesystem.
* **Real-world production example:** If an attacker exploits a file-read vulnerability in `node-api` or `python-api`, `/var/run/secrets/kubernetes.io/serviceaccount/token` does not exist—so they cannot steal a cluster token.
* **Without it:** Defaults to `true`, mounting a Kubernetes API token into every container even when the app never talks to Kubernetes.
