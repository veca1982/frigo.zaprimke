# app/models.py
# -*- coding: utf-8 -*-


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Sequence, BLOB, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime
from sqlalchemy.dialects.postgresql import BYTEA

from app import db, login_manager

#schema = 'frigo'


status = {'Zaprimljeno': 0, 'Obrađeno': 1}
status_back = {0: 'Zaprimljeno', 1: 'Obrađeno'}


class Koperant(db.Model):
    __tablename__ = 'koperanti'
    #__table_args__ = {'schema': schema}
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    #id = db.Column(Integer, Sequence('koperanti_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('koperanti_seq'), primary_key=True)
    ime = db.Column(String, nullable=False)
    prezime = db.Column(String, nullable=False)
    global_gap = db.Column(Boolean, nullable=False)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now())
    zaprimke = db.relationship('Zaprimka', back_populates='koperant', lazy='dynamic')

    def __init__(self, ime, prezime, global_gap):
        self.ime = ime
        self.prezime = prezime
        self.global_gap = global_gap

    def __repr__ (self):
        return '<id {}>'.format(self.id)


class Zaprimka(db.Model):
    __tablename__ = 'zaprimka'
    #__table_args__ = {'schema': schema}
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    #id = db.Column(Integer, Sequence('zaprimka_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('zaprimka_seq'), primary_key=True)
    #id_koperanta = db.Column(Integer, ForeignKey(schema+'.koperanti.id'), nullable=False)
    id_koperanta = db.Column(Integer, ForeignKey('koperanti.id'), nullable=False)
    koperant = db.relationship('Koperant', back_populates='zaprimke')

    brutto_masa = db.Column(Float, nullable=False)
    vl_gajbi = db.Column(Integer, nullable=False)
    kop_gajbi = db.Column(Integer, nullable=False)
    regija = db.Column(String, nullable=False)
    masa_kalib_1x = db.Column(Float)
    masa_kalib_1 = db.Column(Float)
    masa_kalib_2 = db.Column(Float)
    masa_kalib_3 = db.Column(Float)
    masa_kalib_4 = db.Column(Float)
    masa_kalib_5 = db.Column(Float)
    otpad_masa = db.Column(Float)
    netto_masa = db.Column(Float)
    barcode = db.Column(BYTEA)
    cijena_kn = db.Column(Float)
    cijena_1x = db.Column(Integer, ForeignKey('cijena_1x.id'), nullable=False)
    cijena_1x_o = relationship('Cijena1x', back_populates='zaprimke')
    cijena_1 = db.Column(Integer, ForeignKey('cijena_1.id'), nullable=False)
    cijena_1_o = relationship('Cijena1', back_populates='zaprimke')
    cijena_2 = db.Column(Integer, ForeignKey('cijena_2.id'), nullable=False)
    cijena_2_o = relationship('Cijena2', back_populates='zaprimke')
    cijena_3 = db.Column(Integer, ForeignKey('cijena_3.id'), nullable=False)
    cijena_3_o = relationship('Cijena3', back_populates='zaprimke')
    cijena_4 = db.Column(Integer, ForeignKey('cijena_4.id'), nullable=False)
    cijena_4_o = relationship('Cijena4', back_populates='zaprimke')
    cijena_5 = db.Column(Integer, ForeignKey('cijena_5.id'), nullable=False)
    cijena_5_o = relationship('Cijena5', back_populates='zaprimke')
    datum_zaprimanja = db.Column(Date)
    datum_kalibracije = db.Column(Date)
    status = db.Column(Integer, nullable=False)
    tstamp = db.Column(DateTime(timezone=True), server_default=func.now())


    def __init__(self, brutto_masa, vl_gajbi, kop_gajbi, regija, koperant):
        self.brutto_masa = brutto_masa
        self.vl_gajbi = vl_gajbi
        self.kop_gajbi = kop_gajbi
        self.regija = regija
        self.koperant = koperant
        self.id_koperanta = koperant.id

    def __repr__ (self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'ime_koperanta': self.koperant.ime,
            'prezime_koperanta': self.koperant.prezime,
        }


class Cijena1(db.Model):
    __tablename__ = 'cijena_1'
    #__table_args__ = {'schema': schema}

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    #id = db.Column(Integer, Sequence('cijena_1_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('cijena_1_seq'), primary_key=True)
    cijena_kn_kg = Column(Float)
    datum_od = db.Column(Date)
    datum_do = db.Column(Date)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    zaprimke = db.relationship("Zaprimka", back_populates="cijena_1_o", lazy='dynamic')
    def __init__(self, cijena_kn_kg, tstamp):
        self.cijena_kn_kg = cijena_kn_kg
        self.tstapm = datetime.datetime.utcnow().replace(hour=(tstamp.hour + 2) % 24)

    def __repr__ (self):
        return '<id {}>'.format(self.id)


