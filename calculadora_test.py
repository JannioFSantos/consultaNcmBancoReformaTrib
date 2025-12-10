import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


DB_PATH = "calculadora.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def buscar_ncms():
    """Retorna todos os NCMs da tabela."""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT NCM_CD, NCM_DESCRICAO FROM NCM ORDER BY NCM_CD")
    dados = cur.fetchall()
    conn.close()
    return dados


def buscar_por_codigo(codigo):
    """Busca dados do NCM e regras relacionadas."""
    conn = conectar()
    cur = conn.cursor()

    # Busca o NCM
    cur.execute("""
        SELECT NCM_CD, NCM_DESCRICAO, NCM_INICIO_VIGENCIA, NCM_FIM_VIGENCIA
        FROM NCM WHERE NCM_CD = ?
    """, (codigo,))
    dados_ncm = cur.fetchone()

    if not dados_ncm:
        conn.close()
        return None, None

    # Busca regras no NCM_APLICAVEL com JOIN para informações relacionadas
    cur.execute("""
        SELECT 
            na.NCMA_ID,
            na.NCMA_NCM_CD,
            na.NCMA_CLTR_ID,
            na.NCMA_ANXO_ID,
            na.NCMA_INICIO_VIGENCIA,
            na.NCMA_FIM_VIGENCIA,
            ct.CLTR_CD,
            ct.CLTR_DESCRICAO,
            ct.CLTR_MEMORIA_CALCULO,
            a.ANXO_NUMERO,
            a.ANXO_NUMERO_ITEM,
            a.ANXO_TEXTO_ITEM
        FROM NCM_APLICAVEL na
        LEFT JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        LEFT JOIN ANEXO a ON na.NCMA_ANXO_ID = a.ANXO_ID
        WHERE na.NCMA_NCM_CD = ?
        ORDER BY na.NCMA_INICIO_VIGENCIA DESC
    """, (codigo,))
    regras = cur.fetchall()

    conn.close()
    return dados_ncm, regras


def buscar_por_descricao(texto):
    """Busca NCM por parte da descrição."""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT NCM_CD, NCM_DESCRICAO
        FROM NCM
        WHERE NCM_DESCRICAO LIKE ?
        ORDER BY NCM_CD
    """, (f"%{texto}%",))
    dados = cur.fetchall()
    conn.close()
    return dados


# -------------------------- INTERFACE TKINTER --------------------------

janela = tk.Tk()
janela.title("Consulta de NCM – Reforma Tributária")
janela.geometry("900x600")

# Frame de pesquisa
frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Label(frame, text="Pesquisar NCM:").grid(row=0, column=0)
entry_codigo = tk.Entry(frame, width=20)
entry_codigo.grid(row=0, column=1, padx=5)

def acao_buscar_codigo():
    codigo = entry_codigo.get().strip()
    if not codigo:
        messagebox.showwarning("Aviso", "Digite um NCM válido.")
        return

    ncm, regras = buscar_por_codigo(codigo)
    exibir_resultado(ncm, regras)


tk.Button(frame, text="Buscar", command=acao_buscar_codigo).grid(row=0, column=2, padx=5)


# Pesquisa por descrição
tk.Label(frame, text="Pesquisar por descrição:").grid(row=1, column=0, pady=5)
entry_desc = tk.Entry(frame, width=40)
entry_desc.grid(row=1, column=1, padx=5)

def acao_buscar_descricao():
    texto = entry_desc.get().strip()
    ncms = buscar_por_descricao(texto)
    atualizar_lista(ncms)

tk.Button(frame, text="Buscar descrição", command=acao_buscar_descricao).grid(row=1, column=2)


# Lista de NCMs
tk.Label(janela, text="Lista de NCMs").pack()

lista_ncm = ttk.Combobox(janela, width=80)
lista_ncm.pack()

def carregar_lista_todos():
    dados = buscar_ncms()
    lista_ncm["values"] = [f"{c} - {d}" for c, d in dados]

tk.Button(janela, text="Carregar todos os NCMs", command=carregar_lista_todos).pack(pady=5)


def acao_selecionar(event):
    selecionado = lista_ncm.get()
    if not selecionado:
        return
    codigo = selecionado.split(" - ")[0]
    ncm, regras = buscar_por_codigo(codigo)
    exibir_resultado(ncm, regras)

lista_ncm.bind("<<ComboboxSelected>>", acao_selecionar)


# Área de resultado
resultado = tk.Text(janela, height=20, width=110)
resultado.pack(pady=10)


def atualizar_lista(ncms):
    lista_ncm["values"] = [f"{c} - {d}" for c, d in ncms]


def exibir_resultado(ncm, regras):
    resultado.delete("1.0", tk.END)

    if not ncm:
        resultado.insert(tk.END, "NCM não encontrado.")
        return

    codigo, desc, inicio, fim = ncm

    resultado.insert(tk.END, f"📦 NCM: {codigo}\n")
    resultado.insert(tk.END, f"Descrição: {desc}\n")
    resultado.insert(tk.END, f"Início vigência: {inicio}\n")
    resultado.insert(tk.END, f"Fim vigência: {fim}\n\n")

    if not regras:
        resultado.insert(tk.END, "Nenhuma regra adicional cadastrada.\n")
        return

    resultado.insert(tk.END, "📘 REGRAS APLICÁVEIS:\n")
    resultado.insert(tk.END, "=" * 80 + "\n\n")

    for i, r in enumerate(regras, 1):
        (ncm_id, ncm_cd, cltr_id, anxo_id, inicio_vig, fim_vig, 
         cltr_cd, cltr_desc, cltr_memoria, anxo_num, anxo_item, anxo_texto) = r
        
        resultado.insert(tk.END, f"Regra {i}:\n")
        resultado.insert(tk.END, f"  • ID da regra: {ncm_id}\n")
        resultado.insert(tk.END, f"  • Vigência: {inicio_vig} até {fim_vig if fim_vig else 'atual'}\n")
        
        if cltr_cd:
            resultado.insert(tk.END, f"  • Classificação Tributária: {cltr_cd} - {cltr_desc}\n")
            resultado.insert(tk.END, f"  • Memória de cálculo: {cltr_memoria}\n")
        
        if anxo_num:
            resultado.insert(tk.END, f"  • Anexo: {anxo_num}, Item: {anxo_item}\n")
            resultado.insert(tk.END, f"  • Descrição do item: {anxo_texto}\n")
        
        resultado.insert(tk.END, "\n" + "-" * 80 + "\n\n")


janela.mainloop()
