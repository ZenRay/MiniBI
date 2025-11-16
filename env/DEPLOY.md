
# Superset 本地 Docker Compose 部署说明（简要）

本文档简要记录当前项目 (`env` 目录下) 使用 Docker Compose 部署 Apache Superset 的可复现步骤、常用命令与注意事项。

快速步骤（在 `env` 目录下执行）：

- 构建本地 Superset 镜像（镜像使用清华 PyPI 加速）：

```bash
docker compose build --pull --no-cache superset-init superset superset-worker superset-beat
```

- 启动依赖服务（Postgres、Redis）：

```bash
docker compose up -d postgres redis
```

- 初始化 Superset（运行 Alembic 迁移并创建管理员账号）：

```bash
docker compose run --rm --no-deps superset-init
```

- 启动 Superset web、worker、beat：

```bash
docker compose up -d superset superset-worker superset-beat
```

- 健康检查：

```bash
curl -f http://localhost:8088/health
# 或在容器内用 API 登录并验证：
curl -s -X POST "http://localhost:8088/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin","provider":"db","refresh":true}'
```

停止与清理（会删除本地构建镜像与命名卷）：

```bash
docker compose down --rmi local -v --remove-orphans
```

重要文件说明：

- `docker-compose.yml`：Compose 服务定义（superset, superset-init, worker, beat, postgres, redis）。
- `docker/superset_config.py`：挂载到容器的 Superset 配置，用于覆盖默认的 SQLALCHEMY 配置，确保连接到 Postgres。
- `docker/Dockerfile`：本地派生镜像，已在构建时创建 `/app/.venv` 并安装 `psycopg2-binary`，同时使用清华 PyPI 镜像以加速构建。

建议与注意事项：

- 把敏感信息（`SUPERSET_SECRET_KEY`、`POSTGRES_PASSWORD`）从版本控制中移除，使用 CI/密钥管理或 Docker secret。请不要把真实密码写入公开仓库。
- 在生产环境使用反向代理（nginx/traefik）、启用 TLS，并把 Superset 后端和数据库放入受管网络/私有子网中。
- 如果迁移已有数据，请先备份命名卷（或 Postgres 数据）再运行 `superset-init`。示例：`docker compose exec postgres pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > backup.sql`。

故障排查快速命令：

- 查看服务和健康状态：
  `docker compose ps`
- 查看 superset 日志：
  `docker compose logs -f superset`
- 在容器内执行交互命令：
  `docker compose exec -T superset /bin/sh -c "python3 -c 'import superset; print(\"ok\")'"`

常见后续动作：

- 更改管理员密码（容器内执行 SQL 或使用 superset CLI 修改）：
  `docker compose exec superset superset fab reset-password --username admin --password NEWPASSWORD`（如果镜像包含 superset CLI）或通过数据库直接更新 `ab_user`。

如果需要，我可以把此 README 合并到仓库根目录或生成更详尽的生产部署文档（含 systemd / k8s 配置示例）。

---
作者：自动化部署脚本（由 Copilot 协助生成）
