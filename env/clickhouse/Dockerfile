FROM clickhouse/clickhouse-server:latest

# Copy optional custom config fragments (if present)
COPY config.d/ /etc/clickhouse-server/config.d/
COPY users.d/ /etc/clickhouse-server/users.d/

# Ensure config ownership (best-effort)
USER root
RUN if [ -d /etc/clickhouse-server/config.d ]; then chown -R clickhouse:clickhouse /etc/clickhouse-server/config.d; fi || true
RUN if [ -d /etc/clickhouse-server/users.d ]; then chown -R clickhouse:clickhouse /etc/clickhouse-server/users.d; fi || true

USER clickhouse

EXPOSE 8123 9000

# Use upstream image's default entrypoint/cmd