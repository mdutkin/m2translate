from m2translate.interfaces import StoreConnector
import os
import json
import redis

__author__ = 'Maxim Dutkin (max@dutkin.ru)'


class RedisConnector(StoreConnector):
    def __init__(self,
                 redis_host: str = '127.0.0.1',
                 redis_db: int = 0,
                 redis_port: int = 6379,
                 **redis_connection_pool_kwargs):
        self.__r = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(
                host=redis_host,
                port=str(redis_port),
                db=redis_db,
                decode_responses=True,
                password='',
                **redis_connection_pool_kwargs
            ),
        )
        self.__r_scheme = {
            'locales': 'l:%s',
            'placeholders': '%s:%s'
        }
        super(RedisConnector, self).__init__()

    def save_locale(self, locale: str, data: dict):
        self.__r.sadd(self.__locale_tbl(locale), locale)
        for k, v in data.items():
            self.__r.lset(self.__ph_tbl(locale, k), 0, v[0])
            self.__r.lset(self.__ph_tbl(locale, k), 1, v[1])
            self.__r.lset(self.__ph_tbl(locale, k), 2, v[2])

    def remove_locale(self, locale):
        self.__r.srem(self.__locale_tbl(locale), locale)
        for key in self.__r.keys(self.__ph_tbl(locale, '*')):
            self.__r.delete(key)

    def load_locale(self, locale):
        data = {key: self.__r.lrange(key, 0, -1) for key in self.__r.keys(self.__ph_tbl(locale, '*'))}
        return data

    def locales(self) -> list:
        locales = self.__r.keys(self.__locale_tbl('*'))
        return locales

    def __locale_tbl(self, locale: str):
        return self.__r_scheme['locales'] % locale

    def __ph_tbl(self, locale: str, ph: str):
        return self.__r_scheme['placeholders'] % (locale, ph)
