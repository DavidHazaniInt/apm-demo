import enum
import functools

import elasticapm


def transaction(
    trx_type,
    trx_name,
):
    def decorator_transaction(
        func,
    ):
        @functools.wraps(func)
        def wrapper_transaction(
            *args,
            **kwargs,
        ):
            apm_client = args[0].apm_client

            try:
                apm_client.begin_transaction(trx_type.value)

                func_result = func(*args, **kwargs)

                trx_result = TransactionResults.SUCCESS
            except Exception:
                apm_client.capture_exception()
                trx_result = TransactionResults.EXCEPTION

                raise
            finally:
                apm_client.end_transaction(
                    name=trx_name,
                    result=trx_result.value,
                )

            return func_result

        return wrapper_transaction

    return decorator_transaction


class TransactionTypes(
    enum.Enum,
):
    GRPC_REQUEST = 'GRPC request processing'
    REST_REQUEST = 'REST request processing'
    WORKER = 'Worker message processing'
    TASK = 'Scheduled task'


class TransactionResults(
    enum.Enum,
):
    SUCCESS = 'Success'
    FAILURE = 'Failure'
    EXCEPTION = 'Exception'
    RETRY_LATER = 'Retry later'
    SKIPPING = 'Skipping'


class ApmClient(
    elasticapm.Client,
):
    def __init__(
        self,
        server_url,
        secret_token=None,
        app_name='example 1',
    ):
        super().__init__(
            service_name=app_name,
            server_url=server_url,
            secret_token=secret_token,
            server_timeout='10s',
            transaction_sample_rate=0.1,
        )

    def instrument(
        self,
    ):
        elasticapm.instrument()

    def label(
        self,
        **kwargs
    ):
        elasticapm.label(**kwargs)


class Example:
    def __init__(
        self,
        apm_client,
    ):
        self.apm_client = apm_client

    @transaction(
        trx_type=TransactionTypes.TASK,
        trx_name='Example - do_somthing_important'
    )
    def do_somthing_important(
        self,
    ):
        pass


if __name__ == '__main__':
    apm_client = ApmClient(
        server_url='http://localhost:8200',
    )

    example = Example(
        apm_client=apm_client
    )
