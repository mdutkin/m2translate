import unittest
import os
from m2translate import *

__author__ = 'Maxim Dutkin (max@dutkin.ru)'


# init translate module and json store connector
connector = RedisConnector(redis_host='127.0.0.1', redis_port=6379, redis_db=0)
tr = M2Translate(connector, not_found_val='N/A')


class M2TranslateRedis(unittest.TestCase):
    def test_010_signal(self):
        print('redis')
