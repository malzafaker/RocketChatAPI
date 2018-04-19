import logging

import re
import requests

from pytils import translit

from django.conf import settings

logger = logging.getLogger(__name__)


class ChannelsAPIMixin(object):

    def create_channels(self, name='', readOnly=False, members=None):
        """
        Создание публичного канала
        :param name: Название канала
        :param readOnly: true/false - возможность установить канал только для чтения
        :param members: Добавить пользователей в канал
        :return: Статус, id канала, название канала
        """
        name = translit.translify("_".join(name.split(' ')))
        members = [] if members is None else members
        data = {
            'name': name,
            'members': members,
            'readOnly': readOnly
        }
        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.create',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail create_channels: %s' % resp.text, exc_info=True)
            return False
        logger.info('create_channels.resp - %s' % resp, exc_info=True)

        data = resp.json()
        return data['success'], data['channel']['_id'], data['channel']['name'],

    def channels_add_owner(self, roomId, userId):
        """
        Добавляем админа в канал
        :param roomId: id комнаты
        :param userId: id пользователя в чате
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.addOwner',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_add_owner: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_add_owner.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_set_description(self, roomId, description):
        """
        Добавляем описание для канала
        :param roomId: id комнаты
        :param description: описание
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'description': description
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.setDescription',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail set_description: %s' % resp.text, exc_info=True)
            return False
        logger.info('set_description.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_set_topic(self, roomId, topic):
        """
        Добавляем тему для канала
        :param roomId: id комнаты
        :param topic: тема
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'topic': topic
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.setTopic',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail set_topic: %s' % resp.text, exc_info=True)
            return False
        logger.info('set_topic.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_set_type(self, roomId, private=False):
        """
        Публичный/приватный канал
        :param roomId: id комнаты
        :param private: True/False
        :return: status (True/False)
        """
        type = 'p' if private is True else 'c'
        data = {
            'roomId': roomId,
            'type': type
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.setType',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail set_type: %s' % resp.text, exc_info=True)
            return False
        logger.info('set_type.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_rename(self, roomId, name):
        """
        Изменить название канала
        :param roomId: id комнаты
        :param name: название
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'name': name
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.rename',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_rename: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_rename.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_kick(self, roomId, userId):
        """
        Убрать пользователя из канала
        :param roomId: id комнаты
        :param userId: id пользователя в чате
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.kick',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_kick: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_kick.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_invite(self, roomId, userId):
        """
        Добавить пользователя в канал
        :param roomId: id комнаты
        :param userId: id пользователя в чате
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.invite',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_invite: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_invite.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_archive(self, roomId):
        """
        Архивировать канал
        :param roomId: id комнаты
        :return: status (True/False)
        """
        data = {
            'roomId': roomId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.archive',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_archive: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_archive.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def channels_unarchive(self, roomId):
        """
        Разархивировать канал
        :param roomId: id комнаты
        :return: status (True/False)
        """
        data = {
            'roomId': roomId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.unarchive',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_unarchive: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_unarchive.resp - %s' % resp, exc_info=True)
        data = resp.json()

        return data['success']

    def channels_close(self, roomId):
        """
        Закрыть канал
        :param roomId: id комнаты
        :return: status (True/False)
        """
        data = {
            'roomId': roomId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/channels.close',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail channels_close: %s' % resp.text, exc_info=True)
            return False
        logger.info('channels_close.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']


class GroupsAPIMixin(object):

    def create_groups(self, name='', readOnly=False, members=None):
        """
        Создание публичного группы
        :param name: Название группы
        :param readOnly: true/false - возможность установить группу только для чтения
        :param members: Добавить пользователей в группу
        :return: Статус, id канала, название группы
        """
        name = translit.translify("_".join(name.split(' ')))
        members = [] if members is None else members
        data = {
            'name': name,
            'members': members,
            'readOnly': readOnly
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.create',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail create_groups: %s' % resp.text, exc_info=True)
            return False
        logger.info('create_groups.resp - %s' % resp, exc_info=True)

        data = resp.json()
        return data['success'], data['group']['_id'], data['group']['name']

    def groups_add_owner(self, roomId, userId):
        """
        Добавляем админа в группу
        :param roomId: id комнаты
        :param userId: id пользователя в чате
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.addOwner',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_add_owner: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_add_owner.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_set_description(self, roomId, description):
        """ Добавляем описание для группы
        :param roomId: id комнаты
        :param description: описание
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'description': description
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.setDescription',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_set_description: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_set_description.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_set_topic(self, roomId, topic):
        """ Добавляем тему для группы
        :param roomId: id комнаты
        :param topic: тема
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'topic': topic
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.setTopic',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_set_topic: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_set_topic.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_set_type(self, roomId, private=False):
        """ Публичный/приватный группа
        :param roomId: id комнаты
        :param private: True/False
        :return: status (True/False)
        """
        type = 'p' if private is True else 'c'
        data = {
            'roomId': roomId,
            'type': type
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.setType',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_set_type: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_set_type.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_rename(self, roomId, name):
        """ Изменить название группы
        :param roomId: id комнаты
        :param name: название
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'name': name
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.rename',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_rename: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_rename.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_kick(self, roomId, userId):
        """ Убрать пользователя из группы
        :param roomId: id комнаты
        :param userId: id пользователя в чате
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.kick',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_kick: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_kick.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_invite(self, roomId, userId):
        """ Добавить пользователя в группу
        :param roomId: id комнаты
        :param userId: id пользователя в чате
        :return: status (True/False)
        """
        data = {
            'roomId': roomId,
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.invite',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_invite: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_invite.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_archive(self, roomId):
        """ Архивировать группу
        :param roomId: id комнаты
        :return: status (True/False)
        """
        data = {
            'roomId': roomId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.archive',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_archive: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_archive.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']

    def groups_unarchive(self, roomId):
        """ Разархивировать группу
        :param roomId: id комнаты
        :return: status (True/False)
        """
        data = {
            'roomId': roomId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.unarchive',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_unarchive: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_unarchive.resp - %s' % resp, exc_info=True)
        data = resp.json()

        return data['success']

    def groups_close(self, roomId):
        """ Закрыть группу
        :param roomId: id комнаты
        :return: status (True/False)
        """
        data = {
            'roomId': roomId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/groups.close',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail groups_close: %s' % resp.text, exc_info=True)
            return False
        logger.info('groups_close.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data['success']


class RocketChat(ChannelsAPIMixin, GroupsAPIMixin):
    userId = None
    authToken = None
    headers = {
        'X-Auth-Token': None,
        'X-User-Id': None,
    }

    def __init__(self, **kwargs):
        self.userId, self.authToken = self.authorize(settings.ROCKETCHAT_USERNAME, settings.ROCKETCHAT_PASSWORD)
        self.headers = {
            'X-Auth-Token': self.authToken,
            'X-User-Id': self.userId,
        }

    def auth_admin(self):
        self.__init__()
        return self.userId, self.authToken

    def get_headers(self, userId):
        return {
            'X-Auth-Token': self.create_token(userId),
            'X-User-Id': userId,
        }

    def authorize(self, username, password):
        """
        Авторизация пользователя в чате
        :param username: логин
        :param password: пароль
        :return: userId, authToken
        """
        data = {
            'user': username,
            'password': password
        }
        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/login',
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail authorize: %s' % resp.text, exc_info=True)
            return None, None

        logger.info('authorize - %s' % resp, exc_info=True)

        data = resp.json()['data']
        return data['userId'], data['authToken']

    def create_user(self, email, fullname, password):
        """
        Создание пользователя в чате
        :param email: E-mail
        :param fullname: Фамилия и Имя
        :param password: пароль
        :return: id в чате
        """
        username = translit.translify("_".join(fullname.split(' ')))
        result = re.findall(r'@\w+.\w+', email)
        username = username + '_' + email.replace(result[0], '')

        data = {
            'email': email,
            'name': fullname,
            'username': username,
            'password': password,
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/users.create',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Could not create user: %s' % resp.text, exc_info=True)
            return False
        logger.info('create_user.resp - %s' % resp, exc_info=True)
        data = resp.json()['user']
        return data['_id']

    def logout(self, userId):
        """
        Выход из системы чата
        :param userId: id пользователя в чате
        :return: status
        """
        headers = self.get_headers(userId)
        if headers['X-Auth-Token'] is False:
            return True

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/logout',
                             headers=headers)

        if resp.status_code != 200:
            logger.error('Fail logout', exc_info=True)
            return False
        logger.info('logout.resp - %s' % resp, exc_info=True)
        return resp

    def create_token(self, userId):
        """
        Генерация нового токена для пользователя
        :param userId: id пользователя в чате
        :return: authToken
        """
        data = {
            'userId': userId
        }

        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/users.createToken',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail create_token: %s' % resp.text, exc_info=True)
            return False
        logger.info('create_token.resp - %s' % resp, exc_info=True)

        data = resp.json()['data']
        return data['authToken']

    def update_user(self, userId, **kwargs):
        """
        Обновление данных пользователя в чате
        :param userId: id пользователя в чате
        :param kwargs: {"name": "...", "email": "..."}
        :return: status (True/False)
        """
        data = {
            'userId': userId,
            'data': kwargs
        }
        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/users.update',
                             headers=self.headers,
                             json=data)

        if resp.status_code != 200:
            logger.error('Fail update_user: %s' % resp.text, exc_info=True)
            return False
        logger.info('update_user.resp - %s' % resp, exc_info=True)

        data = resp.json()
        return data['success']

    def about_me(self, userId):
        """
        Информация о текущем пользователе
        :param userId: id пользователя в чате
        :return: json
        """
        headers = self.get_headers(userId)

        resp = requests.get(settings.ROCKETCHAT_URL + '/api/v1/me',
                            headers=headers)

        if resp.status_code != 200:
            logger.error('Fail me: %s' % resp.text, exc_info=True)
            return False
        logger.info('about_me.resp - %s' % resp, exc_info=True)
        data = resp.json()
        return data

    def notifications(self, userId):
        """
        Информация о новых сообщениях
        :param userId: id пользователя в чате
        :return: alert True/False, unread кол-ва новых сообщений
        """
        headers = self.get_headers(userId)

        resp = requests.get(settings.ROCKETCHAT_URL + '/api/v1/subscriptions.get',
                            headers=headers)

        if resp.status_code != 200:
            logger.error('Fail notifications: %s' % resp.text, exc_info=True)
            return False
        logger.info('notifications.resp - %s' % resp, exc_info=True)
        data = resp.json()

        alert = False
        unread = 0
        for obj in data['update']:
            if obj['alert'] is True:
                alert = True
                unread += obj['unread']
        return {
            'alert': alert,
            'unread': unread
        }

    def is_unique_name(self, name):
        """
        Проверка на уникальность имени
        :param name: название
        :return: True/False
        """
        params = {
            'query': {
                "name": name
            }
        }

        resp_groups = requests.get(settings.ROCKETCHAT_URL + '/api/v1/groups.list',
                                   headers=self.headers,
                                   params=params)

        if resp_groups.status_code != 200:
            logger.error('Fail groups_close: %s' % resp_groups.text, exc_info=True)
            return False

        resp_channels = requests.get(settings.ROCKETCHAT_URL + '/api/v1/groups.list',
                                     headers=self.headers,
                                     params=params)

        if resp_channels.status_code != 200:
            logger.error('Fail groups_close: %s' % resp_channels.text, exc_info=True)
            return False

        data_groups = resp_groups.json()
        data_channels = resp_channels.json()

        if data_groups['total'] != 0 or data_channels['total'] != 0:
            return False
        return True
