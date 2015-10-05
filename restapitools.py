# -*- coding: utf-8 -*-
import internettools
import lxml.html
import urlparse, urllib

class RESTAPITools():
  app_data = {}
  def __init__(self, acceessPermission, oauth_data, params):
    self.acceessPermission = acceessPermission
    self.oauth_data = oauth_data
    self.params = params
    self.it = internettools.InternetTools()

  def get_scope(self, scopes_list, sep):
    """ Формирует значения параметра scope - списка прав доступа.
        Возможны следующие варианты: {'aaa': 1, 'bbb': 1, 'ccc': 0, 'ddd': 1}
        или ['aaa', 'bbb', 'ddd'] """
    if 'dict' in str(type(scopes_list)):
      scopes_list = [scope for scope, value in scopes_list.items() if value]
    return sep.join(scopes_list)

  def _extract_app_data(self, response):
    fragment = urlparse.urlparse(response.geturl()).fragment
    print fragment
    app_data = urlparse.parse_qs(fragment)
    for k in app_data: app_data[k] = app_data[k][0]
    return app_data

  def _is_there_token(self, response):
    fragment = urlparse.urlparse(response.geturl()).fragment
    app_data = urlparse.parse_qs(fragment)
    if app_data.has_key('access_token'): return True
    else: return False

  def _is_frozen(self, str_page):
    #str_page = str_page.replace('text_panel login_blocked_panel', 'text_panel_login_blocked_panel')
    page = lxml.html.document_fromstring(str_page)
    divs = page.cssselect('div.login_blocked_panel')#text_panel_login_blocked_panel')
    if len(divs):
      for div in divs: print div.text
      print '\n'
      return True
    else: return False

  def is_incorrect_password(self, str_page):
    page = lxml.html.document_fromstring(str_page)
    divs = page.cssselect('div.service_msg_warning')
    if len(divs):
      for div in divs: print div.text
      print '\n'
      return True
    else: return False

  def do_authorize(self, user_data):
    params = {"client_id": user_data[0],
              "redirect_uri": self.oauth_data['uri_redirect'],
              "scope": self.get_scope(self.acceessPermission, self.oauth_data['scope_sep']),
              "response_type": "token",
              'state': '',
              self.params['display_name']: self.params['display_value_for_mobile']
    }

    print u'Открываем страницу для логининга...'
    str_page, res = self.it.urlopen(self.oauth_data['url_toopendialog'], 1, GET=params)
    params2, action_url = self.it.get_dictforms(str_page, res).values()[0]
    params2[self.oauth_data['name_for_email']] = user_data[1]
    params2[self.oauth_data['name_for_password']] = user_data[2]

    print u'Логинимся...'
    str_page, res = self.it.urlopen(action_url, 2, POST=params2)
    if self.is_incorrect_password(str_page): return 0, 'incorrect password'
    # Если вместо страницы логининга была страница подтверждения прав
    # (т. е. мы уже были залогинены), то вынимаем токен.
    if not self._is_there_token(res):
      if self._is_frozen(str_page): return 1, 'frozen'
      params2, action_url, form = self.it.get_dictforms(str_page, res, True).values()[0]
      print params2
      self.it.get_captcha(form, params2, 'captcha_key', 'captcha_img')
      # если мы вводили капчу
      print params2
      if self.oauth_data['name_for_password'] in params2:
        params2[self.oauth_data['name_for_email']] = user_data[1]
        params2[self.oauth_data['name_for_password']] = user_data[2]
      
      #params2 = urlparse.urlparse(action_url).query +"&"+ urllib.urlencode(params2)
      print params2

      print u'Подтверждаем права доступа...'
      str_page, res = self.it.urlopen(action_url, 3, POST=params2)
    else: print u'Пользователь был залогинен ранее.'

    print u'Сохраняем токен доступа.\n'
    self.app_data = self._extract_app_data(res)
    return []

if __name__ == '__main__':
  rat = RESTAPITools()
  print rat.get_scope({'aaa': 1, 'bbb': 1, 'ccc': 0, 'ddd': 1}, ',')
