#############################
# Multi-stage build (builder + runtime)
#############################

# Stage 1: builder – install build deps and create a venv with all Python packages
FROM python:3.10-slim AS builder

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

USER root

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		gcc \
		libkrb5-dev \
		krb5-user \
		libssl-dev \
		libsasl2-dev \
		python3-dev \
		libmariadb-dev-compat libmariadb-dev \
		pkg-config \
		ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# remove any potential upstream source tree if present (defensive)
RUN rm -rf /app/superset || true

# create venv and install runtime packages
RUN python -m venv /app/.venv \
	&& /app/.venv/bin/python -m pip install --upgrade pip setuptools wheel

COPY ./requirements-extensions.txt /tmp/requirements-extensions.txt

RUN /app/.venv/bin/pip install --no-cache-dir -r /tmp/requirements-extensions.txt

#############################
# Stage 2: runtime – lean image with only runtime artifacts
#############################
FROM apache/superset:latest AS runtime

USER root

# Install runtime shared libraries required by some DB drivers (e.g. mysqlclient)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		libmariadb3 \
		ca-certificates \
		redis-tools \
	&& rm -rf /var/lib/apt/lists/*

# ensure old app code is removed so venv-installed packages are authoritative
RUN rm -rf /app/superset || true

# copy venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy any local overrides into the image under /app/overrides.
# Do NOT overwrite installed superset package modules; instead register
# our small safe-shutdown handler via sitecustomize so it runs at Python
# startup in all processes (web, worker, beat) without replacing app objects.
COPY --chown=${CONTAINER_UID}:${CONTAINER_GID} ./overrides /app/overrides

# If a safe shutdown override exists, create a sitecustomize that imports it
# so Python will execute it on interpreter startup (sitecustomize is loaded
# when present on sys.path). This avoids replacing the installed
# superset.tasks.celery_app module and preserves the `app` object.
RUN if [ -f /app/overrides/superset_safe_shutdown.py ]; then \
			cat /app/overrides/superset_safe_shutdown.py > /app/sitecustomize.py; \
		fi

# Copy a local `superset_config.py` into the image so runtime processes
# load our environment-driven overrides (prevents falling back to SQLite).
COPY --chown=${CONTAINER_UID}:${CONTAINER_GID} ./superset_config.py /app/superset_config.py


# allow the runtime UID/GID and username to be provided at build-time
ARG CONTAINER_UID=1000
ARG CONTAINER_GID=1000
ARG CONTAINER_USER=superset

# ensure the runtime home dir exists
ENV SUPERSET_WORKDIR=/app/superset_home

# set ownership of venv and app to the numeric UID/GID
RUN mkdir -p ${SUPERSET_WORKDIR} \
	&& chown -R ${CONTAINER_UID}:${CONTAINER_GID} /app/.venv /app ${SUPERSET_WORKDIR} || true

ENV PATH="/app/.venv/bin:${PATH}"

# Create a named user inside the image with the supplied UID/GID if possible.
# We try to use `useradd`/`groupadd` when available; otherwise we append
# minimal entries to /etc/passwd and /etc/group as a fallback.
RUN if command -v groupadd >/dev/null 2>&1; then \
		groupadd -g ${CONTAINER_GID} ${CONTAINER_USER} 2>/dev/null || true; \
	else \
		grep -q "^${CONTAINER_USER}:" /etc/group || echo "${CONTAINER_USER}:x:${CONTAINER_GID}:" >> /etc/group; \
	fi \
	&& if command -v useradd >/dev/null 2>&1; then \
		useradd -u ${CONTAINER_UID} -g ${CONTAINER_GID} -d ${SUPERSET_WORKDIR} -m -s /bin/sh ${CONTAINER_USER} 2>/dev/null || true; \
	else \
		grep -q "^${CONTAINER_USER}:" /etc/passwd || echo "${CONTAINER_USER}:x:${CONTAINER_UID}:${CONTAINER_GID}::${SUPERSET_WORKDIR}:/bin/sh" >> /etc/passwd; \
	fi \
	&& mkdir -p ${SUPERSET_WORKDIR} \
	&& chown -R ${CONTAINER_UID}:${CONTAINER_GID} ${SUPERSET_WORKDIR} /app/.venv /app || true

# Set the default runtime user to the named user we created
USER ${CONTAINER_USER}:${CONTAINER_USER}
