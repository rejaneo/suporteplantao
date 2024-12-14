import sqlite3

def create_db():
    # Conecta ou cria o banco de dados 'data.db'
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Criação da tabela 'registros'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        cliente TEXT,
        responsavel TEXT,
        quaza TEXT,
        passado_para TEXT
    );
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados e tabela criados com sucesso!")

if __name__ == "__main__":
    create_db()
