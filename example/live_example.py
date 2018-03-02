from m2translate import M2Translate, JSONConnector
import datetime
import locale

__author__ = 'Maxim Dutkin (max@dutkin.ru)'

# init translate module and json store connector
connector = JSONConnector()
t = M2Translate(connector, not_found_val='N/A')
t.clear_store()
t.add_locale('ru_RU')
t.add_locale('en_US')
t.add_locale('fr_FR')

t.set_p('DEMO.INFO1', 'Для того, чтобы увидеть демку, заполните следующие данные', l='ru_RU')
t.set_p('DEMO.INFO1', 'For demo purposes, fill data below', l='en_US')
t.set_p('DEMO.INFO1', 'Pour des fins de démonstration, remplissez les données ci-dessous', l='fr_FR')

t.set_p('DEMO.NAME_PH', 'Ваше имя: ', l='ru_RU')
t.set_p('DEMO.NAME_PH', 'Your name: ', l='en_US')
t.set_p('DEMO.NAME_PH', 'Votre nom: ', l='fr_FR')

t.set_p('DEMO.SURNAME_PH', 'Ваша фамилия: ', l='ru_RU')
t.set_p('DEMO.SURNAME_PH', 'Your surname: ', l='en_US')
t.set_p('DEMO.SURNAME_PH', 'Votre nom de famille: ', l='fr_FR')

t.set_p('DEMO.AGE_PH', 'Сколько вам лет: ', l='ru_RU')
t.set_p('DEMO.AGE_PH', 'How old are you: ', l='en_US')
t.set_p('DEMO.AGE_PH', 'Quel âge avez-vous: ', l='fr_FR')

t.set_p('DEMO.AGE_V', none='лет', single='год', multi='лет', l='ru_RU')
t.set_p('DEMO.AGE_V', none='years old', single='year old', multi='years old', l='en_US')
t.set_p('DEMO.AGE_V', none='ans', single='an', multi='ans', l='fr_FR')

t.set_p('DEMO.INFO2', 'Отлично, теперь посмотри, что получилось!', l='ru_RU')
t.set_p('DEMO.INFO2', 'Awesome, check out the output!', l='en_US')
t.set_p('DEMO.INFO2', 'Génial, consultez la sortie!', l='fr_FR')

t.set_p('DEMO.INFO3', 'Спасибо, что ты проявил интерес к этому пакету. Сегодня `%s` (проверка даты локали), тебя зовут '
                      '%s %s и тебе сейчас %s %s!', l='ru_RU')
t.set_p('DEMO.INFO3', 'Great that you showed interest to this package. Today is `%s` (locale date check), your fullname'
                      ' is %s %s and you are %s %s!', l='en_US')
t.set_p('DEMO.INFO3', 'Génial que vous avez montré de l\'intérêt pour ce package. Aujourd\'hui est `%s` (vérification '
                      'de la date locale), votre nom complet est %s %s et vous avez %s %s!', l='fr_FR')

input_locale = input('select locale from the following list [\'ru_RU\', \'en_US\', \'fr_FR\']: ')
t.set_cur_locale(input_locale)
locale.setlocale(locale.LC_ALL, '%s.UTF-8' % input_locale)

print(t.p('DEMO.INFO1'))
name = input(t.p('DEMO.NAME_PH'))
surname = input(t.p('DEMO.SURNAME_PH'))
age = input(t.p('DEMO.AGE_PH'))
print(t.p('DEMO.INFO2'))
print(t.p('DEMO.INFO3') % (
          datetime.datetime.now().strftime('%c'),
          name,
          surname,
          age,
          t.p('DEMO.AGE_V', age)
      ))
