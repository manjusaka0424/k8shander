#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import os
import sys
import click
import uuid
import subprocess
from datetime import datetime
from flask.cli import with_appcontext

from app.controller.extensions import db
from app.models.users import User
from app.models.rights import Role


@click.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
@with_appcontext
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')

    db.create_all()

    # Create Roles
    Role.init_roles()

    click.echo('Initialized database.')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory."""
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                print('Removing %s' % full_pathname)
                os.remove(full_pathname)


@click.command(name='create_superuser')
@click.option('--username', '-u', help='Please enter your username')
@click.option('--email', '-e', help="whats your email")
@click.option('--password', '-p', help='Please enter your secured password')
@with_appcontext
def create_superuser(username, email, password):
    """Only needed on first execution to create first user"""
    search_user = User.query.filter_by(username=username).first()
    if not search_user:
        search_user = User(
            email=email,
            username=username,
            fs_uniquifier=uuid.uuid4().hex,
            confirmed_at=datetime.now()
        )
        db.session.add(search_user)
        db.session.commit()

        search_user.set_password(password)
        search_user.roles.append(Role.query.filter_by(name='Administrator').first())
        db.session.commit()
