#https://github.com/microsoft/mssql-docker/tree/master/linux/preview/examples/mssql-customize

FROM mcr.microsoft.com/mssql/server:2017-latest

# Create a config directory
RUN mkdir -p /usr/config
WORKDIR /usr/config

# Bundle config source

COPY . .
# Grant permissions for to our scripts to be executable
USER root
RUN chmod +x entrypoint.sh
RUN chmod +x configure-db.sh

ENTRYPOINT ["./entrypoint.sh"]