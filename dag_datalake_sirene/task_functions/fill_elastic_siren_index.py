from dag_datalake_sirene.elasticsearch.indexing_unite_legale import (
    index_unites_legales_by_chunk,
)
from elasticsearch_dsl import connections

from dag_datalake_sirene.sqlite.sqlite_client import SqliteClient


from dag_datalake_sirene.sqlite.queries.select_fields_to_index import (
    select_fields_to_index_query,
)
from dag_datalake_sirene.task_functions.global_variables import (
    SIRENE_DATABASE_LOCATION,
    ELASTIC_URL,
    ELASTIC_USER,
    ELASTIC_PASSWORD,
    ELASTIC_BULK_SIZE,
)


def fill_elastic_siren_index(**kwargs):
    elastic_index = f"siren-blue"
    sqlite_client = SqliteClient(SIRENE_DATABASE_LOCATION)
    sqlite_client.execute(select_fields_to_index_query)

    if(ELASTIC_USER and ELASTIC_PASSWORD):
        connections.create_connection(
            hosts=[ELASTIC_URL],
            http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
            retry_on_timeout=True,
        )
    else:
        connections.create_connection(
            hosts=[ELASTIC_URL],
            retry_on_timeout=True,
        )

    elastic_connection = connections.get_connection()

    doc_count = index_unites_legales_by_chunk(
        cursor=sqlite_client.db_cursor,
        elastic_connection=elastic_connection,
        elastic_bulk_size=ELASTIC_BULK_SIZE,
        elastic_index=elastic_index,
    )
    sqlite_client.commit_and_close_conn()
    return doc_count
