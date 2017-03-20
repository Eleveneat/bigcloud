# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/3/20 Chen Weijian : Init

import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import file
from ..models import File, FileGroup
from ..utils import checksum
from flask_login import login_required, current_user

from .forms import UploadForm, FileGroupForm

from .. import upload, logger


@file.route('/')
@login_required
def index():
    return redirect(url_for('file.filegroup'))


@file.route('/filegroup')
@login_required
def file_filegroup():
    return render_template('file/file_filegroup.html')


@file.route('/upload')
@login_required
def file_upload():
    return render_template('file/file_upload.html')


#################
# file
#################
@file.route('/api/file', methods=['GET'])
@login_required
def get_all_files():
    '''
    【API】得到所有文件的数据。
    :return:
    '''
    files = File.query.all()
    data = []
    for i in files:
        item = {
            "id": i.id,
            "filename": i.filename,
            "url": upload.url(i.filename),
            "size": i.size,
            "md5": i.md5,
        }
        data.append(item)
    res = {"result": True, "data": data, "message": u"Get all packages successfully!"}
    return jsonify(res)


@file.route('/api/file', methods=['POST'])
@login_required
def upload_file():
    '''
    【API】处理上传文件，文件保存到本地并添加信息到数据库。
    :return:
    '''
    form = UploadForm()
    if form.validate_on_submit():
        filename = upload.save(form.upload_file.data, name=form.upload_file.data.filename)
        path = upload.path(filename)
        size = os.stat(path).st_size
        md5 = checksum(path)

        new_file = File(
            filename=filename,
            size=size,
            md5=md5,
        )
        new_file.save()
        logger.info("{0} - Upload {1} file with id {2}".format(current_user.name, filename, new_file.id))
        return jsonify({"result": True, "data": None, "message": "upload the file successfully"})
    err = form.errors
    logger.error("{0} - Fail to upload file because {1}".format(current_user.name, err))
    res = {"result": True, "data": None, "message": err}
    return jsonify(res)


@file.route('/api/file/<int:id>', methods=['DELETE'])
@login_required
def delete_file_by_id(id):
    '''
    【API】根据 id 删除文件。
    :param id: 文件 ID
    :return:
    '''
    file = File.query.get(int(id))
    if file:
        filename = file.filename
        path = upload.path(filename)
        os.remove(path)
        file.delete()
        logger.info("{0} - Delete {1} file with id {2}".format(current_user.name, filename, id))
        return jsonify({"result": True, "data": None, "message": "Delete the file successfully"})
    res_message = u"Failed! The file with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})


#################
# filegroup
#################
@file.route('/api/filegroup', methods=['GET'])
@login_required
def get_all_filegroups():
    '''
    【API】得到所有文件组的数据。
    :return:
    '''
    groups = FileGroup.query.all()
    data = []
    for i in groups:
        files = []
        for f in i.files:
            files.append({"id": f.id, "name": f.filename})
        item = {
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "files": files,
        }
        data.append(item)
    res = {"result": True, "data": data, "message": u"Get all filegroups successfully!"}
    return jsonify(res)


@file.route('/api/filegroup', methods=['POST'])
@login_required
def add_filegroup():
    '''
    【API】添加文件组。
    :return:
    '''
    form = FileGroupForm()
    if form.validate_on_submit():
        name = form.name.data
        files_id = form.files.raw_data
        files = []
        for id in files_id:
            file = File.query.get(int(id))
            if file:
                files.append(file)
        new_filegroup = FileGroup(
            name=form.name.data,
            description=form.description.data,
            files=files,
        )
        new_filegroup.save()
        logger.info("{0} - Add {1} filegroup with id {2}".format(current_user.name, name, new_filegroup.id))
        return jsonify({"result": True, "data": None, "message": "Add the filegroup successfully"})
    err = form.errors
    logger.error("{0} - Fail to add filegroup because {1}".format(current_user.name, err))
    res = {"result": True, "data": None, "message": err}
    return jsonify(res)


@file.route('/api/filegroup/<int:id>', methods=['PUT'])
@login_required
def update_filegroup_by_id(id):
    '''
    【API】根据 id 更新文件组。
    :param id: 文件组 ID
    :return:
    '''
    form = FileGroupForm()
    if form.validate_on_submit():
        group = FileGroup.query.get(int(id))
        if group:
            files_id = form.files.raw_data
            files = []
            for file_id in files_id:
                file = File.query.get(int(file_id))
                if file:
                    files.append(file)

            group.name = form.name.data
            group.description = form.description.data
            group.files = files
            group.save()
            logger.info(
                "{0} - Update {1} filegroup with id {2}".format(current_user.name, group.name, group.id))
            return jsonify({"result": True, "data": None, "message": u"Edit filegroup successfully"})
        res_message = u"Failed! The filegroup with id %s is not excisted" % id
        logger.error("{0} - {1}".format(current_user.name, res_message))
        return jsonify({"result": False, "data": None, "message": res_message})

    error = form.errors
    logger.error("{0} - Fail to update filegroup because {1}".format(current_user.name, error))
    return jsonify({"result": False, "data": None, "message": error})


@file.route('/api/filegroup/<int:id>', methods=['DELETE'])
@login_required
def delete_filegroup_by_id(id):
    '''
    【API】根据 id 删除文件组。
    :param id: 文件组 ID
    :return:
    '''
    group = FileGroup.query.get(int(id))
    if group:
        name = group.name
        group.delete()
        logger.info("{0} - Delete {1} filegroup with id {2}".format(current_user.name, name, id))
        return jsonify({"result": True, "data": None, "message": "Delete the filegroup successfully"})
    res_message = u"Failed! The filegroup with id %s is not excisted" % id
    logger.error("{0} - {1}".format(current_user.name, res_message))
    return jsonify({"result": False, "data": None, "message": res_message})
