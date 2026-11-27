# `01-namespace-and-security.yaml` — True Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps/01-namespace-and-security.yaml`

This file uses `---` (YAML document separators) to define **4 Kubernetes resources** in one file:

1. `Namespace` (Lines 1–9)
2. `ResourceQuota` (Lines 11–22)
3. `LimitRange` (Lines 24–37)
4. `NetworkPolicy` (Lines 39–53)

---

## Block 1: `Namespace` + Pod Security Standards (`lines 1–9`)

### Line 1: `apiVersion: v1`

* **What `apiVersion` means:** Tells Kubernetes which API group and version to use to understand this YAML object.
* **What `v1` means:** The core, stable Kubernetes API version (used for built-in objects like `Namespace`, `Pod`, `Service`, `ConfigMap`).
* **Real-world production example:** Just like a REST API has `/api/v1/users` vs `/api/v2/users`, Kubernetes needs `v1` so it knows the exact schema rules for validating your YAML before saving it to `etcd`.

### Line 2: `kind: Namespace`

* **What `kind` means:** Defines the **type of Kubernetes object** you want to create (like choosing a blueprint: Server, Database, Firewall, etc.).
* **What `Namespace` means:** A virtual cluster / isolated folder inside one physical Kubernetes cluster.
* **Real-world production example:** A company runs one big AWS EKS cluster and creates separate namespaces—`dev`, `staging`, and `prod`—or `payments-team` and `orders-team`—so teams don't accidentally delete or overwrite each other's services with the same name (like `api`).

### Line 3: `metadata:`

* **What `metadata` means:** Information *about* the object (its name, namespace, labels, annotations)—not what it *does*, just how Kubernetes identifies and tags it.
* **Real-world production example:** Used by monitoring tools, Argo CD, and `kubectl` to find and group resources (e.g., `kubectl get all -n prod`).

### Line 4: `  name: prod`

* **What `name` means:** The unique identifier of this object.
* **What `prod` means:** Names this namespace `prod` (short for production).
* **Real-world production example:** In CI/CD pipelines, deploying to `prod` requires manual approval and stricter rules than deploying to `dev`.

### Line 5: `  labels:`

* **What `labels` means:** Key-value tags attached to a Kubernetes object so other Kubernetes features can select or apply rules to it.
* **Real-world production example:** Tagging namespaces with `env: prod` or `team: checkout` so cost-tracking tools (like Kubecost) can bill the right department.

### Line 6: `    # Pod Security Standards (PSS): enforce 'restricted' profile in production`

* **What `#` means:** A YAML comment—ignored by Kubernetes, written only for humans reading the file.

### Line 7: `    pod-security.kubernetes.io/enforce: restricted`

* **What `pod-security.kubernetes.io/enforce` means:** A built-in Kubernetes admission control label that **blocks** insecure Pods from starting in this namespace.
* **What `restricted` means:** The strictest of Kubernetes' 3 security profiles (`privileged`, `baseline`, `restricted`). It forces every container to:
  * Run as **non-root** (`runAsNonRoot: true`)
  * Set `allowPrivilegeEscalation: false`
  * Drop all Linux capabilities (`drop: ["ALL"]`)
  * Use a seccomp profile (`RuntimeDefault`)
* **Real-world production example:** A developer accidentally pushes a Pod running as `root` with host disk access. Kubernetes immediately rejects it with `Forbidden` before the container can even start—stopping potential container-escape attacks.

### Line 8: `    pod-security.kubernetes.io/audit: restricted`

* **What `audit` means:** Does not block, but writes a record to the **Kubernetes API Audit Log** whenever a Pod violates the `restricted` profile.
* **Real-world production example:** Security/SOC teams send audit logs to Splunk, Datadog, or ELK to get alerts when anyone tries to deploy an insecure workload.

### Line 9: `    pod-security.kubernetes.io/warn: restricted`

* **What `warn` means:** Prints a visible warning message in the terminal when someone runs `kubectl apply`, even if another rule allowed it.
* **Real-world production example:** When migrating legacy apps, teams often set `warn: restricted` before turning on `enforce: restricted` so developers see what needs fixing without breaking production.

### Line 10: `---`

* **What `---` means:** YAML document separator. Allows putting multiple Kubernetes resources in a single `.yaml` file instead of 4 separate files.

