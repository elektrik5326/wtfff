import sqlite3
from flask import Flask,request,render_template

is_admin = False
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
    global is_admin
    if request.method == 'POST':
        name = request.form.get('password')
        if name == '1234':
            is_admin = True
    return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def users():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM main')
    data = c.fetchall()

    return render_template('index.html', main=data)

@app.route('/adminpanel', methods=['POST', 'GET'])
def admin_panel():
    global is_admin
    if is_admin == False:
        return '<h1>Вы не вошли</h1><br><a href="/">Обратно</a>'
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
init_db()
app.run()