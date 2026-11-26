# `docker run` with Production Hardening

## Command

```bash
docker run -d --name node-api --cpus="0.5" --memory="128m" --read-only --security-opt=no-new-privileges:true -p 3000:3000 node-api:1.0.0
```

---

## Flag-by-Flag Breakdown

### 1. `docker run`
Creates a **new container** from an image and starts it.

### 2. `-d` (Detached mode)
* **What it does:** Runs the container in the background and immediately returns your terminal prompt.
* **Without `-d`:** The container runs in the foreground, locks up your terminal showing its logs, and pressing `Ctrl + C` or closing the terminal stops the container.

### 3. `--name node-api`
* **What it does:** Gives the container a custom, predictable name (`node-api`) so you can easily manage it later (e.g., `docker logs node-api`, `docker stop node-api`).
* **Without `--name`:** Docker generates a random two-word name (like `angry_newton`).
* **Note:** Container names must be unique — if a stopped or running container named `node-api` already exists, you must remove it before reusing the name.

### 4. `--cpus="0.5"`
* **What it does:** Limits the container to at most **50% of 1 CPU core**.
* **Why it matters:** Prevents an infinite loop or traffic spike in one container from hogging 100% of the server's CPU and starving other services.
* **Without it:** The container can use as much CPU as the host has available.

### 5. `--memory="128m"`
* **What it does:** Caps the container's RAM usage at **128 megabytes**.
* **Why it matters:** If the app has a memory leak, Docker kills *only this container* (`OOMKilled`) once it exceeds 128 MB, protecting the rest of the server.
* **Without it:** A memory leak can consume all server RAM and crash the entire machine and every other service on it.

### 6. `--read-only`
* **What it does:** Mounts the container's root filesystem as **read-only** (no file creation, modification, or deletion).
* **Why it matters:** Even if an attacker exploits your app, they cannot download malware, write backdoor scripts, or modify application binaries on disk.
* **Without it:** Processes inside the container can freely write and modify files in the container's writable layer.
* **Practical tip:** If your app needs to write temporary files (e.g., `/tmp`), pair this with `--tmpfs /tmp` so only `/tmp` is writable in RAM.

### 7. `--security-opt=no-new-privileges:true`
* **What it does:** Blocks any process inside the container from gaining **extra privileges** after starting (e.g., via `setuid` binaries or Linux capabilities escalation).
* **Why it matters:** Even if your app runs as a non-root user, an attacker cannot use a `setuid` binary inside the image to escalate to root.
* **Without it:** A process could potentially escalate privileges inside the container if a `setuid` binary exists in the image.

### 8. `-p 3000:3000` (Port mapping)
* **What it does:** Maps host port to container port (`-p <HOST_PORT>:<CONTAINER_PORT>`). Traffic to `localhost:3000` on the host is forwarded to port `3000` inside the container.
* **Without `-p`:** The app listens on port `3000` inside the isolated container network, but nothing outside (browser, `curl`, external users) can reach it.

### 9. `node-api:1.0.0`
* **What it does:** Specifies the image (`node-api`) and exact version tag (`1.0.0`).
* **Why `1.0.0` instead of `latest`:** Pinning an explicit version in production guarantees you know the exact build running and can roll back cleanly, whereas `latest` can silently change between deployments.
