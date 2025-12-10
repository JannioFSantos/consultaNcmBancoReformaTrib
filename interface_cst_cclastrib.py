"""
Interface gráfica para consulta de CST, CClasTrib e Redução por NCM.
Interface simplificada e focada apenas nos dados solicitados.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database

# Configurações de estilo
COR_PRIMARIA = "#2c3e50"
COR_SECUNDARIA = "#3498db"
COR_FUNDO = "#f0f2f5"
COR_CARD = "#ffffff"
COR_TEXTO = "#2c3e50"
COR_DESTAQUE = "#e74c3c"

FONTE_TITULO = ("Segoe UI", 14, "bold")
FONTE_SUBTITULO = ("Segoe UI", 11, "bold")
FONTE_NORMAL = ("Segoe UI", 10)
FONTE_MONO = ("Consolas", 9)


class InterfaceCSTCClasTrib:
    """Interface gráfica para consulta de CST, CClasTrib e Redução."""
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📊 Consulta CST, CClasTrib e Redução por NCM desenvolvido por JannioFSantos")
        self.janela.geometry("900x700")
        self.janela.configure(bg=COR_FUNDO)
        
        # Configurar tema
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Widgets principais
        self.resultado_texto = None
        self.entry_ncm = None
        
        self.criar_widgets()
    
    def criar_widgets(self):
        """Cria todos os widgets da interface."""
        # Frame principal
        main_frame = tk.Frame(self.janela, bg=COR_FUNDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(titulo_frame, text="📊 CONSULTA CST, CClasTrib E REDUÇÃO", 
                 font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_PRIMARIA).pack()
        
        tk.Label(titulo_frame, text="Digite um código NCM para consultar CST, Classificação Tributária e Reduções", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack()
        
        # Card de pesquisa
        card_pesquisa = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_pesquisa.pack(fill=tk.X, pady=(0, 15))
        
        frame_pesquisa = tk.Frame(card_pesquisa, bg=COR_CARD)
        frame_pesquisa.pack(padx=20, pady=15, fill=tk.X)
        
        tk.Label(frame_pesquisa, text="🔍 Código NCM:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 5))
        
        entrada_frame = tk.Frame(frame_pesquisa, bg=COR_CARD)
        entrada_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.entry_ncm = tk.Entry(entrada_frame, width=30, font=FONTE_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_ncm.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_ncm.bind('<Return>', lambda event: self.consultar_ncm())
        
        self.btn_consultar = tk.Button(entrada_frame, text="Consultar", command=self.consultar_ncm,
                                       bg=COR_SECUNDARIA, fg="white", font=FONTE_SUBTITULO,
                                       relief=tk.FLAT, padx=20, cursor="hand2")
        self.btn_consultar.pack(side=tk.LEFT)
        
        # Exemplos de NCMs
        exemplos_frame = tk.Frame(frame_pesquisa, bg=COR_CARD)
        exemplos_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(exemplos_frame, text="Exemplos: ", 
                 font=FONTE_NORMAL, bg=COR_CARD, fg=COR_TEXTO).pack(side=tk.LEFT)
        
        exemplos = ["100620", "04011010", "30049099", "220710", "851712"]
        for exemplo in exemplos:
            btn_exemplo = tk.Button(exemplos_frame, text=exemplo, 
                                    command=lambda e=exemplo: self.preencher_e_consultar(e),
                                    bg="#ecf0f1", fg=COR_PRIMARIA, font=("Segoe UI", 9),
                                    relief=tk.FLAT, padx=8, cursor="hand2")
            btn_exemplo.pack(side=tk.LEFT, padx=2)
        
        # Card de resultados
        card_resultado = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_resultado.pack(fill=tk.BOTH, expand=True)
        
        frame_resultado = tk.Frame(card_resultado, bg=COR_CARD)
        frame_resultado.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_resultado, text="📄 Resultados:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de resultado com scrollbar
        resultado_frame = tk.Frame(frame_resultado, bg=COR_CARD)
        resultado_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto com scroll
        self.resultado_texto = tk.Text(resultado_frame, height=20, width=80, font=FONTE_MONO,
                                       yscrollcommand=scrollbar.set, bg="#f8f9fa", fg=COR_TEXTO,
                                       relief=tk.SOLID, bd=1, wrap=tk.WORD)
        self.resultado_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.resultado_texto.yview)
        
        # Configurar tags para formatação do texto
        self.resultado_texto.tag_configure("titulo", font=("Segoe UI", 11, "bold"), foreground=COR_PRIMARIA)
        self.resultado_texto.tag_configure("subtitulo", font=("Segoe UI", 10, "bold"), foreground=COR_SECUNDARIA)
        self.resultado_texto.tag_configure("destaque", font=("Segoe UI", 10, "bold"), foreground=COR_DESTAQUE)
        self.resultado_texto.tag_configure("normal", font=FONTE_MONO, foreground=COR_TEXTO)
        self.resultado_texto.tag_configure("info", font=FONTE_MONO, foreground="#7f8c8d")
        
        # Status bar
        status_bar = tk.Frame(main_frame, bg=COR_PRIMARIA, height=25)
        status_bar.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(status_bar, text="Pronto para consultar", 
                                     bg=COR_PRIMARIA, fg="white", font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def preencher_e_consultar(self, ncm):
        """Preenche o campo NCM e executa a consulta."""
        self.entry_ncm.delete(0, tk.END)
        self.entry_ncm.insert(0, ncm)
        self.consultar_ncm()
    
    def formatar_reducao(self, valor):
        """Formata o valor da redução para exibição."""
        if valor is None:
            return "Sem redução"
        
        try:
            # Converter para float se for string
            if isinstance(valor, str):
                # Verificar se é uma data (YYYY-MM-DD)
                if len(valor) == 10 and valor[4] == '-' and valor[7] == '-':
                    return f"Data inválida: {valor}"
                valor_float = float(valor)
            else:
                valor_float = float(valor)
            
            # Valores como 10000.00% provavelmente são fatores de multiplicação
            if valor_float >= 10000:
                return "Isenção total (100%)"
            elif valor_float >= 100:
                # Redução maior que 100% - pode ser erro ou fator especial
                return f"{valor_float:.2f}% (fator especial)"
            else:
                return f"{valor_float:.2f}%"
        except (ValueError, TypeError):
            # Se não puder converter, retornar como string
            return str(valor)
    
    def consultar_ncm(self):
        """Consulta o NCM e exibe os resultados."""
        codigo = self.entry_ncm.get().strip()
        
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um código NCM válido.")
            return
        
        self.status_label.config(text=f"Consultando NCM: {codigo}...")
        self.janela.update()
        
        # Limpar área de resultados
        self.resultado_texto.delete("1.0", tk.END)
        
        # Buscar os dados
        resultados = database.buscar_cst_cclastrib_reducao_ncm(codigo)
        
        if not resultados:
            self.resultado_texto.insert(tk.END, f"🔍 CONSULTA: NCM {codigo}\n", "titulo")
            self.resultado_texto.insert(tk.END, "=" * 70 + "\n\n")
            self.resultado_texto.insert(tk.END, "❌ NENHUM RESULTADO ENCONTRADO\n\n", "destaque")
            self.resultado_texto.insert(tk.END, "Possíveis causas:\n", "subtitulo")
            self.resultado_texto.insert(tk.END, "1. O código NCM pode estar incorreto\n")
            self.resultado_texto.insert(tk.END, "2. O NCM pode não ter regras tributárias cadastradas\n")
            self.resultado_texto.insert(tk.END, "3. Verifique a formatação (ex: 30049099 em vez de 3004.90.99)\n")
            self.status_label.config(text=f"Nenhum resultado para NCM: {codigo}")
            return
        
        # Agrupar resultados por classificação tributária
        resultados_agrupados = {}
        for resultado in resultados:
            ncm_cd, ncm_desc, sitr_cd, sitr_desc, cltr_cd, cltr_desc, pere_valor, tbto_sigla, tbto_nome = resultado
            
            # Chave única para agrupamento: NCM + CST + CClasTrib
            chave = (ncm_cd, sitr_cd, cltr_cd)
            
            if chave not in resultados_agrupados:
                resultados_agrupados[chave] = {
                    'ncm_descricao': ncm_desc,
                    'sitr_descricao': sitr_desc,
                    'cltr_descricao': cltr_desc,
                    'reducoes': []
                }
            
            # Adicionar redução se existir
            if pere_valor is not None:
                reducao_formatada = self.formatar_reducao(pere_valor)
                tributo_info = f"{tbto_sigla} ({tbto_nome})" if tbto_sigla else "Tributo não especificado"
                resultados_agrupados[chave]['reducoes'].append({
                    'valor': pere_valor,
                    'formatado': reducao_formatada,
                    'tributo': tributo_info
                })
        
        # Exibir resultados
        self.resultado_texto.insert(tk.END, f"✅ CONSULTA: NCM {codigo}\n", "titulo")
        self.resultado_texto.insert(tk.END, "=" * 70 + "\n\n")
        
        if len(resultados_agrupados) == 1:
            self.resultado_texto.insert(tk.END, f"📋 1 COMBINAÇÃO ENCONTRADA\n\n", "subtitulo")
        else:
            self.resultado_texto.insert(tk.END, f"📋 {len(resultados_agrupados)} COMBINAÇÕES ENCONTRADAS\n\n", "subtitulo")
        
        for i, (chave, dados) in enumerate(resultados_agrupados.items(), 1):
            ncm_cd, sitr_cd, cltr_cd = chave
            
            self.resultado_texto.insert(tk.END, f"\n{i}. ", "subtitulo")
            self.resultado_texto.insert(tk.END, f"NCM: {ncm_cd}\n", "normal")
            
            # Descrição do NCM (limitada)
            desc_ncm = dados['ncm_descricao']
            if len(desc_ncm) > 100:
                desc_ncm = desc_ncm[:100] + "..."
            self.resultado_texto.insert(tk.END, f"   Descrição: {desc_ncm}\n", "info")
            
            # CST
            self.resultado_texto.insert(tk.END, f"   CST: ", "normal")
            self.resultado_texto.insert(tk.END, f"{sitr_cd} - {dados['sitr_descricao']}\n", "destaque")
            
            # CClasTrib
            self.resultado_texto.insert(tk.END, f"   CClasTrib: ", "normal")
            self.resultado_texto.insert(tk.END, f"{cltr_cd} - {dados['cltr_descricao']}\n", "destaque")
            
            # Reduções
            if dados['reducoes']:
                self.resultado_texto.insert(tk.END, f"   Reduções aplicáveis:\n", "normal")
                for reducao in dados['reducoes']:
                    self.resultado_texto.insert(tk.END, f"     • {reducao['tributo']}: ", "normal")
                    self.resultado_texto.insert(tk.END, f"{reducao['formatado']}\n", "destaque")
            else:
                self.resultado_texto.insert(tk.END, f"   Redução: Sem redução cadastrada\n", "info")
            
            self.resultado_texto.insert(tk.END, "-" * 70 + "\n", "info")
        
        # Resumo final
        self.resultado_texto.insert(tk.END, f"\n📊 RESUMO:\n", "subtitulo")
        self.resultado_texto.insert(tk.END, f"• Total de combinações: {len(resultados_agrupados)}\n", "normal")
        
        # Contar reduções totais
        total_reducoes = sum(len(dados['reducoes']) for dados in resultados_agrupados.values())
        self.resultado_texto.insert(tk.END, f"• Total de reduções: {total_reducoes}\n", "normal")
        
        # Contar reduções com 100%
        reducoes_100 = 0
        for dados in resultados_agrupados.values():
            for reducao in dados['reducoes']:
                try:
                    valor = float(reducao['valor'])
                    if valor >= 100:
                        reducoes_100 += 1
                except:
                    pass
        
        if reducoes_100 > 0:
            self.resultado_texto.insert(tk.END, f"• Reduções de 100% (isenção): {reducoes_100}\n", "normal")
        
        self.status_label.config(text=f"Consulta concluída para NCM: {codigo}")

def main():
    """Função principal para iniciar a interface gráfica."""
    janela = tk.Tk()
    app = InterfaceCSTCClasTrib(janela)
    janela.mainloop()

if __name__ == "__main__":
    main()
