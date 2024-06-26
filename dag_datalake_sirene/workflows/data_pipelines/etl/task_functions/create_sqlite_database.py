import logging
import os
import shutil


from dag_datalake_sirene.helpers.sqlite_client import SqliteClient

from dag_datalake_sirene.config import (
    DATA_DIR,
    SIRENE_DATABASE_LOCATION,
)


def create_sqlite_database():
    if os.path.exists(DATA_DIR) and os.path.isdir(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.makedirs(os.path.dirname(DATA_DIR), exist_ok=True)
    if os.path.exists(SIRENE_DATABASE_LOCATION):
        os.remove(SIRENE_DATABASE_LOCATION)
        logging.info(
            f"******************** Existing database removed from "
            f"{SIRENE_DATABASE_LOCATION}"
        )
    logging.info("******************* Creating database! *******************")
    sqlite_client = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client.commit_and_close_conn()
