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
        app_name='example',
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
        trx_name='Example - with_decorator'
    )
    def with_decorator(
        self,
    ):
        pass

    def without_decorator(
        self,
    ):
        apm_client.begin_transaction(transaction_type='tasks')

        try:
            # Do something very important
            pass
        except Exception:
            result = 'failure'
        else:
            result = 'success'
        finally:
            self.apm_client.end_transaction(
                name='Example - without_decorator',
                result=result,
            )


if __name__ == '__main__':
    apm_client = ApmClient(
        server_url='http://localhost:8200',
        app_name='apm_client_example'
    )

    example = Example(
        apm_client=apm_client
    )
