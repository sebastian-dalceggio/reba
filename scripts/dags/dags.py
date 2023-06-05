from airflow.decorators import dag
import pendulum
from dags.tasks import run_migrations
from dags.config import DATABASE_STRING

@dag(
    schedule=None,
    start_date=pendulum.datetime(2022, 11, 1, 1, 0, 0, tz="America/Argentina/Buenos_Aires"),
    catchup=True,
    max_active_runs=1,
)
def data_preparation_dag(database_string):

    run_migrations_r = run_migrations(database_string)

    run_migrations_r

database_string = DATABASE_STRING

data_preparation_dag(database_string)