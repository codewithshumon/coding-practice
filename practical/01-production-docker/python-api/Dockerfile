# syntax=docker/dockerfile:1

FROM python:3.12-alpine AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV=production \
    PORT=5000

WORKDIR /app

# Create non-root user with numeric UID (required by K8s runAsNonRoot)
RUN addgroup -S -g 10001 appgroup && adduser -S -u 10001 appuser -G appgroup

COPY --chown=10001:10001 app.py ./

USER 10001

EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:5000/health >/dev/null || exit 1

CMD ["python", "app.py"]
