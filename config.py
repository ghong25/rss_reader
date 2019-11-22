import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-mystery'
    SQLALCHEMY_DATABASE_URI = "mysql://root:GeneHong1996@localhost/rss_reader"
    SQLALCHEMY_TRACK_MODIFICATIONS = False;

