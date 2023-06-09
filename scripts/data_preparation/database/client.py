import abc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SqlClient():
    """
    Abstract class used as a client of a database.
    This is an abstract class. For each database type there is a class that inherits this one.
    ...

    Attributes
    ----------
    database_type : {"sqlite", "postgresql", "mssql+pyodbc"}
        Database type.
    database_name : string
        Database name.
    host : string
        Database host.
    user : string
        Database user.
    password : string
        Database password.
    driver : string
        Database driver.
    _engine : SQLAlchemy engine
        SQLAlchemy engine to operate with the database.
    ...
    Methods
    -------
    _get_engine()
        Creates and returns an engine to be used to interact with the database.
    get_session()
        Returns an session to be used to interact with the database.
    get_dataframe(query)
        Return a table as a Pandas dataframe.
    """

    def __init__(
        self, database_type, database_name, host=None, user=None, password=None, driver=None
    ):
        """
        Parameters
        ----------
        database_type : {"sqlite", "postgresql", "mssql+pyodbc"}
            Database type.
        database_name : string
            Database name.
        host : string, default None
            Database host.
        user : string, default None
            Database user.
        password : string, default None
            Database password.
        driver : string, default None
            Database driver.
        """
        self.database_type = database_type
        self.database_name = database_name
        self.host = host
        self.user = user
        self.password = password
        self.driver = driver
        self._engine = None

    @abc.abstractmethod
    def _get_engine(self):
        """
        Returns
        -------
        engine : SQLAlchemy engine
            Return the client engine.
        """

    def get_session(self):
        """
        Returns
        -------
        session : SQLAlchemy session
            Return a SQLAlchemy session.
        """
        if not self._engine:
            self._engine = self._get_engine()
        return sessionmaker(self._engine)

    def get_dataframe(self, query, index_col=None, parse_dates=None):
        """
        Parameters
        ----------
        query : string
            Query to send to the database.

        Returns
        -------
        df : Pandas dataframe
            Result of the query as a Pandas dataframe
        """
        if not self._engine:
            self._engine = self._get_engine()
        return pd.read_sql(query, self._engine, index_col=index_col, parse_dates=parse_dates)

    def insert_dataframe(self, dataframe, table_name, if_exists="fail", index=False):
        """
        Parameters
        ----------
        dataframe : Pandas dataframe
            Dataframe to be loaded
        table_name : string
            Query to send to the database.
        if_exists : {"fail", "replace", "append"}, default "fail"
            How to behave if the table already exists.
        index : bool, default False
            if the datafrme index is loaded to the database
        """
        if not self._engine:
            self._engine = self._get_engine()
        return dataframe.to_sql(table_name, self._engine, if_exists=if_exists, index=index)
    
class ComplexClient(SqlClient):
    def _get_engine(self):
        db_uri = f"{self.database_type}://{self.user}:{self.password}@{self.host}/{self.database_name}{''if not self.driver else f'?driver={self.driver}'}"
        if not self._engine:
            self._engine = create_engine(db_uri)
        return self._engine

class SqLiteClient(SqlClient):
    def _get_engine(self):
        db_uri = f"{self.database_type}:///{self.database_name}"
        if not self._engine:
            self._engine = create_engine(db_uri)
        return self._engine