#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, time

f = open('repper.py', 'r')
text = f.read()
f.close()

path = os.path.dirname(__file__)
if os.sep == '\\': path = path.replace('\\', '\\\\')
text = text.replace('{DIR_REPOSITORY_PERSONAL}', path)
print __file__

for path in sys.path:
  if sys.platform == 'win32':
    if len(re.findall(r'.+\\Python[0-9]{2}\\lib$', path)) != 1: continue
  elif 'linux' in sys.platform:
    if len(re.findall(r'/usr/lib/python[0-9](?:\.[0-9])?$', path)) != 1: continue
  else:
    print 'Unknown OS: %s!' % sys.platform
    break
  f = open(os.path.join(path, 'repper.py'), 'w')
  f.write(text)
  f.close()
  print u'Сделано! Файл repper.py скопирован сюда:', path
  break

time.sleep(5)

'''
Для запуска файла из консоли (linux) необходимо указывать полный путь к данному файлу. Например
$: cd /home/konstantin/repositories/repository_personal/
$: python /home/konstantin/repositories/repository_personal/repper_install.py
'''