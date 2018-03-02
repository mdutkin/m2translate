import unittest
import redis
from m2translate import *

__author__ = 'Maxim Dutkin (max@dutkin.ru)'


# init translate module and redis store connector
redis_host = '127.0.0.1'
redis_port = 6379
redis_db = 0
connector = RedisConnector(redis_host=redis_host, redis_port=redis_port, redis_db=redis_db)
tr = M2Translate(connector, not_found_val='N/A')
tr.clear_store()


def count_redis_locales():
    r = redis.StrictRedis(
        connection_pool=redis.ConnectionPool(
            host=redis_host,
            port=str(redis_port),
            db=redis_db,
            decode_responses=True,
            password=''
        ),
    )
    return len([l for l in r.keys('l:*')])


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

    def test_004_create_new_locale(self):
        tr.add_locale('en_US', dump_permanently=False)
        self.assertEqual(len(tr.locales), 2)
        print('#004 Locale `en_US` created in memory')

    def test_005_set_active_locale(self):
        tr.set_cur_locale('en_US')
        self.assertEqual(tr.cur_locale, 'en_US')
        print('#005 Locale `en_US` has been set as active')

    def test_006_add_phs_to_en(self):
        tr.set_p('FORM1.NAME', none='Name')
        tr.set_p('FORM1.SURNAME', none='Surname', l='en_US')
        tr.set_p('FORM1.VISITS', none='visits', single='visit', multi='visits')
        tr.set_p('FORM1.SUBMIT', none='OK')
        self.assertEqual(len(tr.locales['ru_RU']), 3)
        self.assertEqual(len(tr.locales['en_US']), 4)
        print('#006 Added placeholders for `en_US`')

    def test_007_dump_en_locale(self):
        tr.dump_locales()
        self.assertEqual(len(tr.locales['ru_RU']), 4)
        self.assertEqual(len(tr.locales['en_US']), 4)
        print('#007 Dumped locales (`en_US`)')

    def test_008_reload_locales(self):
        tr.set_p('WILL_BE_ERASED', none='', single='', multi='')
        self.assertEqual(len(tr.locales['en_US']), 5)
        tr.reload_locales()
        self.assertEqual(len(tr.locales['en_US']), 4)
        print('#008 Locales are reloaded')

    def test_009_remove_locale(self):
        tr.add_locale('tmp_locale')
        tr.dump_locales()
        self.assertEqual(count_redis_locales(), 3)
        tr.remove_locale('tmp_locale', dump_permanently=True)
        self.assertEqual(count_redis_locales(), 2)
        print('#009 Locale was successfully created and then removed')

    def test_010_get_translations(self):
        tr.set_cur_locale('ru_RU')
        self.assertEqual(tr.p('FORM1.VISITS', 0), 'визитов')
        self.assertEqual(tr.p('FORM1.VISITS', 1), 'визит')
        self.assertEqual(tr.p('FORM1.VISITS', 10), 'визитов')
        tr.set_cur_locale('en_US')
        self.assertEqual(tr.p('FORM1.VISITS', 0), 'visits')
        self.assertEqual(tr.p('FORM1.VISITS', 1), 'visit')
        self.assertEqual(tr.p('FORM1.VISITS', 10), 'visits')
        print('#010 Placeholder values were successfully returned')
