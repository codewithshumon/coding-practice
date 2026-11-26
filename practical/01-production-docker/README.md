# Step 1: Production Container Images (`node-api`, `python-api`, `go-api`)

These 3 polyglot services are built from production-hardened `Dockerfile`s and pushed to your OCI registry (`localhost:5001`, simulating **AWS ECR / Azure ACR / GCP Artifact Registry**).  
**Nothing is run with `docker run`** — Kubernetes (`kind`) runs them in Step 3.

| Service | Port | Base / Runtime | Production Hardening |
| :--- | :--- | :--- | :--- |
| **node-api** | `3000` | `node:22-alpine` (multi-stage) | Non-root `appuser`, `HEALTHCHECK`, `SIGTERM` graceful shutdown |
| **python-api** | `5000` | `python:3.12-alpine` | `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`, non-root `appuser`, `SIGTERM` |
| **go-api** | `8080` | `golang:1.23-alpine` -> `distroless:nonroot` | Static binary (`-ldflags="-s -w"`), **~10 MB**, no shell, UID `65532` |

---

## Build & Push Images (Using BuildKit)

*(Run this after Step 2 starts your `localhost:5001` registry, or build locally now with `--load`.)*

```bash
cd /home/shumon/Documents/coding-practice/practical/01-production-docker
```

### Build & push all 3 images to your local OCI registry (`localhost:5001`)
```bash
docker buildx build --network=host -t localhost:5001/node-api:1.0.0 --push ./node-api
docker buildx build --network=host -t localhost:5001/python-api:1.0.0 --push ./python-api
docker buildx build --network=host -t localhost:5001/go-api:1.0.0 --push ./go-api
```

### Verify images are in the registry
```bash
curl -s http://localhost:5001/v2/_catalog
```
Expected output:
```json
{"repositories":["go-api","node-api","python-api"]}
```
