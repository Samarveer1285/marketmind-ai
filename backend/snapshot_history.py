from providers import get_provider


def load_snapshot_history():
    """
    Full snapshot history across every category and date. snapshot_date now
    comes straight from the database column instead of being parsed back out
    of a CSV filename.
    """
    return get_provider().get_historical_snapshots()
