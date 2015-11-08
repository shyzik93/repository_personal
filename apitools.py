# -*- coding: utf-8 -*-
# Added 2015.11.06

class proto_api(object):
  def __init__(self):
    pass

  def shell(self, api_name, api_params):
    '''необхдимо перегрузить!
       Функция принимает имя метода и параметры,
       затем - делает запрос к серверу, возвращает ответ от сервера.'''
    pass

  def __getattr__(self, api_name, *args):
    return lambda **args: self.shell(api_name, args)

if __name__ == '__main__':
  class api(proto_api):
    def __init__(self):
      pass
    def shell(self, api_name, api_params):
      print api_name, api_params

  a = api()
  print a.ticker(arg1='value')
