# -*- coding: utf-8 -*-
import urllib2, os, re

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
  page = urllib2.urlopen(url)
  f = open(path, mode)
  f.write(page.read())
  f.close()

def joiner(path_png, path_rar, path_outpng):
  ''' Маскирует архив с содержимым под картинку '''
  f1 = open(path_rar, 'rb')
  f2 = open(path_png, 'rb')

  f = open(path_outpng, 'wb')
  f.write(f2.read())
  f.write(f1.read())
  f.close()

  f1.close()
  f2.close()

def find_str(in_dir, string, except_files=[], file_log=None):
  ''' Осуществляет поиск строки (регулярного выражения) по содержимому файлов '''
  def _find_str(string, dirname, names):
    for name in names:
      path = os.path.join(dirname, name)
      if os.path.isdir(path): continue
      if path.split('.')[-1] in except_files: continue
      f = open(path, 'r')
      text = f.read()
      f.close()
      finded = re.findall(string, text)
      count = len(finded)
      if count > 0:
        print count, path
        if file_log == None: continue
        f1.write('....' + str(count) + ' ' + path + '\n')
        for _finded in finded:
          f1.write(_finded.strip() + '\n')
        f1.write('\n')
  os.path.walk('wb', _find_str, '.*str_replace.*')

if __name__ == '__main__':
  with open('finded_strings.txt', 'w') as f1:
    find_str('wb', '.*str_replace.*', except_files = ['css', 'js', 'htt', 'txt'], file_log=f1)
