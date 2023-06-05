from decouple import AutoConfig

dconfig = AutoConfig()

DATA_PREPARATION_DOCKER_IMAGE = dconfig("DATA_PREPARATION_DOCKER_IMAGE")
DATABASE_TYPE = dconfig("DATABASE_TYPE")
DATABASE_USER = dconfig("DATABASE_USER")
DATABASE_PASSWORD = dconfig("DATABASE_PASSWORD")
DATABASE_HOST = dconfig("DATABASE_HOST")
DATABASE_NAME = dconfig("DATABASE_NAME")
DATABASE_STRING = f"{DATABASE_TYPE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"