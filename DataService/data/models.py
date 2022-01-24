from enum import unique
from django.db import models
from django_sorcery.db import databases
from sqlalchemy import JSON

db = databases.get('default', echo=True)

# Create your models here.
UserFormTitle = db.Table('UserFormTitle',
    # db.Column('id', db.Integer, primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('formtitleId', db.Integer, db.ForeignKey('form_title.id'), primary_key=True)
    )
# class UserFormTitle(db.Model): 
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     formtitleId = db.Column(db.Integer, db.ForeignKey('form_title.id'), primary_key=True)
    
    
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(length=128), unique=True, nullable=False)
    formtitles = db.relationship('FormTitle', secondary='UserFormTitle', backref='formtitles', overlaps="formtitles,formtitles")


class FormTitle(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    slug = db.Column(db.String(length=128), unique=True, nullable=False)
    users = db.relationship('User', secondary='UserFormTitle', backref='users', overlaps="formtitles,formtitles")


class Data(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    formtitle = db.ManyToOne(FormTitle, backref=db.backref("datas", cascade="all, delete-orphan"))
    user = db.ManyToOne(User, backref=db.backref("datas", cascade="all, delete-orphan"))

    firstname = db.Column(db.String(length=128))
    lastname = db.Column(db.String(length=128))
    age = db.Column(db.Integer())
    extra_fields = db.Column(JSON)


# class UserFormTitle(db.Model):
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     formtitle = db.ManyToOne(FormTitle, backref=db.backref("userformtitles", cascade="all, delete-orphan"))
#     user = db.ManyToOne(User, backref=db.backref("users", cascade="all, delete-orphan"))
