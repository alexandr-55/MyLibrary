from flask import Flask, session, redirect, request, render_template, flash, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, EqualTo
from myLibr_db import DB
from myLibr_login_form import LoginForm
from myLibr_reg_form import RegForm
from myLibr_user_model import UsersModel
from myLibr_book_model import BooksModel
from myLibr_zakaz_form import ZakazModel
from myLibr_add_book_form import AddBookForm

#import json
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB("Library.db")

class avtForm(FlaskForm):
    avtorf = StringField('avtor', validators=[DataRequired()])
    submit = SubmitField('vvvvvvv') 
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_error = ''
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        user = users.exists(form.username.data, form.password.data)
        if user[0]:
            session['userid'] = users.get(user[1])[0]
            session['username'] = users.get(user[1])[1]
            session['admin'] = users.get(user[1])[3]
            session['main_photo'] = url_for('static', filename='img/' + users.get(user[1])[4])
            print(session['username'])
            session['sort'] = 0
            return redirect('/')
        else:
            login_error = 'Неправильный логин или пароль.  *** Если ранее не входили в приложение, то нужно зарегистрироваться ***'
    return render_template('myLibr_login.html', title='Библиотека', form=form, login_error=login_error)


@app.route('/spisok_book')
def spisok_book():
    if "username" not in session:
        return redirect('/login')
    if session['admin'] == 1:      
        books = BooksModel(db.get_connection()).get_all()
        return render_template('myLibr_book.html', title='Библиотека', books=books)

@app.route('/spisok_zakaz')
def spisok_zakaz():
    if "username" not in session:
        return redirect('/login')
    if session['admin'] == 1:      
        zakaz = ZakazModel(db.get_connection()).get_all()
        new_zakaz = []
        for i in zakaz:
            bm = BooksModel(db.get_connection()).get(i[2])
            um = UsersModel(db.get_connection()).get(i[1])
            new_zakaz.append((i[0], bm[1], bm[2], bm[3], bm[4], bm[5], um[1]))
        return render_template('myLibr_zakaz.html', title='Заказы', zakaz=new_zakaz)

@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" not in session:
        return redirect('/login')
    if session['admin'] == 1:      
        #print('!!!!!!!!!!!!!!!!!!!')
        #books = BooksModel(db.get_connection()).get_all()
        #return render_template('myLibr_book.html', title='Библиотека', books=books)
        #zakaz = ZakazModel(db.get_connection()).get_all()
        #return render_template('myLibr_zakaz.html', title='Библиотека', zakaz=zakaz)
        return render_template('myLibr_zakaz.html', title='Библиотека')    
    
    else:  
        form = avtForm()
        print(form.avtorf.data) 
        #print(avtorf)
        books = BooksModel(db.get_connection()).get_all()

        #all_news = []
        #for i in news.get_all(session['userid'], session['sort']):
            #all_news.append({'pub_date': datetime.fromtimestamp(i[4]).strftime('%d.%m.%Y %H:%M'),
                         #'title': i[1], 'photo': url_for('static', filename='img/' + i[2]), 'nid': i[0]})
        #return render_template('myLibr_index.html', title='Библиотека', news=all_news)
        return render_template('myLibr_book_us.html', title='Библиотека', books=books)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        users.insert(form.username.data, form.password.data)
        flash('Спасибо за регистрацию', 'success')
        return redirect('/login')
    return render_template('myLibr_reg.html', title='Библиотека', form=form)


@app.route('/sort/<sort>')
def change_sort(sort):
    if "username" not in session:
        return redirect('/login')
    session['sort'] = sort
    return redirect('/')



@app.route('/logout')
def diaries_logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('admin', None)
    return redirect('/')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session:
        return redirect('/login')
    form = AddBookForm()
    if form.validate_on_submit():
        avtor = form.avtor.data
        name_book = form.name_book.data
        kol = form.kol.data
        stellag = form.stellag.data
        polka = form.polka.data
        bm = BooksModel(db.get_connection())
        bm.insert(avtor, name_book, kol, stellag, polka)
        return redirect("/spisok_book")
    return render_template('myLibr_add_book.html', title='Добавление книги', form=form, username=session['username'])

@app.route('/delete_book/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    #print(book_id)
    if 'username' not in session:
        return redirect('/login')
    bm = BooksModel(db.get_connection())
    bm.delete(book_id)
    return redirect("/spisok_book")

@app.route('/edit_book/<int:book_id>', methods=['GET'])
def edit_book(book_id):
    print(book_id)
    print('22')
    if 'username' not in session:
        return redirect('/login')
    bm = BooksModel(db.get_connection())
    #bm.delete(book_id)
    return redirect("/")

@app.route('/add_zakaz/<int:book_id>', methods=['GET', 'POST'])
def add_zakaz(book_id):
    if request.method == 'GET':
        print(999)
        #return render_template('div_mod.html', title="Деление")
    elif request.method == 'POST':
        print(000)   
    
    if 'username' not in session:
        return redirect('/login')
    bm = BooksModel(db.get_connection())
    zm = ZakazModel(db.get_connection())
    userid =  session['userid']
    zm.insert(userid, book_id)
    return redirect("/")


@app.route('/delete_zakaz/<int:zakaz_id>', methods=['GET'])
def delete_zakaz(zakaz_id):
    #print(book_id)
    if 'username' not in session:
        return redirect('/login')
    zm = ZakazModel(db.get_connection())
    zm.delete(zakaz_id)
    return redirect("/spisok_zakaz")

@app.route('/del_all_zakaz', methods=['GET'])
def del_all_zakaz():
    #print(book_id)
    if 'username' not in session:
        return redirect('/login')
    zm = ZakazModel(db.get_connection()).del_all()
    #for i in zm:
        #zm.delete(i[0]) 
    return redirect("/spisok_zakaz")


@app.route('/my_find/<string:avtorf>')
def my_find(avtorf):
    print(avtorf)
    return redirect("/")
    

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
