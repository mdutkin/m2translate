import unittest
import os
from m2translate import *


__author__ = 'Maxim Dutkin (max@dutkin.ru)'


# clear all translate files for json store connector
json_path = os.path.join('json_store')


def count_json_locales(path):
    locales_cnt = 0
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            basename = os.path.split(file_path)[1]
            l, ext = os.path.splitext(basename)
            if ext == '.json':
                locales_cnt += 1
    return locales_cnt


# init translate module and json store connector
connector = JSONConnector()
tr = M2Translate(connector, not_found_val='N/A')
tr.clear_store()


class M2TranslateTests(unittest.TestCase):
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
        tr.add_locale('en_EN', dump_permanently=False)
        self.assertEqual(len(tr.locales), 2)
        print('#004 Locale `en_EN` created in memory')

    def test_005_set_active_locale(self):
        tr.set_cur_locale('en_EN')
        self.assertEqual(tr.cur_locale, 'en_EN')
        print('#005 Locale `en_EN` has been set as active')

    def test_006_add_phs_to_en(self):
        tr.set_p('FORM1.NAME', none='Name')
        tr.set_p('FORM1.SURNAME', none='Surname', l='en_EN')
        tr.set_p('FORM1.VISITS', none='visits', single='visit', multi='visits')
        tr.set_p('FORM1.SUBMIT', none='OK')
        self.assertEqual(len(tr.locales['ru_RU']), 3)
        self.assertEqual(len(tr.locales['en_EN']), 4)
        print('#006 Added placeholders for `en_EN`')

    def test_007_dump_en_locale(self):
        tr.dump_locales()
        self.assertEqual(len(tr.locales['ru_RU']), 4)
        self.assertEqual(len(tr.locales['en_EN']), 4)
        print('#007 Dumped locales (`en_EN`)')

    def test_008_reload_locales(self):
        tr.set_p('WILL_BE_ERASED', none='', single='', multi='')
        self.assertEqual(len(tr.locales['en_EN']), 5)
        tr.reload_locales()
        self.assertEqual(len(tr.locales['en_EN']), 4)
        print('#008 Locales are reloaded')

    def test_009_remove_locale(self):
        tr.add_locale('tmp_locale')
        tr.dump_locales()
        self.assertEqual(count_json_locales(json_path), 3)
        tr.remove_locale('tmp_locale', dump_permanently=True)
        self.assertEqual(count_json_locales(json_path), 2)
        print('#009 Locale was successfully created and then removed')
