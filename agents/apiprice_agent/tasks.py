from celery import shared_task
import structlog
from libs.shared_utils.config import publish_status

logger = structlog.get_logger(__name__)

@shared_task(bind=True, name='agents.fetch_price')
def fetch_price(self):
    """Fetch latest price data and store in PostgreSQL (placeholder)."""
    logger.info("fetch_price.start", task_id=self.request.id)
    price_id = 1
    publish_status("ApiPriceAgent", "task_complete", {"price_id": price_id})
    return price_id
