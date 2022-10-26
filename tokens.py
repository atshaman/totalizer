# -*-coding: utf-8 -*-
# Универсальный класс для работы с токеном доступа
import os.path
import sys
import requests
import datetime
import pickle
import hashlib
from loguru import logger

timeout = 5


class Token:
    # Класс для работы с токеном. Поддерживает автоматическое обновление и загрузку с диска.
    def __init__(self, tokenurl, client, secret, persist=False):
        self.tokenurl = tokenurl
        self.client = client
        self.secret = secret
        self.persist = persist
        self.path = f'{hashlib.md5(self.tokenurl.encode()).hexdigest()}.dmp'
        self._token, self.expired_in, self.received = self.load()

    @logger.catch()
    def get_token(self):
        try:
            result = requests.post(self.tokenurl,
                                   data={'username': self.client, 'password': self.secret, 'grant_type': 'password',
                                         'client_id': 'portal'}, timeout=timeout)
            result.raise_for_status()
            result = result.json()
            return result['access_token'], result['expires_in'], datetime.datetime.now()
        except requests.exceptions.Timeout:
            logger.error('Токен не получен, превышен timeout!')
            sys.exit()
        except requests.exceptions.HTTPError as err:
            logger.error(f'Токен не получен из-за ошибки {err}!')
            sys.exit()
        except Exception as err:
            logger.error(f'Невозможно получить токен из-за ошибки {err}!')
            sys.exit()

    def save(self):
        # Сохраняем состояние токена
        with open(self.path, 'wb') as tokenfile:
            pickle.dump(self, tokenfile)
            logger.trace(f'Токен сохранен, {self.path}')

    def load(self):
        if os.path.exists(self.path) and self.persist:
            with open(self.path, 'rb') as tokenfile:
                self.__dict__ = pickle.load(tokenfile).__dict__
                logger.trace(f'Токен загружен из сохраненного файла {self.path}')
            return self._token, self.expired_in, self.received
        else:
            return self.get_token()

    @property
    def token(self):
        # Автообновление токена
        if self.received + datetime.timedelta(seconds=self.expired_in) < datetime.datetime.now():
            self._token, self.expired_in, self.received = self.get_token()
            logger.trace('Токен обновлен')
            if self.persist:
                self.save()
        return self._token

    @property
    def header(self):
        return dict(Authorization=f'Bearer {self.token}')

    def __repr__(self):
        return self.token
