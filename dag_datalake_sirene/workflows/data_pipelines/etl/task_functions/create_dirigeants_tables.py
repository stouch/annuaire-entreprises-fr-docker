import logging

# fmt: off
from dag_datalake_sirene.workflows.data_pipelines.etl.data_fetch_clean.dirigeants\
    import (
    preprocess_dirigeant_pm,
    preprocess_dirigeants_pp,
)
# fmt: on
from dag_datalake_sirene.helpers.sqlite_client import SqliteClient

from dag_datalake_sirene.workflows.data_pipelines.etl.sqlite.helpers import (
    drop_table,
    get_distinct_column_count,
    create_index,
)
from dag_datalake_sirene.workflows.data_pipelines.etl.sqlite.queries.dirigeants import (
    create_table_dirigeant_pp_query,
    create_table_dirigeant_pm_query,
    get_chunk_dirig_pp_from_db_query,
    get_chunk_dirig_pm_from_db_query,
)

from dag_datalake_sirene.config import (
    SIRENE_DATABASE_LOCATION,
)


def create_dirig_pp_table():
    sqlite_client_siren = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client_siren.execute(drop_table("dirigeants_pp"))
    sqlite_client_siren.execute(create_table_dirigeant_pp_query)
    sqlite_client_siren.execute(create_index("siren_pp", "dirigeants_pp", "siren"))
    sqlite_client_siren.commit_and_close_conn()


def create_dirig_pm_table():
    sqlite_client_siren = SqliteClient(SIRENE_DATABASE_LOCATION)
    # Create table dirigeants_pm in siren database
    sqlite_client_siren.execute(drop_table("dirigeants_pm"))
    sqlite_client_siren.execute(create_table_dirigeant_pm_query)
    sqlite_client_siren.execute(create_index("siren_pm", "dirigeants_pm", "siren"))
    sqlite_client_siren.commit_and_close_conn()
