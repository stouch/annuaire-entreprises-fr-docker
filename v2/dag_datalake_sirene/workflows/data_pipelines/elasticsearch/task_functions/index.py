import logging
from datetime import datetime
from elasticsearch_dsl import connections
from elasticsearch import NotFoundError

from dag_datalake_sirene.workflows.data_pipelines.elasticsearch.create_index import (
    ElasticCreateIndex,
)
from dag_datalake_sirene.helpers.sqlite_client import SqliteClient

# fmt: off
from dag_datalake_sirene.workflows.data_pipelines.elasticsearch.sqlite.\
    fields_to_index import (
    select_fields_to_index_query,
)
from dag_datalake_sirene.workflows.data_pipelines.elasticsearch.\
    indexing_unite_legale import (
    index_unites_legales_by_chunk,
)
# fmt: on
from dag_datalake_sirene.config import (
    DATA_DIR,
    ELASTIC_URL,
    ELASTIC_USER,
    ELASTIC_PASSWORD,
    ELASTIC_BULK_SIZE,
    ELASTIC_MAX_LIVE_VERSIONS,
)


def get_next_index_name(**kwargs):
    current_date = datetime.today().strftime("%Y%m%d%H%M%S")
    elastic_index = f"siren-{current_date}"
    #airflow: kwargs["ti"].xcom_push(key="elastic_index", value=elastic_index)
    return elastic_index

INDEX_NAME = get_next_index_name()

def create_elastic_index(**kwargs):
    elastic_index = INDEX_NAME
    logging.info(f"******************** Index to create: {elastic_index}")
    create_index = ElasticCreateIndex(
        elastic_url=ELASTIC_URL,
        elastic_index=elastic_index,
        elastic_user=ELASTIC_USER,
        elastic_password=ELASTIC_PASSWORD,
        elastic_bulk_size=ELASTIC_BULK_SIZE,
    )
    create_index.execute()


def fill_elastic_siren_index(**kwargs):
    elastic_index = INDEX_NAME
    sqlite_client = SqliteClient(DATA_DIR + "sirene.db")
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
    #airflow: kwargs["ti"].xcom_push(key="doc_count", value=doc_count)
    sqlite_client.commit_and_close_conn()

def update_elastic_alias(**kwargs):
    """
    The annuaire-entreprises-search-api queries the "siren-reader" index alias to process user requests.
    The "siren-reader" index alias acts as a symbolic link to the current live index and should be associated to one and only one siren index at any given time.

    This function performs an atomic update of the alias to attach the new live index and detach any other index without any downtime.

    Example:
        Given that the siren-reader is associated to the index "siren-20240206011523"
        And that the new siren index is "siren-20240208001729"
        When called, this function detach the "siren-20240206011523" index from the alias "siren-reader"
        And attach the "siren-20240208001729" index to the alias "siren-reader"

    @see: https://www.elastic.co/guide/en/elasticsearch/reference/7.17/aliases.html
    """

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

    alias = "siren-reader"
    elastic_index = INDEX_NAME

    indices = []

    try:
        config = elastic_connection.indices.get_alias(name=alias)
        indices = config.keys() if config is not None else []
    except NotFoundError:
        pass

    actions = [
        {
            "remove": {
                "index": index,
                "alias": alias,
            }
        }
        for index in indices
    ]

    actions.append({"add": {"index": elastic_index, "alias": alias}})

    logging.info(
        f"Updating alias siren-reader : add {elastic_index}, remove {', '.join(indices)}"
    )

    elastic_connection.indices.update_aliases({"actions": actions})