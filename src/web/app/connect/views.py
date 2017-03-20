# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask import jsonify, render_template
from . import connect
from ..models import LittleCloud, AppGroup, FileGroup
from flask_login import login_required, current_user
from .forms import LittleCloudForm, UpdateGroupsForm
from .. import logger


@connect.route('/', methods=['GET', 'POST'])
@login_required
def index():
    '''
    渲染「云接入」页面。
    :return:
    '''
    return render_template('connect/connect.html')


@connect.route('/api/littlecloud', methods=['GET'])
@login_required
def get_all_littleclouds():
    '''
    【API】得到所有小云的数据。
    :return:
    '''
    littleclouds = LittleCloud.query.all()
    dic = []
    for i in littleclouds:
        appgroups = []
        for a in i.appgroups:
            appgroups.append({"id": a.id, "name": a.name})
        filegroups = []
        for f in i.filegroups:
            filegroups.append({"id": f.id, "name": f.name})
        item = {
            "id": i.id,
            "name": i.name,
            "url": i.url,
            "is_connectible": i.is_connectible,
            "is_connected": i.is_connected,
            "phone": i.phone,
            "email": i.email,
            "ip": str(i.ip),
            "port": i.port,
            "protocol": i.protocol,
            "appgroups": appgroups,
            "filegroups": filegroups,
        }
        dic.append(item)
    # logger.info("{0} - Get all littleclouds".format(current_user.name))
    res = {"result": True, "data": dic, "message": u"Get all littleclouds successfully"}
    return jsonify(res)


@connect.route('/api/littlecloud', methods=['POST'])
@login_required
def add_littlecloud():
    '''
    【API】添加小云。
    :return:
    '''
    form = LittleCloudForm()
    if form.validate_on_submit():
        cloud1 = LittleCloud.query.filter(LittleCloud.name == form.name.data).first()
        cloud2 = LittleCloud.query.filter(LittleCloud.url == form.url.data).first()

        # 防止添加同名称和同URL的小云
        if cloud1 or cloud2:
            res_massage = u"Failed! The littlecloud with same name '{0}' or url '{0}' have already excisted".format(
                form.name.data, form.url.data)
            logger.error("{0} - {1}".format(current_user.name, res_massage))
            return jsonify({"result": False, "data": None, "message": res_massage})

        new_cloud = LittleCloud(
            name=form.name.data,
            url=form.url.data,
            phone=form.phone.data,
            email=form.email.data,
            ip=form.ip.data,
            port=form.port.data,
            protocol=form.protocol.data,
        )
        new_cloud.save()
        logger.info("{0} - Add {1} littlecloud with id {2}".format(current_user.name, form.name.data, new_cloud.id))
        return jsonify({"result": True, "data": None, "message": u"Add new littlecloud successfully"})
    error = form.errors
    logger.error("{0} - Fail to add littlecloud because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


@connect.route('/api/littlecloud/<int:id>', methods=['DELETE'])
@login_required
def delete_littlecloud_by_id(id):
    '''
    【API】根据 id 删除小云。
    :param id: 小云 ID
    :return:
    '''
    cloud = LittleCloud.query.get(int(id))
    if cloud:
        name = cloud.name
        cloud.delete()
        logger.info("{0} - Delete {1} littlecloud with id {2}".format(current_user.name, name, id))
        return jsonify({"result": True, "data": None, "message": "Delete the littlecloud successfully"})
    res_message = u"Failed! The littlecloud with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})


@connect.route('/api/littlecloud/<int:id>', methods=['PUT'])
@login_required
def update_littlecloud_by_id(id):
    '''
    【API】根据 id 更新小云。
    :param id: 小云 ID
    :return:
    '''
    form = LittleCloudForm()
    if form.validate_on_submit():
        cloud = LittleCloud.query.get(int(id))
        if cloud:
            cloud.name = form.name.data
            cloud.url = form.url.data
            cloud.phone = form.phone.data
            cloud.email = form.email.data
            cloud.ip = form.ip.data
            cloud.port = form.port.data
            cloud.protocol = form.protocol.data
            cloud.save()
            logger.info("{0} - Update {1} littlecloud with id {2}".format(current_user.name, cloud.name, cloud.id))
            return jsonify({"result": True, "data": None, "message": u"Edit new littlecloud successfully"})
        res_message = u"Failed! The littlecloud with id %s is not excisted" % id
        logger.error("{0} - {1}".format(current_user.name, res_message))
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    logger.error("{0} - Fail to update littlecloud because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


@connect.route('/api/littlecloud/<int:id>', methods=['GET'])
@login_required
def get_littlecloud_by_id(id):
    '''
    【API】根据 id 获取小云。
    :param id: 小云 ID
    :return:
    '''
    cloud = LittleCloud.query.get(int(id))
    if cloud:
        data = {
            "id": cloud.id,
            "name": cloud.name,
            "url": cloud.url,
            "is_connectible": cloud.is_connectible,
            "is_connected": cloud.is_connected,
            "phone": cloud.phone,
            "email": cloud.email,
            "ip": str(cloud.ip),
            "port": cloud.port,
            "protocol": cloud.protocol,
        }
        logger.info("{0} - Get {1} littlecloud with id {2}".format(current_user.name, cloud.name, cloud.id))
        return jsonify({"result": True, "data": data, "message": u"Get the littlecloud successfully"})
    res_message = u"Failed! The littlecloud with id %s is not excisted!" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})


