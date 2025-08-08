# Dynamic, Hot-Reloadable, Agent-Based System

This repository outlines an architecture for a modular, event-driven system built with **Python**, **Celery**, **Redis**, and **PostgreSQL**.  The design focuses on rapid development, isolated services, and real-time communication.

## 1. Monorepo Layout
```
/
├── agents/
│   ├── postgressdatabase_agent/
│   ├── apiprice_agent/
│   ├── 3emaindicator_agent/
│   └── bangstate_agent/
├── libs/
│   ├── shared_models/
│   └── shared_utils/
├── infra/
│   ├── docker/
│   └── supervisord.conf
├── trigger/
├── frontend_gateway/
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```
The monorepo enables atomic commits and shared dependency management.  Agents consume common models and utilities via editable, path-based installs.

## 2. Core Technologies
* **PostgreSQL** – durable system of record.
* **Redis** – Celery broker, runtime configuration store, Pub/Sub bus, and cache.
* **Celery** – asynchronous task execution with per-agent queues.

## 3. Celery Application & Workflow
A single Celery app discovers tasks in each agent.  `task_routes` directs tasks to dedicated queues:
```python
app.conf.task_routes = {
    "agents.apiprice_agent.tasks.*": {"queue": "price_queue"},
    "agents.3emaindicator_agent.tasks.*": {"queue": "indicator_queue"},
    "agents.bangstate_agent.tasks.*": {"queue": "bang_queue"},
}
```
Tasks are chained to create the workflow:
1. `fetch_price` – stores prices in PostgreSQL.
2. `calculate_ema` – computes the 3‑EMA indicator.
3. `check_for_bang` – records events when crossovers occur.

## 4. Logging and Observability
All services emit JSON logs using **structlog**.  A consistent schema captures timestamps, log level, logger name, task id, duration, and structured exception data.

## 5. Dynamic Control
* **supervisord** manages Celery workers and supporting processes.
* Runtime flags in Redis allow enabling/disabling specific agent behaviour without restarts.

## 6. Hot Reloading in Containers
Docker Compose runs each agent in its own container.  Source code is mounted as a volume and `watchmedo auto-restart` wraps the worker command, restarting the process when Python files change.  Only the modified agent is reloaded.

## 7. Frontend Data Delivery
* **Redis Pub/Sub** broadcasts agent status updates to a FastAPI WebSocket gateway.
* Historical chart data uses a cache‑aside strategy: Redis caches expensive PostgreSQL queries.

## 8. Next Steps
The design can evolve with orchestration via Kubernetes, high availability for Redis/PostgreSQL, and a CI/CD pipeline.

