from datetime import datetime, timedelta

# fmt: off
from dag_datalake_sirene.workflows.data_pipelines.elasticsearch.task_functions.\
    index import (
    create_elastic_index,
    fill_elastic_siren_index,
    update_elastic_alias,
)

# fmt: on

create_elastic_index()
fill_elastic_siren_index()
update_elastic_alias()


