from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Thêm thư mục src/ vào sys.path để import các script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crawl import crawl_cat_breeds
from transform import transform_data
from save import save_to_postgres

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="cat_pipeline_dag",
    default_args=default_args,
    description="DAG ETL dữ liệu giống mèo",
    schedule_interval="0 9 * * *",  # 9h sáng mỗi ngày
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["cat", "etl"]
) as dag:

    crawl = PythonOperator(
        task_id="crawl_cat",
        python_callable=crawl_cat_breeds
    )

    transform = PythonOperator(
        task_id="transform_cat",
        python_callable=transform_data
    )

    save = PythonOperator(
        task_id="save_cat",
        python_callable=save_to_postgres
    )

    crawl >> transform >> save
