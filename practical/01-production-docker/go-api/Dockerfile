# syntax=docker/dockerfile:1

# ==========================================
# Stage 1: Build static Go binary
# ==========================================
FROM golang:1.23-alpine AS builder
WORKDIR /src

COPY go.mod main.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/go-api main.go

# ==========================================
# Stage 2: Distroless non-root runtime (~10MB)
# ==========================================
FROM gcr.io/distroless/static-debian12:nonroot AS runtime

ENV ENV=production \
    PORT=8080

COPY --from=builder /out/go-api /go-api

EXPOSE 8080

# Distroless already runs as UID 65532 (nonroot) and has no shell
ENTRYPOINT ["/go-api"]
