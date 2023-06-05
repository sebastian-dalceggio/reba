from alembic.config import Config
from alembic import command
from pathlib import Path

def run_migrations(dsn):
    """
    Read the table models saved in the env.py file and compares it
    with the current database model. Then generate the transition script and run it.

    Parameters
    ----------
    dsn : script
        SQLAlchemy script connection to a database
    """
    alembic_cfg = Config()
    script_location = Path(__file__).parent / "migrations"
    alembic_cfg.set_main_option("script_location", str(script_location))
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    command.revision(alembic_cfg, autogenerate=True)
    command.upgrade(alembic_cfg, "head")