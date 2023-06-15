from alembic.config import Config
from alembic import command
from pathlib import Path


def run_migrations(database_string):
    alembic_cfg = Config()
    script_location = Path(__file__).parent
    alembic_cfg.set_main_option("script_location", str(script_location))
    alembic_cfg.set_main_option("sqlalchemy.url", database_string)
    command.revision(alembic_cfg, autogenerate=True)
    command.upgrade(alembic_cfg, "head")
