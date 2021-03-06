## Implemented by API reference - https://www.elastic.co/guide/en/apm/agent/python/current/api.html

import elasticapm
import pymongo
import redis
import requests


apm_client = elasticapm.Client(
    service_name='instrument',
    server_url='http://localhost:8200',
)
redis_client = redis.Redis()
mongo_client = pymongo.MongoClient()


def uranium_enrichment():
    requests.get('https://www.google.com/search?q=Where+i+can+find+enrichmed+uranium&oq=Where+i+can+find+enrichmed+uranium&aqs=chrome..69i57j33.32739j0j1&sourceid=chrome&ie=UTF-8')


def push_to_queue():
    redis_client.lpush(
        'til_atom_queue',
        b'til lapanim',
    )


def complete_mission():
    mongo_client.til.missions.insert({
        'id': 'til_atom',
        'status': 'done',
    })


def til_atom(
    request_id,
    user_id,
):
    # Starting a transaction - passing the transaction type as an argument
    apm_client.begin_transaction(transaction_type='tasks')

    try:
        # Do something very important
        uranium_enrichment()
        push_to_queue()
        complete_mission()
    except Exception:
        result = 'failure'
    else:
        result = 'success'

    # Finishing the transaction - passing the transaction *name* and transaction result as an argument
    apm_client.end_transaction(
        name='til_atom',
        result=result,
    )


if __name__ == '__main__':
    # Inject apm code to all the known libraries
    elasticapm.instrument()

    for _ in range(3):
        til_atom(
            request_id='request_id',
            user_id='user_id',
        )
