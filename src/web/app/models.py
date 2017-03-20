# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import datetime
from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import EmailType, IPAddressType


##################
# auth
##################
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('用户名', db.String(50), unique=True)
    email = db.Column('邮箱', db.String(120), nullable=True)
    password_hash = db.Column('哈希加密密码', db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def insert_default_users():
        if len(User.query.all()) == 0:
            User(name=u"admin123", email=u"admin@test.com", password=u"admin123").save()


@login_manager.user_loader
def load_user(user_id):
    # user_id is a unicode string, needed to be converted it to int
    return User.query.get(int(user_id))


#################
# push
#################
class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column('文件名', db.Unicode(255), unique=True)
    size = db.Column('文件总大小', db.Integer, default=0)
    md5 = db.Column('MD5', db.String(255), default='MD5')
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Package %r>' % self.filename

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class FirstClassification(db.Model):
    __tablename__ = 'first_classifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('一级分类名', db.Unicode(255))
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<FirstClassification %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def cover_save(self):
        f = FirstClassification.query.get(self.id)
        if f:
            f.name = self.name
            f.save()
        else:
            self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class SecondaryClassification(db.Model):
    __tablename__ = 'secondary_classifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('二级分类名', db.Unicode(255))
    first_classification_id = db.Column(db.Integer, db.ForeignKey('first_classifications.id'))
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    first_classification = db.relationship('FirstClassification', backref=db.backref('SecondaryClassification'))

    def __repr__(self):
        return '<SecondaryClassification %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def cover_save(self):
        s = SecondaryClassification.query.get(self.id)
        if s:
            s.name = self.name
            s.first_classification_id = self.first_classification_id
            s.save()
        else:
            self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Function(db.Model):
    __tablename__ = 'functions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('功能名', db.Unicode(255), unique=True)
    secondary_classification_id = db.Column(db.Integer, db.ForeignKey('secondary_classifications.id'))
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    secondary_classification = db.relationship('SecondaryClassification', backref=db.backref('Function'))

    def __repr__(self):
        return '<Function %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def cover_save(self):
        f = Function.query.get(self.id)
        if f:
            f.name = self.name
            f.secondary_classification_id = self.secondary_classification_id
            f.save()
        else:
            self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def insert_default_functions():
        firstC1 = FirstClassification(id=10000, name=u"系统软件")
        firstC1.cover_save()
        firstC2 = FirstClassification(id=30000, name=u"支持软件")
        firstC2.cover_save()
        firstC3 = FirstClassification(id=60000, name=u"应用软件")
        firstC3.cover_save()

        s1 = SecondaryClassification(id=11000, first_classification_id=firstC1.id, name=u"操作系统")
        s1.cover_save()
        s2 = SecondaryClassification(id=12000, first_classification_id=firstC1.id, name=u"系统实用程序")
        s2.cover_save()
        s3 = SecondaryClassification(id=13000, first_classification_id=firstC1.id, name=u"系统扩充程序")
        s3.cover_save()
        s4 = SecondaryClassification(id=14000, first_classification_id=firstC1.id, name=u"网络系统软件")
        s4.cover_save()
        s5 = SecondaryClassification(id=19900, first_classification_id=firstC1.id, name=u"其他系统软件")
        s5.cover_save()

        s6 = SecondaryClassification(id=31000, first_classification_id=firstC2.id, name=u"软件开发工具")
        s6.cover_save()
        s7 = SecondaryClassification(id=32000, first_classification_id=firstC2.id, name=u"软件评测工具")
        s7.cover_save()
        s8 = SecondaryClassification(id=33000, first_classification_id=firstC2.id, name=u"界面工具")
        s8.cover_save()
        s9 = SecondaryClassification(id=34000, first_classification_id=firstC2.id, name=u"转换工具")
        s9.cover_save()
        s10 = SecondaryClassification(id=35000, first_classification_id=firstC2.id, name=u"软件管理工具")
        s10.cover_save()
        s11 = SecondaryClassification(id=36000, first_classification_id=firstC2.id, name=u"语言处理工具")
        s11.cover_save()
        s12 = SecondaryClassification(id=37000, first_classification_id=firstC2.id, name=u"数据库管理系统")
        s12.cover_save()
        s13 = SecondaryClassification(id=38000, first_classification_id=firstC2.id, name=u"网络支持软件")
        s13.cover_save()
        s14 = SecondaryClassification(id=39900, first_classification_id=firstC2.id, name=u"其他支持软件")
        s14.cover_save()

        s15 = SecondaryClassification(id=61000, first_classification_id=firstC3.id, name=u"科学和工程计算软件")
        s15.cover_save()
        s16 = SecondaryClassification(id=61500, first_classification_id=firstC3.id, name=u"文字处理软件")
        s16.cover_save()
        s17 = SecondaryClassification(id=62000, first_classification_id=firstC3.id, name=u"数据处理软件")
        s17.cover_save()
        s18 = SecondaryClassification(id=62500, first_classification_id=firstC3.id, name=u"图形软件")
        s18.cover_save()
        s19 = SecondaryClassification(id=63000, first_classification_id=firstC3.id, name=u"图像处理软件")
        s19.cover_save()
        s20 = SecondaryClassification(id=64000, first_classification_id=firstC3.id, name=u"应用数据库软件")
        s20.cover_save()
        s21 = SecondaryClassification(id=65000, first_classification_id=firstC3.id, name=u"事务处理软件")
        s21.cover_save()
        s22 = SecondaryClassification(id=65500, first_classification_id=firstC3.id, name=u"辅助类软件")
        s22.cover_save()
        s23 = SecondaryClassification(id=66000, first_classification_id=firstC3.id, name=u"控制类软件")
        s23.cover_save()
        s24 = SecondaryClassification(id=66500, first_classification_id=firstC3.id, name=u"智能软件")
        s24.cover_save()
        s25 = SecondaryClassification(id=67000, first_classification_id=firstC3.id, name=u"仿真软件")
        s25.cover_save()
        s26 = SecondaryClassification(id=67500, first_classification_id=firstC3.id, name=u"网络应用软件")
        s26.cover_save()
        s27 = SecondaryClassification(id=68000, first_classification_id=firstC3.id, name=u"安全与保密软件")
        s27.cover_save()
        s28 = SecondaryClassification(id=68500, first_classification_id=firstC3.id, name=u"社会公益服务软件")
        s28.cover_save()
        s29 = SecondaryClassification(id=69000, first_classification_id=firstC3.id, name=u"游戏软件")
        s29.cover_save()
        s30 = SecondaryClassification(id=69900, first_classification_id=firstC3.id, name=u"其他应用软件")
        s30.cover_save()

        Function(id=11000, secondary_classification_id=s1.id, name=u"操作系统").cover_save()
        Function(id=12000, secondary_classification_id=s2.id, name=u"系统实用软件").cover_save()
        Function(id=13000, secondary_classification_id=s3.id, name=u"系统扩充程序").cover_save()
        Function(id=14000, secondary_classification_id=s4.id, name=u"网络系统软件").cover_save()
        Function(id=19900, secondary_classification_id=s5.id, name=u"其他系统软件").cover_save()

        Function(id=31010, secondary_classification_id=s6.id, name=u"需求分析软件").cover_save()
        Function(id=31020, secondary_classification_id=s6.id, name=u"设计工具").cover_save()
        Function(id=31030, secondary_classification_id=s6.id, name=u"编码实现工具").cover_save()
        Function(id=31040, secondary_classification_id=s6.id, name=u"测试工具").cover_save()
        Function(id=31050, secondary_classification_id=s6.id, name=u"维护工具").cover_save()
        Function(id=31060, secondary_classification_id=s6.id, name=u"文档生成工具").cover_save()
        Function(id=31070, secondary_classification_id=s6.id, name=u"集成化软件开发工具").cover_save()
        Function(id=31099, secondary_classification_id=s6.id, name=u"其他软件开发工具").cover_save()
        Function(id=32000, secondary_classification_id=s7.id, name=u"软件评测工具").cover_save()
        Function(id=33000, secondary_classification_id=s8.id, name=u"界面工具").cover_save()
        Function(id=34000, secondary_classification_id=s9.id, name=u"转换工具").cover_save()
        Function(id=35010, secondary_classification_id=s10.id, name=u"项目管理工具").cover_save()
        Function(id=35020, secondary_classification_id=s10.id, name=u"配置管理工具").cover_save()
        Function(id=35030, secondary_classification_id=s10.id, name=u"质量管理工具").cover_save()
        Function(id=35099, secondary_classification_id=s10.id, name=u"其他软件管理工具").cover_save()
        Function(id=36000, secondary_classification_id=s11.id, name=u"语言处理程序").cover_save()
        Function(id=37010, secondary_classification_id=s12.id, name=u"关系型数据库管理系统").cover_save()
        Function(id=37020, secondary_classification_id=s12.id, name=u"层次型数据库管理系统").cover_save()
        Function(id=37030, secondary_classification_id=s12.id, name=u"网状型数据库管理系统").cover_save()
        Function(id=37099, secondary_classification_id=s12.id, name=u"其他数据库管理系统").cover_save()
        Function(id=38000, secondary_classification_id=s13.id, name=u"网络支持软件").cover_save()
        Function(id=39900, secondary_classification_id=s14.id, name=u"其他支持软件").cover_save()

        Function(id=61010, secondary_classification_id=s15.id, name=u"数学软件").cover_save()
        Function(id=61020, secondary_classification_id=s15.id, name=u"科学计算软件").cover_save()
        Function(id=61030, secondary_classification_id=s15.id, name=u"工程应用软件").cover_save()
        Function(id=61099, secondary_classification_id=s15.id, name=u"其他科学和工程计算软件").cover_save()
        Function(id=61510, secondary_classification_id=s16.id, name=u"编辑排版软件").cover_save()
        Function(id=61520, secondary_classification_id=s16.id, name=u"表处理软件").cover_save()
        Function(id=61530, secondary_classification_id=s16.id, name=u"汉字输入处理软件").cover_save()
        Function(id=61540, secondary_classification_id=s16.id, name=u"多文种文字处理软件").cover_save()
        Function(id=61599, secondary_classification_id=s16.id, name=u"其他文字处理软件").cover_save()
        Function(id=62010, secondary_classification_id=s17.id, name=u"数据采集软件").cover_save()
        Function(id=62020, secondary_classification_id=s17.id, name=u"统计及预测软件").cover_save()
        Function(id=62030, secondary_classification_id=s17.id, name=u"数据综合处理软件").cover_save()
        Function(id=62040, secondary_classification_id=s17.id, name=u"信息检索软件").cover_save()
        Function(id=62099, secondary_classification_id=s17.id, name=u"其他数据处理软件").cover_save()
        Function(id=62510, secondary_classification_id=s18.id, name=u"图形输入软件").cover_save()
        Function(id=62520, secondary_classification_id=s18.id, name=u"图形处理软件").cover_save()
        Function(id=62530, secondary_classification_id=s18.id, name=u"图形输出软件").cover_save()
        Function(id=62599, secondary_classification_id=s18.id, name=u"其他图形软件").cover_save()
        Function(id=63010, secondary_classification_id=s19.id, name=u"图像生成软件").cover_save()
        Function(id=63020, secondary_classification_id=s19.id, name=u"图像编辑软件").cover_save()
        Function(id=63030, secondary_classification_id=s19.id, name=u"图像识别软件").cover_save()
        Function(id=63099, secondary_classification_id=s19.id, name=u"其他图像处理软件").cover_save()
        Function(id=64000, secondary_classification_id=s20.id, name=u"应用数据库软件").cover_save()
        Function(id=65000, secondary_classification_id=s21.id, name=u"事务管理软件").cover_save()
        Function(id=65510, secondary_classification_id=s22.id, name=u"辅助设计软件").cover_save()
        Function(id=65520, secondary_classification_id=s22.id, name=u"辅助制造软件").cover_save()
        Function(id=65530, secondary_classification_id=s22.id, name=u"辅助测试软件").cover_save()
        Function(id=65540, secondary_classification_id=s22.id, name=u"辅助教育软件").cover_save()
        Function(id=65599, secondary_classification_id=s22.id, name=u"其他辅助类软件").cover_save()
        Function(id=66010, secondary_classification_id=s23.id, name=u"实时控制软件").cover_save()
        Function(id=66020, secondary_classification_id=s23.id, name=u"非实时控制软件").cover_save()
        Function(id=66510, secondary_classification_id=s24.id, name=u"专家系统").cover_save()
        Function(id=66520, secondary_classification_id=s24.id, name=u"模式识别软件").cover_save()
        Function(id=66530, secondary_classification_id=s24.id, name=u"自然语言理解与处理软件").cover_save()
        Function(id=66540, secondary_classification_id=s24.id, name=u"机器证明软件").cover_save()
        Function(id=66550, secondary_classification_id=s24.id, name=u"机器翻译软件").cover_save()
        Function(id=66599, secondary_classification_id=s24.id, name=u"其他智能软件").cover_save()
        Function(id=67010, secondary_classification_id=s25.id, name=u"模拟仿真软件").cover_save()
        Function(id=67020, secondary_classification_id=s25.id, name=u"数字仿真软件").cover_save()
        Function(id=67030, secondary_classification_id=s25.id, name=u"混合仿真软件").cover_save()
        Function(id=67099, secondary_classification_id=s25.id, name=u"其他仿真软件").cover_save()
        Function(id=67500, secondary_classification_id=s26.id, name=u"网络应用软件").cover_save()
        Function(id=68000, secondary_classification_id=s27.id, name=u"安全与保密软件").cover_save()
        Function(id=68500, secondary_classification_id=s28.id, name=u"社会公益软件").cover_save()
        Function(id=69000, secondary_classification_id=s29.id, name=u"游戏软件").cover_save()
        Function(id=69900, secondary_classification_id=s30.id, name=u"其他应用软件").cover_save()


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('语言', db.Unicode(255), unique=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Language %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def insert_default_languages():
        if len(Language.query.all()) == 0:
            Language(id=1, name=u"中文简体").save()
            Language(id=2, name=u"中文繁体").save()
            Language(id=3, name=u"美式英文").save()


class CPU(db.Model):
    __tablename__ = 'cpu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('CPU', db.Unicode(255), unique=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<CPU %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def insert_default_cpus():
        if len(CPU.query.all()) == 0:
            CPU(id=1, name=u"32BIT").save()
            CPU(id=2, name=u"64BIT").save()


class OS(db.Model):
    __tablename__ = 'os'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('操作系统', db.Unicode(255), unique=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<OS %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def insert_default_oses():
        if len(OS.query.all()) == 0:
            OS(id=1, name=u"OSX").save()
            OS(id=2, name=u"Windows").save()
            OS(id=3, name=u"Ubuntu").save()
            OS(id=4, name=u"CentOS").save()
            OS(id=5, name=u"Darwin").save()


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('应用名', db.Unicode(255), unique=True)
    version = db.Column('版本号', db.String(255), default='1.0')
    function_id = db.Column(db.Integer, db.ForeignKey('functions.id'), nullable=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=True)
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpu.id'), nullable=True)
    os_id = db.Column(db.Integer, db.ForeignKey('os.id'), nullable=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=True)
    install_command = db.Column('安装命令', db.String(255), nullable=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    function = db.relationship('Function', backref=db.backref('Application'))
    language = db.relationship('Language', backref=db.backref('Application'))
    cpu = db.relationship('CPU', backref=db.backref('Application'))
    os = db.relationship('OS', backref=db.backref('Application'))
    package = db.relationship('Package', backref=db.backref('Application'))

    def __repr__(self):
        return '<Application %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


AppGroup_Application = db.Table('appgroup_application',
                                db.Column('appgroup_id', db.Integer, db.ForeignKey('appgroups.id')),
                                db.Column('application_id', db.Integer, db.ForeignKey('applications.id'))
                                )


class AppGroup(db.Model):
    __tablename__ = 'appgroups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('应用组名', db.Unicode(255), unique=True)
    description = db.Column('描述', db.Unicode(255), unique=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    applications = db.relationship('Application', secondary=AppGroup_Application, backref=db.backref('AppGroup'))

    def __repr__(self):
        return '<AppGroup %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


#################
# file
#################
class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column('文件名', db.Unicode(255), unique=True)
    size = db.Column('文件总大小', db.Integer, default=0)
    md5 = db.Column('MD5', db.String(255), default='MD5')
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<File %r>' % self.filename

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


FileGroup_File = db.Table('filegroup_file',
                          db.Column('filegroup_id', db.Integer, db.ForeignKey('filegroups.id')),
                          db.Column('file_id', db.Integer, db.ForeignKey('files.id'))
                          )


class FileGroup(db.Model):
    __tablename__ = 'filegroups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('文件组名', db.Unicode(255), unique=True)
    description = db.Column('描述', db.Unicode(255), unique=True)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    files = db.relationship('File', secondary=FileGroup_File, backref=db.backref('FileGroup'))

    def __repr__(self):
        return '<FileGroup %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


#################
# connect
#################
class ProtocolType(object):
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'


LittleCloud_AppGroup = db.Table('littlecloud_appgroup',
                                db.Column('littlecloud_id', db.Integer, db.ForeignKey('littleclouds.id')),
                                db.Column('appgroup_id', db.Integer, db.ForeignKey('appgroups.id'))
                                )


class LittleCloud(db.Model):
    __tablename__ = 'littleclouds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('小云平台名称', db.Unicode(255), unique=True)
    url = db.Column('小云平台URL', db.String(255), unique=True)
    is_connectible = db.Column('是否允许接入', db.Boolean, default=False)
    is_connected = db.Column('是否已经接入', db.Boolean, default=False)
    phone = db.Column('联系电话', db.String(30), nullable=True)
    email = db.Column('联系邮箱', EmailType, nullable=True)
    ip = db.Column('接入IP', IPAddressType, nullable=True)
    port = db.Column('接入端口', db.Integer, nullable=True)
    protocol = db.Column('接入协议', db.String(20), default=ProtocolType.HTTP)
    created_time = db.Column('创建时间', db.DateTime, default=datetime.datetime.now)
    modified_time = db.Column('修改时间', db.DateTime, onupdate=datetime.datetime.now)

    appgroups = db.relationship('AppGroup', secondary=LittleCloud_AppGroup, backref=db.backref('LittleCloud'))

    def __repr__(self):
        return '<LittleCloud %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
