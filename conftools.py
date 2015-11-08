# -*- coding: utf-8 -*-
# Added 2015.08.11

"""
Type 0:
-----------------------

service: YourNameService1
YourName1: YourValue
YourName2: YourValue

service: YourNameService2
YourName1: YourValue
YourName2: YourValue

-------------------------

{ 'YourNameService1': {'YourName1': 'YourValue', 'YourName2': 'YourValue'},
  'YourNameService2': {'YourName1': 'YourValue', 'YourName2': 'YourValue'} }
"""

def loadconf(path, _type=0):
  f = open(path, 'r')
  _conf = f.read().split('\n')
  f.close()

  if _type == 0:
    conf = {}
    service = None
    for string in _conf:
      if not string: continue
      name, value = string.split(':')
      value = value.strip()
      if name == 'service':
        service = value
        conf[service] = {}
        continue
      conf[service][name] = value
  return conf
