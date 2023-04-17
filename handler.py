import json
import boto3
import os

def get_s3_credentials():

    print("Fetching S3 Credentials...")

    response = boto3.client("sts").assume_role(
        RoleArn=os.getenv('DATA_ACCESS_ROLE_ARN'),
        RoleSessionName="assuming-data-acess-role",
    )
    return {
        "aws_access_key_id": response["Credentials"]["AccessKeyId"],
        "aws_secret_access_key": response["Credentials"]["SecretAccessKey"],
        "aws_session_token": response["Credentials"]["SessionToken"],
    }
    
    print('Done fetching credentials')



def handler(event, context):
    bckt = event.pop('bucket')
    credentials = get_s3_credentials()
    print('creating boto resource')
    s3 = boto3.resource('s3', **credentials)
    print('done creating boto resource')
    print('creating bucket object')
    my_bucket = s3.Bucket(bckt)
    print('done creating bucket object')
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object)
    return {
        'statusCode': 200,
        'body': json.dumps('accessed bucket!')
    }