# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/3/20 Chen Weijian : Init

import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
from . import file
from ..models import Package
from flask_login import login_required, current_user

from .forms import UploadForm, ApplicationForm, FunctionForm, AppGroupForm

from .. import upload, logger


@file.route('/')
@login_required
def index():
    return redirect(url_for('file.filegroup'))


@file.route('/filegroup')
@login_required
def filegroup():
    return render_template('file/file_filegroup.html')


@file.route('/upload')
@login_required
def upload():
    return render_template('file/file_upload.html')
