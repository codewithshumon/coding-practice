# Troubleshooting `CreateContainerConfigError` (`runAsNonRoot` + Non-Numeric User) & `503`

## What Happened

1. **`go-api`** started (`1/1 Running`) and `https://api.localtest.me/go` returned `200 OK` JSON.
2. **`node-api`** and **`python-api`** got stuck in **`0/1 CreateContainerConfigError`**.
3. Because 0 Pods were ready for `node-api` and `python-api`, NGINX Ingress had no healthy backend endpoints and returned **`503 Service Temporarily Unavailable`** for `/node` and `/python`.
4. `kubectl get pdb,hpa -n prod` showed:
   * `ALLOWED DISRUPTIONS: 0` for `node-api-pdb` and `python-api-pdb` (since 0 Pods are running, `minAvailable: 1` is already violated).
   * `cpu: <unknown>/70%` on all 3 HPAs (because `metrics-server` is not installed in `kind` by default).

---

## Exact Root Cause (from `kubectl get events -n prod`)

```text
Error: container has runAsNonRoot and image has non-numeric user (appuser), cannot verify user is non-root
```

* In `02-apps.yaml` (and required by `pod-security.kubernetes.io/enforce: restricted`), every Pod has **`runAsNonRoot: true`**.
* In `node-api/Dockerfile` and `python-api/Dockerfile`, the user is set by **name** (`USER appuser`), **not by numeric UID** (like `USER 1000` or `USER 10001`).
* Kubernetes `kubelet` checks the image metadata *before* starting the container; it does not read `/etc/passwd` inside the image to translate `appuser` to a number. Because it cannot prove `appuser != 0 (root)`, it blocks the container with `CreateContainerConfigError`.
* `go-api` succeeded because its `distroless:nonroot` base image uses a **numeric UID** (`65532`).

---

## How to Fix It

### Option 1: Set `runAsUser` in `02-apps.yaml` (Fastest — no image rebuild needed)
Under `spec.template.spec.securityContext` for `node-api` and `python-api` in `02-apps.yaml`, add a non-zero numeric UID:
```yaml
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
```
Then re-apply:
```bash
kubectl apply -f 02-apps.yaml
```

### Option 2: Use a Numeric `USER` in the `Dockerfile` (Best long-term practice)
In `node-api/Dockerfile` and `python-api/Dockerfile`, use a numeric UID (e.g., `USER 10001` or `adduser -u 10001 -S appuser ...` + `USER 10001`), rebuild, and push to `localhost:5001`.
