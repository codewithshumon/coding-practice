# Step 1: Production-Grade Docker (Node.js + Python + Go)

Now you have **3 real polyglot microservices**, each built with production best practices:

| Service | Port | Base / Runtime | Key Production Practice |
| :--- | :--- | :--- | :--- |
| **node-api** | `3000` | `node:22-alpine` (multi-stage) | Non-root `appuser`, `HEALTHCHECK`, `SIGTERM` graceful shutdown |
| **python-api** | `5000` | `python:3.12-alpine` | `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`, non-root `appuser`, `SIGTERM` |
| **go-api** | `8080` | `golang:1.23-alpine` -> `distroless:nonroot` | Static binary (`-ldflags="-s -w"`), **~10 MB** image with **no shell** |

---

## Hands-On Commands

```bash
cd /home/shumon/Documents/coding-practice/practical/01-production-docker
```

### 1. Build all 3 production images
```bash
docker build -t node-api:1.0.0 ./node-api
docker build -t python-api:1.0.0 ./python-api
docker build -t go-api:1.0.0 ./go-api
```

### 2. Compare image sizes
```bash
docker images | grep -E "node-api|python-api|go-api"
```
Notice how tiny `go-api` is compared to `node-api` and `python-api`!

### 3. Run all 3 with production hardening (`--read-only`, resource limits, no new privileges)
```bash
docker run -d --name node-api   --cpus="0.5" --memory="128m" --read-only --security-opt=no-new-privileges:true -p 3000:3000 node-api:1.0.0
docker run -d --name python-api --cpus="0.5" --memory="128m" --read-only --security-opt=no-new-privileges:true -p 5000:5000 python-api:1.0.0
docker run -d --name go-api     --cpus="0.5" --memory="64m"  --read-only --security-opt=no-new-privileges:true -p 8080:8080 go-api:1.0.0
```

### 4. Test endpoints & non-root users
```bash
curl -s http://localhost:3000/ | jq .
curl -s http://localhost:5000/ | jq .
curl -s http://localhost:8080/ | jq .

docker exec node-api id
docker exec python-api id
# Note: go-api uses distroless (no shell), so `docker exec go-api id` won't run — that's extra security!
```

### 5. Test graceful shutdown (`SIGTERM`) & clean up
```bash
docker stop node-api python-api go-api
docker logs --tail 3 node-api
docker logs --tail 3 python-api
docker logs --tail 3 go-api
docker rm node-api python-api go-api
```
