import requests
from google.cloud import storage
from data_preparation.logger import get_logger


def download(url, file_name):
    """
    It downloads a file from the url passed and saves it with the name file_name.

    Parameters
    ----------
    url : string
        url from where the file is downloaded
    file_name : string
        file name of the file
    """
    logger = get_logger(download.__name__)
    try:
        response = requests.get(url)
        with open("tmp/" + file_name, "wb") as f:
            f.write(response.content)
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise e


def download_from_gcp(bucket_name, month, year, file_name):
    """
    It downloads a file from the url passed and saves it with the name file_name.

    Parameters
    ----------
    bucket_name : string
        url from where the Excel file is downloaded
    month : string
        ipc data month, it is used to create a subfolder in the bucket
    year : string
        ipc data year, it is used to create a folder in the bucket
    file_name : string
        file name of the file

    """
    logger = get_logger(download_from_gcp.__name__)
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(year + "/" + month + "/" + file_name)
        blob.download_to_filename("tmp/" + file_name)
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise e
