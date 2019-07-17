from dotenv import load_dotenv
import os
import boto3
import requests
from requests_aws4auth import AWS4Auth

load_dotenv()


def register():
    payload = {
        "type": "s3",
        "settings": {
            "bucket": os.getenv("s3_bucket"),
            "region": os.getenv('s3_region'),
            "role_arn": os.getenv('role_arn')
        }
    }

    r = requests.put(
        make_snapshot_url(),
        auth=make_aws_auth(),
        headers=json_header(),
        json=payload
    )

    print(r.status_code)
    print(r.text)


def take_snapshot(name):
    r = requests.put(
        make_snapshot_url('/' + name),
        auth=make_aws_auth(),
        headers=json_header()
    )

    print(r.status_code)
    print(r.text)


def get_snapshot_status():
    r = requests.get(
        make_snapshot_url('/_all?pretty'),
        auth=make_aws_auth(),
        headers=json_header()
    )

    print(r.status_code)
    print(r.text)


def make_aws_auth():
    es_region = os.getenv('es_region')

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    credentials = session.get_credentials()
    return AWS4Auth(credentials.access_key, credentials.secret_key, es_region, 'es')


def make_snapshot_url(name=""):
    es_host = os.getenv("es_host")
    es_snapshot_name = os.getenv('es_snapshot_name')

    return es_host + '_snapshot/' + es_snapshot_name + name


def json_header():
    return {"Content-Type": "application/json"}
