import logging
logger = logging.getLogger(__name__)


from dag_datalake_sirene.sqlite.sqlite_client import SqliteClient
from dag_datalake_sirene.sqlite.queries.helpers import (
    drop_table,
    get_table_count,
)

from dag_datalake_sirene.task_functions.global_variables import (
    SIRENE_DATABASE_LOCATION,
    DATA_DIR,
)


def create_and_fill_table_model(
    table_name,
    create_table_query,
    create_index_func,
    index_name,
    index_column,
    preprocess_table_data,
):
    sqlite_client = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client.execute(drop_table(table_name))
    sqlite_client.execute(create_table_query)
    sqlite_client.execute(create_index_func(index_name, table_name, index_column))
    df_table = preprocess_table_data(data_dir=DATA_DIR)
    df_table.to_sql(table_name, sqlite_client.db_conn, if_exists="append", index=False)
    del df_table
    for row in sqlite_client.execute(get_table_count(table_name)):
        logging.info(
            f"************ {row} total records have been added to the "
            f"{table_name} table!"
        )
    sqlite_client.commit_and_close_conn()


def create_table_model(
    table_name,
    create_table_query,
    create_index_func,
    index_name,
    index_column,
):
    sqlite_client = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client.execute(drop_table(table_name))
    sqlite_client.execute(create_table_query)
    sqlite_client.execute(create_index_func(index_name, table_name, index_column))
    return sqlite_client
