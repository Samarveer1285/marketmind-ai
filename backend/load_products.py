from providers import get_provider


def get_latest_market_data():
    """
    Each category's most recent snapshot only (not full history) — matches
    this function's original intent. Previously this glob'd CSV filenames and
    picked whichever file glob.glob() happened to return last per keyword,
    which wasn't reliably the most recent date; the provider's
    get_latest_snapshot() fixes that by actually comparing snapshot_date.
    """
    data = get_provider().get_latest_snapshot()

    if data.empty:
        return data

    if "fetched_at" in data.columns:
        print("Latest Fetch Time:", data["fetched_at"].max())
    print("Total Products:", len(data))

    return data
