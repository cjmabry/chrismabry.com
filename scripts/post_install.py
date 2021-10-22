#!/usr/bin/env python

import boto3
import json
import time
import subprocess

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

AMAZON_PROJECT_SLUG = "chrismabry"

def create_iam_users():
    iam_client = boto3.client('iam')

    # Create staging and prod IAM users
    iam_user_staging = iam_client.create_user(
        UserName=AMAZON_PROJECT_SLUG+'-staging',
    )

    iam_user_prod = iam_client.create_user(
        UserName=AMAZON_PROJECT_SLUG+'-prod',
    )

    # Policies for Staging and Prod IAM users
    policy_document_staging = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObjectAcl",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                    "s3:PutObjectAcl"
                ],
                "Resource": [
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-staging/*",
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-staging"
                ]
            }
        ]
    }

    policy_document_prod = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObjectAcl",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                    "s3:PutObjectAcl"
                ],
                "Resource": [
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-prod/*",
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-prod"
                ]
            }
        ]
    }

    # Create policies for both staging and prod IAM users
    policy_staging_resp = iam_client.create_policy(
        PolicyName=AMAZON_PROJECT_SLUG+'-staging',
        PolicyDocument=json.dumps(policy_document_staging),
    )

    policy_prod_resp = iam_client.create_policy(
        PolicyName=AMAZON_PROJECT_SLUG+'-prod',
        PolicyDocument=json.dumps(policy_document_prod),
    )

    # Attach policies to previously created IAM users
    staging_response = iam_client.attach_user_policy(
        UserName=AMAZON_PROJECT_SLUG+'-staging',
        PolicyArn=policy_staging_resp['Policy']['Arn']
    )

    prod_response = iam_client.attach_user_policy(
        UserName=AMAZON_PROJECT_SLUG+'-prod',
        PolicyArn=policy_prod_resp['Policy']['Arn']
    )

    # Create Access Keys for both staging and prod
    access_key_staging = iam_client.create_access_key(
        UserName=AMAZON_PROJECT_SLUG+'-staging'
    )

    access_key_prod = iam_client.create_access_key(
        UserName=AMAZON_PROJECT_SLUG+'-prod'
    )

    # Output these access keys for the user
    print(WARNING + 'IMPORTANT: Remember to store the following keys in 1Password as this is the only time they will be outputted!')
    print('Access Keys for Staging: ', access_key_staging)
    print('Access Keys for Prod: ', access_key_prod)

    create_heroku_apps_pipeline(access_key_staging, access_key_prod)


def generate_aws_buckets():
    client = boto3.client('s3')

    staging_bucket = client.create_bucket(
        ACL='public-read',
        Bucket=AMAZON_PROJECT_SLUG+'-staging',
    )

    prod_bucket = client.create_bucket(
        ACL='public-read',
        Bucket=AMAZON_PROJECT_SLUG+'-prod',
    )

    pa_staging_response = client.put_public_access_block(
        Bucket=AMAZON_PROJECT_SLUG+'-staging',
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        },
    )

    pa_prod_response = client.put_public_access_block(
        Bucket=AMAZON_PROJECT_SLUG+'-staging',
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        },
    )

    staging_policy = {
        "Version": "2012-10-17",
        "Id": "Policy1596173288877",
        "Statement": [
            {
                "Sid": "Stmt1596173135946",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-staging/*"
            },
            {
                "Sid": "Stmt1596173166968",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::224438817900:user/" + AMAZON_PROJECT_SLUG + "-staging"
                },
                "Action": "s3:*",
                "Resource": [
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-staging",
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-staging/*"
                ]
            }
        ]
    }

    prod_policy = {
        "Version": "2012-10-17",
        "Id": "Policy1596173288877",
        "Statement": [
            {
                "Sid": "Stmt1596173135946",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-prod/*"
            },
            {
                "Sid": "Stmt1596173166968",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::224438817900:user/" + AMAZON_PROJECT_SLUG + "-prod"
                },
                "Action": "s3:*",
                "Resource": [
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-prod",
                    "arn:aws:s3:::" + AMAZON_PROJECT_SLUG + "-prod/*"
                ]
            }
        ]
    }

    staging_bp_response = client.put_bucket_policy(
        Bucket=AMAZON_PROJECT_SLUG+'-staging',
        Policy=json.dumps(staging_policy),
    )

    prod_bp_response = client.put_bucket_policy(
        Bucket=AMAZON_PROJECT_SLUG+'-prod',
        Policy=json.dumps(prod_policy),
    )

    staging_cors_response = client.put_bucket_cors(
        Bucket=AMAZON_PROJECT_SLUG+'-staging',
        CORSConfiguration={
            'CORSRules': [
                {
                    "AllowedHeaders": [
                        "Authorization"
                    ],
                    "AllowedMethods": [
                        "GET"
                    ],
                    "AllowedOrigins": [
                        "*"
                    ],
                    "ExposeHeaders": [],
                    "MaxAgeSeconds": 3000
                },
            ]
        },
    )

    prod_cors_response = client.put_bucket_cors(
        Bucket=AMAZON_PROJECT_SLUG+'-prod',
        CORSConfiguration={
            'CORSRules': [
                {
                    "AllowedHeaders": [
                        "Authorization"
                    ],
                    "AllowedMethods": [
                        "GET"
                    ],
                    "AllowedOrigins": [
                        "*"
                    ],
                    "ExposeHeaders": [],
                    "MaxAgeSeconds": 3000
                },
            ]
        },
    )


def create_heroku_apps_pipeline(access_key_staging, access_key_prod):
    # get secret access key from access_key JSON
    secret_access_key_staging = access_key_staging['AccessKey']['SecretAccessKey']
    secret_access_key_prod = access_key_prod['AccessKey']['SecretAccessKey']

    access_key_id_staging = access_key_staging['AccessKey']['AccessKeyId']
    access_key_id_prod = access_key_prod['AccessKey']['AccessKeyId']



    # create prod and staging apps
    subprocess.run(['heroku', 'create', 'chrismabry-prod'])
    subprocess.run(['heroku', 'create', 'chrismabry-staging'])

    # create Heroku pipeline and add prod + staging apps to pipeline
    subprocess.run(['heroku', 'pipelines:create', '-a', 'chrismabry-prod', '--team', 'with-the-ranks'])
    subprocess.run(['heroku', 'pipelines:add', '-a', 'chrismabry-staging'])

    # set environment variables in Heroku
    # set AWS bucket name
    subprocess.run(['heroku', 'config:set', 'DJANGO_AWS_STORAGE_BUCKET_NAME=chrismabry-staging', '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'DJANGO_AWS_STORAGE_BUCKET_NAME=chrismabry-prod', '-a', 'chrismabry-prod'])

    # set allowed hosts
    subprocess.run(['heroku', 'config:set', 'DJANGO_ALLOWED_HOSTS=chrismabry-staging.herokuapp.com', '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'DJANGO_ALLOWED_HOSTS=chrismabry-prod.herokuapp.com', '-a', 'chrismabry-prod'])

    # set django admin URL
    subprocess.run(['heroku', 'config:set', 'DJANGO_ADMIN_URL=admin', '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'DJANGO_ADMIN_URL=admin', '-a', 'chrismabry-prod'])

    # set django settings module
    subprocess.run(['heroku', 'config:set', 'DJANGO_ADMIN_URL=config.settings.production', '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'DJANGO_ADMIN_URL=config.settings.production', '-a', 'chrismabry-prod'])

    # set django settings module
    subprocess.run(['heroku', 'config:set', 'MAILGUN_API_KEY=tempvalue', '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'MAILGUN_API_KEY=tempvalue', '-a', 'chrismabry-prod'])

    # set AWS secret access key
    subprocess.run(['heroku', 'config:set', 'DJANGO_AWS_SECRET_ACCESS_KEY=' + secret_access_key_staging, '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'DJANGO_AWS_SECRET_ACCESS_KEY=' + secret_access_key_prod, '-a', 'chrismabry-prod'])

    # set AWS access key ID
    subprocess.run(['heroku', 'config:set', 'DJANGO_AWS_ACCESS_KEY_ID=' + access_key_id_staging, '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'DJANGO_AWS_ACCESS_KEY_ID=' + access_key_id_prod, '-a', 'chrismabry-prod'])

    # set cache frontend enabled
    subprocess.run(['heroku', 'config:set', 'CACHE_FRONTEND_ENABLED=FALSE', '-a', 'chrismabry-staging'])
    subprocess.run(['heroku', 'config:set', 'CACHE_FRONTEND_ENABLED=TRUE', '-a', 'chrismabry-prod'])



create_iam_users()
print(INFO + 'Sleeping for 30 seconds before creating buckets...' + TERMINATOR)
time.sleep(30)
print(INFO + 'Creating buckets' + TERMINATOR)
generate_aws_buckets()
create_heroku_apps_pipeline()
