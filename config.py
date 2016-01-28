import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.db')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#This should be disabled form final product
SQLALCHEMY_TRACK_MODIFICATIONS = True