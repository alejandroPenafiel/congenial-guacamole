from celery import Celery

app = Celery(
    'trading_engine',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1',
    include=[
        'agents.apiprice_agent.tasks',
        'agents.3emaindicator_agent.tasks',
        'agents.bangstate_agent.tasks',
        'agents.thea_agent.tasks',
        'agents.vwapcross_agent.tasks',
    ],
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

app.conf.task_routes = {
    'agents.apiprice_agent.tasks.*': {'queue': 'price_queue'},
    'agents.3emaindicator_agent.tasks.*': {'queue': 'indicator_queue'},
    'agents.bangstate_agent.tasks.*': {'queue': 'bang_queue'},
    'agents.thea_agent.tasks.*': {'queue': 'thea_queue'},
    'agents.vwapcross_agent.tasks.*': {'queue': 'vwapcross_queue'},
}
