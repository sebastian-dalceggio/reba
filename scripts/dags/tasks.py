from airflow.decorators import task
from docker.types import Mount
from config import DATA_PREPARATION_DOCKER_IMAGE, PROJECT_DIR, GCP_PROJECT

@task.docker(
    image=DATA_PREPARATION_DOCKER_IMAGE,
    mount_tmp_dir=False,
    mounts=[
        Mount(
            source=f"{PROJECT_DIR}/scripts/data_preparation/migrations/versions",
            target="/usr/local/lib/python3.8/site-packages/data_preparation/migrations/versions",
            type="bind",
        ),
        Mount(
            source=f"{PROJECT_DIR}/scripts/logs",
            target="/logger",
            type="bind",
        ),
    ],
    network_mode="airflow-nt"
)
def upgrade_tables(database_string):
    """
    Read the table models saved in the env.py file and compares it
    with the current database model. Then generate the transition script and run it.

    Parameters
    ----------
    database_string : script
        SQLAlchemy script connection to a database
    """
    from data_preparation.migrations.run_migrations import run_migrations
    run_migrations(database_string)
    


@task.docker(
    image=DATA_PREPARATION_DOCKER_IMAGE,
    network_mode="airflow-nt",
    private_environment={
        "GOOGLE_APPLICATION_CREDENTIALS": "/key_file/key_file.json",
        "GCLOUD_PROJECT": GCP_PROJECT
    },
    mounts=[
        Mount(
            source=f"{PROJECT_DIR}/../key_file",
            target="/key_file",
            type="bind",
        ),
        Mount(
            source=f"{PROJECT_DIR}/scripts/logs",
            target="/logger",
            type="bind",
        ),
    ],
)
def extract(url, bucket_name, month, year, file_name_xls):
    """
    It downloads a file from the url, saves it in tmp folder and then uploads it to gcp storage.

    Parameters
    ----------
    url : string
        url from where the file is downloaded
    bucket_name : string
        gcp bucket name
    month : string
        ipc data month, it is used to create a subfolder in the bucket
    year : string
        ipc data year, it is used to create a folder in the bucket
    file_name : string
        file name of the file
    """
    
    from data_preparation.process_data.getters import download
    from data_preparation.process_data.loaders import upload_to_gcp

    download(url, file_name_xls)
    upload_to_gcp(bucket_name, month, year, file_name_xls)

@task.docker(
    image=DATA_PREPARATION_DOCKER_IMAGE,
    network_mode="airflow-nt",
    private_environment={
        "GOOGLE_APPLICATION_CREDENTIALS": "/key_file/key_file.json",
        "GCLOUD_PROJECT": GCP_PROJECT
    },
    mounts=[
        Mount(
            source=f"{PROJECT_DIR}/../key_file",
            target="/key_file",
            type="bind",
        ),
        Mount(
            source=f"{PROJECT_DIR}/scripts/logs",
            target="/logger",
            type="bind",
        ),
    ],
)
def transform(bucket_name, month, year, file_name_xls, file_name_csv, sheet_name):
    """
    It downloads an Excel file from the bucket in the folder year/month, saves it in tmp/"file_name_xls", transforms it, saves the
    transformed dataframe in tmp/"file_name_csv" and then uploads it to gcp storage.

    Parameters
    ----------
    bucket_name : string
        gcp bucket name
    month : string
        ipc data month, it is used to create a subfolder in the bucket
    year : string
        ipc data year, it is used to create a folder in the bucket
    file_name_xls : string
        file name of the Excel file
    file_name_csv : string
        file name of the csv file
    sheet_name: string
        name of the Excel sheet
    """   
    from data_preparation.process_data.getters import download_from_gcp
    from data_preparation.process_data.loaders import upload_to_gcp
    from data_preparation.process_data.transformers import transform, fill_nan, test_dataset

    download_from_gcp(bucket_name, month, year, file_name_xls)
    df = transform(file_name_xls, sheet_name)
    df = fill_nan(df)
    test_dataset(df)
    df.to_csv("tmp/" + file_name_csv)
    upload_to_gcp(bucket_name, month, year, file_name_csv)

@task.docker(
    image=DATA_PREPARATION_DOCKER_IMAGE,
    network_mode="airflow-nt",
    private_environment={
        "GOOGLE_APPLICATION_CREDENTIALS": "/key_file/key_file.json",
        "GCLOUD_PROJECT": GCP_PROJECT
    },
    mounts=[
        Mount(
            source=f"{PROJECT_DIR}/../key_file",
            target="/key_file",
            type="bind",
        ),
        Mount(
            source=f"{PROJECT_DIR}/scripts/logs",
            target="/logger",
            type="bind",
        ),
    ],
)
def load(bucket_name, month, year, file_name_csv, database_type, database_name, database_host, database_user, database_password, database_driver):
    """
    It downloads an csv file from the bucket in the folder year/month, saves it in tmp/"file_name_csv" and loads it to
    the database.

    Parameters
    ----------
    bucket_name : string
        gcp bucket name
    month : string
        ipc data month, it is used to create a subfolder in the bucket
    year : string
        ipc data year, it is used to create a folder in the bucket
    file_name_csv : string
        file name of the csv file
    database_type : string
        database : type
    database_name: string
        database name
    database_host : string
        database host
    database_user : string
        database user
    database_password : string
        database password
    database_driver : string
        database driver
    """
    import pandas as pd
    from data_preparation.process_data.getters import download_from_gcp
    from data_preparation.process_data.loaders import load_to_database
    from data_preparation.database.client import ComplexClient
    from data_preparation.database.models import IndiceAperturas

    client = ComplexClient(database_type, database_name, database_host, database_user, database_password, database_driver)
    table_model = IndiceAperturas

    download_from_gcp(bucket_name, month, year, file_name_csv)
    df = pd.read_csv("tmp/" + file_name_csv)
    load_to_database(df, table_model, client, index=False)