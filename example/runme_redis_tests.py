import unittest
import os
from m2translate import *

__author__ = 'Maxim Dutkin (max@dutkin.ru)'


# init translate module and json store connector
connector = RedisConnector(redis_host='127.0.0.1', redis_port=6379, redis_db=0)
tr = M2Translate(connector, not_found_val='N/A')
tr.clear_store()


def count_redis_locales(path):
    locales_cnt = 0
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            basename = os.path.split(file_path)[1]
            l, ext = os.path.splitext(basename)
            if ext == '.json':
                locales_cnt += 1
    return locales_cnt


class M2TranslateRedis(unittest.TestCase):
    def test_001_create_locale(self):
        tr.add_locale('ru_RU', dump_permanently=False)
        self.assertEqual(len(tr.locales), 1)
        print('#001 Locale `ru_RU` created in memory')

    def test_002_add_phs_to_ru(self):
        tr.set_p('FORM1.NAME', none='Имя')
        tr.set_p('FORM1.SURNAME', none='Фамилия', l='ru_RU')
        tr.set_p('FORM1.VISITS', none='визитов', single='визит', multi='визитов')
        self.assertEqual(len(tr.locales['ru_RU']), 3)
        print('#002 Added placeholders for `ru_RU`')

    def test_003_dump_ru_locale(self):
        tr.dump_locales()
        print('#003 Dumped locales (`ru_RU`)')