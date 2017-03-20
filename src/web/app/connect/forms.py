# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, IPAddress, NumberRange, Email


class LittleCloudForm(FlaskForm):
    name = StringField(id='name', validators=[DataRequired(), Length(3, 20)])
    url = StringField(id='url', validators=[DataRequired(), Length(1, 2083)])
    ip = StringField(id='ip', validators=[DataRequired(), IPAddress()])
    port = IntegerField(id='port', validators=[DataRequired(), NumberRange(0, 65535)])
    protocol = StringField(id='protocol', validators=[DataRequired(), Length(1, 20)])
    email = StringField(id='email', validators=[DataRequired(), Email()])
    phone = IntegerField(id='phone', validators=[DataRequired()])


class UpdateGroupsForm(FlaskForm):
    appgroups = StringField(id='appgroups', validators=[])
    filegroups = StringField(id='filegroups', validators=[])
