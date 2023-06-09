import pandas as pd
from data_preparation.logger import get_logger

REGIONS = {"GBA": (5, 46),
           "Pampeana": (56, 44),
           "Noroeste": (105, 44),
           "Noreste": (154, 44),
           "Cuyo": (203,44),
           "Patagonia": (252,44)}

def transform(file_name, sheet_name, save_path=None):
    """
    It takes a sheet in the Excel file and returns a Pandas Dataframe with four columns: region, date, category and value.

    Parameters
    ----------
    file_name : string
        file name of the file
    sheet_name : string
        name of the sheet in the Excel file
    save_path : string, default None
        path where the csv file is saved

    Returns
    -------
    df : Pandas dataframe
        Returns the data as pandas dataframe
    """

    data = []

    for region, values in REGIONS.items():

        df = pd.read_excel("tmp/" + file_name, sheet_name=sheet_name, skiprows=values[0], nrows=values[1])

        df.dropna(inplace=True) #drops na rows

        df_melted = df.melt(id_vars=df.columns[[0]], var_name="date", value_name="value") # pivot date columns into rows
        df_melted["region"] = region
        df_melted.columns.values[0] = "category"
        df_melted["value"] = pd.to_numeric(df_melted["value"], errors='coerce')
        df_melted["date"] = pd.to_datetime(df_melted["date"], errors='coerce')
        data.append(df_melted)

    df = pd.concat(data)

    if save_path:
        df.to_csv(save_path)
    return df

def fill_nan(df):
    """
    It takes a dataframe and fills null values using interpolation.

    Parameters
    ----------
    df : Pandas dataframe
        dataframe to fill

    Returns
    -------
    df_filled : Pandas dataframe
        Returns the filled dataframe
    """
    df = df.sort_values(["category", "region", "date"])
    df = df.sort_index()
    df_filled = df.groupby(["category", "region"]).apply(lambda x: x.set_index("date").interpolate(method="index").reset_index()).reset_index(drop=True)
    return df_filled

def test_dataset(df):
    """
    It takes a dataframe and checks if it has duplicated or null values.

    Raise
    ----------
    Custom Exceptions
    
    """
    logger = get_logger(test_dataset.__name__)

    duplicated = df[["category", "region", "date"]].duplicated().any()

    if duplicated:
        e = Exception("The dataset has duplicated values.")
        logger.error(f"Exception: {e}")
        raise e
    
    contains_nulls = df.isnull().values.any()

    if contains_nulls:
        e = Exception("The dataset contains null values.")
        logger.error(f"Exception: {e}")
        raise e

    