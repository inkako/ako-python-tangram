# ako-python-tangram
A Tangram for an AMP-Based Python Web Project.Tangram is a modular toolkit for web apps, and it's built on the AMP stack — API, Modules, and Platform.

## 项目常见三方库
- 数据库类：sqlalchemy, asyncpg, psycopg, aiomysql, pymongo, motor
- 网络类：urllib3, requests, httpx, aiohttp, httplib2
- 缓存类：redis, aiomcache, pymemcache, django-redis
- 消息队列：celery, kombu, taskiq, pika, confluent-kafka
- 云 SDK：boto3, google-cloud-*, azure-core
- 其他常见：uvicorn, gunicorn, watchfiles, paramiko

## 数据库迁移 Migration
- 初始化 Alembic：uv run alembic init -t async migrations
- 配置 alembic.ini：把 sqlalchemy.url 那行注释掉或删掉（因为你会在 env.py 里动态配置）
- 修改 env.py：让 Alembic 使用项目的数据库配置、模型元数据及模型
- 运行迁移命令：
  - 生成迁移文件：uv run alembic revision --autogenerate -m "msg"
  - 执行迁移：uv run alembic upgrade head

### 常用迁移命令
| 命令 | 含义 |
|---|---|
| `alembic upgrade head` | 升级到最新版本 |
| `alembic upgrade +1` | 只往前迁移一步 |
| `alembic downgrade -1` | 回退一步 |
| `alembic downgrade base` | 回退到初始状态（所有表删除） |
| `alembic upgrade abc1234` | 升级到指定版本（迁移文件的 revision id） |
| `alembic current` | 查看当前数据库处于哪个版本 |
| `alembic history` | 查看所有迁移历史 |

### 迁移模式
> 有无 --sql 参数决定了迁移模式
#### 离线模式
`以离线模式输出 SQL 脚本：uv run alembic upgrade head --sql > migration.sql`
#### 在线模式
`直接连接数据库执行迁移：uv run alembic upgrade head`