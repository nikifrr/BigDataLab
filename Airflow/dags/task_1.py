"""
Task 1 DAG for BigData lab homework.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from datetime import timedelta


# Set default tasks parameters
default_args = {
        'owner': 'airflow',
        'start_date': days_ago(2),
        'shedule_interval': timedelta(days=1),
        'retries': 5,
        'retry_delay': timedelta(hours=6)
        }


# Initiate DAG
with DAG('Homework-task1',
         default_args=default_args,
         description='Hellow-wording in Airflow',
         ) as dag:

    dag.doc_md = """
    This DAG prints messages "Good Morning", "Good day", "Good evening" to stdout in a separate task
    one after other.
    """

    t1 = BashOperator(
        task_id='Good-morning',
        bash_command='echo Good morning'
    )

    t2 = BashOperator(
        task_id='Good-day',
        bash_command='echo Good day'
    )

    t3 = BashOperator(
        task_id='Good-evening',
        bash_command='echo Good evening'
    )

    # Define tasks order
    t1 >> t2 >> t3
