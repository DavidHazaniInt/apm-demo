## Implemented by API reference - https://www.elastic.co/guide/en/apm/agent/python/current/api.html

import elasticapm
import time


apm_client = elasticapm.Client(
    service_name='spans',
    server_url='http://localhost:8200',
)


@elasticapm.capture_span(
    span_type='db',
    span_subtype='Mongo',
    span_action='query',
)
def uranium_enrichment():
    time.sleep(0.80)


@elasticapm.capture_span(
    span_type='bucket',
    span_subtype='google',
    span_action='download',
)
def validation():
    time.sleep(0.25)


def til_atom(
    request_id,
    user_id,
):
    # Starting a transaction - passing the transaction type as an argument
    apm_client.begin_transaction(transaction_type='tasks')

    try:
        # Do something very important
        uranium_enrichment()
        validation()
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
    for _ in range(3):
        til_atom(
            request_id='request_id',
            user_id='user_id',
        )
