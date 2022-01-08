# -*- coding: utf-8 -*-
import os, urllib2, urllib, cookielib, urlparse, itertools, mimetools, mimetypes
import lxml.html

def encode_multipart(key_words, *list_file_dicts):
  """Return a string representing the form data, including attached files."""
  files = []
  for file_dict in list_file_dicts:
    filename = os.path.basename(file_dict['path'])
    if 'mimetype' not in file_dict: mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    else: mimetype = file_dict['mimetype']
    with open(file_dict['path'], 'rb') as f:
      files.append((file_dict['field'], filename, mimetype, f.read()))

  form_fields = key_words.items()
  boundary = mimetools.choose_boundary()
  part_boundary = '--' + boundary

  parts = []
        
  # Add the form fields
  parts.extend(
    [ part_boundary, 'Content-Disposition: form-data; name="%s"' % name, '', value, ]
      for name, value in form_fields
  )
  # Add the files to upload
  parts.extend(
    [ part_boundary,
      'Content-Disposition: file; name="%s"; filename="%s"' % (field_name, filename),
      'Content-Type: %s' % content_type,
      '', body,
     ]
     for field_name, filename, content_type, body in files
  )
  flattened = list(itertools.chain(*parts))
  flattened.append('--' + boundary + '--')
  flattened.append('')
  return '\r\n'.join(flattened), boundary

class InternetTools():
  def __init__(self, logdir=None, geterrors=False):
    if logdir == None:
      self.logdir = os.path.join('logs', '%s')
      if not os.path.exists(self.logdir%''): os.mkdir(self.logdir%'')
    else: self.logdir = logdir
    self.geterrors = geterrors
    self.cookie_handler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    self.redirect_handler = urllib2.HTTPRedirectHandler()
    self.http_handler = urllib2.HTTPHandler()
    self.https_handler = urllib2.HTTPSHandler()
    self.opener = urllib2.build_opener(self.cookie_handler, self.redirect_handler, self.http_handler, self.https_handler)

  def save_log(self, log_name, page, response):
    log_name = self.logdir % str(log_name)+'.html'

    f = open(log_name, 'w')
    f.write(str(page))
    f.close()

    f = open(log_name+'.txt', 'w')
    f.write(response.geturl())
    f.write('\n\n')
    f.write(str(response.code) + ' ' + response.msg)
    f.write('\n')
    f.write(str(response.info()))
    f.close()

  def urlopen(self, url, log_name=None, POST=None, GET=None, headers={}):
    if isinstance(POST, dict): POST = urllib.urlencode(POST)
    if isinstance(GET, dict): GET = urllib.urlencode(GET)
    if GET != None: url += '?' + GET

    self.opener.addheaders.extend(headers.items())
    if not self.geterrors: response = self.opener.open(url, POST)
    else:
      try: response = self.opener.open(url, POST)
      except Exception as e: return e[0], None, None
    str_page = response.read()
    if log_name != None: self.save_log(log_name, str_page, response)

    #print 1111111111111111
    #return str_page, response if not self.geterrors else None, str_page, response # повторяет две инструкции два раза
    if not self.geterrors: return str_page, response
    else: return None, str_page, response

  def send_files(self, url, log_name, key_words, *list_file_dicts):
    POST, boundary = encode_multipart(key_words, *list_file_dicts)

    request = urllib2.Request(url)
    request.add_header('Content-type', 'multipart/form-data; boundary=' + boundary)
    request.add_header('Content-length', len(POST))
    request.add_data(POST)

    #self.cookieJar.add_cookie_header(request)
    return self.urlopen(request, log_name)

  def form2dict(self, form, response):
    # Собираем параметры
    key_value = {}
    for inpt in form.inputs:
        value = inpt.value
        name = inpt.name
        if None not in [name, value]: key_value[name] = value.encode('utf-8')
        if None == value: key_value[name] = ''
    #if key_value.has_key(None): del key_value[None] # У кнопки обычно нет имени.
    # Извлекаем адрес отправки формы
    action_url = form.action
    if action_url == None: action_url = response.geturl()

    parts = urlparse.urlsplit(action_url)
    # если относительный адрес...
    if parts.scheme == '' and parts.netloc == '':
        # относительно сервера
        if action_url[0] == '/':
            netloc = urlparse.urlsplit(response.geturl()).netloc
            action_url = 'https://' + netloc + action_url
        # относительно адреса текущей страницы
        else: action_url = os.path.dirname(response.geturl()) +'/'+ action_url
        print 'action url after parse: ', action_url
    return {'data': key_value, 'url': action_url, 'method': form.method}

  def get_dictforms(self, str_page, response, return_forms=False):
    page = lxml.html.document_fromstring(str_page)
    forms = page.forms
    dictforms = {}
    index = 0
    for form in forms:
      _form = self.form2dict(form, response)
      if return_forms: _form['form'] = form
      dictforms[form.get('name')] = _form
      index += 1
    return dictforms

  def get_form(self, str_page, response, selector):
    page = lxml.html.document_fromstring(str_page)
    if isinstance(selector, int): form = page.forms[selector]
    else: form = page.cssselect(selector)
    return self.form2dict(form, response)

  def get_captcha(self, form, key_value, captcha_input_name, captcha_img_class):
    if captcha_input_name in key_value:
      img = form.cssselect('img.'+captcha_img_class)[0]
      captcha_url = img.attrib['src']
      captcha_img = self.opener.open(captcha_url).read()


      #dataMngt.write(logdir % 'captcha.jpg', captcha_img, 'wb')
      f = open(self.logdir % 'captcha.jpg', 'wb')
      f.write(captcha_img)
      f.close()

      captcha_key = raw_input('Input the captcha number:')
      key_value[captcha_input_name] = captcha_key

#class BrowserEmulator():
#  def __init__(self):
#    self.it = InternetTools()

  def openForm(self, url, values, id_form, log_name=None, func=None):
    # открываем страницу с формой
    str_page, response = self.urlopen(url, log_name)
    # вынимаем данные формы id_form (адрес отправки, имена полей и их значения по умолчаниею)
    form = self.get_form(str_page, response, id_form) #get_dictforms(str_page, response)[id_form]
    # отправляем данные формы и взозвращаем страницу
    if func is not None: func(form['data'])
    form['data'].update(values)
    data = {form['method']: form['data']}
    if log_name is not None: log_name += '_result'
    str_page, response = self.urlopen(form['url'], log_name, **data)
    return str_page.decode('utf-8')

if __name__ == '__main__':
  #it = InternetTools(geterrors=True)
  #print it.urlopen('http://for-skills.h2m.ru', headers={'User-agent': 'bl'}, GET={'emode': 'true'})[1]
  be = InternetTools()#BrowserEmulator()
  #be.openForm('http://spaces.ru/registration/', {'contact':'test@mail.ru'}, 0)
  be.openForm('http://socialtools.ru', {'usertype':2, 'username': 'username', 'password':''}, 0)
