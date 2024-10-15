from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('passwords.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    passwords = conn.execute('SELECT * FROM passwords').fetchall()
    conn.close()
    return render_template('index.html', passwords=passwords)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO passwords (password) VALUES (?)', (password,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM passwords WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
