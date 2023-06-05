#!/bin/bash

echo "Waiting for SQL Server to initialize..."

until /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $MSSQL_SA_PASSWORD -Q "SELECT 1" &>/dev/null; do
    sleep 1
    echo "Waiting for SQL Server to initialize..."
done

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $MSSQL_SA_PASSWORD -d master -i setup.sql;