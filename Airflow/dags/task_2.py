'''
Task 2 DAG for BigData lab homework
'''

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator
from airflow.utils.dates import days_ago

from datetime import timedelta


# Set default tasks parameters
default_args = {
        'owner': 'airflow',
        'start_date': days_ago(2),
        'retries': 5,
        'retry_delay': timedelta(seconds=20)
        }

# Initiate DAG

with DAG('Homework-task2',
    default_args=default_args,
    description='csv row counting and avro saving') as dag:

    dag.doc_md = '''
    Counts rows for input csv table,
    report row_count to stdout,
    saves to avro format (with overwrite).
    '''

    # TODO: replace by Airflow variables

    CSV_URL = 'https://www.stats.govt.nz/assets/Uploads/Greenhouse-gas-emissions-by-region-industry-and-household/Greenhouse-gas-emissions-by-region-industry-and-household-year-ended-2018/Download-data/greenhouse-gas-emissions-by-region-industry-and-household-year-ended-2018-csv.csv'
    DATA_FOLDER = 'data'

    
    download = BashOperator(
        task_id = 'download',
        bash_command = f'mkdir -p $AIRFLOW_HOME/data; curl {CSV_URL} > $AIRFLOW_HOME/data/downloaded_file.csv; echo file downloaded'
    )

    row_count = BashOperator(
        task_id='row_count',
        bash_command = 'wc -l < $AIRFLOW_HOME/data/downloaded_file.csv'
    )


    def convert_fastavro():
        from fastavro import writer, parse_schema
        from csv import DictReader
        path = '/opt/airflow/data/downloaded_file.csv'
        with open(path, 'r') as file:
            csv_content = ([_ for _ in DictReader(file)])
            
        # convert dtypes
        for record in csv_content:
            record['year'] = int(record['year'])
            record['data_val'] = float(record['data_val'])
        
        # print sample for debugging
        print('File content:')
        print(csv_content[0:10])
        
        schema = {
            'doc': 'greenhouse_csv',
            'name': 'gh_2018',
            'namespace': 'test',
            'type': 'record',
            'fields': [
                {'name': 'region', 'type': 'string'},
                {'name': 'anzsic_descriptor', 'type': 'string'},
                {'name': 'gas', 'type': 'string'},
                {'name': 'units', 'type': 'string'},
                {'name': 'magnitude', 'type': 'string'},
                {'name': 'year', 'type': 'long'},
                {'name': 'data_val', 'type': 'float'}
            ],
        }
        
        parsed_schema = parse_schema(schema)

        with open('output.avro', 'wb') as out:
            writer(out, parsed_schema, csv_content)
        print('convert to avro OK')


    convert_to_avro = PythonVirtualenvOperator(
        task_id='convert_to_avro',
        python_callable=convert_fastavro,
        requirements=['fastavro==1.4.4'],
        system_site_packages=False
    )

download >> row_count >> convert_to_avro
