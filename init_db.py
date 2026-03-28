"""
Database initialisation via Alembic migrations.

Run:  python init_db.py
"""
from alembic import command
from alembic.config import Config


def init_db() -> None:
    alembic_cfg = Config("alembic.ini")
    print("Running Alembic migrations to head...")
    command.upgrade(alembic_cfg, "head")
    print("Database initialised successfully.")


if __name__ == "__main__":
    init_db()
