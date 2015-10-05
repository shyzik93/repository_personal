# -*- coding: utf-8 -*-
import zipfile, os

class ArchiveTools():
  def __init__(self): pass

  def _write_file(self, path, f):
    # lichtfjyr
    if not os.path.exists(os.path.dirname(path)):
      spath = os.path.dirname(path).split(os.sep)
      tpath = spath.pop(0) + os.sep
      for name in spath:
        tpath = os.path.join(tpath, name)
        if not os.path.exists(tpath): os.makedirs(tpath)
    f1 = open(path, 'wb')
    f1.write(f.read())
    f1.close()
  
  def unpack(self, archive_path, unpack_dir):
    archive = zipfile.ZipFile(archive_path, 'r')
    paths = archive.namelist()
    for path in paths:
      f = archive.open(path)
      if os.path.basename(path):
        self._write_file(os.path.normpath(os.path.join(unpack_dir, path)), f)
    archive.close()

  def _createZip(self, rec, _path=None, names=None):
    for name in names:
      #print _path, name
      path = os.path.join(_path, name)
      #print os.path.join(rec[1], path.replace(rec[0], '')), rec[1], rec[0]
      if os.path.isfile(path): rec[2].write(path, rec[1]+path.replace(rec[0], ''))

  def pack(self, archive_path, unpack_dir, mode='w', start_dir='', user_zp=None):
    if user_zp == None: zp = zipfile.ZipFile(archive_path, mode, zipfile.ZIP_DEFLATED)
    else: zp = user_zp
    os.path.walk(unpack_dir, self._createZip, [unpack_dir, start_dir, zp])
    if user_zp==None: zp.close()

  def zipopen(self, archive_path, mode, _type=zipfile.ZIP_DEFLATED):
    return zipfile.ZipFile(archive_path, mode, _type)
