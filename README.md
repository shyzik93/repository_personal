# repository_personal

<<<<<<< HEAD
Это мой личный набор модулей, написанных мной (есть, конечно, "утащенные строчки") для упрощения кода проектов. При запуске файла repper_install в стандартную папку Питона добавится модуль repper. В дальнейшем, его нужно импортировать перед импорта остальных модулей из репозитория - он добавляет в sys.path директорию repository_personal. Это позволяет хранить личный репозиторий в любой директории, оставляя его доступным всем Вашим проектам.
=======
Это мой личный набор модулей, написанных мной (есть, конечно, "утащенные строчки") для упрощения кода проектов. При запуске файла repper_install в стандартную папку Питона добавится модуль repper. Его нужно импортировать перед импорта остальных модулей из репозитория - он добавляет в sys.path директорию repository_personal. Это позволяет хранить личный репозиторий в любой директории, оставляя его доступным всем Вашим проектам.
>>>>>>> f77e91de41ec6c045cb2f354f51c194588ef492d

Но чтобы не заморачиваться, можно нужные модули вручную забарсывать или в основную директорию Питона, или в директорию с Вашим проектом.

# Содержание репозитория

## apitools

Модуль для создания модулей, реализующих API для различных сервисов, имеющих соответсвующую поддержку. Модуль содержит класс **proto_api**. Этот класс наследуется Вашим классом API, и Ваш класс должен содержать функцию **shell**, которой будет передаваться имя метода и аргументы в виде словаря. Это позволяет не писать множество похожих функций для сервиса. Например, Ваш класс может быть таким:
```
import repper, apitools
import urllib, urllib2, json, hashlib, os, time

class API(apitools.proto_api):
  __url = "https://api.example.com/v1/"
  def __init__(self, api_key, api_secret):
    self.__api_key = api_key
    self.__api_secret = api_secret

  def public_api(self, api_name, api_params={}):
    x = 1
    while x:
      req = urllib2.Request(self.__url + api_name+'?'+urllib.urlencode(api_params), headers={'Accept-Charset': 'utf-8' })
      x = 0
    return urllib2.urlopen(req).read()

  # Имя - обязательно shell!
  def shell(self, api_name, api_params):
    if api_name[0] == '_': answer = self.auth_api(api_name[1:], api_params)
    else: answer = self.public_api(api_name, api_params)

    jd = json.JSONDecoder()
    return jd.decode(answer) 
```
После чего вы можете легко обращаться к разным методам сервиса api.example.com без написания специальных функций:
```
api = API(key, secret)
print api.get_user_info(user_id=123456789)
```
В результате будет вызван URL "https://api.example.com/v1/get_user_info?user_id=123456789" . В функции **shell** также можно реализовать предварительную обработку ответа сервера - например, ошибок.

## archivetools

Модуль для работы с архивами. Пока только zip. Модуль содержит один класс ArchiveTools(), имеющий следующие функции:

- **ArchiveTools.unpack(archive_path, unpack_dir)** - распаковывает архив с путём **archive_path** в директорию **unpack_dir**.
- **ArchiveTools.pack(archive_path, unpack_dir, mode='w', start_dir='', user_zp=None)** - архивирует содержимое директории **unpack_dir** в архив по пути **archive_path**. Режим mode позволяет как создать новый архив ("w" - по умолчанию), так и дополнить существующий ("a"). **start_dir** - начальная директория в архиве, в которую будет записываться содержимое. **user_zp** - это объект Вашего архива, если он уже открыт, если он указан, то путь **archive_path** будет проигнорирован.
- **ArchiveTools.zipopen(archive_path, mode, _type=zipfile.ZIP_DEFLATED)** - возвращает объект архива по пути **archive_path**.

## conftools

Модуль для загрузки настроек из файла. Имеет одну функцию:

- **loadconf(path, _type=0)** - парсит файл path и возвращает словарь словарей настроек. Например, файл с содержимым

```
service: YourNameService1
YourName1: YourValue
YourName2: YourValue
service: YourNameService2
YourName1: YourValue
YourName2: YourValue
```

будет возвращён вышеуказанной функцией в виде словаря:

```
{ 'YourNameService1': {'YourName1': 'YourValue', 'YourName2': 'YourValue'},
  'YourNameService2': {'YourName1': 'YourValue', 'YourName2': 'YourValue'} }
```
## internettools

Модуль с инструментами для работы с Интернетом  и веб-документами. Содержит определение класса InternetTools(), имеющего следующие методы:

- **InternetTools.urlopen(url, log_name=None, POST=None, GET=None, headers={})** - возвращает содержимое страницы **url**,  а также, сохраненяет эту страницу в файл **log_name**, если он указан. Возможно передать как GET-,  так POST-запрос, а также все необходимые заголовки. Запрос может быть в вде словаря или же в виде строки, возвращаемой функцией **urllib.urlencode()**. Класс хранит все куи и автоматиченски обрабатывает заголовки, перенапрвления им прочее.
- **send_files(url, log_name, key_words, *list_file_dicts)** - отправляет файл через POST-запрос.
- **form2dict(form, response)** - преобразует объект формы в словарь.
- **get_dictforms(str_page, response, return_forms=False)** - извлекает из страницы **str_page** объекты форм и возвращает список форм в виде словаря.
- **get_captcha(form, key_value, captcha_input_name, captcha_img_class)** - извлекает изображение капчи при REST API авторизации. Работает пока лишь для соцсети ВКонтакте.
