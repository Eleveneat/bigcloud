# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

from app import app, db
from flask import redirect, url_for
from flask_login import login_required
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

# from app.models import init_db

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
@login_required
def index():
    return redirect(url_for('home.index'))


@manager.command
def deploy():
    """Run deployment tasks."""
    from app.models import init_db
    init_db()


@manager.command
def runserver():
    app.debug = True
    app.run(host='0.0.0.0', port=5354)


if __name__ == '__main__':
    manager.run()
