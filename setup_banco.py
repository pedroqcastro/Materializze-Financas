import sqlite3
import os

def inicializar_sistema():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'banco_producao.db')
    
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Arquivo criado em: {caminho_banco}")

if __name__ == "__main__":
    inicializar_sistema()