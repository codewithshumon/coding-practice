# Testing APIs (`curl | jq`), User Checks (`docker exec id`), and Graceful Cleanup

## 1. Testing APIs and Formatting JSON

```bash
curl -s http://localhost:3000/ | jq .
curl -s http://localhost:5000/ | jq .
curl -s http://localhost:8080/ | jq .
```

* **`curl`** — Sends an HTTP `GET` request to each running service (`3000` = Node API, `5000` = Python API, `8080` = Go API).
* **`-s` (silent)** — Hides `curl`'s progress bar and transfer stats so only the raw response body is passed into the pipe.
* **`|`** — Pipes the HTTP response from `curl` into `jq`.
* **`jq .`** — Command-line JSON processor; `.` pretty-prints the entire JSON response with indentation and colors.
  * *Without `jq .`:* JSON prints as a single hard-to-read line.

---

## 2. Checking the Container User (`docker exec ... id`)

```bash
docker exec node-api id
docker exec python-api id
```

* **`docker exec`** — Runs a one-off command inside an **already-running** container.
* **`id`** — Linux command that prints the user ID (`uid`), group ID (`gid`), and groups of the process user.
* **Why it matters (Security check):** Verifies the container runs as a **non-root user** (e.g., `uid=1000` or `uid=1001`) instead of `uid=0(root)`.

---

## 3. Graceful Stop, Log Check, and Removal

```bash
docker stop node-api python-api go-api
docker logs --tail 3 node-api
docker logs --tail 3 python-api
docker logs --tail 3 go-api
docker rm node-api python-api go-api
```

* **`docker stop`** — Gracefully stops containers by sending `SIGTERM` (allowing up to 10s to finish in-flight requests and close cleanly before sending `SIGKILL`). Stopped containers remain on disk in `Exited` state.
* **`docker logs --tail 3 <name>`** — Prints only the **last 3 lines** of `stdout`/`stderr` from a container (works even after it is stopped). Run after `docker stop` to verify graceful shutdown.
* **`docker rm`** — Permanently deletes the stopped containers, freeing their names (`node-api`, `python-api`, `go-api`) for reuse without deleting the underlying Docker images.
