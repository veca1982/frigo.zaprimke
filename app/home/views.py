# app/home/views.py
# -*- coding: utf-8 -*-


# update imports
from flask import abort, render_template, flash, redirect, url_for, request, jsonify, send_from_directory, make_response
from flask_login import current_user, login_required
from ..models import Zaprimka, Koperant, status, status_back, Cijena1x, Cijena1, Cijena2, Cijena3, Cijena4, Cijena5
from .forms import ZaprimkaForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_
from ..web.models import make_paginator, Paginator
import numpy as np
import pdfkit

import os
import subprocess
import sys

from .. import db

from . import home
import datetime

#path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


def __check_user_has_role():
    if not current_user.is_admin and not current_user.role_id:
        abort(403)



@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    __check_user_has_role()
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/zaprimke')
@login_required
def zaprimke():
    """
    Render the dashboard template on the /dashboard route
    """
    num_items_per_page = 10
    __check_user_has_role()
    num_of_items = Zaprimka.query.count()
    #pages = make_paginator(range(1, int(np.ceil(num_of_items/10.00))+1), active_page=1)
    paginator = Paginator(num_items=num_of_items, num_items_per_page=num_items_per_page, max_pages_per_block=5)
    pages = paginator.make_paginator(active_page=1)
    #zaprimkas = Zaprimka.query.limit(10).all()
    zaprimkas = Zaprimka.query.order_by(Zaprimka.id.desc()).paginate(1, num_items_per_page, error_out=False).items

    return render_template('home/zaprimke.html',
                           zaprimkas=zaprimkas, status_back=status_back, pages=pages,
                           title="Zaprimke").encode( "utf-8" )

@home.route('/zaprimke_page/<int:page>')
@login_required
def zaprimke_pager(page):
    """
    Render the dashboard template on the /dashboard route
    """
    num_items_per_page = 10
    __check_user_has_role()
    num_of_items = Zaprimka.query.count()
    #pages = make_paginator(range(1, int(np.ceil(num_of_items/10.00))+1), active_page=page)
    paginator = Paginator(num_items=num_of_items, num_items_per_page=num_items_per_page, max_pages_per_block=5)
    pages = paginator.make_paginator(active_page=page)
    #zaprimkas = Zaprimka.query.limit(10).all()
    zaprimkas = Zaprimka.query.order_by(Zaprimka.id.desc()).paginate(page, num_items_per_page, error_out=False).items

    return render_template('home/zaprimke.html',
                           zaprimkas=zaprimkas, status_back=status_back, pages=pages,
                           title="Zaprimke").encode( "utf-8" )


@home.route('/home/add_zaprimka', methods=['GET', 'POST'])
@login_required
def add_zaprimka():
    """
    Add a department to the database
    """
    __check_user_has_role()
    add_zaprimka = True

    form = ZaprimkaForm()
    form.koperant.choices = [(row.id, row.prezime+', '+row.ime+(', '+row.sifra_koperanta if row.sifra_koperanta else '')) for row in Koperant.query.order_by(Koperant.prezime.asc()).all()]
    if form.validate_on_submit():
        #form.koperant.data je id selectiranog Koperanta
        zaprimka = Zaprimka(form.brutto_masa.data, form.vl_gajbi.data, form.kop_gajbi.data,
                            form.regija.data, __get_koperant(form.koperant.data), form.napomena.data)
        zaprimka.calculate_netto_1()
        zaprimka.status = status['Zaprimljeno']
        zaprimka.datum_zaprimanja = datetime.datetime.now()
        try:
            db.session.add(zaprimka)
            db.session.commit()
            flash('Uspjesno zaprimljeno.')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(str(e))

        # redirect to departments page
        return redirect(url_for('home.zaprimke'))

    # load department template
    return render_template('home/zaprimka.html', action="Add",
                           add_zaprimka=add_zaprimka, form=form,
                           title="Dodaj Zaprimku").encode( "utf-8" )