---

## Block 2: `ResourceQuota` (`lines 11–22`)

### Line 11: `apiVersion: v1`

* **What it means:** `ResourceQuota` belongs to the core `v1` Kubernetes API.

### Line 12: `kind: ResourceQuota`

* **What `kind` means:** Object type.
* **What `ResourceQuota` means:** A **namespace-wide budget/ceiling** on total compute resources and object counts.
* **Real-world production example:** On a shared cluster, you give the `prod` namespace a strict budget so one buggy service scaling up cannot eat all CPU/RAM and crash other namespaces like `monitoring` or `ingress-nginx`.

### Lines 13–15: `metadata:` / `  name: prod-quota` / `  namespace: prod`

* **`name: prod-quota`:** Names this quota object `prod-quota`.
* **`namespace: prod`:** Places this quota **inside** the `prod` namespace so it only restricts `prod`.
* **Real-world production example:** Every namespace (`dev`, `staging`, `prod`) gets its own quota—`dev` might get `1` CPU while `prod` gets `16` CPUs.

### Line 16: `spec:`

* **What `spec` means:** "Specification"—the desired rules/configuration you want Kubernetes to enforce for this object.

### Line 17: `  hard:`

* **What `hard` means:** Strict, non-negotiable maximum limits. Once reached, Kubernetes refuses to create new Pods until resources are freed.

### Line 18: `    requests.cpu: "2"`

* **What `requests.cpu` means:** Total **guaranteed** CPU reserved across **all Pods combined** in `prod`.
* **What `"2"` means:** 2 full CPU cores (2000 millicores). Note the quotes—Kubernetes expects string or number, and quoting avoids YAML parsing quirks.
* **Real-world production example:** If you have 10 Pods each requesting `200m` CPU (`10 × 200m = 2000m = 2 cores`), the quota is full; an 11th Pod will be rejected.

### Line 19: `    requests.memory: 1Gi`

* **What `requests.memory` means:** Total **guaranteed** RAM reserved across all Pods in `prod`.
* **What `1Gi` means:** 1 Gibibyte ($1024\text{ MiB} \approx 1.07\text{ GB}$).
* **Real-world production example:** Ensures total reserved memory in `prod` fits safely within your worker nodes' RAM.

### Line 20: `    limits.cpu: "4"`

* **What `limits.cpu` means:** Total maximum **burst** CPU caps allowed across all Pods in `prod`.
* **What `"4"` means:** 4 full CPU cores.

### Line 21: `    limits.memory: 2Gi`

* **What `limits.memory` means:** Total maximum RAM caps across all Pods in `prod`.
* **What `2Gi` means:** 2 Gibibytes ($2048\text{ MiB}$).

### Line 22: `    pods: "20"`

* **What `pods` means:** Maximum number of Pods allowed in `prod` at once.
* **Real-world production example:** If a misconfigured Horizontal Pod Autoscaler tries to spin up 200 Pods during a spike, Kubernetes stops it at 20 Pods so it doesn't overwhelm node IPs or `etcd`.

### Line 23: `---`

* Separates `ResourceQuota` from `LimitRange`.

---

## Block 3: `LimitRange` (`lines 24–37`)

### Line 24: `apiVersion: v1`

* Core `v1` API.

### Line 25: `kind: LimitRange`

* **What `LimitRange` means:** Sets **per-container** default resource requests and limits when a Pod/Deployment doesn't specify them.
* **Real-world production example:** When a `ResourceQuota` is active, Kubernetes **rejects** any Pod that omits `resources.requests/limits`. `LimitRange` acts as a safety net by automatically filling in defaults so deployments don't fail.

### Lines 26–28: `metadata:` / `  name: prod-limits` / `  namespace: prod`

* Names this `LimitRange` `prod-limits` and applies it inside the `prod` namespace.

### Lines 29–30: `spec:` / `  limits:`

* Starts the list of resource rules for this `LimitRange`.

### Line 31: `    - type: Container`

* **What `type: Container` means:** Applies these defaults to each **individual container** inside a Pod (as opposed to `Pod` or `PersistentVolumeClaim`).
* **Real-world production example:** If a Pod has 2 containers (e.g., an app container + a log sidecar), each container gets these defaults if it didn't specify its own.

