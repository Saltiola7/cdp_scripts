# query_builder.py
class QueryBuilder:
    def __init__(self, bigquery_client):
        self.client = bigquery_client

    def execute_query(self, query, params=None):
        query_job = self.client.query(query, job_config=self._get_query_config(params))
        return query_job.result()

    def _get_query_config(self, params):
        job_config = bigquery.QueryJobConfig()
        if params:
            job_config.query_parameters = params
        return job_config
