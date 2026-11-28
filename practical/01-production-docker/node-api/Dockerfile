# syntax=docker/dockerfile:1

# ==========================================
# Stage 1: Builder (dependencies / build)
# ==========================================
FROM node:22-alpine AS builder
WORKDIR /app

# Copy only package manifests first for Docker layer caching
COPY package*.json ./
RUN mkdir -p node_modules && (npm ci --omit=dev 2>/dev/null || npm install --omit=dev)

# ==========================================
# Stage 2: Production Runtime (minimal)
# ==========================================
FROM node:22-alpine AS runtime

ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

# Create a non-root user & group with numeric UID (required by K8s runAsNonRoot)
RUN addgroup -S -g 10001 appgroup && adduser -S -u 10001 appuser -G appgroup

# Copy dependencies and source with proper ownership
COPY --from=builder --chown=10001:10001 /app/node_modules ./node_modules
COPY --chown=10001:10001 package.json app.js ./

# Drop root privileges using numeric UID
USER 10001

EXPOSE 3000

# Built-in healthcheck for Docker / Compose
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health >/dev/null || exit 1

# Use exec form (JSON array) so Node receives SIGTERM directly as PID 1
CMD ["node", "app.js"]