@connect.route('/api/littlecloud/<int:id>/toggle_access_permission', methods=['GET'])
@login_required
def toggle_access_permission_by_id(id):
    '''
    【API】根据 id 切换小云的接入权限，对应于 is_connectible 参数。
    :param id: 小云 ID
    :return:
    '''
    cloud = LittleCloud.query.get(int(id))
    if cloud:
        cloud.is_connectible = not cloud.is_connectible
        cloud.save()
        logger.info(
            "{0} - Toggle the access permission of {1} littlecloud with id {2} and the value is {3}".format(
                current_user.name, cloud.name,
                cloud.id, cloud.is_connectible))
        return jsonify({"result": True, "data": None, "message": u"Toggle the access permission successfully!"})
    res_message = u"Failed! The littlecloud with id %s is not excisted!" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})


@connect.route('/api/littlecloud/<int:id>/groups', methods=['PUT'])
@login_required
def update_groups_of_littlecloud(id):
    '''
    【API】更新小云的 AppGroup 以及 FileGroup。
    :param id: 小云 ID
    :return:
    '''
    form = UpdateGroupsForm()
    if form.validate_on_submit():
        cloud = LittleCloud.query.get(int(id))
        if cloud:
            appgroups_id = form.appgroups.raw_data
            appgroups = []
            for appgourp_id in appgroups_id:
                appgroup = AppGroup.query.get(int(appgourp_id))
                if appgroup:
                    appgroups.append(appgroup)

            filegroups_id = form.filegroups.raw_data
            print(filegroups_id)
            filegroups = []
            for filegourp_id in filegroups_id:
                filegroup = FileGroup.query.get(int(filegourp_id))
                if filegroup:
                    filegroups.append(filegroup)

            cloud.appgroups = appgroups
            cloud.filegroups = filegroups
            cloud.save()
            logger.info(
                "{0} - Update {1} littlecloud with id {2}".format(current_user.name, cloud.name, cloud.id))
            return jsonify({"result": True, "data": None,
                            "message": u"Update appgroups and filegroups of littlecloud successfully"})
        res_message = u"Failed! The littlecloud with id %s is not excisted" % id
        logger.error("{0} - {1}".format(current_user.name, res_message))
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    logger.error(
        "{0} - Fail to update appgroups and filegroups of littlecloud because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})
