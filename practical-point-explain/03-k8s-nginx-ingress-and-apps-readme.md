# `03-k8s-nginx-ingress-and-apps/README.md` — Line-by-Line & Flag-by-Flag Explanation

Source file: `/home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps/README.md`

---

## Step 1: Build & Push All 3 Images to Local OCI Registry (`lines 7–16`)

```bash
cd /home/shumon/Documents/coding-practice/practical/01-production-docker
docker buildx build --network=host -t localhost:5001/node-api:1.0.0 --push ./node-api
docker buildx build --network=host -t localhost:5001/python-api:1.0.0 --push ./python-api
docker buildx build --network=host -t localhost:5001/go-api:1.0.0 --push ./go-api

curl -s http://localhost:5001/v2/_catalog
```

* **`cd .../01-production-docker`** — Moves into the directory containing the 3 `Dockerfile`s (`node-api`, `python-api`, `go-api`).
* **`docker buildx build`** — Uses **BuildKit** (modern Docker builder) instead of the legacy builder. Faster, supports multi-platform builds and direct registry pushing.
* **`--network=host`** — Runs the build steps using the host's network stack.
  * **Why it matters:** Allows `buildx` (if running inside a buildx container) to reach `localhost:5001` on your host machine during `--push`.
  * **Without it:** A containerized BuildKit builder's `localhost` is itself, so `--push` to `localhost:5001` could fail with `connection refused`.
* **`-t localhost:5001/node-api:1.0.0`** — `-t` (tag) names the image with `<registry>/<image>:<version>`.
  * *Real-world production example:* In AWS, this looks like `123456789.dkr.ecr.us-east-1.amazonaws.com/node-api:1.0.0`.
* **`--push`** — Immediately pushes the built image to `localhost:5001` instead of only saving it locally. (Kubernetes `kind` nodes pull from `localhost:5001`, not your local Docker image cache.)
* **`./node-api`** — The **build context** folder (where `Dockerfile` and source code live).
* **`curl -s http://localhost:5001/v2/_catalog`** — Verifies all 3 repositories (`go-api`, `node-api`, `python-api`) are now stored in the local registry.

---

## Step 2: Install NGINX Ingress Controller inside `kind` (`lines 20–35`)

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Pin NGINX Ingress onto the control-plane node (where ports 80/443 are mapped)
kubectl patch deployment ingress-nginx-controller -n ingress-nginx \
  --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/nodeSelector/ingress-ready","value":"true"}]'

# Wait until NGINX Ingress Pod is Ready (image pull can take ~2-3 min on first run)
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s
```

* **`kubectl apply -f <URL>`** — Downloads and applies the official `kind`-tuned NGINX Ingress Controller manifest directly from GitHub (`hostPort: 80/443`, `publishService` disabled for `kind`, etc.).
  * *Real-world production example:* On AWS EKS/GKE, you install NGINX Ingress via Helm (`helm install ingress-nginx ...`) and it provisions a cloud Load Balancer.
* **`kubectl patch deployment ingress-nginx-controller -n ingress-nginx ...`** — Surgically modifies the already-applied `ingress-nginx-controller` Deployment in-place without editing or re-downloading the upstream YAML:
  * **`--type='json'`** — Uses **JSON Patch (RFC 6902)**, which applies an array of explicit operations (`add`, `replace`, `remove`) at exact JSON paths.
  * **`-p='[{"op":"add","path":"/spec/template/spec/nodeSelector/ingress-ready","value":"true"}]'`** — Adds `ingress-ready: "true"` under `spec.template.spec.nodeSelector` of the Deployment's Pod template.
  * **Why it matters:** Guarantees the NGINX Ingress Pod is scheduled **only** onto `prod-k8s-control-plane` (the node we labeled `ingress-ready=true` and mapped ports `80/443` to in `kind-config.yaml`).
  * **Without it:** If the upstream manifest didn't have `ingress-ready: "true"` (or if it got scheduled onto a worker node), `localhost:80` and `localhost:443` would not reach NGINX.
* **`kubectl wait`** — Pauses your script/terminal until a condition is met instead of guessing with `sleep`.
  * **`--namespace ingress-nginx`** — Looks inside the `ingress-nginx` namespace.
  * **`--for=condition=ready pod`** — Waits until the Pod's `Ready` condition becomes `True`.
  * **`--selector=app.kubernetes.io/component=controller`** — Targets only the main NGINX controller Pod (ignoring one-off admission webhook Jobs).
  * **`--timeout=300s`** — Gives Kubernetes up to **300 seconds (5 minutes)** before failing (important on the first run when pulling the NGINX image takes 2–3 minutes).

---

## Step 3: Apply Namespace, Security, TLS Secret, Apps, Ingress & HPA (`lines 34–54`)

### A. Namespace & Security

```bash
cd /home/shumon/Documents/coding-practice/practical/03-k8s-nginx-ingress-and-apps
kubectl apply -f 01-namespace-and-security.yaml
```

Creates the `prod` namespace, Pod Security Standards (`restricted`), `ResourceQuota`, `LimitRange`, and `NetworkPolicy` **first**, before any apps are deployed.

### B. Self-Signed TLS Certificate + Kubernetes Secret

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=api.localtest.me"
kubectl create secret tls api-tls-secret \
  --namespace prod \
  --key /tmp/tls.key --cert /tmp/tls.crt
rm -f /tmp/tls.key /tmp/tls.crt
```

