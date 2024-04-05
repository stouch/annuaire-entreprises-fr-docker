from datetime import timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from dag_datalake_sirene.workflows.data_pipelines.sirene.flux.task_functions import (
    get_current_flux_etablissement,
    get_current_flux_non_diffusible,
    get_current_flux_unite_legale,
    send_notification,
    send_notification_stock,
    get_stock_non_diffusible,
    send_flux_minio,
    send_stock_minio,
)

from dag_datalake_sirene.helpers.utils import (
    check_if_monday,
)
from dag_datalake_sirene.config import (
    INSEE_FLUX_TMP_FOLDER,
)

DAG_NAME = "data_processing_sirene_flux"

default_args = {
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id=DAG_NAME,
    default_args=default_args,
    schedule_interval="0 4 * * *",  # Daily at 4 AM
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
    tags=["sirene", "flux"],
) as dag:
    clean_previous_outputs = BashOperator(
        task_id="clean_previous_outputs",
        bash_command=(
            f"rm -rf {INSEE_FLUX_TMP_FOLDER} && mkdir -p {INSEE_FLUX_TMP_FOLDER}"
        ),
    )

    get_current_flux_unite_legale = PythonOperator(
        task_id="get_current_flux_unite_legale",
        python_callable=get_current_flux_unite_legale,
    )

    get_current_flux_etablissement = PythonOperator(
        task_id="get_current_flux_etablissement",
        python_callable=get_current_flux_etablissement,
    )

    get_current_flux_non_diffusible = PythonOperator(
        task_id="get_current_flux_non_diffusible",
        python_callable=get_current_flux_non_diffusible,
    )

    send_flux_minio = PythonOperator(
        task_id="send_flux_minio",
        python_callable=send_flux_minio,
    )

    check_if_monday = ShortCircuitOperator(
        task_id="check_if_monday", python_callable=check_if_monday
    )

    get_stock_non_diffusible = PythonOperator(
        task_id="get_stock_non_diffusible",
        python_callable=get_stock_non_diffusible,
    )

    send_stock_minio = PythonOperator(
        task_id="send_stock_minio",
        python_callable=send_stock_minio,
    )

    send_notification = PythonOperator(
        task_id="send_notification",
        python_callable=send_notification,
    )

    send_notification_stock = PythonOperator(
        task_id="send_notification_stock",
        python_callable=send_notification_stock,
    )

    get_current_flux_unite_legale.set_upstream(clean_previous_outputs)
    get_current_flux_etablissement.set_upstream(get_current_flux_unite_legale)
    get_current_flux_non_diffusible.set_upstream(get_current_flux_etablissement)
    send_flux_minio.set_upstream(get_current_flux_non_diffusible)
    send_notification.set_upstream(send_flux_minio)
    check_if_monday.set_upstream(send_flux_minio)
    get_stock_non_diffusible.set_upstream(check_if_monday)
    send_stock_minio.set_upstream(get_stock_non_diffusible)
    send_notification_stock.set_upstream(send_stock_minio)
