# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, Length

from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role
import config



class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


class KooperantForm(FlaskForm):
    ime = StringField('Ime', validators=[DataRequired()])
    prezime = StringField('Prezime', validators=[DataRequired()])
    sifra_koperanta = StringField('Šifra kooperanta', validators=[DataRequired(), Length(min=4, max=4)])
    global_gap = BooleanField("Global gap", default=False)
    submit = SubmitField('Submit')


class CijenaForm(FlaskForm):
    caliber = SelectField('Kalibri', coerce=int, choices=config.caliber_categories,  id='caliber')
    cijena_kn_kg = DecimalField('Cijena po kg', validators=[DataRequired()], id='cijena')
    datum_od = DateField('Datum od', validators=[DataRequired()], id='datum_od')
    datum_do = DateField('Datum do', id='datum_do')
    submit = SubmitField('Submit')