## Implemented by API reference - https://www.elastic.co/guide/en/apm/agent/python/current/api.html

import elasticapm


apm_client = elasticapm.Client(
    service_name='simple',
    server_url='http://localhost:8200',
)


def uranium_enrichment():
    pass


def til_atom(
    request_id,
    user_id,
):
    # Starting a transaction - passing the transaction type as an argument
    apm_client.begin_transaction(transaction_type='tasks')

    try:
        # Do something very important
        uranium_enrichment()
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


def til():
    # Starting a transaction - passing the transaction type as an argument
    apm_client.begin_transaction(transaction_type='tasks')

    try:
        # Do something very important
        pass
    except Exception:
        result = 'failure'
    else:
        result = 'success'
    finally:
        # Finishing the transaction - passing the transaction *name* and transaction result as an argument
        apm_client.end_transaction(
            name='til',
            result=result,
        )


if __name__ == '__main__':
    for _ in range(10):
        til()

    for _ in range(3):
        til_atom(
            request_id='request_id',
            user_id='user_id',
        )
