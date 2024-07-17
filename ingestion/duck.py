from loguru import logger

def create_table_from_dataframe(duckdb_con, table_name: str, dataframe: str):
    duckdb_con.sql(
        f"""
        CREATE TABLE {table_name} AS 
            SELECT *
            FROM {dataframe}
        """
    )

def connect_to_md(duckdb_con, motherduck_token: str):
    duckdb_con.sql(f"INSTALL md;")
    duckdb_con.sql(f"LOAD md;")
    duckdb_con.sql(f"SET motherduck_token='{motherduck_token}';")
    duckdb_con.sql(f"ATTACH 'md:'")

def write_to_md_from_duckdb(
    duckdb_con,
    table: str,
    local_database: str,
    remote_database: str,
    timestamp_column: str,
    start_date: str,
    end_date: str,
):
    logger.info(f"Writing data to motherduck {remote_database}.main.{table}")
    duckdb_con.sql(f"CREATE DATABASE IF NOT EXISTS {remote_database}")
    duckdb_con.sql(
        f"CREATE TABLE IF NOT EXISTS {remote_database}.{table} AS SELECT * FROM {local_database}.{table} limit 0"
    )
    # Delete any existing data in the date range
    duckdb_con.sql(
        f"DELETE FROM {remote_database}.main.{table} WHERE {timestamp_column} BETWEEN '{start_date}' AND '{end_date}'"
    )
    # Insert new data
    duckdb_con.sql(
        f"""
    INSERT INTO {remote_database}.main.{table}
    SELECT *
        FROM {local_database}.{table}"""
    )