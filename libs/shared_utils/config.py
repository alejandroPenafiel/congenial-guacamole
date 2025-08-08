import json
import redis

_config_client = redis.Redis(host='redis', port=6379, db=0)


def get_agent_config(agent_name: str) -> dict:
    """Retrieve dynamic configuration for an agent from Redis."""
    raw = _config_client.hgetall('agent:configs')
    config = {}
    prefix = f"{agent_name}:"
    for key, value in raw.items():
        key = key.decode()
        if key.startswith(prefix):
            param = key[len(prefix):]
            try:
                config[param] = json.loads(value.decode())
            except Exception:
                config[param] = value.decode()
    return config


def publish_status(agent_name: str, event: str, data: dict) -> None:
    """Publish an agent status update to the Redis Pub/Sub channel."""
    message = {
        'source': agent_name,
        'event': event,
        'payload': data,
    }
    _config_client.publish('agent-events', json.dumps(message))
