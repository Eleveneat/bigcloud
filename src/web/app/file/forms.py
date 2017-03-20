# -*- encoding: utf-8 -*-
# Copyright 2017 Vinzor Co.,Ltd.
#
# 2017/3/20 Chen Weijian : Init

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length,Required
from .. import upload


class UploadForm(FlaskForm):
    upload_file = FileField(validators=[
        FileAllowed(upload, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])


class ApplicationForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    first_classification_id = StringField(id='first_classification_id', validators=[DataRequired(), Length(1, 10)])
    secondary_classification_id = StringField(id='secondary_classification_id',
                                              validators=[DataRequired(), Length(1, 10)])
    function_id = StringField(id='function_id', validators=[DataRequired(), Length(1, 10)])
    language_id = StringField(id='language_id', validators=[DataRequired(), Length(1, 255)])
    os_id = StringField(id='os_id', validators=[DataRequired(), Length(1, 255)])
    cpu_id = StringField(id='cpu_id', validators=[DataRequired(), Length(1, 255)])
    package_id = StringField(id='package_id', validators=[DataRequired(), Length(1, 255)])
    install_command = StringField(id='install_command', validators=[DataRequired(), Length(1, 2083)])
    version = StringField(id='version', validators=[DataRequired(), Length(1, 255)])



class FunctionForm(FlaskForm):
    id = StringField(id='id', validators=[DataRequired()])
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    secondary_classification_id = StringField(id='secondary_classification_id',
                                              validators=[DataRequired(), Length(1, 10)])



class AppGroupForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(1, 50)])
    description = StringField(id='description', validators=[DataRequired(), Length(1, 50)])
    apps = StringField(id='apps', validators=[])
