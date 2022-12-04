import os
import requests
import json
# get endpoint from env
secret = os.environ['HASURA_GRAPHQL_ADMIN_SECRET']
hasura_service = os.environ['HASURA_SERVICE_NAME']

# read from create.sql
payload = open('create.sql', 'r').read()

# make function to create headers

headers = {
    "Content-Type": "application/json",
    "x-hasura-admin-secret": secret
}


def get_url(endpoint):
    return os.path.join(hasura_service, endpoint)


# read hasura_metadata.json
metadata = open('hasura_metadata.json', 'r').read()

response = requests.post(
    url=get_url('v2/query'),
    json={
        "type": "run_sql",
        "args": {
            "source": "default",
            "sql": payload
        }
    },
    headers=headers)

response = requests.post(
    url=get_url('v1/metadata'),
    headers=headers,
    json={
        "type": "replace_metadata",
        "version": 1,
        "args": json.loads(metadata)
    }
)

print(json.dumps(response.json()))

# asi treba sleep na par sekund aby sa dal pouzivat endpoint graphql
# add dummy data
#users = [{"password": "pista", "username": "baci"}]
lon = E = 21.242813
lat = N = 48.731743

for x in range(0, 37):
    # daco je napicu ale nejak tak to ma fungovat
    response = requests.post(
        url=get_url('v1/graphql'),
        headers=headers,
        # pouzit user namiesto hardcoded
        json={
            'operationName': "MyMutation",
            'query': 'mutation MyMutation {\n  insert_parking_data_spots_one(object: {latitude:"' + str(lat) + '", longitude:"' + str(lon) + '", available: 2, last_updated: \"2022-12-04T09:35:43+00:00\"}) {\n    id\n  }\n}\n',
            'variables': {}
        }
    )
    print("graphql: " + json.dumps(response.json()))
    lon -= 0.000017
    lat += 0.00002

lon = E = 21.242943
lat = N = 48.731785

for x in range(0, 37):
    # daco je napicu ale nejak tak to ma fungovat
    response = requests.post(
        url=get_url('v1/graphql'),
        headers=headers,
        # pouzit user namiesto hardcoded
        json={
            'operationName': "MyMutation",
            'query': 'mutation MyMutation {\n  insert_parking_data_spots_one(object: {latitude:"' + str(lat) + '", longitude:"' + str(lon) + '", available: 2, last_updated: \"2022-12-04T09:35:43+00:00\"}) {\n    id\n  }\n}\n',
            'variables': {}
        }
    )
    print("graphql: " + json.dumps(response.json()))
    lon -= 0.000017
    lat += 0.00002

response = requests.post(
    url=get_url('v1/graphql'),
    headers=headers,
    # pouzit user namiesto hardcoded
    json={
        "query": """query MyQuery {
  parking_data_users {
    id
    password
    username
  }
}

            """
    }
)
print("users: " + json.dumps(response.json()))

# vygenerovat parking boxy podla GPS pointov a nejakeho smeru ulice napr (rucne to je nadlho)
# staci 1-2 ulice
