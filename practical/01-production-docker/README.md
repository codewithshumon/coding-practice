# Step 1: Production-Grade Docker

## What You're Practicing Here (Real-World Standards)
1. **Multi-stage build (`builder` -> `runtime`)** — Keeps build tools/caches out of the final production image.
2. **Pinned minimal base (`node:22-alpine`)** — Smaller attack surface and faster pulls in EKS/AKS/GKE.
3. **`.dockerignore`** — Prevents `.git`, `.env`, and `node_modules` from leaking secrets or slowing builds.
4. **Non-root user (`USER appuser`)** — Required in production Kubernetes (Pod Security `restricted` profile).
5. **Exec-form `CMD ["node", "app.js"]`** — Ensures `SIGTERM` reaches Node directly for zero-downtime rolling updates.
6. **`HEALTHCHECK` + `/health` endpoint** — Returns `503` during graceful shutdown so load balancers stop routing traffic.

---

## Hands-On Commands (Run in this directory)

### 1. Build the production image
```bash
cd /home/shumon/Documents/coding-practice/practical/01-production-docker
docker build -t prod-api-demo:1.0.0 .
```

### 2. Check image size & layers
```bash
docker images prod-api-demo:1.0.0
docker history prod-api-demo:1.0.0
```

### 3. Run with production resource limits & read-only root filesystem
```bash
docker run -d \
  --name prod-api \
  --cpus="0.5" \
  --memory="128m" \
  --read-only \
  --security-opt=no-new-privileges:true \
  -p 3000:3000 \
  prod-api-demo:1.0.0
```

### 4. Verify non-root user, healthcheck & endpoints
```bash
docker exec prod-api id
curl -s http://localhost:3000/ | jq .
curl -s http://localhost:3000/health | jq .
docker inspect --format='{{.State.Health.Status}}' prod-api
```

### 5. Test graceful shutdown (`SIGTERM`)
```bash
docker stop prod-api
docker logs prod-api
docker rm prod-api
```
You should see `Received SIGTERM. Starting graceful shutdown...` and `All connections closed. Exiting cleanly.`

---

## Next
Once you run and verify these commands, tell me **"done"** (or paste any error) and we will move to **Step 2: Linux & Nginx Production Reverse Proxy**.
