from airflow.decorators import task
from docker.types import Mount
from dags.config import DATA_PREPARATION_DOCKER_IMAGE, PROJECT_DIR

@task.docker(
    image=DATA_PREPARATION_DOCKER_IMAGE,
    mount_tmp_dir=False,
    mounts=[
        Mount(
            source="script/data_preparation/migrations/versions",
            target="/usr/local/lib/python3.8/site-packages/data_preparation/migrations/versions",
            type="bind",
        ),
    ],
)
def upgrade_tables(database_string):
    from data_preparation.dags_functions import run_migrations
    run_migrations(database_string)