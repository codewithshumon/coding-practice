# `04-hpa-and-rbac.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps/04-hpa-and-rbac.yaml`

This file uses `---` separators to define **3 production scaling and access-control resources**:
1. `HorizontalPodAutoscaler` (`node-api-hpa`) — Automatic Pod scaling based on CPU usage
2. `Role` (`prod-readonly`) — Least-privilege read-only permissions inside `prod`
3. `RoleBinding` (`prod-readonly-binding`) — Attaches that `Role` to a subject (`ServiceAccount`)

---

## Block 1: `HorizontalPodAutoscaler` (`lines 1–19`)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: node-api-hpa
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: node-api
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Line 1: `apiVersion: autoscaling/v2`
* **What `apiVersion` means:** The Kubernetes API group and version.
* **What `autoscaling/v2` means:** The modern stable autoscaling API (supports multiple metrics like CPU, memory, and custom Prometheus metrics, unlike older `v1`).

### Line 2: `kind: HorizontalPodAutoscaler`
* **What `kind` means:** Object type.
* **What `HorizontalPodAutoscaler` (HPA) means:** Automatically **increases or decreases the number of Pods** (`replicas`) in a Deployment based on live traffic/resource load.
* **Real-world production example:** During Black Friday or a morning traffic spike, HPA scales `node-api` from 2 Pods up to 5 Pods automatically; at 3 AM when traffic drops, it scales back down to 2 Pods to save cloud compute costs.
* **Prerequisite:** Requires **Metrics Server** running in the cluster (otherwise HPA shows `<unknown>` for CPU).

### Lines 3–5: `metadata:` / `  name: node-api-hpa` / `  namespace: prod`
* Names this autoscaler `node-api-hpa` inside the `prod` namespace (must be in the same namespace as the target Deployment).

### Lines 6–10: `spec:` / `scaleTargetRef:`
* **`scaleTargetRef:`** — Points to the exact Kubernetes object HPA should scale:
  * **`apiVersion: apps/v1`** — API version of `Deployment`.
  * **`kind: Deployment`** — Target type (`Deployment`, `StatefulSet`, etc.).
  * **`name: node-api`** — Target Deployment name.

### Lines 11–12: `minReplicas: 2` / `maxReplicas: 5`
* **`minReplicas: 2`** — HPA will **never** scale below 2 Pods (preserves high availability even at 0% traffic).
* **`maxReplicas: 5`** — HPA will **never** scale above 5 Pods (prevents runaway cloud bills or exhausting `prod-quota` during a DDoS attack).

### Lines 13–19: `metrics:` / `Resource` / `cpu` / `Utilization` / `averageUtilization: 70`
* **`type: Resource`** — Scale based on a built-in container resource (`cpu` or `memory`).
* **`resource.name: cpu`** — Monitor CPU usage.
* **`target.type: Utilization`** & **`averageUtilization: 70`** — Target **70% of `resources.requests.cpu`** averaged across all `node-api` Pods.
  * *Math in our setup:* `node-api` requests `50m` CPU per Pod. `70%` of `50m` = `35m`. If average CPU across the 2 Pods climbs to `70m` (`140%` utilization), HPA scales up to ~4 Pods (`140 / 70 * 2 = 4`) to bring average utilization back near 70%.
  * **Important gotcha:** HPA calculates utilization against `requests.cpu`, **not** `limits.cpu`. If `requests.cpu` is missing, HPA cannot calculate utilization!

---

## Block 2: `Role` (`lines 21–30`)

```yaml
# Least-privilege RBAC: read-only viewer role for developers in 'prod'
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: prod-readonly
  namespace: prod
rules:
  - apiGroups: ["", "apps", "networking.k8s.io"]
    resources: ["pods", "pods/log", "services", "deployments", "ingresses"]
    verbs: ["get", "list", "watch"]
```

### Line 22: `apiVersion: rbac.authorization.k8s.io/v1`
* **What it means:** The stable Kubernetes **RBAC** (Role-Based Access Control) API group.

### Line 23: `kind: Role`
* **What `Role` means:** A set of **namespace-scoped permissions** (what actions are allowed on which resources inside **one** namespace).
  * *(Compare with `ClusterRole`: `Role` only applies inside `prod`; `ClusterRole` applies cluster-wide across all namespaces.)*
* **Real-world production example:** Letting developers debug `prod` issues by viewing Pods and logs without giving them permission to `delete` Pods, read `Secrets`, or `exec` into containers.

### Lines 24–26: `metadata:` / `  name: prod-readonly` / `  namespace: prod`
* Names this permission set `prod-readonly` inside `prod`.

### Lines 27–30: `rules:`
* **`apiGroups: ["", "apps", "networking.k8s.io"]`** — Which Kubernetes API groups the resources belong to:
  * `""` (empty string) = Core API group (`pods`, `pods/log`, `services`)
  * `"apps"` = Apps API group (`deployments`)
  * `"networking.k8s.io"` = Networking API group (`ingresses`)
* **`resources: ["pods", "pods/log", "services", "deployments", "ingresses"]`** — Exact object types allowed.
  * Notice **`secrets`** and **`pods/exec`** are **excluded**! Even with this role, you cannot read database passwords/TLS keys (`secrets`) or open a shell (`kubectl exec`) inside `prod` Pods.
* **`verbs: ["get", "list", "watch"]`** — Read-only actions:
  * `get`: Fetch one specific resource (`kubectl get pod node-api-xyz -n prod`)
  * `list`: List all resources (`kubectl get pods -n prod`)
  * `watch`: Stream live updates (`kubectl get pods -n prod -w` or `kubectl logs -f`)
  * Notice `create`, `update`, `patch`, `delete` are **not** included—so it's strictly read-only.

---

## Block 3: `RoleBinding` (`lines 32–44`)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: prod-readonly-binding
  namespace: prod
subjects:
  - kind: ServiceAccount
    name: api-workload-sa
    namespace: prod
roleRef:
  kind: Role
  name: prod-readonly
  apiGroup: rbac.authorization.k8s.io
```

### Lines 32–36: `apiVersion` / `kind: RoleBinding` / `metadata`
* **What `RoleBinding` means:** The **glue** that connects a `Role` (permissions) to a `subject` (a `User`, `Group`, or `ServiceAccount`) inside `prod`.
* **Real-world production example:** A `Role` by itself does nothing until a `RoleBinding` assigns it to someone (e.g., assigning `prod-readonly` to the `developers` Okta/AWS IAM group, or to a CI/CD/monitoring `ServiceAccount`).

### Lines 37–40: `subjects:`
* **Who** gets the permissions:
  * **`kind: ServiceAccount`** — Grants the role to a Kubernetes ServiceAccount (could also be `User` or `Group`).
  * **`name: api-workload-sa`** — The `ServiceAccount` created in `02-apps.yaml`.
  * **`namespace: prod`** — The namespace where that `ServiceAccount` lives.

### Lines 41–44: `roleRef:`
* **Which `Role`** is being granted:
  * **`kind: Role`** — References a `Role` (not a `ClusterRole`).
  * **`name: prod-readonly`** — Matches `Role` `prod-readonly` from line 25.
  * **`apiGroup: rbac.authorization.k8s.io`** — Standard RBAC API group.
