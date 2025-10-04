import datetime as dt

DEFAULT_CURRENT_TIMESTAMP = lambda: int(dt.datetime.now(dt.timezone.utc).timestamp())