from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Filtro para formatar data no formato dd/mm/aaaa hh:mm
@app.template_filter('format_date')
def format_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Captura a data no formato datetime-local e converte para o formato do SQLite
        data_input = request.form['data']  # Exemplo: 2024-12-14T12:47
        data = datetime.strptime(data_input, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")

        cliente = request.form['cliente']
        responsavel = request.form['responsavel']
        quaza = request.form['quaza']
        passado_para = request.form['passado_para']

        conn = get_db_connection()
        conn.execute('INSERT INTO registros (data, cliente, responsavel, quaza, passado_para) VALUES (?, ?, ?, ?, ?)',
                     (data, cliente, responsavel, quaza, passado_para))
        conn.commit()
        conn.close()

    # Busca os registros ordenados pela data de forma decrescente
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM registros ORDER BY data DESC').fetchall()  # Ordenação por data decrescente
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM registros WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        # Captura a data no formato datetime-local e converte para o formato do SQLite
        data_input = request.form['data']  # Exemplo: 2024-12-14T12:47
        data = datetime.strptime(data_input, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")

        cliente = request.form['cliente']
        responsavel = request.form['responsavel']
        quaza = request.form['quaza']
        passado_para = request.form['passado_para']

        conn.execute('UPDATE registros SET data = ?, cliente = ?, responsavel = ?, quaza = ?, passado_para = ? WHERE id = ?',
                     (data, cliente, responsavel, quaza, passado_para, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', row=row)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM registros WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
