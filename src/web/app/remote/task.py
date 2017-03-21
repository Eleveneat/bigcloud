# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/02/20 Chen Weijian : Init

import json

from .. import logger
from ..models import LittleCloud, Application, File
from ..common.singleton import Singleton
from .message import MessageType, ReceiveMessage, ResponseCode, ResponseMessage
from .. import upload


class TaskBroker(object):
    """
    message broker for message processing
    """

    @classmethod
    def dispatch(cls, request):
        message_type, message = None, None
        try:
            data = cls._get_message_data(request)
            littlecloud_id = cls._authentication(data)
            # 检查小云是否具有可接入的权限
            if not littlecloud_id:
                logger.error('Auth fail for little cloud %s' % data['token'])
                return ResponseMessage.create(result=ResponseCode.FAIL)

            message_type, message = cls._get_message(data)
            if ReceiveMessage.support_message_type(message_type):
                return eval(cls._classname(message_type) + 'Task.execute')(param=message, cloud_id=littlecloud_id)
            else:
                logger.error('Not support little cloud message %s.', message_type)
                return ResponseMessage.create(result=ResponseCode.FAIL)
        except Exception as e:
            logger.error('Fail to process message %s.', message_type)
            return ResponseMessage.create(result=ResponseCode.FAIL)

    @classmethod
    def _get_message_data(cls, request):
        return json.loads(request.data.decode())

    @classmethod
    def _authentication(cls, data):
        try:
            token = data['token']
            cloud_name = token
            little_cloud = LittleCloud.query.filter_by(name=cloud_name, is_connectible=True).first()
            if not little_cloud:
                return None
            else:
                return little_cloud.id
        except Exception as e:
            logger.error('Authentication error for little cloud')
            return None

    @classmethod
    def _get_message(cls, data):
        return data['type'], data['message']

    @classmethod
    def _classname(cls, message):
        return message.title().replace('_', '')


class BaseTask(Singleton):
    @classmethod
    def execute(cls, param, cloud_id):
        return cls.process(param, cloud_id)

    @classmethod
    def process(cls, param, cloud_id):
        pass


class ConnectTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            if not little_cloud.is_connected:
                little_cloud.is_connected = True
                little_cloud.save()
        except Exception as e:
            logger.error('ConnectTask error')
            return ResponseMessage.create(message_type=MessageType.CONNECT, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.CONNECT, result=ResponseCode.SUCCESS)


class SyncAppGroupTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, result=ResponseCode.FAIL)

            data = []
            all_groups = little_cloud.appgroups
            for group in all_groups:
                all_applications = group.applications
                all_applications_info = []
                for app in all_applications:
                    app_info = {
                        'name': app.name,
                        'version': app.version,
                        'function': app.function.name if app.function else None,
                        'os': app.os.name if app.os else None,
                        'cpu': app.cpu.name if app.cpu else None,
                        'language': app.language.name if app.language else None,
                        'install_command': app.install_command,
                        'package': {
                            'filename': app.package.filename,
                            'size': app.package.size,
                            'md5': app.package.md5,
                        } if app.package else None,
                    }
                    all_applications_info.append(app_info)
                group_info = {
                    'name': group.name,
                    'description': group.description,
                    'applications': all_applications_info,
                }
                data.append(group_info)
        except Exception as e:
            logger.error('SyncAppGroupTask error')
            return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.SYNC_APP_GROUP, message=data,
                                      result=ResponseCode.SUCCESS)


class DownloadAppTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.DOWNLOAD_APP, result=ResponseCode.FAIL)

            data = []
            apps_info = param
            for app in apps_info:
                name = app["name"]
                version = app["version"]
                application = Application.query.filter_by(name=name, version=version).first()
                if application and application.package:
                    filename = application.package.filename
                    data.append({"name": name, "version": version, "url": upload.url(filename), "filename": filename})

        except Exception as e:
            logger.error('DownloadAppTask error')
            return ResponseMessage.create(message_type=MessageType.DOWNLOAD_APP, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.DOWNLOAD_APP, message=data,
                                      result=ResponseCode.SUCCESS)


class SyncFileGroupTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.SYNC_FILE_GROUP, result=ResponseCode.FAIL)

            data = []
            all_groups = little_cloud.filegroups
            for group in all_groups:
                all_files = group.files
                all_files_info = []
                for file in all_files:
                    file_info = {
                        'filename': file.filename,
                        'size': file.size,
                        'md5': file.md5,
                    }
                    all_files_info.append(file_info)
                group_info = {
                    'name': group.name,
                    'description': group.description,
                    'files': all_files_info,
                }
                data.append(group_info)
        except Exception as e:
            logger.error('SyncFileGroupTask error')
            return ResponseMessage.create(message_type=MessageType.SYNC_FILE_GROUP, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.SYNC_FILE_GROUP, message=data,
                                      result=ResponseCode.SUCCESS)


class DownloadFileTask(BaseTask):
    @classmethod
    def process(cls, param, cloud_id):
        try:
            little_cloud = LittleCloud.query.get(int(cloud_id))
            # 检查小云是否已接入
            if not little_cloud.is_connected:
                return ResponseMessage.create(message_type=MessageType.DOWNLOAD_FILE, result=ResponseCode.FAIL)

            data = []
            files_info = param
            for file_info in files_info:
                filename = file_info["filename"]
                file = File.query.filter_by(filename=filename).first()
                if file:
                    filename = file.filename
                    data.append({"filename": filename, "url": upload.url(filename)})

        except Exception as e:
            logger.error('DownloadFileTask error')
            return ResponseMessage.create(message_type=MessageType.DOWNLOAD_FILE, result=ResponseCode.FAIL)

        return ResponseMessage.create(message_type=MessageType.DOWNLOAD_FILE, message=data,
                                      result=ResponseCode.SUCCESS)
