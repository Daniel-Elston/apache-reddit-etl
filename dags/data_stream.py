from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.data.pyspark import PySparkManagement
from src.pipeline import Pipeline


"""
SAMPLE DAG FILE:
Dags ran from /Airflow Directory
"""


default_args = {
    'owner': 'Daniel Elston',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kafka_data_stream',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5)
)


# cassandra_task = PythonOperator(
#     task_id='cassandra_manager',
#     python_callable=CassandraManagement().main,
#     dag=dag,
# )

produce_task = PythonOperator(
    task_id='stream_to_kafka',
    python_callable=Pipeline().kafka_stream,
    dag=dag,
)

extract_task = PythonOperator(
    task_id='pyspark_processing',
    python_callable=PySparkManagement().main,
    dag=dag,
)

# cassandra_task >>
produce_task >> extract_task
