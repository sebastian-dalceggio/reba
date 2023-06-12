from google.cloud import storage
from data_preparation.logger import get_logger

def upload_to_gcp(bucket_name, month, year, file_name):
    """
    It takes a file with the name file_name from the tmp directory and uploads it to gcp storage.

    Parameters
    ----------
    bucket_name : string
        gcp bucket name
    month : string
        ipc data month
    year : string
        ipc data year
    file_name : string
        file name of the file
    """
    logger = get_logger(upload_to_gcp.__name__)

    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(year + "/" + month + "/" + file_name)
        blob.upload_from_filename("tmp/" + file_name)
        logger.info(f"The file was loaded into GCP and saved in tmp/{file_name}")
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise e

def load_to_database(dataframe, table_model, client, index=False):
    """
    It loads a dataframe into a database.
    
    Parameters
    ----------
    dataframe : Pandas dataframe
        Pandas dataframe to be load to the database
    table_model: SQAlchemy _DeclarativeBase
        Table model of the table where the dataframe is to be inserted.
    client : SqlClient
        Database client.
    index : bool, default False
        if the datafrme index is loaded to the database
    """
    logger = get_logger(load_to_database.__name__)
    try:
        client.insert_dataframe(dataframe, table_model.__tablename__, if_exists="replace", index=index)
        number_of_rows = dataframe.shape[0]
        logger.info(f"{number_of_rows} records was loaded into the database")
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise e