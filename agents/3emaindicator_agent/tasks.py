from celery import shared_task
import structlog
from libs.shared_utils.config import get_agent_config, publish_status

logger = structlog.get_logger(__name__)

@shared_task(bind=True, name='agents.calculate_ema')
def calculate_ema(self, price_id):
    """Calculate EMA from price data (placeholder)."""
    config = get_agent_config('3EMAIndicatorAgent')
    if not config.get('enabled', True):
        logger.info("agent.disabled", agent="3EMAIndicatorAgent")
        return None
    logger.info("calculate_ema.start", price_id=price_id)
    result = {"price": 123.45, "ema": 123.00}
    publish_status("3EMAIndicatorAgent", "task_complete", result)
    return result
