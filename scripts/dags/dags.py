from airflow.decorators import dag
import pendulum
from tasks import upgrade_tables, extract, transform, load
from config import DATABASE_STRING, GCP_PROJECT, URL_FILE, FILE_NAME_XLS, FILE_NAME_CSV, BUCKET_NAME, MONTH, YEAR, SHEET_NAME, DATABASE_TYPE, DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_DRIVER

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 6, 1, 1, 0, 0, tz="America/Argentina/Buenos_Aires"),
    catchup=True,
    max_active_runs=1,
)
def etl(database_string, url, bucket_name, month, year, file_name_xls, project, file_name_csv, sheet_name, database_type, database_name, database_host, database_user, database_password, database_driver):
    """
    Extract, transform and load inflation data into a database.

    Parameters
    ----------
    database_string : script
        SQLAlchemy script connection to a database
    url : string
        url from where the file is downloaded
    bucket_name : string
        gcp bucket name
    month : string
        ipc data month, it is used to create a subfolder in the bucket
    year : string
        ipc data year, it is used to create a folder in the bucket
    file_name_xls : string
        file name of the Excel file
    project : string
        gpc project
    file_name_csv : string
        file name of the csv file
    sheet_name: string
        name of the Excel sheet
    database_type string
        database type
    database_name: string
        database name
    database_host: string
        database host
    database_user: string
        database user
    database_password: string
        database password
    database_driver: string
        database driver
    """
    upgrade_tables_r = upgrade_tables(database_string)

    upload_r = extract(url, bucket_name, month, year, file_name_xls, project)

    transform_r = transform(bucket_name, month, year, file_name_xls, file_name_csv, project, sheet_name)
    
    load_r = load(bucket_name, month, year, file_name_csv, project, database_type, database_name, database_host, database_user, database_password, database_driver)
    
    upgrade_tables_r >> upload_r >> transform_r >> load_r

database_string = DATABASE_STRING
database_type = DATABASE_TYPE
database_name = DATABASE_NAME
database_host = DATABASE_HOST
database_user = DATABASE_USER
database_password = DATABASE_PASSWORD
database_driver = DATABASE_DRIVER
url = URL_FILE
file_name_xls = FILE_NAME_XLS
file_name_csv = FILE_NAME_CSV
bucket_name = BUCKET_NAME
project = GCP_PROJECT
month = MONTH
year = YEAR
sheet_name = SHEET_NAME


etl(database_string, url, bucket_name, month, year, file_name_xls, project, file_name_csv, sheet_name, database_type, database_name, database_host, database_user, database_password, database_driver)