import sqlite3
import random
import os
from datetime import datetime, timedelta

def popular_banco():
    # --- FORÇAR O CAMINHO CORRETO ---
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'banco_producao.db')
    
    print(f"📡 Tentando conectar em: {caminho_banco}")
    
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Garantir que a tabela exista antes de inserir
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

    categorias_venda = ["Action Figure", "Suporte Celular", "Vaso Decorativo", "Luminária", "Peça Técnica"]
    categorias_gasto = ["Filamento PLA", "Energia Elétrica", "Resina", "Manutenção Bico", "Embalagem"]

    dados = []
    for i in range(60):
        tipo = random.choice(["Entrada", "Saída"])
        data = (datetime.now() - timedelta(days=random.randint(0, 45))).strftime('%Y-%m-%d')
        
        if tipo == "Entrada":
            cat = random.choice(["Venda Peça Genérica", "Venda Peça Personalizada"])
            desc = random.choice(categorias_venda)
            valor = round(random.uniform(50, 250), 2)
        else:
            cat = random.choice(categorias_gasto)
            desc = f"Compra de {cat}"
            valor = round(random.uniform(15, 90), 2)
            
        dados.append((data, tipo, cat, desc, valor))

    cursor.executemany("INSERT INTO financeiro (data, tipo, categoria, descricao, valor) VALUES (?,?,?,?,?)", dados)
    conn.commit()
    conn.close()
    print("🚀 SUCESSO! 60 registros inseridos no banco correto.")

if __name__ == "__main__":
    popular_banco()