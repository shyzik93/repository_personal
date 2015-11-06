# -*- coding: utf-8 -*-
import urllib2

def fopen(path, mode=None, data=None):
  if not mode: mode='r'
  f = open(path, mode)
  if data:
    f.write(data)
    f.close()
  else:
    data = f.read()
    f.close()
    return data

def safe_from_web(url, path, mode='wb'):
  ''' Маскирует архив с содержимым под картинку '''
  page = urllib2.urlopen(url)
  f = open(path, mode)
  f.write(page.read())
  f.close()

def joiner(path_png, path_rar, path_outpng):
  f1 = open(path_rar, 'rb')
  f2 = open(path_png, 'rb')

  f = open(path_outpng, 'wb')
  f.write(f2.read())
  f.write(f1.read())
  f.close()

  f1.close()
  f2.close()
