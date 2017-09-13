# app/home/business.py
# -*- coding: utf-8 -*-
from app.models import Cijena1x, Cijena1, Cijena2, Cijena3, Cijena4, Cijena5
import datetime


def get_cijena(calibar_id, cijena):
    if calibar_id == '1x':
        cijena = Cijena1x(cijena, datetime.datetime.utcnow())
    elif calibar_id == '1':
        cijena = Cijena1(cijena, datetime.datetime.utcnow())
    elif calibar_id == '2':
        cijena = Cijena2(cijena, datetime.datetime.utcnow())
    elif calibar_id == '3':
        cijena = Cijena3(cijena, datetime.datetime.utcnow())
    elif calibar_id == '4':
        cijena = Cijena4(cijena, datetime.datetime.utcnow())
    else:
        cijena = Cijena5
    return cijena

def get_last_active_cijena(calibar_id):
    if calibar_id == '1x':
        cijena = Cijena1x.query.order_by(Cijena1x.tstapm.desc()).filter(Cijena1x.datum_do == None).first()
    elif calibar_id == '1':
        cijena = Cijena1.query.order_by(Cijena1.tstapm.desc()).filter(Cijena1.datum_do == None).first()
    elif calibar_id == '2':
        cijena = Cijena2.query.order_by(Cijena2.tstapm.desc()).filter(Cijena2.datum_do == None).first()
    elif calibar_id == '3':
        cijena = Cijena3.query.order_by(Cijena3.tstapm.desc()).filter(Cijena3.datum_do == None).first()
    elif calibar_id == '4':
        cijena = Cijena4.query.order_by(Cijena4.tstapm.desc()).filter(Cijena4.datum_do == None).first()
    else:
        cijena = Cijena5.query.order_by(Cijena5.tstapm.desc()).filter(Cijena5.datum_do == None).first()
    return cijena