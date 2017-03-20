# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/3/20 Chen Weijian : Init

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Required
from .. import upload


class UploadForm(FlaskForm):
    upload_file = FileField(validators=[
        FileAllowed(upload, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])


class FileGroupForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    description = StringField(id='description', validators=[DataRequired(), Length(1, 50)])
    files = StringField(id='files', validators=[])
