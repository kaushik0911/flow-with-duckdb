from ingestion.bigquery import (
    get_bigquery_client,
    get_bigquery_result,
    build_pypi_query,
)
import os

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '';

    df = get_bigquery_result(
        query_str=build_pypi_query(),
        bigquery_client=get_bigquery_client(),
    )
    print(df.head())
    print('hello pipeline')

if __name__ == '__main__':
    main()