from ingestion.bigquery import (
    get_bigquery_client,
    get_bigquery_result,
    build_pypi_query,
)
import os
import fire
from ingestion.models import PypiJobParameters

def main(params: PypiJobParameters):

    df = get_bigquery_result(
        query_str=build_pypi_query(params=params),
        bigquery_client=get_bigquery_client(project_name=params.gcp_project),
    )
    print(df.head())
    print('hello pipeline')

if __name__ == '__main__':
    fire.Fire(lambda **kwargs: main(PypiJobParameters(**kwargs)))