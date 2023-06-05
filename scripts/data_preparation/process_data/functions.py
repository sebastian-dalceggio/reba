import pandas as pd
import requests

def download(url, save_path):
    """
    It downloads an Excel file from the url passed and save it in path.

    Parameters
    ----------
    url : string
        url from where the Excel file is downloaded
    path : string
        path where the Excel file is saved
    """
    response = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(response.content)


def transform(load_path, sheet_name, regions, save_path=None):
    """
    It takes a sheet in the Excel file and returns a Pandas Dataframe with four columns: region, date, category and value.

    Parameters
    ----------
    path_to_load : string
        path from where the csv file is loaded
    sheet_name : string
        name of the sheet in the Excel file
    regions : dict
        dict with the first row and number of row of each region
    path_to_save : string
        path where the csv file is saved

    Returns
    -------
    df : Pandas dataframe
        Returns the data as pandas dataframe
    """

    data = []
    for region, values in regions.items():
        df = pd.read_excel(load_path, sheet_name=sheet_name, skiprows=values[0], nrows=values[1])
        df.dropna(inplace=True)
        df_melted = df.melt(id_vars=df.columns[[0]], var_name="date", value_name="value")
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
    df_filled = df.copy()
    df_grouped = df.groupby(["region", "category"])
    df_filled["value"] = df_grouped["value"].apply(lambda x: x.interpolate()).reset_index()["value"]
    return df_filled

def load_to_database(dataframe, table_model, client, keep_index=False):
    """
    It loads a dataframe into a database.
    
    Parameters
    ----------
    dataframe : Pandas dataframe
        Pandas dataframe to be load to the database
    table_model: SQAlchemy _DeclarativeBase
        Table model of the table where the dataframe is to be inserted.
    client : Client
        Database client.
    """
    client.insert_dataframe(dataframe, table_model.__name__, if_exists="replace")

    