import logging
logger = logging.getLogger(__name__)

from dag_datalake_sirene.elasticsearch.mapping_sirene_index import (
    ElasticsearchSireneIndex,
)
from dag_datalake_sirene.elasticsearch.process_unites_legales import (
    process_unites_legales,
)
from elasticsearch.helpers import parallel_bulk


def elasticsearch_doc_siren_generator(data):
    # Serialize the instance into a dictionary so that it can be saved in elasticsearch.
    for index, document in enumerate(data):
        etablissements_count = len(document["etablissements"])
        # If ` unité légale` had more than 100 `établissements`, the main document is
        # separated into smaller documents consisting of 100 établissements each
        if etablissements_count > 100:
            smaller_document = document.copy()
            etablissements = document["etablissements"]
            etablissements_left = etablissements_count
            etablissements_indexed = 0
            while etablissements_left > 0:
                # min is used for the last iteration
                number_etablissements_to_add = min(etablissements_left, 100)
                # Select a 100 etablissements from the main document,
                # and use it as a list for the smaller document
                smaller_document["etablissements"] = etablissements[
                    etablissements_indexed : etablissements_indexed
                    + number_etablissements_to_add
                ]
                etablissements_left = etablissements_left - 100
                etablissements_indexed += 100
                yield ElasticsearchSireneIndex(
                    meta={
                        "id": f"{smaller_document['siren']}-{etablissements_indexed}"
                    },
                    **smaller_document,
                ).to_dict(include_meta=True)
        # Otherwise, (the document has less than 100 établissements), index document
        # as is
        else:
            yield ElasticsearchSireneIndex(
                meta={"id": document["siren"]}, **document
            ).to_dict(include_meta=True)


def index_unites_legales_by_chunk(
    cursor, elastic_connection, elastic_bulk_size, elastic_index
):
    logger = 0
    chunk_unites_legales_sqlite = 1
    while chunk_unites_legales_sqlite:
        chunk_unites_legales_sqlite = cursor.fetchmany(elastic_bulk_size)
        unite_legale_columns = tuple([x[0] for x in cursor.description])
        liste_unites_legales_sqlite = []
        # Group all fetched unites_legales from sqlite in one list
        for unite_legale in chunk_unites_legales_sqlite:
            liste_unites_legales_sqlite.append(
                {
                    unite_legale_columns: value
                    for unite_legale_columns, value in zip(
                        unite_legale_columns, unite_legale
                    )
                }
            )

        liste_unites_legales_sqlite = tuple(liste_unites_legales_sqlite)

        chunk_unites_legales_processed = process_unites_legales(
            liste_unites_legales_sqlite
        )
        logger += 1
        if logger % 100000 == 0:
            logging.info(f"logger={logger}")
        try:
            chunk_doc_generator = elasticsearch_doc_siren_generator(
                chunk_unites_legales_processed
            )
            # Bulk index documents into elasticsearch using the parallel version of the
            # bulk helper that runs in multiple threads
            # The bulk helper accept an instance of Elasticsearch class and an
            # iterable, a generator in our case
            for success, details in parallel_bulk(
                elastic_connection, chunk_doc_generator, chunk_size=elastic_bulk_size
            ):
                if not success:
                    raise Exception(f"A file_access document failed: {details}")
        except Exception as e:
            logging.error(f"Failed to send to Elasticsearch: {e}")
        doc_count = elastic_connection.cat.count(
            index=elastic_index, params={"format": "json"}
        )[0]["count"]
        logging.info(f"Number of documents indexed: {doc_count}")
    return doc_count
