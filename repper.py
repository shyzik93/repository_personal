# -*- coding: utf-8 -*-
import sys, os
#path = os.path.join('E:'+os.sep, 'repository_personal')
path = os.path.join('{DIR_REPOSITORY_PERSONAL}')
if path not in sys.path: sys.path.append(path)
del path

'''
Этот модуль копируется в стандартный репозиторий и затем импортируется в той
программе, которая использует личный репозитрий.

Правила импорта:
import repper, далее следуют модули из личного репозитория
import модули из стандартного репозитория
import модули из стандартного репозитория, но загруженные извне
import модулей из поддиректорий программы
'''
