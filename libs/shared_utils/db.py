TRADING_METRICS = []


def store_trading_metrics(symbol: str, metrics: dict) -> None:
    """Store trading metrics in memory (placeholder for DB)."""
    TRADING_METRICS.append({'symbol': symbol, **metrics})


def query_historical_data(symbol: str, timeframe: str, start: str, end: str):
    """Return stored trading metrics (placeholder for DB query)."""
    return [m for m in TRADING_METRICS if m['symbol'] == symbol]
