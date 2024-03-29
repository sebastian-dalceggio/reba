# REBA

Este proyecto procesa un excel con datos de la inflación acumulada desde 2016, descargándolo de la web del Indec y cargando los datos transformados en una base de datos.

### Justificación

Para orquestrar todo el proceso utilicé Airflow. Hay un único dag compuesto por cuatro tareas:

1. upgrade_tables: usando Alembic se actualiza el modelo de la tabla en la base de datos
2. extract: se descarga el archivo Excel con los datos y se lo almacena en GCP
3. transform: se descarga de GCP el archivo Excel, se lo transforma para que adopte un formato adecuado y se lo carga en GCP como csv
4. load: se toma el archivo csv de GCP y se lo carga en la base de datos

Para realizar todas las operaciones armé un paquete de Python (data_preparation) usando Poetry. Este paquete se instala en una imagen de docker (data_preparation:0.1.0). Cada tarea de Airflow levanta un contenedor con esta imagen y ejecuta todas las tareas en un ambiente separado del de
Airflow. De esta forma no entran en conflicto los paquetes necesarios para las tareas con los propios del ambiente de Airflow.

La base de datos utilizada es SQL Server. Modifiqué la imagen de Docker original agregando un script de bash para que cree la base de datos ipc_database
cuando se levanta el servicio.

Para crear el storage en GCP utilicé Terraform. El bucket se divide en subcarpetas con un formato año/mes.

El proceso de tranformación de los datos es el siguiente:

1. Se abre el excel con Pandas
2. Se testea que cada subtabla de cada región cumpla con los patrones preestablecidos.
3. Se toma cada tabla de cada región de forma separada
4. Se pivotean las fechas para que haya una única fila por fecha, categoría
5. Se agrega una columna con la región
6. Se concatenan todas las tablas
7. Se rellenan los valores faltantes interpolando respetando la categoría y región
8. Se testea que no haya valore nulos ni filas repetidas

Para correr crear y correr el stored procedure hay que entrar al contenedor del servidor de SQL Server y correr los siguientes comandos:

    ```
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P Password123! -i query.sql
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P Password123! -Q "USE ipc_database; EXECUTE interanual @Region='GBA'"
    ```

El stored procedure se encuentra en ./scripts/docker_images/sql_server_image/query.sql

### Instrucciones

En ./terraform

1. En el directorio "../key_file/" guardar el archivo de credenciales de GCP con el nombre key_file.json
2. Crear la infraestructura en GCP:

    ```
    terraform init
    terraform apply --auto-approve
    ```

En ./

3. Crear las imágenes necesarias y levantar los contenedores para correr Airflow y la base de datos:
    ```
    docker-compose up --build
    ```

En el explorador entrar a localhost:8080

4. Correr el dag