class Cijena2(db.Model):
    __tablename__ = 'cijena_2'
    #__table_args__ = {'schema': schema}

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    #id = db.Column(Integer, Sequence('cijena_2_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('cijena_2_seq'), primary_key=True)
    cijena_kn_kg = db.Column(Float)
    datum_od = db.Column(Date)
    datum_do = db.Column(Date)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    zaprimke = db.relationship("Zaprimka", back_populates="cijena_2_o", lazy='dynamic')

    def __init__(self, cijena_kn_kg, tstamp):
        self.cijena_kn_kg = cijena_kn_kg
        self.tstapm = datetime.datetime.utcnow().replace(hour=(tstamp.hour + 2) % 24)

    def __repr__ (self):
        return '<id {}>'.format(self.id)


class Cijena1x(db.Model):
    __tablename__ = 'cijena_1x'
    #__table_args__ = {'schema': schema}

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    #id = db.Column(Integer, Sequence('cijena_1x_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('cijena_1x_seq'), primary_key=True)
    cijena_kn_kg = db.Column(Float)
    datum_od = db.Column(Date)
    datum_do = db.Column(Date)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    zaprimke = db.relationship("Zaprimka", back_populates="cijena_1x_o", lazy='dynamic')

    def __init__ (self, cijena_kn_kg, tstamp):
        self.cijena_kn_kg = cijena_kn_kg
        self.tstapm = datetime.datetime.utcnow().replace(hour=(tstamp.hour + 2) % 24)

    def __repr__ (self):
        return '<id {}>'.format(self.id)


class Cijena3(db.Model):
    __tablename__ = 'cijena_3'
    #__table_args__ = {'schema': schema}

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    #id = db.Column(Integer, Sequence('cijena_3_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('cijena_3_seq'), primary_key=True)
    cijena_kn_kg = db.Column(Float)
    datum_od = db.Column(Date)
    datum_do = db.Column(Date)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    zaprimke = db.relationship("Zaprimka", back_populates="cijena_3_o", lazy='dynamic')

    def __init__(self, cijena_kn_kg, tstamp):
        self.cijena_kn_kg = cijena_kn_kg
        self.tstapm = datetime.datetime.utcnow().replace(hour=(tstamp.hour + 2) % 24)

    def __repr__ (self):
        return '<id {}>'.format(self.id)


class Cijena4(db.Model):
    __tablename__ = 'cijena_4'
    #__table_args__ = {'schema': schema}

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(Integer, Sequence('cijena_4_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('cijena_4_seq'), primary_key=True)
    cijena_kn_kg = db.Column(Float)
    datum_od = Column(Date)
    datum_do = db.Column(Date)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    zaprimke = db.relationship("Zaprimka", back_populates="cijena_4_o", lazy='dynamic')

    def __init__ (self, cijena_kn_kg, tstamp):
        self.cijena_kn_kg = cijena_kn_kg
        self.tstapm = datetime.datetime.utcnow().replace(hour=(tstamp.hour + 2) % 24)

    def __repr__ (self):
        return '<id {}>'.format(self.id)

class Cijena5(db.Model):
    __tablename__ = 'cijena_5'
    #__table_args__ = {'schema': schema}

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(Integer, Sequence('cijena_5_seq', schema=schema), primary_key=True)
    id = db.Column(Integer, Sequence('cijena_5_seq'), primary_key=True)
    cijena_kn_kg = db.Column(Float)
    datum_od = db.Column(Date)
    datum_do = db.Column(Date)
    tstapm = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    zaprimke = db.relationship("Zaprimka", back_populates="cijena_5_o", lazy='dynamic')

    def __init__(self, cijena_kn_kg, tstamp):
        self.cijena_kn_kg = cijena_kn_kg
        self.tstapm = datetime.datetime.utcnow().replace(hour=(tstamp.hour + 2) % 24)

    def __repr__ (self):
        return '<id {}>'.format(self.id)


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'
    #__table_args__ = {'schema': schema}

    #id = db.Column(db.Integer, db.Sequence('employees_seq', schema=schema), primary_key=True)
    id = db.Column(db.Integer, db.Sequence('employees_seq'), primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    #department_id = db.Column(db.Integer, db.ForeignKey(schema+'.departments.id'))
    #role_id = db.Column(db.Integer, db.ForeignKey(schema+'.roles.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'
    #__table_args__ = {'schema': schema}


    #id = db.Column(db.Integer, db.Sequence('departments_seq', schema=schema), primary_key=True)
    id = db.Column(db.Integer, db.Sequence('departments_seq'), primary_key=True)

    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    #__tablename__ = 'roles'
    __table_args__ = {'schema': schema}

    #id = db.Column(db.Integer, db.Sequence('roles_seq', schema=schema), primary_key=True)
    id = db.Column(db.Integer, db.Sequence('roles_seq'), primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


