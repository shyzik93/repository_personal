# -*- coding: utf-8 -*-
import sys, os, re, time

f = open('repper.py', 'r')
text = f.read()
f.close()

path = os.path.dirname(__file__)
if os.sep == '\\': path = path.replace('\\', '\\\\')
text = text.replace('{DIR_REPOSITORY_PERSONAL}', path)

for path in sys.path:
  if len(re.findall(r'.+\\Python[0-9]{2}\\lib$', path)) != 1: continue
  f = open(os.path.join(path, 'repper.py'), 'w')
  f.write(text)
  f.close()
  print u'Сделано! Файл repper.py скопирован сюда:', path
  break

time.sleep(5)
