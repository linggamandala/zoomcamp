# Import libraries
import argparse
import os
from time import time
import pandas as pd
from sqlalchemy import create_engine

# create function for engine
def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f'wget {url} -O {csv_name}')
        
    # Create engine for export dataset
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # df = pd.read_csv(csv_name, compression='gzip', low_memory=False)
    # Limit the iterator by 100000 rows
    df_iter = pd.read_csv(csv_name, compression='gzip', low_memory=False, iterator=True, chunksize=10000)

    # Checking the iterator limit
    df = next(df_iter)

    # Change tpep_pickup_datetime & tpep_dropoff_datetimee columns to datetime
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Export the dataset head to database
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Export the dataset to database
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Export the dataset to database using time
    while True:
        try:
            t_start = time()
            
            df = next(df_iter)
            
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            
            print('insert another chunk, took %.3f second' % (t_end - t_start))
        
        except StopIteration:
            print('Finished ingesting data into the postgres database')
            break

if __name__ == '__main__':
    # Use argparase for 
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, database name, table name
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password name for postgres')
    parser.add_argument('--host', required=True, help='host name for postgres')
    parser.add_argument('--port', required=True, help='port name for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()
    
    main(args)