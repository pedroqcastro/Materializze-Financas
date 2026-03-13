import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Materializze Finanças", page_icon="💸", layout="wide")

# --- FUNÇÕES DE BANCO DE DADOS ---

def carregar_dados():
    try:
        conn = sqlite3.connect('banco_producao.db')
        df = pd.read_sql_query("SELECT * FROM financeiro ORDER BY data DESC", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame(columns=['id', 'data', 'tipo', 'categoria', 'descricao', 'valor'])

def salvar_registro(data, tipo, categoria, desc, valor):
    conn = sqlite3.connect('banco_producao.db')
    c = conn.cursor()
    c.execute("INSERT INTO financeiro (data, tipo, categoria, descricao, valor) VALUES (?,?,?,?,?)",
              (data, tipo, categoria, desc, valor))
    conn.commit()
    conn.close()

# --- INTERFACE PRINCIPAL ---
st.title("💸 Sistema de Gestão Financeira: Materializze Studio")

with st.expander("➕ Registrar Novo Lançamento", expanded=True):
    with st.form("form_registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            dt = st.date_input("Data", date.today())
            tp = st.selectbox("Tipo", ["Entrada", "Saída"])
        with col2:
            vl = st.number_input("Valor (R$)", min_value=0.0, step=0.50)
            cat = st.selectbox("Categoria", ["Venda Peça Personalizada", "Venda Peça Genérica", "Filamento", "Resina", "Manutenção", "Energia", "Outros"])
        
        ds = st.text_input("Descrição do item (Ex: Action Figure Batman)")
        enviado = st.form_submit_button("Salvar no Banco de Dados")

        if enviado:
            salvar_registro(dt.strftime('%Y-%m-%d'), tp, cat, ds, vl)
            st.success("✅ Registrado com sucesso!")
            st.rerun()

st.divider()

# --- DASHBOARD (BI) ---
st.header("📊 Painel de Indicadores (BI)")

df_atual = carregar_dados()

if not df_atual.empty:
    # --- MÉTRICAS DE TOPO ---
    total_entrada = df_atual[df_atual['tipo'] == 'Entrada']['valor'].sum()
    total_saida = df_atual[df_atual['tipo'] == 'Saída']['valor'].sum()
    saldo = total_entrada - total_saida

    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Total", f"R$ {total_entrada:,.2f}")
    c2.metric("Custos Totais", f"R$ {total_saida:,.2f}", delta=f"-{total_saida:,.2f}", delta_color="inverse")
    c3.metric("Lucro Líquido", f"R$ {saldo:,.2f}")

    st.markdown("---")

    # --- GRÁFICOS ---

    # --- GRÁFICOS DE ROSCA (LADO A LADO) ---
    col_rosca1, col_rosca2 = st.columns(2)

    with col_rosca1:
        st.subheader("Faturamento por Categoria")
        df_entradas = df_atual[df_atual['tipo'] == 'Entrada']
        if not df_entradas.empty:
            fig_ent = px.pie(df_entradas, values='valor', names='categoria', hole=0.5,
                             color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig_ent, use_container_width=True)
        else:
            st.info("Sem dados de entrada.")

    with col_rosca2:
        st.subheader("Custos por Categoria")
        df_saidas = df_atual[df_atual['tipo'] == 'Saída']
        if not df_saidas.empty:
            fig_sai = px.pie(df_saidas, values='valor', names='categoria', hole=0.5,
                             color_discrete_sequence=px.colors.sequential.Reds_r)
            st.plotly_chart(fig_sai, use_container_width=True)
        else:
            st.info("Sem dados de saída.")

    # --- GRÁFICO DE BARRAS TEMPORAL ---
    st.markdown("---")
    st.subheader("Evolução Financeira no Tempo")
    df_agrupado = df_atual.groupby(['data', 'tipo'])['valor'].sum().reset_index()
    fig_barras = px.bar(df_agrupado, x='data', y='valor', color='tipo', 
                        barmode='group', labels={'valor': 'R$', 'data': 'Data'},
                        color_discrete_map={'Entrada': '#00CC96', 'Saída': '#EF553B'})
    st.plotly_chart(fig_barras, use_container_width=True)

    # --- NOVO: CONTADORES DE TRANSAÇÕES ---
    st.markdown("---")
    cont_ent = len(df_atual[df_atual['tipo'] == 'Entrada'])
    cont_sai = len(df_atual[df_atual['tipo'] == 'Saída'])
    
    col_inf1, col_inf2 = st.columns(2)
    col_inf1.info(f"📈 **Total de Vendas/Entradas:** {cont_ent} registros")
    col_inf2.error(f"📉 **Total de Compras/Saídas:** {cont_sai} registros")

    # --- TABELA DETALHADA ---
    st.subheader("📑 Histórico de Transações")
    st.dataframe(df_atual, use_container_width=True)
    
    # Botão de exportação opcional
    st.download_button(
        label="📥 Baixar Dados (CSV)",
        data=df_atual.to_csv(index=False).encode('utf-8'),
        file_name='dados_extensao_3d.csv',
        mime='text/csv'
    )

else:
    st.warning("O banco de dados está vazio ou não foi encontrado. Registre algo acima ou rode o gerador de dados!")

# --- ÁREA DE PERIGO (LIMPEZA DO BANCO) ---
st.markdown("---")
st.subheader("⚠️ Zona de Perigo")

with st.expander("Clique aqui para apagar todos os registros"):
    st.error("Atenção: Esta ação é irreversível e apagará todo o histórico!")
    
    # Pergunta de segurança (Checkbox)
    confirmacao = st.checkbox("Eu entendo que isso apagará todos os dados permanentemente.")
    
    if st.button("LIMPAR BANCO DE DADOS AGORA"):
        if confirmacao:
            try:
                conn = sqlite3.connect('banco_producao.db')
                c = conn.cursor()
                c.execute("DELETE FROM financeiro")
                conn.commit()
                conn.close()
                st.success("💥 Banco de dados limpo com sucesso!")
                st.rerun() # Atualiza a tela para zerar os gráficos
            except Exception as e:
                st.error(f"Erro ao limpar banco: {e}")
        else:
            st.warning("Marcou a caixa de confirmação acima antes de clicar no botão!")