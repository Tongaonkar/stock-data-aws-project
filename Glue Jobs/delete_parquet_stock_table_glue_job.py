import json
import boto3

# replace these with the names from your environment
BUCKET_TO_DEL = 'stock-data-parquet-bucket'
DATABASE_TO_DEL = 'de_project_database'
TABLE_TO_DEL = 'stock_data_parquet_tbl'
QUERY_OUTPUT_BUCKET = 's3://stock-query-results-location-de-project/'


# delete all objects in the bucket
s3_client = boto3.client('s3')

while True:
    objects = s3_client.list_objects(Bucket=BUCKET_TO_DEL)
    content = objects.get('Contents', [])
    if len(content) == 0:
        break
    for obj in content:
        s3_client.delete_object(Bucket=BUCKET_TO_DEL, Key=obj['Key'])


# drop the table too
client = boto3.client('athena')

queryStart = client.start_query_execution(
    QueryString = f"""
    DROP TABLE IF EXISTS {DATABASE_TO_DEL}.{TABLE_TO_DEL};
    """,
    QueryExecutionContext = {
        'Database': f'{DATABASE_TO_DEL}'
    }, 
    ResultConfiguration = { 'OutputLocation': f'{QUERY_OUTPUT_BUCKET}'}
)
