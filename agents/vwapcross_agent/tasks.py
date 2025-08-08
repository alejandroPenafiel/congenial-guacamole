from celery import shared_task
import structlog
from libs.shared_utils.config import publish_status

logger = structlog.get_logger(__name__)


@shared_task(bind=True, name='agents.check_vwap_cross')
def check_vwap_cross(self, data):
    """Detect if VWAP has crossed the latest price."""
    price = data.get('price')
    vwap = data.get('vwap')
    crossed = False
    if price is not None and vwap is not None:
        crossed = price > vwap
    publish_status('VwapCrossAgent', 'task_complete', {'cross': crossed})
    logger.info('check_vwap_cross.complete', price=price, vwap=vwap, cross=crossed)
    return crossed
