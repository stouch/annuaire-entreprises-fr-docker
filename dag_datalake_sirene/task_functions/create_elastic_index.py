import logging
logger = logging.getLogger(__name__)

from dag_datalake_sirene.elasticsearch.create_sirene_index import ElasticCreateSiren
from dag_datalake_sirene.task_functions.global_variables import (
    ELASTIC_BULK_SIZE,
    ELASTIC_PASSWORD,
    ELASTIC_USER,
    ELASTIC_URL,
)


def create_elastic_index(**kwargs):
    elastic_index = f"siren-blue"
    logging.info(f"******************** Index to create: {elastic_index}")
    create_index = ElasticCreateSiren(
        elastic_url=ELASTIC_URL,
        elastic_index=elastic_index,
        elastic_user=ELASTIC_USER,
        elastic_password=ELASTIC_PASSWORD,
        elastic_bulk_size=ELASTIC_BULK_SIZE,
    )
    create_index.execute()
