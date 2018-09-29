from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired, InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField



class ZaprimkaForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    #koperant = QuerySelectField(query_factory=lambda: Koperant.query.all(), get_label="prezime")
    koperant = SelectField('Koperant:', coerce=int, id='koperant')
    brutto_masa = DecimalField('Brutto masa kg', validators=[DataRequired()], id='brutto_masa')
    vl_gajbi = IntegerField('Vlastitih gajbi', validators=[InputRequired ()], id='vl_gajbi')
    kop_gajbi = IntegerField('Koperant gajbi', validators=[InputRequired ()] , id='kop_gajbi')
    regija = StringField('Regija', validators=[DataRequired()], id='regija')
    masa_kalib_1x = DecimalField('Masa kalibar 1x kg', id='masa_kalib_1x')
    masa_kalib_1 = DecimalField('Masa kalibar 1 kg', id='masa_kalib_1')
    masa_kalib_2 = DecimalField('Masa kalibar 2 kg', id='masa_kalib_2')
    masa_kalib_3 = DecimalField('Masa kalibar 3 kg', id='masa_kalib_3')
    masa_kalib_4 = DecimalField('Masa kalibar 4 kg', id='masa_kalib_4')
    masa_kalib_5 = DecimalField('Masa kalibar 5 kg', id='masa_kalib_5')
    masa_kalo = DecimalField('Masa kalo kg', id='masa_kalo')
    otpad_masa = DecimalField('Otpad masa kg', id='otpad_masa')
    napomena = TextField('Napomena', id='napomena')

    submit = SubmitField('Submit')