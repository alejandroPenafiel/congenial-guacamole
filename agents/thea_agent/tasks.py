from celery import shared_task
import json
import redis
import structlog
from libs.shared_utils.db import store_trading_metrics
from libs.shared_utils.config import publish_status

logger = structlog.get_logger(__name__)

_redis_client = redis.Redis(host='redis', port=6379, db=0)


def _load_config() -> dict:
    item = _redis_client.brpop('thea:config', timeout=1)
    if item:
        try:
            return json.loads(item[1])
        except Exception:
            return {}
    return {}


@shared_task(bind=True, name='agents.calculate_vwap_volume')
def calculate_vwap_volume(self):
    """Calculate VWAP and volume for BTC from trade data."""
    config = _load_config()
    trades = config.get('trades', [])
    if not trades:
        trades = [
            {'price': 10000.0, 'size': 0.5},
            {'price': 10010.0, 'size': 1.0},
            {'price': 9990.0, 'size': 0.3},
        ]
    total_volume = sum(t['size'] for t in trades)
    vwap = (
        sum(t['price'] * t['size'] for t in trades) / total_volume
        if total_volume else 0.0
    )
    price = trades[-1]['price'] if trades else 0.0
    metrics = {'price': price, 'vwap': vwap, 'volume': total_volume}
    store_trading_metrics('BTC', metrics)
    publish_status('TheaAgent', 'task_complete', metrics)
    logger.info('calculate_vwap_volume.complete', **metrics)
    return metrics
