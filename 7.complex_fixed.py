## Implemented by API reference - https://www.elastic.co/guide/en/apm/agent/python/current/api.html

import elasticapm
import itertools
import pymongo
import random

rand = random.Random()

apm_client = elasticapm.Client(
    service_name='complex',
    server_url='http://localhost:8200',
)
mongo_client = pymongo.MongoClient()
cats_collection = mongo_client.ocatqupied.indexed_cats


def chunkify(
    iterable,
    chunk_size,
):
    iterable = iter(iterable)

    return iter(lambda: tuple(itertools.islice(iterable, chunk_size)), ())


class CatsService:
    def get_cats(
        self,
        user_id,
    ):
        apm_client.begin_transaction(transaction_type='http_request')

        elasticapm.label(user_id=user_id)

        try:
            self.get_cats_for_user(user_id=user_id)
        finally:
            apm_client.end_transaction(
                name='CatsService - get_cats',
                result='success',
            )

    def ignore_cat(
        self,
        user_id,
        cat_id,
    ):
        apm_client.begin_transaction(transaction_type='http_request')

        elasticapm.label(user_id=user_id)

        try:
            cats_collection.update_one(
                filter={
                    'id': user_id,
                },
                update={
                    '$addToSet': {
                        'ignore_list': cat_id,
                    },
                },
            )
        finally:
            apm_client.end_transaction(
                name='CatsService - ignore_cat',
                result='success',
            )

    def get_cats_for_user(
        self,
        user_id,
    ):
        cat_ignore_list = cats_collection.find_one({'id': user_id}, {'ignore_list'})['ignore_list']

        return list(cats_collection.find({
            'id': {
                '$nin': cat_ignore_list,
            }
        }, limit=100))


if __name__ == '__main__':
    elasticapm.instrument()

    cats_service = CatsService()

    user_ids = (
        f'generated_id_{i}'
        for i in range(30_000_000)
    )

    # DB initialization
    # cats_collection.delete_many({})

    # user_ids = list(user_ids)

    # for user_ids_chunk in chunkify(user_ids, 500_000):
    #     insert_operations = []

    #     for user_id in user_ids_chunk:
    #         insert_operations.append(
    #             pymongo.InsertOne({
    #                 'id': user_id,
    #                 'ignore_list': [],
    #             })
    #         )

    #     cats_collection.bulk_write(insert_operations)

    last_user_id = 'None'

    for user_id in user_ids:
        print(f'{user_id} process')

        cats_service.ignore_cat(
            user_id=user_id,
            cat_id=last_user_id,
        )

        cats_service.get_cats(
            user_id=user_id
        )

        last_user_id = user_id

