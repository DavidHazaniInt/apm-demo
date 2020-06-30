## Implemented by API reference - https://www.elastic.co/guide/en/apm/agent/python/current/api.html

import elasticapm
import time
import pymongo
import redis
import random
import requests

rand = random.Random()

apm_client = elasticapm.Client(
    service_name='comlex',
    server_url='http://localhost:8200',
)
redis_client = redis.Redis()
mongo_client = pymongo.MongoClient()


def is_prime(
    number,
):
    for i in range(2, number):
        if (number % i) == 0:
            return False

    return True

@elasticapm.capture_span()
def generate_prime_number():
    number = rand.randint(1, 50000)

    while not is_prime(number):
        number = rand.randint(1, 50000)

    return number

@elasticapm.capture_span()
def sleep(seconds):
    time.sleep(seconds)


class CatsService:
    def get_cats(
        self,
        user_id,
    ):
        apm_client.begin_transaction(transaction_type='http_request')

        elasticapm.label(user_id=user_id)

        if user_id == 'TEST':
            apm_client.end_transaction(
                name='CatsService - get_cats',
                result='skipped',
            )

            return []

        try:
            generate_prime_number()
            self.search_cat_image()
            self.get_cats_for_user(user_id=user_id)
            self.sleep(rand.randint(1, 3))
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
            generate_prime_number()
            mongo_client.ocatqupied.cats.update_one(
                filter={
                    'id': cat_id,
                },
                update={
                    '$addToSet': {
                        'ignored_by': user_id,
                    },
                },
            )
            self.sleep(rand.randint(1, 3))
        finally:
            apm_client.end_transaction(
                name='CatsService - ignore_cat',
                result='success',
            )

    def search_cat_image(
        self,
    ):
        requests.get(
            url='https://www.google.com/search?q=cat+images&oq=cat+image&aqs=chrome.0.0j69i57j0l5j69i60.6987j0j1&sourceid=chrome&ie=UTF-8',
        )

    def get_cats_for_user(
        self,
        user_id,
    ):
        return list(mongo_client.ocatqupied.cats.find({
            'ignored_by': {
                '$ne': user_id,
            }
        }))




if __name__ == '__main__':
    elasticapm.instrument()

    cats_service = CatsService()

    for user_id in [
        'TEST',
        'TheKingCat',
        'CatTil',
        'NoOne',
        'HowHowHow',
        'PssPss',
    ]:
        cats_service.get_cats(
            user_id=user_id
        )

        cats_service.ignore_cat(
            user_id=user_id,
            cat_id='IchsaFichsa',
        )