from ingestion.bigquery import (
    get_bigquery_client,
    get_bigquery_result,
    build_pypi_query,
)
import os
import fire
import duckdb
from ingestion.models import PypiJobParameters, validate_dataframe, FileDownloads
from loguru import logger
from ingestion.duck import (
    create_table_from_dataframe,
    connect_to_md,
    write_to_md_from_duckdb,
    write_to_parquet_from_duckdb,
    write_to_csv_from_duckdb
)

def main(params: PypiJobParameters):

    df = get_bigquery_result(
        query_str=build_pypi_query(params=params),
        bigquery_client=get_bigquery_client(project_name=params.gcp_project),
    )

    validate_dataframe(df, FileDownloads)
    # Loading to DuckDB
    conn = duckdb.connect()
    create_table_from_dataframe(conn, params.table_name, "df")

    logger.info(f"Sinking data to {params.destination}")
    if "local-csv" in params.destination:
        write_to_csv_from_duckdb(conn, table=params.table_name)

    if "md" in params.destination:
        connect_to_md(conn, os.environ["MOTHERDUCK_TOKEN"])
        write_to_md_from_duckdb(
            duckdb_con=conn,
            table=f"{params.table_name}",
            local_database="memory",
            remote_database="pypi",
            timestamp_column=params.timestamp_column,
            start_date=params.start_date,
            end_date=params.end_date,
        )

    if "local-parquet" in params.destination:
        write_to_parquet_from_duckdb(
            duckdb_con=conn,
            table=f"{params.table_name}",
            bucket_path=os.environ["TRANSFORM_S3_PATH_INPUT"],
            timestamp_column="timestamp"
        )

if __name__ == '__main__':
    fire.Fire(lambda **kwargs: main(PypiJobParameters(**kwargs)))
