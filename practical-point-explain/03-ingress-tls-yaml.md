# `03-ingress-tls.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps/03-ingress-tls.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: polyglot-api-ingress
  namespace: prod
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/limit-rps: "10"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.localtest.me
      secretName: api-tls-secret
  rules:
    - host: api.localtest.me
      http:
        paths:
          - path: /node(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: node-api
                port:
                  number: 3000
          - path: /python(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: python-api
                port:
                  number: 5000
          - path: /go(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: go-api
                port:
                  number: 8080
```

---

## 1. Header & Metadata (`lines 1–5`)

### Line 1: `apiVersion: networking.k8s.io/v1`
* **What `apiVersion` means:** The Kubernetes API group and version used to validate this object.
* **What `networking.k8s.io/v1` means:** The stable networking API group where `Ingress` and `NetworkPolicy` live.

### Line 2: `kind: Ingress`
* **What `kind` means:** The type of Kubernetes object to create.
* **What `Ingress` means:** An **HTTP/HTTPS reverse proxy & routing rule** at the edge of the cluster. It exposes internal `ClusterIP` Services (`node-api`, `python-api`, `go-api`) to the outside world under one domain name and TLS certificate.
* **Real-world production example:** Instead of paying for 3 separate AWS Load Balancers for 3 microservices, you use 1 Load Balancer + 1 `Ingress` to route `https://api.example.com/node`, `/python`, and `/go` to the right backend Service.

### Lines 3–5: `metadata:` / `  name: polyglot-api-ingress` / `  namespace: prod`
* **`name: polyglot-api-ingress`:** Unique name of this Ingress object.
* **`namespace: prod`:** Must be in the **same namespace (`prod`)** as the backend Services (`node-api`, `python-api`, `go-api`). An `Ingress` cannot route directly to Services in a different namespace.

---

## 2. NGINX Annotations (`lines 6–9`)

### Line 6: `  annotations:`
* **What `annotations` means:** Key-value metadata used to pass **controller-specific configuration** (here, extra NGINX settings) that aren't part of the generic Kubernetes `Ingress` spec.

### Line 7: `    nginx.ingress.kubernetes.io/rewrite-target: /$2`
* **What it means:** Rewrites the URL path **before** forwarding the request to your backend app, using regex capture group `$2` from the `path` below.
* **How it works with `path: /node(/|$)(.*)`:**
  * Capture group `($1)` = `(/|$)` (the slash `/` or end of URL)
  * Capture group `($2)` = `(.*)` (everything after `/node/`)
  * Examples:
    * User requests `/node` $\rightarrow$ `$2` is `""` $\rightarrow$ app receives `/`
    * User requests `/node/` $\rightarrow$ `$2` is `""` $\rightarrow$ app receives `/`
    * User requests `/node/health` $\rightarrow$ `$2` is `health` $\rightarrow$ app receives `/health`
* **Real-world production example:** Your Node/Python/Go apps only define routes like `/` and `/health`—they don't know they're mounted under `/node` or `/python`. Without `rewrite-target: /$2`, `node-api` would receive `GET /node/health` and return `404 Not Found`.

### Line 8: `    nginx.ingress.kubernetes.io/ssl-redirect: "true"`
* **What it means:** Forces all plain HTTP (`http://`, port 80) requests to automatically redirect (`308 Permanent Redirect`) to HTTPS (`https://`, port 443).
* **Real-world production example:** Prevents users or clients from accidentally sending unencrypted passwords, JWT tokens, or API keys over HTTP.

### Line 9: `    nginx.ingress.kubernetes.io/limit-rps: "10"`
* **What it means:** Rate limits each client IP address to **10 requests per second** (`rps`). Extra burst traffic beyond NGINX's burst buffer gets rejected with HTTP `503 Service Temporarily Unavailable` (or `429`).
* **Real-world production example:** Protects your backend APIs from simple DDoS floods, brute-force login attempts, or buggy client retry loops.

---

## 3. Ingress Class & TLS (`lines 10–15`)

### Line 10: `spec:`
* **What `spec` means:** The desired routing and TLS configuration for this `Ingress`.

### Line 11: `  ingressClassName: nginx`
* **What it means:** Tells Kubernetes *which* Ingress Controller should read and enforce this `Ingress` (since a cluster can have multiple controllers like `nginx`, `alb`, `traefik`, or `istio`).
* **Without it:** If no default `IngressClass` is set in the cluster, NGINX Ingress Controller ignores this `Ingress` completely and routing returns `404`.

### Lines 12–15: `tls:` / `- hosts:` / `- api.localtest.me` / `secretName: api-tls-secret`
* **`tls:`** — Enables HTTPS (TLS termination) at the NGINX Ingress Controller.
* **`hosts: [api.localtest.me]`** — Lists the domain name(s) covered by the TLS certificate.
  * *Why `localtest.me`?* `*.localtest.me` is a real public DNS wildcard domain that always resolves to `127.0.0.1` (`localhost`)—no `/etc/hosts` editing needed!
* **`secretName: api-tls-secret`** — Points to a Kubernetes `Secret` (type `kubernetes.io/tls`) in the `prod` namespace containing `tls.crt` (certificate) and `tls.key` (private key).
* **Real-world production example:** In EKS/GKE, `cert-manager` automatically gets a free Let's Encrypt certificate and stores it in `api-tls-secret`. NGINX terminates HTTPS at the edge and forwards plain HTTP internally inside the cluster to your Pods.

---

## 4. Routing Rules (`lines 16–40`)

### Line 16–18: `rules:` / `- host: api.localtest.me` / `http:`
* **`rules:`** — List of host-based HTTP routing rules.
* **`host: api.localtest.me`** — Only requests with the HTTP `Host: api.localtest.me` header match these paths (virtual hosting—you can host multiple domains on one Ingress IP).

### Lines 19–26: Node API Route
```yaml
        paths:
          - path: /node(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: node-api
                port:
                  number: 3000
```
* **`path: /node(/|$)(.*)`** — Regex path match:
  * `/node` followed by either `/` or end-of-string (`$`), plus anything after it `(.*)`.
  * *Why `(/|$)` matters:* Ensures `/node` and `/node/health` match, while `/nodejs` does **not** accidentally match!
* **`pathType: ImplementationSpecific`** — Tells Kubernetes that the matching behavior is decided by the Ingress Controller (required when using NGINX regex paths like `(/|$)(.*)` instead of `Prefix` or `Exact`).
* **`backend.service.name: node-api`** — Sends matching requests to the `node-api` Kubernetes `Service` in `prod`.
* **`backend.service.port.number: 3000`** — Connects to port `3000` on the `node-api` `Service`.

### Lines 27–33: Python API Route
* **`path: /python(/|$)(.*)`** $\rightarrow$ Rewrites to `/$2` $\rightarrow$ forwards to Service **`python-api`** on port **`5000`**.

### Lines 34–40: Go API Route
* **`path: /go(/|$)(.*)`** $\rightarrow$ Rewrites to `/$2` $\rightarrow$ forwards to Service **`go-api`** on port **`8080`**.

---

## End-to-End Request Flow Summary

1. Client calls `https://api.localtest.me/go/health` (or `http://...`, which redirects `308` to `https://`).
2. Traffic enters `kind` control-plane port `443` $\rightarrow$ **NGINX Ingress Controller** (`ingress-nginx` namespace).
3. NGINX checks rate limit (`10 rps`), decrypts TLS using **`api-tls-secret`**, matches host `api.localtest.me` and path `/go(/|$)(.*)`.
4. NGINX rewrites `/go/health` $\rightarrow$ `/health` (using `rewrite-target: /$2`).
5. NGINX forwards the request to **`go-api:8080`** in `prod` (allowed by `NetworkPolicy` `allow-only-ingress-nginx`), which load-balances across the 2 `go-api` Pods.
