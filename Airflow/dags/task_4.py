'''
Task 4 DAG for BigData lab homework
'''
# Before start configure SMTP sever in airflow.cfg file

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.operators.email_operator import EmailOperator

from datetime import timedelta


default_args = {
        'owner': 'airflow',
        'start_date': days_ago(2),
        'retries': 5,
        'retry_delay': timedelta(seconds=20),
        'email': ['nikifor_ostanin@epam.com'],
        'email_on_success': True
        }


with DAG('Homework-task4',
      default_args=default_args,
      description='Send email') as dag:

    task0 = DummyOperator(task_id='start_the_dag')

    task1 = BashOperator(task_id='bash',
                bash_command='echo some command')


    email = EmailOperator(
                task_id='send_email',
                to='nikifor_ostanin@epam.com',
                subject='Airflow Alert',
                html_content='Airflow check',
                )


    task0 >> task1 >> email
