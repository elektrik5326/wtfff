import sqlite3
from flask import Flask,request,render_template

is_admin = False
is_developer = False
result = ""
result_develop = ""

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS main (data integer,name text,comment text)')
    conn.commit()
    conn.close()

def add_data(word,comm,name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f'INSERT INTO main (data,name,comment) VALUES ("{word}","{name}","{comm}")')
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST', 'GET'])
def main():
    global result_develop
    global result
    global is_admin
    global is_developer


    if request.method == 'POST':
        name = request.form.get('password')
        pas = request.form.get('pass')
        button = request.form.get('sumbit')
        if button == 'admin':
            if name == '1234':
                is_admin = True
                result = 'Вы успешно вошли, теперь вам доступна админ-панель'
                result_develop = ""
            else:
                result = 'Вы не вошли, пароль: 1234'
                result_develop = ""
        elif button == 'developer':
            if pas == '2014':
                is_developer = True
                result_develop = 'Вы успешно вошли'
                result = ""
            else:
                result = ""
                result_develop = 'Вы не вошли'

    return render_template('login.html', result=result, result_develop=result_develop)

@app.route('/', methods=['POST', 'GET'])
def users():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT *, rowid FROM main')
    data = c.fetchall()

    return render_template('index.html', main=data, is_developer=is_developer)

@app.route('/adminpanel', methods=['POST', 'GET'])
def admin_panel():
    global is_admin
    if is_admin == False:
        return render_template('notadmin.html')
    elif is_admin == True:
        if request.method == 'POST':
            word = int(request.form.get('word'))
            name = request.form.get('name')
            comm = request.form.get('comm')
            try:
                x = float(name)
                return '<h1>Имя ученика не может быть цифрой</h1><br><a href="/">Обратно</a>'
            except:
                pass
            if word > 5:
                return '<h1>Оценка не может быть больше пяти </h1><br><a href="/">Обратно</a>'
            elif word < 2:
                return  '<h1>Оценка не может быть меньше двух</h1><br><a href="/">Обратно</a>'
            else:
                conn = sqlite3.connect('data.db')
                c = conn.cursor()
                c.execute(f'INSERT INTO main (data,name,comment) VALUES ("{word}","{name}","{comm}")')
                conn.commit()
                conn.close()
                return render_template('admin.html')
        elif request.method == 'GET':
            return render_template('admin.html')
        
@app.route('/developerpanel', methods=['POST','GET'])
def developer():
    if is_developer == False:
        return render_template('notadmin.html')
    else:
        btn = request.form.get('btn')
        text = request.form.get('rowid')

        if btn == "value":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute('DELETE FROM main')
            conn.commit()
            conn.close()
            result_all = 'Все очищено'
            return render_template('developer.html', result_all=result_all)
        elif btn == 'value1':
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f'DELETE FROM main WHERE rowid = {text}')
            conn.commit()
            conn.close()
            
            result_rowid = f'Успешно удалено сообщение по ID = {text}'
            return render_template('developer.html',result_rowid=result_rowid)
        return render_template('developer.html')
    
init_db()
app.run()
