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
users = [{"password": "pista", "username": "baci"}]
for user in users:
    # daco je napicu ale nejak tak to ma fungovat
    response = requests.post(
        url=get_url('v1/graphql'),
        headers=headers,
        # pouzit user namiesto hardcoded
        json={
            "query": """mutation MyMutation {
                    insert_parking_data_users_one(object: {username: "baci", password: "pista"}) {
                        id
                    }
                }
            """
        }
    )
    print("graphql: " + json.dumps(response.json()))

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
