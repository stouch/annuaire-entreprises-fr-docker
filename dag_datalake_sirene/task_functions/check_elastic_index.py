import logging
logger = logging.getLogger(__name__)


def check_elastic_index(**kwargs):
    doc_count = kwargs["doc_count"]
    count_sieges = kwargs["count_sieges"]

    logging.info(f"******************** Documents indexed: {doc_count}")

    if float(count_sieges) - float(doc_count) > 100000:
        raise ValueError(
            f"*******The data has not been correctly indexed: "
            f"{doc_count} documents indexed instead of {count_sieges}."
        )
