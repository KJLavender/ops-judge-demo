def total(prices: list[float], tax_rate: float = 0.05) -> float:
    """Order total with tax, rounded to cents."""
    return round(sum(prices) * (1 + tax_rate), 2)
