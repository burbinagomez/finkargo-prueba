import uuid
from db import db
import datetime
from peewee import *

class BaseModel(Model):
    class Meta:
        database = db

class Country(BaseModel):
    name = CharField()

class Role(BaseModel):
    name = CharField()

class Company(BaseModel):
    name = CharField()

class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField() 
    email = CharField(unique=True, null=True) 
    password = CharField(null=True)
    country = ForeignKeyField(Country, backref='user', null=True)
    role = ForeignKeyField(Role, backref='user', null=True)
    company = ForeignKeyField(Company, backref='user', null=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    
class Pc(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_date = DateTimeField(default=datetime.datetime.now)
    origin = CharField()
    user_agent = CharField()
    browser = CharField()
    platform = CharField()
    version = CharField()

class Form(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref='pcs')
    created_date = DateTimeField(default=datetime.datetime.now)
    answer = FloatField()
    updated_date = DateTimeField(default=datetime.datetime.now)

def create_tables():
    with db:
        db.create_tables([Country, Role, Company, User, Pc, Form])