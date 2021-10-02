'''
Task 3 DAG for BigData lab homework
'''

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator
from airflow.utils.dates import days_ago

from datetime import timedelta


default_args = {
        'owner': 'airflow',
        'start_date': days_ago(2),
        'retries': 5,
        'retry_delay': timedelta(seconds=20)
        }


with DAG('Homework-task3',
    default_args=default_args,
    description='csv downloading and pivoting'
    ) as dag:

    dag.doc = '''
        Download csv file, 
        transforms to pivot (group by region and year),
        saves result to csv
        '''

    CSV_URL = 'https://www.stats.govt.nz/assets/Uploads/Greenhouse-gas-emissions-by-region-industry-and-household/Greenhouse-gas-emissions-by-region-industry-and-household-year-ended-2018/Download-data/greenhouse-gas-emissions-by-region-industry-and-household-year-ended-2018-csv.csv'
 
    download = BashOperator(
        task_id = 'download',
        trigger_rule = 'all_success',
        bash_command = f'''mkdir -p /opt/airflow/data; 
                        curl {CSV_URL} > /opt/airflow/data/downloaded_file.csv;
                        echo file downloaded'''
    )


    def pivot_table():
        '''
        Load csv to pandas dataframe,
        make desired transformations (pivoting according Task),
        save to csv location. Subset of resulting table printed to console.
        '''
        import pandas as pd
        import numpy as np

        df = pd.read_csv('/opt/airflow/data/downloaded_file.csv')
        pivoted_df = pd.pivot_table(data=df,
                                    index=['region'],
                                    columns = ['year'],
                                    values = ['data_val'],
                                    aggfunc=np.sum,
                                    margins=True)

        print(pivoted_df)
        path = '/opt/airflow/data/result.csv'
        pivoted_df.to_csv(path)
        # Save path to XCom
        return(path)


    pivot = PythonVirtualenvOperator(
        task_id = 'pivot',
        python_callable = pivot_table,
        requirements=['pandas==1.3.3', 'numpy==1.21.2'],
        system_site_packages=False
    )

    download >> pivot
