import logging
import sqlite3

from dag_datalake_sirene.helpers.labels.departements import all_deps
from dag_datalake_sirene.helpers.sqlite_client import SqliteClient

# fmt: off
from dag_datalake_sirene.workflows.data_pipelines.etl.data_fetch_clean.etablissements\
    import (
        preprocess_etablissement_data,
        preprocess_historique_etablissement_data,
    )
from dag_datalake_sirene.workflows.data_pipelines.etl.sqlite.helpers import (
    get_table_count,
    create_index,
    create_table_model,
    create_unique_index,
    execute_query,
)
from dag_datalake_sirene.workflows.data_pipelines.etl.sqlite.queries.etablissements\
    import (
    create_table_etablissements_query,
    create_table_historique_etablissement_query,
    create_table_date_fermeture_etablissement_query,
    create_table_siret_siege_query,
    insert_date_fermeture_etablissement_query,
    insert_date_fermeture_siege_query,
    populate_table_siret_siege_query,
    create_table_count_etablissements_query,
    count_nombre_etablissements_query,
    create_table_count_etablissements_ouverts_query,
    count_nombre_etablissements_ouverts_query,
    insert_remaining_rne_sieges_data_into_main_table_query,
    update_sieges_table_fields_with_rne_data_query,
    create_table_flux_etablissements_query,
    replace_table_siret_siege_query,
    replace_table_etablissement_query,
)
# fmt: on
from dag_datalake_sirene.config import DATA_DIR
from dag_datalake_sirene.config import (
    SIRENE_DATABASE_LOCATION,
)


def create_etablissements_table():
    sqlite_client = create_table_model(
        table_name="siret",
        create_table_query=create_table_etablissements_query,
        create_index_func=create_index,
        index_name="index_siret",
        index_column="siren",
    )
    # Upload geo data by departement
    for dep in all_deps:
        df_dep = preprocess_etablissement_data("stock", dep, None)
        df_dep.to_sql("siret", sqlite_client.db_conn, if_exists="append", index=False)
        for row in sqlite_client.execute(get_table_count("siret")):
            logging.debug(
                f"************ {row} total records have been added to the "
                f"`établissements` table!"
            )
    del df_dep
    sqlite_client.commit_and_close_conn()

def create_flux_etablissements_table():
    sqlite_client = create_table_model(
        table_name="flux_siret",
        create_table_query=create_table_flux_etablissements_query,
        create_index_func=create_index,
        index_name="index_flux_siret",
        index_column="siren",
    )
    sqlite_client.commit_and_close_conn()

def create_siege_only_table(**kwargs):
    sqlite_client = create_table_model(
        table_name="siretsiege",
        create_table_query=create_table_siret_siege_query,
        create_index_func=create_index,
        index_name="index_siret_siren",
        index_column="siren",
    )
    sqlite_client.execute(populate_table_siret_siege_query)
    for count_sieges in sqlite_client.execute(get_table_count("siretsiege")):
        logging.info(
            f"************ {count_sieges} total records have been added to the "
            f"sieges table!"
        )
    #airflow: kwargs["ti"].xcom_push(key="count_sieges", value=count_sieges[0])
    sqlite_client.commit_and_close_conn()

def replace_etablissements_table():
    return execute_query(
        query=replace_table_etablissement_query,
    )

def replace_siege_only_table():
    return execute_query(
        query=replace_table_siret_siege_query,
    )

def count_nombre_etablissements():
    sqlite_client = create_table_model(
        table_name="count_etab",
        create_table_query=create_table_count_etablissements_query,
        create_index_func=create_unique_index,
        index_name="index_count_siren",
        index_column="siren",
    )

    sqlite_client.execute(count_nombre_etablissements_query)
    sqlite_client.commit_and_close_conn()


def count_nombre_etablissements_ouverts():
    sqlite_client = create_table_model(
        table_name="count_etab_ouvert",
        create_table_query=create_table_count_etablissements_ouverts_query,
        create_index_func=create_unique_index,
        index_name="index_count_ouvert_siren",
        index_column="siren",
    )
    sqlite_client.execute(count_nombre_etablissements_ouverts_query)
    sqlite_client.commit_and_close_conn()


def create_historique_etablissement_table(**kwargs):
    table_name = "historique_etablissement"
    sqlite_client = create_table_model(
        table_name=table_name,
        create_table_query=create_table_historique_etablissement_query,
        create_index_func=create_index,
        index_name="index_historique_siret",
        index_column="siret",
    )

    for df_hist_etablissement in preprocess_historique_etablissement_data(
        DATA_DIR,
    ):
        df_hist_etablissement.to_sql(
            table_name, sqlite_client.db_conn, if_exists="append", index=False
        )
        for row in sqlite_client.execute(get_table_count(table_name)):
            logging.debug(
                f"************ {row} total records have been added "
                f"to the {table_name} table!"
            )

    del df_hist_etablissement

    for count_etablissements in sqlite_client.execute(get_table_count(table_name)):
        logging.info(
            f"************ {count_etablissements} total records have been added to the "
            f"{table_name} table!"
        )
    sqlite_client.commit_and_close_conn()
    #airflow: kwargs["ti"].xcom_push(
    #    key="count_historique_etablissements", value=count_etablissements
    #)


def create_date_fermeture_etablissement_table(**kwargs):
    table_name = "date_fermeture_etablissement"
    sqlite_client = create_table_model(
        table_name=table_name,
        create_table_query=create_table_date_fermeture_etablissement_query,
        create_index_func=create_unique_index,
        index_name="index_date_fermeture_siret",
        index_column="siret",
    )

    for count_etablissements in sqlite_client.execute(get_table_count(table_name)):
        logging.info(
            f"************ {count_etablissements} total records have been added to the "
            f"{table_name} table!"
        )
    sqlite_client.commit_and_close_conn()
    #airflow: kwargs["ti"].xcom_push(
    #    key="count_date_fermeture_etablissements", value=count_etablissements
    #)


def insert_date_fermeture_etablissement(**kwargs):
    sqlite_client = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client.execute(insert_date_fermeture_etablissement_query)
    sqlite_client.execute(insert_date_fermeture_siege_query)
    sqlite_client.commit_and_close_conn()
