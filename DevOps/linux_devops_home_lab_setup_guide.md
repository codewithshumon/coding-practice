# Practical DevOps Lab Setup on a Local Linux Machine

This guide walks you through setting up a complete, zero-cost DevOps practice lab on your local Linux workstation (Ubuntu/Debian-based systems assumed; adjust package manager commands if using Fedora/Arch).

---

## Prerequisites & Hardware Recommendations

* **OS:** Ubuntu 22.04 / 24.04 LTS (or any modern Debian-based distro)
* **RAM:** Minimum **8 GB** (16 GB recommended if running Kubernetes + Jenkins + Monitoring simultaneously)
* **Disk Space:** At least **30–40 GB** free space for container images, local clusters, and logs
* **Privileges:** A non-root user with `sudo` access

---

## Step 1: Prepare Your Base Linux Environment

Update your system and install essential networking, debugging, and scripting utilities.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  curl wget git jq unzip htop tree net-tools \
  dnsutils iproute2 procps ca-certificates gnupg lsb-release
```

### Organize Your Lab Workspace
Create a clean directory structure to isolate each practice area:

```bash
mkdir -p ~/devops-lab/{scripts,docker,k8s,cicd,iac,monitoring}
cd ~/devops-lab
```

---

## Step 2: Install Docker Engine & Docker Compose

Install official Docker Engine so you can run containers without `sudo` and use `docker compose`.

```bash
# Add Docker's official GPG key and repository
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Compose plugin
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Allow running docker without sudo (log out and back in after running this)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

### Hands-On Lab 2A: Multi-Container Stack with Reverse Proxy
Create `~/devops-lab/docker/docker-compose.yml` to practice networking between an Nginx reverse proxy, an app container, and Redis:

```yaml
services:
  web:
    image: nginxdemos/hello:plain-text
    networks:
      - app-net

  cache:
    image: redis:7-alpine
    networks:
      - app-net

  proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - web
    networks:
      - app-net

networks:
  app-net:
    driver: bridge
```

Create `~/devops-lab/docker/nginx.conf`:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://web:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Test it:
```bash
cd ~/devops-lab/docker
docker compose up -d
curl http://localhost:8080
docker compose down
```

---

## Step 3: Set Up Local Kubernetes (`kubectl` + `kind`)

`kind` (Kubernetes in Docker) runs real multi-node Kubernetes clusters inside Docker containers—ideal for low-overhead local testing and fast resets.

### 1. Install `kubectl`
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl
kubectl version --client
```

### 2. Install `kind`
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

### 3. Spin Up a Multi-Node Cluster (1 Control Plane + 2 Workers)
Create `~/devops-lab/k8s/kind-cluster.yaml`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Create and verify your cluster:
```bash
kind create cluster --name devops-lab --config ~/devops-lab/k8s/kind-cluster.yaml
kubectl get nodes -o wide
```

### Hands-On Lab 3A: Simulate & Debug `OOMKilled` / `CrashLoopBackOff`
Create `~/devops-lab/k8s/oom-test.yaml` with a strict memory limit so you can observe real termination events:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: oom-demo
spec:
  containers:
    - name: stress
      image: polinux/stress
      resources:
        requests:
          memory: "32Mi"
        limits:
          memory: "64Mi"
      command: ["stress"]
      args: ["--vm", "1", "--vm-bytes", "128M", "--vm-hang", "1"]
```

Run and inspect the failure:
```bash
kubectl apply -f ~/devops-lab/k8s/oom-test.yaml
sleep 10
kubectl get pod oom-demo
kubectl describe pod oom-demo
kubectl delete pod oom-demo
```

---

## Step 4: Set Up a Local CI/CD Server (Jenkins in Docker)

Run Jenkins locally to practice declarative `Jenkinsfile` pipelines, credentials management, and automated Docker builds.

Create `~/devops-lab/cicd/docker-compose.yml`:

```yaml
services:
  jenkins:
    image: jenkins/jenkins:lts-jdk17
    container_name: local-jenkins
    user: root
    ports:
      - "8081:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  jenkins_home:
```

Start Jenkins and retrieve the initial admin password:
```bash
cd ~/devops-lab/cicd
docker compose up -d
sleep 15
docker exec local-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Open `http://localhost:8081` in your browser, paste the password, install suggested plugins, and create your admin user. *(Stop it with `docker compose stop` when not in use to save RAM.)*

---

## Step 5: Install Infrastructure as Code & Automation Tools (Terraform + Ansible)

### 1. Install Terraform
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
terraform -version
```

### 2. Install Ansible
```bash
sudo apt install -y ansible
ansible --version
```

### Hands-On Lab 5A: Practice Terraform Locally (Zero Cloud Cost)
Create `~/devops-lab/iac/main.tf` using the `local` and `docker` providers to learn `init`, `plan`, `apply`, state files, and `destroy`:

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "server_config" {
  filename = "${path.module}/generated_nginx.conf"
  content  = <<-EOT
    # Managed by Terraform
    worker_processes auto;
    events { worker_connections 1024; }
  EOT
}
```

Run the Terraform workflow:
```bash
cd ~/devops-lab/iac
terraform init
terraform plan
terraform apply -auto-approve
cat generated_nginx.conf
terraform destroy -auto-approve
```

---

## Step 6: Set Up Local Observability (Prometheus + Grafana)

Practice scraping metrics and building dashboards locally.

Create `~/devops-lab/monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

Create `~/devops-lab/monitoring/docker-compose.yml`:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

Start the stack:
```bash
cd ~/devops-lab/monitoring
docker compose up -d
```
* **Prometheus UI:** `http://localhost:9090`
* **Grafana UI:** `http://localhost:3000` (login: `admin` / `admin` → Add Prometheus data source at `http://prometheus:9090`)

---

## Step 7: Resource Management & Cleanup Commands

Keep your Linux workstation fast by stopping services you aren't actively practicing with:

```bash
# Pause or delete your local Kubernetes cluster
kind delete cluster --name devops-lab

# Stop all running Docker Compose stacks
docker stop $(docker ps -q)

# Check disk usage by Docker
docker system df

# Clean up unused stopped containers, dangling images, and unused networks
docker system prune -f
```

---

## Suggested Weekly Practice Routine

1. **Days 1–2 (Linux & Bash):** Write Bash scripts in `~/devops-lab/scripts` to parse Nginx logs, monitor disk usage, and automate backups with `cron`.
2. **Days 3–4 (Docker & Nginx):** Build multi-stage Dockerfiles for a Node.js or Python app and put it behind Nginx with rate limiting and custom headers.
3. **Days 5–6 (Kubernetes):** Deploy the containerized app to `kind` using `Deployment`, `ClusterIP` Service, `ConfigMap`, `Secret`, and resource limits.
4. **Day 7 (CI/CD & IaC):** Automate building and testing that project with Jenkins or GitHub Actions, and manage configs/containers declaratively with Terraform.