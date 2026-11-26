# Step 2: Linux & Nginx Production Reverse Proxy

## What You're Practicing Here (Real-World Standards)
1. **TLS/SSL Termination (`443`) + HTTP->HTTPS Redirect (`301`)** — Encrypts traffic at the edge.
2. **Security Headers & `server_tokens off`** — Hides Nginx version, adds `HSTS`, `X-Frame-Options`, `X-Content-Type-Options`.
3. **Rate Limiting (`limit_req_zone` -> `429`)** — Protects backend APIs from traffic spikes/abuse while exempting `/health`.
4. **Structured JSON Access Logs** — Production format ready for Loki / ELK ingestion.
5. **Linux & Network Debugging** — Inspecting ports, configs, TLS handshakes, and container logs.

---

## Hands-On Commands

### 1. Generate a local TLS certificate with OpenSSL
```bash
cd /home/shumon/Documents/coding-practice/practical/02-linux-nginx
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/server.key \
  -out certs/server.crt \
  -subj "/CN=localhost"
```

### 2. Start Nginx + `prod-api` together
```bash
docker compose up -d
```

### 3. Validate Nginx config & inspect listening ports (Linux debugging)
```bash
docker exec prod-nginx nginx -t
ss -tulpn | grep -E '8080|8443'
```

### 4. Test HTTP -> HTTPS redirect, TLS, and security headers
```bash
curl -i http://localhost:8080/
curl -vk https://localhost:8443/
```
Verify:
- `HTTP/1.1 301 Moved Permanently` on port `8080`.
- `Strict-Transport-Security`, `X-Frame-Options`, and `Server: nginx` (without version number) on port `8443`.

### 5. Test Rate Limiting (`429 Too Many Requests`)
```bash
for i in $(seq 1 20); do
  curl -sk -o /dev/null -w "%{http_code}\n" https://localhost:8443/
done
```
You should see `200` for the first ~11 requests, then `429`.

### 6. Inspect structured JSON logs
```bash
docker logs --tail 10 prod-nginx
```

### 7. Clean up before Step 3
```bash
docker compose down
```

---

## Next
Tell me **"done"** once verified, and we'll move to **Step 3: Kubernetes (`kind`) Production Primitives**.
