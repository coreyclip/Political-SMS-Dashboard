from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, optional

class SearchForm(FlaskForm):
    author = SelectField('Campaign',
                         choices=[
                             ('Everyone', 'All Campaigns on Record'),
                             ('Trump','Donald Trump'),
                             ('Warnock', 'Raphael Warnock'),
                             ('Ron_DeSantis','Ron DeSantis'),
                             ('AOC','Alexandra Ocasio-Cortez' ),
                             ('RNC', 'Republican National Committee'),
                             ('DCCC', 'Democratic Congressional Campaign Committee'),
                             ('DNC','Democratic National Committee'),
                             ('Peoples_Convoy', 'Peoples Convoy')
                             ('Dr._Oz', 'Dr. Oz')
                         ],
                         validators=[DataRequired()])
    search = StringField(u'Keyword Search', default=None, validators=[optional()])
    submit = SubmitField('Search!')
