from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
 
class AddBookForm(FlaskForm):
    avtor = StringField('Автор', validators=[DataRequired()])
    name_book = TextAreaField('Название книги', validators=[DataRequired()])
    kol = StringField('Количество', validators=[DataRequired()])
    submit = SubmitField('Добавить')