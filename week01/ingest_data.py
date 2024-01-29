import os
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine, text
from argparse import ArgumentParser
from time import time


def main(args):
    user = args.user
    password = args.password
    host = args.host
    port = args.port
    database_name = args.database_name
    table_name = args.table_name
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
    parquet_path = "input.parquet"

    os.system(f"wget {url} -O {parquet_path}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database_name}")
    # with engine.connect() as con:
        # query =f"SELECT count(1) FROM {table_name};"
        # result = con.execute(text(query)).fetchall()
        # for row in result:
        #     print(row)

        # query =f"DROP TABLE IF EXISTS {table_name};"
        # result = con.execute(text(query)).fetchall()
        # print(result)

    dfall = pd.read_csv(parquet_path, compression='gzip', iterator=True, chunksize=100000)
    while True:
        start = time()
        df = next(dfall)
        print(df)
        print(f"{len(df)} lines are going to be ingested...")
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists="append")
        print(f"Ingestion took {time() - start} seconds\n")


if __name__ == "__main__":
    parser = ArgumentParser(description="Ingest parquet data to postgres")

    parser.add_argument("--user", help= "user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host" , help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--database_name", help="database name for postgres")
    parser.add_argument("--table_name", help="table name for postgres to write the results to")
    parser.add_argument("--url" , help="url of the source parquet file")

    args = parser.parse_args()

    main(args)