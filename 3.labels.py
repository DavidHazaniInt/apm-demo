## Implemented by API reference - https://www.elastic.co/guide/en/apm/agent/python/current/api.html

import elasticapm
import time


apm_client = elasticapm.Client(
    service_name='labels',
    server_url='http://localhost:8200',
)


def uranium_enrichment(
    tts=1,
):
    time.sleep(tts)


def til_atom(
    request_id,
    user_id,
    tts,
):
    # Starting a transaction - passing the transaction type as an argument
    apm_client.begin_transaction(transaction_type='tasks')

    # Adding a label
    elasticapm.label(request_id=request_id)

    try:
        # Do something very important
        uranium_enrichment(tts=tts)
    except Exception:
        result = 'failure'
    else:
        result = 'success'
    finally:
        # Finishing the transaction - passing the transaction *name* and transaction result as an argument
        apm_client.end_transaction(
            name='til_atom',
            result=result,
        )


if __name__ == '__main__':
    for i in range(3):
        til_atom(
            request_id=f'request_id {i}',
            user_id='user_id',
            tts=i,
        )
