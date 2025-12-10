"""
Script de teste para verificar se a calculadora.py está funcionando corretamente.
"""

import tkinter as tk
from tkinter import messagebox
import database

def testar_conexao():
    """Testa a conexão com o banco de dados."""
    sucesso, mensagem = database.testar_conexao()
    print(f"Teste de conexão: {mensagem}")
    return sucesso

def testar_consulta_cst():
    """Testa a consulta de CST, CClasTrib e redução."""
    print("\nTestando consulta de CST, CClasTrib e redução...")
    
    # Testar com NCM conhecido
    resultados = database.buscar_cst_cclastrib_reducao_ncm("100620")
    
    if resultados:
        print(f"✓ Consulta bem-sucedida! {len(resultados)} resultados encontrados.")
        
        # Mostrar primeiro resultado
        ncm_cd, ncm_desc, sitr_cd, sitr_desc, cltr_cd, cltr_desc, pere_valor, tbto_sigla, tbto_nome = resultados[0]
        print(f"  NCM: {ncm_cd}")
        print(f"  CST: {sitr_cd} - {sitr_desc}")
        print(f"  CClasTrib: {cltr_cd} - {cltr_desc}")
        
        if pere_valor:
            print(f"  Redução: {pere_valor} para {tbto_sigla} ({tbto_nome})")
        
        return True
    else:
