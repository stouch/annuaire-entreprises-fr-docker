from datetime import datetime, timedelta

# fmt: off
from dag_datalake_sirene.workflows.data_pipelines.etl.task_functions.\
    create_etablissements_tables import (
    count_nombre_etablissements,
    count_nombre_etablissements_ouverts,
    create_etablissements_table,
    create_date_fermeture_etablissement_table,
    create_historique_etablissement_table,
    create_siege_only_table,
    insert_date_fermeture_etablissement,
    create_flux_etablissements_table,
    replace_siege_only_table,
)

from dag_datalake_sirene.workflows.data_pipelines.etl.task_functions.\
    create_additional_data_tables import (
    create_agence_bio_table,
    create_bilan_financiers_table,
    create_colter_table,
    create_ess_table,
    create_rge_table,
    create_finess_table,
    create_egapro_table,
    create_elu_table,
    create_organisme_formation_table,
    create_spectacle_table,
    create_uai_table,
    create_convention_collective_table,
)
from dag_datalake_sirene.workflows.data_pipelines.etl.task_functions.\
    create_dirigeants_tables import (
    create_dirig_pm_table,
    create_dirig_pp_table,
)


from dag_datalake_sirene.workflows.data_pipelines.etl.task_functions.\
    create_sqlite_database import (
    create_sqlite_database,
)
from dag_datalake_sirene.workflows.data_pipelines.etl.task_functions.\
    create_unite_legale_tables import (
    create_date_fermeture_unite_legale_table,
    create_historique_unite_legale_table,
    create_unite_legale_table,
    insert_date_fermeture_unite_legale,
    replace_unite_legale_table,
    create_flux_unite_legale_table,
)

# fmt: on

create_sqlite_database()

create_unite_legale_table()
create_historique_unite_legale_table()
create_date_fermeture_unite_legale_table()
create_etablissements_table()
create_flux_unite_legale_table()
create_flux_etablissements_table()
replace_unite_legale_table()
insert_date_fermeture_unite_legale()
count_nombre_etablissements()
count_nombre_etablissements_ouverts()
create_siege_only_table()
replace_siege_only_table()
create_historique_etablissement_table()
create_date_fermeture_etablissement_table()
insert_date_fermeture_etablissement()

create_dirig_pp_table()
create_dirig_pm_table()

create_bilan_financiers_table()
create_convention_collective_table()
create_ess_table()
create_rge_table()
create_finess_table()
create_agence_bio_table()
create_organisme_formation_table()
create_uai_table()
create_spectacle_table()
create_egapro_table()
create_colter_table()
create_elu_table()


