# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(id='username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(id='password', validators=[DataRequired(), Length(5, 64)])
    submit = SubmitField(id='login_btn', label='登 录') # 貌似没啥用啊这东西

