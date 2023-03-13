import logging
logging.basicConfig(
    level = logging.INFO,
    format = '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'
)

from datetime import datetime, timedelta

from dag_datalake_sirene.task_functions.check_elastic_index import check_elastic_index
from dag_datalake_sirene.task_functions.count_nombre_etablissements import (
    count_nombre_etablissements,
)
from dag_datalake_sirene.task_functions.count_nombre_etablissements_ouverts import (
    count_nombre_etablissements_ouverts,
)
from dag_datalake_sirene.task_functions.create_additional_data_tables import (
    create_colter_table,
    create_rge_table,
    create_finess_table,
    create_elu_table,
    create_spectacle_table,
    create_uai_table,
    create_convention_collective_table,
)
from dag_datalake_sirene.task_functions.create_dirig_tables import (
    create_dirig_pm_table,
    create_dirig_pp_table,
)
from dag_datalake_sirene.task_functions.create_elastic_index import create_elastic_index
from dag_datalake_sirene.task_functions.create_etablissements_table import (
    create_etablissements_table,
)
from dag_datalake_sirene.task_functions.create_siege_only_table import (
    create_siege_only_table,
)
from dag_datalake_sirene.task_functions.create_sqlite_database import (
    create_sqlite_database,
)
from dag_datalake_sirene.task_functions.create_unite_legale_table import (
    create_unite_legale_table,
)
from dag_datalake_sirene.task_functions.fill_elastic_siren_index import (
    fill_elastic_siren_index,
)


create_sqlite_database() 

count_unites_legales = create_unite_legale_table()

create_etablissements_table()
count_nombre_etablissements()
count_nombre_etablissements_ouverts()
nb_siege = create_siege_only_table()

# For now, suppose we do not have the inpi.db access :
""" get_dirigeants_database = PythonOperator(
    task_id="get_dirig_database",
    provide_context=True,
    python_callable=get_object_minio,
    op_args=(
        "inpi.db",
        "inpi/",
        f"{TMP_FOLDER}{DAG_FOLDER}{DAG_NAME}/data/inpi.db",
    ),
) """
#get_dirigeants_database.set_upstream(create_siege_only_table)

create_dirig_pp_table()
create_dirig_pm_table()

create_convention_collective_table()
create_rge_table()
create_finess_table()
create_uai_table()
create_spectacle_table() 
create_colter_table()
create_elu_table()

create_elastic_index()
doc_count = fill_elastic_siren_index()
check_elastic_index(
    doc_count=doc_count,
    count_sieges=nb_siege,
)
