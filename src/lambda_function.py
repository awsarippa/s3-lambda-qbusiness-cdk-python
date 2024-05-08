import boto3
import os
import logging

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

region_name = os.getenv("region", "us-east-1")
index_id = os.getenv("index_id")
application_id = os.getenv("application_id")
qbusiness_obj = boto3.client("qbusiness", region_name=region_name)
s3 = boto3.client('s3')
bucket_mapping = \
[
  { "bucket": "amazon-q-workshop-571387307529", "data_sourceid": "d093ce64-2518-4a9d-8375-51c8658f3f2c"},
  { "bucket": "bucket2", "data_sourceid": "89d3ce64-2518-4a9d-8375-51c8658f3v3s"}
]
status = "Sync-up initiation completed, please check logs!!"

def get_sourceid(s3_bucket):
    LOG.info(f"S3 bucket is {s3_bucket}")
    for dictionary in bucket_mapping:
        if dictionary["bucket"] == s3_bucket:
            LOG.info(f"Data source id is {dictionary['data_sourceid']}")
            return dictionary["data_sourceid"]

def lambda_handler(event, context):
    """
    :param event: Input from the user, through a S3 bucket upload event
    :param context: Any methods and properties that provide information about the invocation, function, and execution environment
    :return: The response from Q Business service after the initiation of the Sync job.
    """
    try:
        LOG.info(f"Event is {event}")
        s3_bucket = event["Records"][0]["s3"]["bucket"]["name"]
        LOG.info(f"S3 bucket is {s3_bucket}")

        data_sourceid = get_sourceid(s3_bucket)
        response = qbusiness_obj.start_data_source_sync_job(
            dataSourceId=data_sourceid,
            applicationId='80157a1c-a12e-427a-8e8a-98d16822a367',
            indexId='ff2b881f-4abc-4095-b450-6b6f46344178'
        )
        LOG.info(response)

        return response["executionId"], status

    except Exception as e:
        LOG.error("Data sync-up job initiation failed!!")
        raise e