### Lines 32–34: `defaultRequest:` / `cpu: 50m` / `memory: 64Mi`

* **What `defaultRequest` means:** If a container doesn't specify `resources.requests`, Kubernetes automatically assigns these **guaranteed minimums** for scheduling:
  * **`cpu: 50m`:** 50 millicores = 5% of 1 CPU core (`1000m = 1 core`).
  * **`memory: 64Mi`:** 64 Mebibytes of RAM.
* **Real-world production example:** A small microservice or cron job deployed without `resources` still gets a fair 50m CPU / 64Mi RAM reservation on a worker node.

### Lines 35–37: `default:` / `cpu: 200m` / `memory: 128Mi`

* **What `default` means:** If a container doesn't specify `resources.limits`, Kubernetes automatically assigns these **hard maximums**:
  * **`cpu: 200m`:** 200 millicores = 20% of 1 CPU core (throttled if it tries to use more).
  * **`memory: 128Mi`:** 128 Mebibytes (killed with `OOMKilled` if it exceeds 128Mi).
* **Real-world production example:** Prevents a forgotten test container from leaking gigabytes of RAM and crashing a production worker node.

### Line 38: `---`

* Separates `LimitRange` from `NetworkPolicy`.

---

## Block 4: `NetworkPolicy` (`lines 39–53`)

### Line 39: `# Zero-Trust NetworkPolicy: allow ingress ONLY from ingress-nginx namespace`

* Human-readable comment explaining the firewall rule below.

### Line 40: `apiVersion: networking.k8s.io/v1`

* **What `networking.k8s.io/v1` means:** `NetworkPolicy` is not in core `v1`—it lives in the `networking.k8s.io` API group (`v1`), alongside `Ingress`.

### Line 41: `kind: NetworkPolicy`

* **What `NetworkPolicy` means:** A Kubernetes **Pod-level firewall** controlling which Pods can talk to each other over the network.
* **Real-world production example:** In a bank or SaaS app, you block direct access to backend APIs and databases so only authorized services (like the API gateway or Ingress) can reach them.

### Lines 42–44: `metadata:` / `  name: allow-only-ingress-nginx` / `  namespace: prod`

* Names this firewall rule `allow-only-ingress-nginx` and applies it to the `prod` namespace.

### Line 45: `spec:`

* Starts the firewall rules.

### Line 46: `  podSelector: {}`

* **What `podSelector` means:** Chooses *which Pods* in `prod` this firewall protects.
* **What `{}` means:** An empty selector matches **ALL Pods** in `prod` (`node-api`, `python-api`, `go-api`, etc.).
* **Real-world production example:** Applying a default-lockdown rule to every service in `prod` instead of configuring each service one by one.

### Lines 47–48: `  policyTypes:` / `    - Ingress`

* **What `policyTypes` means:** Which traffic direction(s) this policy controls (`Ingress` = incoming, `Egress` = outgoing).
* **What `Ingress` means:** Controls **incoming** connections *to* the Pods in `prod` (outgoing connections *from* `prod` Pods remain unrestricted here).

### Line 49: `  ingress:`

* Lists the **allow rules** for incoming traffic. Anything NOT listed here is **blocked (denied)** by default.

### Line 50: `    - from:`

* Specifies **who** is allowed to send traffic into `prod` Pods.

### Lines 51–53: `namespaceSelector:` / `matchLabels:` / `kubernetes.io/metadata.name: ingress-nginx`

* **What `namespaceSelector` means:** Allows traffic from Pods located in any namespace matching the given label.
* **What `matchLabels` means:** Exact key-value label match.
* **What `kubernetes.io/metadata.name: ingress-nginx` means:** Kubernetes automatically labels every namespace with `kubernetes.io/metadata.name: <namespace-name>`. So this matches **only** the `ingress-nginx` namespace.
* **Real-world production example:** External users hit `https://api.example.com` $\rightarrow$ NGINX Ingress Controller (in `ingress-nginx` namespace) $\rightarrow$ your APIs (in `prod` namespace). That traffic is **allowed**. If a compromised Pod in `dev` or `default` tries to connect directly to `http://node-api.prod.svc.cluster.local`, it is **blocked**.
