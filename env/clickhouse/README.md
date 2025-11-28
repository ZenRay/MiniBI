# ClickHouse 镜像构建与使用说明

简要说明如何构建并使该 ClickHouse 容器被两个 Compose 项目访问（`env` 下的 Superset 与 `dispatcher` 下的 Airflow）。

1) 构建镜像

```bash
docker build -t local/clickhouse:latest -f env/clickhouse/Dockerfile ./env/clickhouse
```

2) 创建一个共享的用户网络（只需执行一次）

```bash
docker network create analytics_net
```

3) 运行 ClickHouse 容器并加入共享网络

```bash
docker run -d --name clickhouse_server \
  --network analytics_net \
  -p 9000:9000 -p 8123:8123 \
  -v clickhouse_data:/var/lib/clickhouse \
  local/clickhouse:latest
```

4) 在 Compose 中使用该外部网络（示例）

在 `env/docker-compose.yml` 与 `dispatcher/docker-compose.yml` 中，把 networks 下对应网络改为指向外部网络，例如：

```yaml
networks:
  superset_network:
    external:
      name: analytics_net

# dispatcher/docker-compose.yml 中类似：
networks:
  airflow-network:
    external:
      name: analytics_net
```

这样两个 Compose 项目的服务都能通过容器名 `clickhouse_server` 在内部网络上互相访问，Superset 连接字符串可以使用 `clickhouse://default@clickhouse_server:9000/<db>`（取决于你的 ClickHouse 驱动配置）。

注意：
- 若不想修改现有 Compose 网络名，也可以在两个 Compose 中添加一个额外的 `analytics_net` network 并声明为 `external: true`。
- `depends_on` 对外部容器无效；需保证 ClickHouse 在 Superset/Airflow 启动前已经可用（可用 healthcheck/wait-for 脚本）。
- 在生产环境中，请配置用户密码与访问控制，避免空密码。
