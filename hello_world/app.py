import json
import boto3
from aws_lambda_types.sns import SNSEventDict

s3 = boto3.client('s3')

def lambda_handler(event:SNSEventDict, context):

    # personId = event['queryStringParameters']['personId']

    return {
        "statusCode": 200,
        "body": json.dumps({
            "personId": 'Hello World' ,
        }),
    }
