import logging
logger = logging.getLogger(__name__)

from dag_datalake_sirene.data_preprocessing.dirigeants_pm import preprocess_dirigeant_pm
from dag_datalake_sirene.data_preprocessing.dirigeants_pp import (
    preprocess_dirigeants_pp,
)

from dag_datalake_sirene.sqlite.sqlite_client import SqliteClient
from dag_datalake_sirene.sqlite.queries.helpers import (
    drop_table,
    get_distinct_column_count,
    create_index,
)
from dag_datalake_sirene.sqlite.queries.create_table_dirigeant_pp import (
    create_table_dirigeant_pp_query,
)

from dag_datalake_sirene.sqlite.queries.select_dirigeants_pp_from_db import (
    get_chunk_dirig_pp_from_db_query,
)
from dag_datalake_sirene.sqlite.queries.create_table_dirigeant_pm import (
    create_table_dirigeant_pm_query,
)
from dag_datalake_sirene.sqlite.queries.select_dirigeants_pm_from_db import (
    get_chunk_dirig_pm_from_db_query,
)


from dag_datalake_sirene.task_functions.global_variables import (
    SIRENE_DATABASE_LOCATION,
    DIRIG_DATABASE_LOCATION,
)


def create_dirig_pp_table():
    sqlite_client_siren = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client_siren.execute(drop_table("dirigeant_pp"))
    sqlite_client_siren.execute(create_table_dirigeant_pp_query)
    sqlite_client_siren.execute(create_index("siren_pp", "dirigeant_pp", "siren"))

    """ 
    # TODO : Use the inpi.db to fill this table
    sqlite_client_dirig = SqliteClient(DIRIG_DATABASE_LOCATION)
    chunk_size = int(100000)
    for row in sqlite_client_dirig.execute(
        get_distinct_column_count("rep_pp", "siren")
    ):
        nb_iter = int(int(row[0]) / chunk_size) + 1
    for i in range(nb_iter):
        query = sqlite_client_dirig.execute(
            get_chunk_dirig_pp_from_db_query(chunk_size, i)
        )
        dir_pp_clean = preprocess_dirigeants_pp(query)
        dir_pp_clean.to_sql(
            "dirigeant_pp",
            sqlite_client_siren.db_conn,
            if_exists="append",
            index=False,
        )
        logging.info(f"Iter: {i}")
    del dir_pp_clean
    sqlite_client_dirig.commit_and_close_conn() """

    sqlite_client_siren.commit_and_close_conn()


def create_dirig_pm_table():
    sqlite_client_siren = SqliteClient(SIRENE_DATABASE_LOCATION)

    # Create table dirigeants_pm in siren database
    sqlite_client_siren.execute(drop_table("dirigeant_pm"))
    sqlite_client_siren.execute(create_table_dirigeant_pm_query)
    sqlite_client_siren.execute(create_index("siren_pm", "dirigeant_pm", "siren"))

    """ 
    # TODO : import inpi.db with :
    sqlite_client_dirig = SqliteClient(DIRIG_DATABASE_LOCATION)
    chunk_size = int(100000)
    for row in sqlite_client_dirig.execute(
        get_distinct_column_count("rep_pm", "siren")
    ):
        nb_iter = int(int(row[0]) / chunk_size) + 1
    for i in range(nb_iter):
        query = sqlite_client_dirig.execute(
            get_chunk_dirig_pm_from_db_query(chunk_size, i)
        )
        dir_pm_clean = preprocess_dirigeant_pm(query)
        dir_pm_clean.to_sql(
            "dirigeant_pm", sqlite_client_siren.db_conn, if_exists="append", index=False
        )
        logging.info(f"Iter: {i}")
    del dir_pm_clean
    sqlite_client_dirig.commit_and_close_conn() """

    sqlite_client_siren.commit_and_close_conn()
