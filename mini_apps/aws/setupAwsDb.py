#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
# from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
import json
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

DUMP_PATH = "/Users/xavierthomas/pythonProjects/GenerateData/db_dump/rethinkdb_dump_2019-03-24T01:44:08/friendly_neighbor"

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

db_client = dynamodb.meta.client

response = db_client.list_tables()

zip_table_response = None
communities_table_response = None

if "zip_codes" in response['TableNames']:
    print("Attempting to Delete Zip Codes Table")
    try:
        db_client.delete_table(
            TableName='zip_codes'
        )
        db_client.get_waiter('table_not_exists').wait(TableName='zip_codes')
        print("Deleted zip_code Table")
    except db_client.exceptions.RequestExpired:
        pass

if "communities" in response['TableNames']:
    print("Attempting to Delete Communities Table")
    try:
        db_client.delete_table(
            TableName='communities'
        )
        db_client.get_waiter('table_not_exists').wait(TableName='communities')
        print("Deleted Communities Table")
    except db_client.exceptions.RequestExpired:
        pass

print("Attempting to Create Zip Codes Table")
try:
    zip_table_response = db_client.create_table(
        TableName='zip_codes',
        KeySchema=[
            {
                'AttributeName': 'zip_code',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'zip_code',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 50
        }
    )
except db_client.exceptions.ResourceInUseException:
    print("Zip_codes Table Already Created")
finally:
    db_client.get_waiter('table_exists').wait(TableName='zip_codes')

print("Attempting to Create Communities Table")
try:
    communities_table_response = db_client.create_table(
        TableName='communities',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'zip_code',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'zip_code',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'simplicy_index',
                'AttributeType': 'N'
            }
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'simplicy_field',
                'KeySchema': [
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'simplicy_index',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                }
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 50
        }
    )
except db_client.exceptions.ResourceInUseException:
    print("Communities Table Already Created")
finally:
    db_client.get_waiter('table_exists').wait(TableName='communities')


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        time.sleep(2)
        yield l[i:i + n]


def thread_batch_insert(table_name, data, item_creator):
    thread_db_client = boto3.resource('dynamodb', region_name='us-east-1').meta.client
    for chunk in chunks(data, 25):
        thread_db_client.batch_write_item(
            RequestItems={
                table_name: [
                    {'PutRequest': {
                        'Item': item_creator(item)
                    }}
                    for item in chunk
                ]
            }
        )


def insert_data_into_table(table_name, file_path, item_creator):
    thread_amount = 50
    with open(DUMP_PATH + file_path) as json_file:
        data = json.load(json_file, parse_float=Decimal)
        data_chunk_length = int(len(data) / thread_amount)
        with ThreadPoolExecutor(max_workers=thread_amount) as executor:
            start_range = 0
            counter = 0
            while counter < thread_amount:
                executor.submit(thread_batch_insert, table_name, data[start_range:start_range + data_chunk_length],
                                item_creator)
                start_range += data_chunk_length
                counter += 1


def zip_insertion(item):
    return {
        'bordering_zips': item['bordering_zips'],
        'bounding_coords': item['bounding_coords'],
        'city': item['city'],
        'county': item['county'],
        'state': item['state'],
        'state_abrv': item['state_abrv'],
        'zip_code': item['zip_code'],
        'zip_cords': item["zip_coords"]
    }


def community_insertion(item):
    return {
        "id": item['id'],
        "zip_code": item['zip_code'],
        "simplicy_index": item['simplicy_index'],
        "simplicy": item['simplicy'],
        "boundary_coordinates": item['boundary_coordinates'] if len(
            item['boundary_coordinates']) is not 0 else None,
        "neighboring_communities": item['neighboring_communities'] if len(
            item['neighboring_communities']) is not 0 else None
    }


if zip_table_response is not None and communities_table_response is not None:
    print("Starting to load zip_code data into db")
    t = Thread(target=insert_data_into_table, daemon=True, args=("zip_codes","/zip_codes.json",zip_insertion))
    t.start()
    t.join()
    print("Zip Code data loaded")

    print("Starting to load Communities data into db")
    t = Thread(target=insert_data_into_table, daemon=True, args=("communities","/communities.json",community_insertion))
    t.start()
    t.join()
    print("Community data loaded")

