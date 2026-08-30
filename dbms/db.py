import os
from pathlib import Path

from mysql import connector
from mysql.connector import Error


def _load_env_file(path):
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


_load_env_file(Path(__file__).resolve().parent.parent / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "AEToluca")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE", "tipbank")

if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is not set. Copy .env.example to .env and fill in your password, "
        "or set the DB_PASSWORD environment variable."
    )

try:
    connection = connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
    )
    print("Connected to MySQL successfully.")
except Error:
    print("error connecting")
    raise