@home.route('/home/edit_zaprimka/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_zaprimka(id):
    __check_user_has_role()

    add_zaprimka = False
    zaprimka = Zaprimka.query.get_or_404(id)
    form = ZaprimkaForm(obj=zaprimka)
    form.koperant.choices = [(row.id, row.prezime + ', ' + row.ime+(', '+row.sifra_koperanta if row.sifra_koperanta else '')) for row in Koperant.query.order_by(Koperant.prezime.asc()).all()]

    if request.method == 'GET':
        #prikayi onog koji jest u bazi
        form.koperant.data = zaprimka.id_koperanta
    else:
        if form.validate_on_submit():
            validation_message = __validate_mase(form)
            if validation_message:
                flash(validation_message)
            else:
                zaprimka = __populate_zaprimka(zaprimka, form)
                __calculate_cijene(zaprimka)
                try:
                    db.session.commit()
                    flash('Uspjesno azurirano.')
                except SQLAlchemyError as e:
                    db.session.rollback()
                    flash(str(e))
            return redirect(url_for('home.zaprimke'))

    # load department template
    return render_template('home/zaprimka.html', action="Edit",
                           add_zaprimka=add_zaprimka, form=form,
                           zaprimka=zaprimka,
                           title="Uredi Zaprimku").encode( "utf-8" )


@home.route('/home/delete_zaprimka/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_zaprimka(id):
    """
    Delete a department from the database
    """
    __check_user_has_role()

    zaprimka = Zaprimka.query.get_or_404(id)
    db.session.delete(zaprimka)
    db.session.commit()
    flash('Izbrisali ste zaprimku.')

    # redirect to the departments page
    return redirect(url_for('home.zaprimke'))


# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


@home.route('/rest/zaprimkas/', methods = ['GET'])
@login_required
def return_all_zaprimkas():
    __check_user_has_role()

    zaprimkas = []
    upit = request.args.get('upit')
    if upit.isdigit():
        zaprimkas = Zaprimka.query.filter(Zaprimka.id == int(upit)).all()
    if not zaprimkas:
        koperants = Koperant.query.filter(Koperant.ime.like(upit+"%")).all()
        if koperants:
            for koperant in koperants:
                zaprimkas.extend(Zaprimka.query.filter(Zaprimka.id_koperanta == koperant.id).all())
    if not zaprimkas:
        koperants = Koperant.query.filter(Koperant.prezime.like(upit + "%")).all()
        if koperants:
            for koperant in koperants:
                zaprimkas.extend(Zaprimka.query.filter(Zaprimka.id_koperanta == koperant.id).all())

    return jsonify(results=[zaprimka.serialize() for zaprimka in zaprimkas])


@home.route('/hello/', defaults={'id': '13'})
@home.route('/hello/<id>/')
@login_required
def hello_html(id):
    __check_user_has_role()

    os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable)  
    WKHTMLTOPDF_CMD = subprocess.Popen(
        ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], # Note we default to 'wkhtmltopdf' as the binary name
        stdout=subprocess.PIPE).communicate()[0].strip()
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'no-outline': None
    }
    zaprimka = Zaprimka.query.get_or_404(id)
    rendered = render_template('home/hello.html', name=id, zaprimka=zaprimka)
    css = ['pdf.css', 'bootstrap.min.css']
    pdf = pdfkit.from_string(rendered, False, css = css, options=options, configuration=pdfkit_config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


@home.route("/<path:path>")
def static_web(path):
    return send_from_directory('../static/html/hello.html', path)


def __get_koperant(id):
    if id != 0:
        #get by id koperanta
        koperant = Koperant.query.get_or_404(id)
        return koperant
    return None


def __validate_mase(form):
    if form.brutto_masa.data >= form.masa_kalib_4.data + form.masa_kalib_5.data:
        return None
    else:
        return 'Brutto masa ne smije biti manja od zbroja masa kalibra 4 i 5!'
     

def __populate_zaprimka(zaprimka, form):
    zaprimka.brutto_masa = form.brutto_masa.data
    zaprimka.vl_gajbi = form.vl_gajbi.data
    zaprimka.kop_gajbi = form.kop_gajbi.data
    zaprimka.regija = form.regija.data
    zaprimka.id_koperanta = form.koperant.data
    zaprimka.koperant = __get_koperant(form.koperant.data)
    zaprimka.masa_kalib_1x = form.masa_kalib_1x.data
    zaprimka.masa_kalib_1 = form.masa_kalib_1.data
    zaprimka.masa_kalib_2 = form.masa_kalib_2.data
    zaprimka.masa_kalib_3 = form.masa_kalib_3.data
    zaprimka.masa_kalib_4 = form.masa_kalib_4.data
    zaprimka.masa_kalib_5 = form.masa_kalib_5.data
    zaprimka.masa_kalo = form.masa_kalo.data
    zaprimka.otpad_masa = form.otpad_masa.data
    zaprimka.status = status['Obrađeno']
    zaprimka.napomena = form.napomena.data
    zaprimka.datum_kalibracije = zaprimka.datum_zaprimanja + datetime.timedelta(days=5)
    return zaprimka


def __calculate_cijene(zaprimka):
    zaprimka.netto_masa_2 = float(zaprimka.netto_masa_1) - float(zaprimka.otpad_masa) - float(zaprimka.masa_kalo)
    #zaprimka.masa_kalib_1x = ( float(zaprimka.netto_masa_2) - ( float(zaprimka.masa_kalib_4) + float(zaprimka.masa_kalib_5 ) ) ) / 4
    zaprimka.masa_kalib_1 = ( float(zaprimka.netto_masa_2) - ( float(zaprimka.masa_kalib_4) + float(zaprimka.masa_kalib_5 ) + float(zaprimka.masa_kalib_1x ) ) ) / 3
    zaprimka.masa_kalib_2 = zaprimka.masa_kalib_1
    zaprimka.masa_kalib_3 = zaprimka.masa_kalib_1
    zaprimka.cijena_kn = 0
    #if not zaprimka.cijena_1x_o:
        # = Cijena1x.query.order_by(Cijena1x.tstapm.desc()).filter(Cijena1x.datum_do == None).first()
    cijena_1x = Cijena1x.query.order_by(Cijena1x.tstapm.asc()).filter(and_(Cijena1x.datum_od <= zaprimka.datum_zaprimanja, or_(Cijena1x.datum_do > zaprimka.datum_zaprimanja, Cijena1x.datum_do == None ))).first()
    zaprimka.cijena_1x_o = cijena_1x
    zaprimka.cijena_1x = cijena_1x.id
    zaprimka.cijena_kn += float(zaprimka.cijena_1x_o.cijena_kn_kg) * float(zaprimka.masa_kalib_1x)
    #if not zaprimka.cijena_1_o:
        #cijena_1 = Cijena1.query.order_by(Cijena1.tstapm.desc()).filter(Cijena1.datum_do == None).first()
    cijena_1 = Cijena1.query.order_by(Cijena1.tstapm.asc()).filter(and_(Cijena1.datum_od <= zaprimka.datum_zaprimanja, or_(Cijena1.datum_do > zaprimka.datum_zaprimanja, Cijena1.datum_do == None ))).first()
    zaprimka.cijena_1_o = cijena_1
    zaprimka.cijena_1 = cijena_1.id
    zaprimka.cijena_kn += float(zaprimka.cijena_1_o.cijena_kn_kg) * float(zaprimka.masa_kalib_1)
    #if not zaprimka.cijena_2_o:
        #cijena_2 = Cijena2.query.order_by(Cijena2.tstapm.desc()).filter(Cijena2.datum_do == None).first()
    cijena_2 = Cijena2.query.order_by(Cijena2.tstapm.asc()).filter(and_(Cijena2.datum_od <= zaprimka.datum_zaprimanja, or_(Cijena2.datum_do > zaprimka.datum_zaprimanja, Cijena2.datum_do == None ))).first()
    zaprimka.cijena_2_o = cijena_2
    zaprimka.cijena_2 = cijena_2.id
    zaprimka.cijena_kn += float(zaprimka.cijena_2_o.cijena_kn_kg) * float(zaprimka.masa_kalib_2)
    #if not zaprimka.cijena_3_o:
        #cijena_3 = Cijena3.query.order_by(Cijena3.tstapm.desc()).filter(Cijena3.datum_do == None).first()
    cijena_3 = Cijena3.query.order_by(Cijena3.tstapm.asc()).filter(and_(Cijena3.datum_od <= zaprimka.datum_zaprimanja, or_(Cijena3.datum_do > zaprimka.datum_zaprimanja, Cijena3.datum_do == None ))).first()
    zaprimka.cijena_3_o = cijena_3
    zaprimka.cijena_3 = cijena_3.id
    zaprimka.cijena_kn += float(zaprimka.cijena_3_o.cijena_kn_kg) * float(zaprimka.masa_kalib_3)
    #if not zaprimka.cijena_4_o:
        #cijena_4 = Cijena4.query.order_by(Cijena4.tstapm.desc()).filter(Cijena4.datum_do == None).first()
    cijena_4 = Cijena4.query.order_by(Cijena4.tstapm.asc()).filter(and_(Cijena4.datum_od <= zaprimka.datum_zaprimanja, or_(Cijena4.datum_do > zaprimka.datum_zaprimanja, Cijena4.datum_do == None ))).first()
    zaprimka.cijena_4_o = cijena_4
    zaprimka.cijena_4 = cijena_4.id
    zaprimka.cijena_kn += float(zaprimka.cijena_4_o.cijena_kn_kg) * float(zaprimka.masa_kalib_4)
    #if not zaprimka.cijena_5_o:
        #cijena_5 = Cijena5.query.order_by(Cijena5.tstapm.desc()).filter(Cijena5.datum_do == None).first()
    cijena_5 = Cijena5.query.order_by(Cijena5.tstapm.asc()).filter(and_(Cijena5.datum_od <= zaprimka.datum_zaprimanja, or_(Cijena5.datum_do > zaprimka.datum_zaprimanja, Cijena5.datum_do == None ))).first()
    zaprimka.cijena_5_o = cijena_5
    zaprimka.cijena_5 = cijena_5.id
    zaprimka.cijena_kn += float(zaprimka.cijena_5_o.cijena_kn_kg) * float(zaprimka.masa_kalib_5)


