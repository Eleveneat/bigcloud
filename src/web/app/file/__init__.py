# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/3/20 Chen Weijian : Init

from flask import Blueprint

file = Blueprint('file', __name__)

from . import views