Every `openssl` flag explained:

* **`openssl req`** — OpenSSL certificate request/generation tool.
* **`-x509`** — Outputs a **self-signed X.509 certificate** directly (instead of a Certificate Signing Request `.csr`).
* **`-nodes`** — "No DES" — do **not** encrypt the private key with a passphrase (NGINX needs to read it automatically without a human typing a password).
* **`-days 365`** — Certificate is valid for 1 year.
* **`-newkey rsa:2048`** — Generates a fresh 2048-bit RSA private key.
* **`-keyout /tmp/tls.key`** & **`-out /tmp/tls.crt`** — Saves the private key and public certificate temporarily in `/tmp/`.
* **`-subj "/CN=api.localtest.me"`** — Sets the Common Name (`CN`) non-interactively to `api.localtest.me` (matches `03-ingress-tls.yaml`).

And the `kubectl` + `rm` commands:

* **`kubectl create secret tls api-tls-secret --namespace prod --key /tmp/tls.key --cert /tmp/tls.crt`** — Stores the cert and key inside Kubernetes as a `Secret` of type `kubernetes.io/tls` named `api-tls-secret` in `prod` (referenced by `03-ingress-tls.yaml` line 15).
  * *Real-world production example:* In production, `cert-manager` + Let's Encrypt creates and renews `api-tls-secret` automatically instead of `openssl`.
* **`rm -f /tmp/tls.key /tmp/tls.crt`** — Deletes the private key from `/tmp/` immediately after uploading it to Kubernetes so no secret key is left sitting on disk.

### C. Deploy Apps, Ingress, HPA & RBAC

```bash
kubectl apply -f 02-apps.yaml
kubectl apply -f 03-ingress-tls.yaml
kubectl apply -f 04-hpa-and-rbac.yaml
```

Applies the 3 microservices (`Deployment`, `Service`, `PDB`), the `Ingress` TLS routing rules, and the `HPA` + `Role`/`RoleBinding`.

---

## Step 4: Verify Pods, Nodes & Ingress (`lines 58–66`)

```bash
kubectl get pods -n prod -o wide
kubectl get ingress -n prod
kubectl get pdb,hpa -n prod
```

* **`kubectl get pods -n prod -o wide`** — Lists all Pods in `prod` and shows the `NODE` column so you can verify replicas are spread across `prod-k8s-worker` and `prod-k8s-worker2` (high availability).
* **`kubectl get ingress -n prod`** — Shows `polyglot-api-ingress`, its host (`api.localtest.me`), ports (`80, 443`), and `ADDRESS` (populated once NGINX Ingress picks it up).
* **`kubectl get pdb,hpa -n prod`** — Checks two resource types in one command:
  * `pdb`: `PodDisruptionBudget` (`MIN AVAILABLE: 1`, `ALLOWED DISRUPTIONS: 1`).
  * `hpa`: `HorizontalPodAutoscaler` (`MINPODS: 2`, `MAXPODS: 5`, `REPLICAS: 2`).

---

## Step 5: Test HTTPS Routing & Load Balancing (`lines 70–78`)

```bash
curl -sk --resolve api.localtest.me:443:127.0.0.1 https://api.localtest.me/node
curl -sk --resolve api.localtest.me:443:127.0.0.1 https://api.localtest.me/python
curl -sk --resolve api.localtest.me:443:127.0.0.1 https://api.localtest.me/go
```

* **`-s`** — Silent mode (hides `curl` progress bar).
* **`-k` (`--insecure`)** — Tells `curl` to trust our self-signed certificate from `openssl` (without `-k`, `curl` rejects self-signed certs because they aren't signed by a public CA like Let's Encrypt).
* **`--resolve api.localtest.me:443:127.0.0.1`** — Forces `curl` to connect `api.localtest.me` port `443` directly to `127.0.0.1` locally without needing external DNS or `/etc/hosts`, while still sending the real `Host: api.localtest.me` header and TLS SNI!
* **Why run `/node` twice?** The `node-api` `Service` load-balances round-robin/randomly across its **2 Pod replicas**, so calling `/node` twice shows `"hostname"` switching between the 2 Pods!
