"""
Arquivo principal da Calculadora Tributária.
Versão atualizada com funcionalidades de CST, CClasTrib, Redução, Alíquotas e Legislação.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database

# Configurações de estilo
COR_PRIMARIA = "#2c3e50"
COR_SECUNDARIA = "#3498db"
COR_TERCIARIA = "#2ecc71"
COR_FUNDO = "#f0f2f5"
COR_CARD = "#ffffff"
COR_TEXTO = "#2c3e50"
COR_DESTAQUE = "#e74c3c"

FONTE_TITULO = ("Segoe UI", 14, "bold")
FONTE_SUBTITULO = ("Segoe UI", 11, "bold")
FONTE_NORMAL = ("Segoe UI", 10)
FONTE_MONO = ("Consolas", 9)


class CalculadoraTributariaCompleta:
    """Classe principal da Calculadora Tributária com funcionalidades completas."""
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📊 Desenvolvido por JannioFSantos - CST, CClasTrib, Redução, Alíquotas e Legislação")
        self.janela.geometry("1200x900")
        self.janela.configure(bg=COR_FUNDO)
        
        # Configurar tema
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Widgets principais
        self.resultado_texto = None
        self.entry_ncm = None
        self.entry_busca_desc = None
        self.lista_ncms = None
        self.label_info_lista = None
        self.status_label = None
        self.btn_consultar = None
        self.btn_buscar_desc = None
        self.btn_listar_todos = None
        self.modo_consulta = tk.StringVar(value="cst_cclastrib")
        
        self.criar_widgets()
    
    def criar_widgets(self):
        """Cria todos os widgets da interface."""
        # Frame principal
        main_frame = tk.Frame(self.janela, bg=COR_FUNDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título compacto
        titulo_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        titulo_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(titulo_frame, text="📊 Consulta NCM", 
                 font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_PRIMARIA).pack()
        
        # Frame para controles (20% da altura) - Área aumentada para lista de NCMs
        controles_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        controles_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Linha 1: Modo de consulta e pesquisa
        linha1_frame = tk.Frame(controles_frame, bg=COR_FUNDO)
        linha1_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Modo de consulta (compacto)
        modo_frame = tk.Frame(linha1_frame, bg=COR_FUNDO)
        modo_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(modo_frame, text="Modo:", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Radiobutton(modo_frame, text="CST/CClasTrib", variable=self.modo_consulta, 
                      value="cst_cclastrib", bg=COR_FUNDO, font=FONTE_NORMAL).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(modo_frame, text="Completo", variable=self.modo_consulta, 
                      value="completo", bg=COR_FUNDO, font=FONTE_NORMAL).pack(side=tk.LEFT)
        
        # Pesquisa (compacta)
        pesquisa_frame = tk.Frame(linha1_frame, bg=COR_FUNDO)
        pesquisa_frame.pack(side=tk.LEFT)
        
        tk.Label(pesquisa_frame, text="NCM:", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry_ncm = tk.Entry(pesquisa_frame, width=15, font=FONTE_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_ncm.pack(side=tk.LEFT, padx=(0, 5))
        self.entry_ncm.bind('<Return>', lambda event: self.consultar_ncm())
        
        self.btn_consultar = tk.Button(pesquisa_frame, text="Consultar", command=self.consultar_ncm,
                                       bg=COR_SECUNDARIA, fg="white", font=FONTE_NORMAL,
                                       relief=tk.FLAT, padx=12, cursor="hand2")
        self.btn_consultar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Exemplos compactos
        tk.Label(pesquisa_frame, text="Ex:", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack(side=tk.LEFT, padx=(0, 5))
        
        exemplos = ["100620", "04011010", "30049099"]
        for exemplo in exemplos:
            btn_exemplo = tk.Button(pesquisa_frame, text=exemplo, 
                                    command=lambda e=exemplo: self.preencher_e_consultar(e),
                                    bg="#ecf0f1", fg=COR_PRIMARIA, font=("Segoe UI", 8),
                                    relief=tk.FLAT, padx=4, cursor="hand2")
            btn_exemplo.pack(side=tk.LEFT, padx=1)
        
        # Linha 2: Navegação em NCMs (compacta)
        linha2_frame = tk.Frame(controles_frame, bg=COR_FUNDO)
        linha2_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(linha2_frame, text="Navegar NCMs:", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry_busca_desc = tk.Entry(linha2_frame, width=25, font=FONTE_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_busca_desc.pack(side=tk.LEFT, padx=(0, 5))
        self.entry_busca_desc.bind('<Return>', lambda event: self.buscar_ncms_por_descricao())
        
        self.btn_buscar_desc = tk.Button(linha2_frame, text="Buscar", command=self.buscar_ncms_por_descricao,
                                         bg=COR_TERCIARIA, fg="white", font=FONTE_NORMAL,
                                         relief=tk.FLAT, padx=12, cursor="hand2")
        self.btn_buscar_desc.pack(side=tk.LEFT, padx=(0, 5))
        
        self.btn_listar_todos = tk.Button(linha2_frame, text="Listar Todos", command=self.listar_todos_ncms,
                                          bg="#95a5a6", fg="white", font=FONTE_NORMAL,
                                          relief=tk.FLAT, padx=12, cursor="hand2")
        self.btn_listar_todos.pack(side=tk.LEFT, padx=(0, 5))
        
        # Frame para lista de NCMs (ÁREA AUMENTADA)
        lista_frame = tk.Frame(controles_frame, bg=COR_FUNDO)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Scrollbar vertical para a lista (agora vertical para mais linhas)
        scrollbar_vertical = tk.Scrollbar(lista_frame)
        scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scrollbar horizontal para a lista
        scrollbar_horizontal = tk.Scrollbar(lista_frame, orient=tk.HORIZONTAL)
        scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Listbox para mostrar NCMs (ALTURA AUMENTADA para 6 linhas)
        self.lista_ncms = tk.Listbox(lista_frame, height=6, width=100, font=FONTE_MONO,
                                     yscrollcommand=scrollbar_vertical.set,
                                     xscrollcommand=scrollbar_horizontal.set,
                                     bg="#f8f9fa", fg=COR_TEXTO,
                                     relief=tk.SOLID, bd=1, selectmode=tk.SINGLE)
        self.lista_ncms.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lista_ncms.bind('<<ListboxSelect>>', self.selecionar_ncm_lista)
        
        scrollbar_vertical.config(command=self.lista_ncms.yview)
        scrollbar_horizontal.config(command=self.lista_ncms.xview)
        
        # Frame para informações da lista
        info_frame = tk.Frame(controles_frame, bg=COR_FUNDO)
        info_frame.pack(fill=tk.X, pady=(2, 0))
        
        self.label_info_lista = tk.Label(info_frame, text="Clique em um NCM para consultar automaticamente", 
                                         font=("Segoe UI", 8), bg=COR_FUNDO, fg="#7f8c8d")
        self.label_info_lista.pack(side=tk.LEFT)
        
        # Frame para resultados (80% da altura) - Ainda mantendo foco nos resultados
        resultados_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        # Card de resultados com borda destacada
        card_resultado = tk.Frame(resultados_frame, bg=COR_CARD, relief=tk.RAISED, bd=2)
        card_resultado.pack(fill=tk.BOTH, expand=True)
        
        frame_resultado = tk.Frame(card_resultado, bg=COR_CARD)
        frame_resultado.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_resultado, text="📄 RESULTADOS:", 
                 font=("Segoe UI", 12, "bold"), bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de resultado com scrollbar (máximo espaço)
        resultado_frame = tk.Frame(frame_resultado, bg=COR_CARD)
        resultado_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto com scroll (altura máxima)
        self.resultado_texto = tk.Text(resultado_frame, height=35, width=120, font=FONTE_MONO,
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
        self.resultado_texto.tag_configure("aliquota", font=FONTE_MONO, foreground="#27ae60")
        self.resultado_texto.tag_configure("legislacao", font=FONTE_MONO, foreground="#8e44ad")
        
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
    
    def formatar_aliquota(self, valor):
        """Formata o valor da alíquota para exibição."""
        if valor is None:
            return "Não especificada"
        
        try:
            # Converter para float se for string
            if isinstance(valor, str):
                valor_float = float(valor)
            else:
                valor_float = float(valor)
            
            return f"{valor_float:.2f}%"
        except (ValueError, TypeError):
            return str(valor)
    
    def consultar_ncm(self):
        """Consulta o NCM e exibe os resultados conforme o modo selecionado."""
        codigo = self.entry_ncm.get().strip()
        
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um código NCM válido.")
            return
        
        modo = self.modo_consulta.get()
        self.status_label.config(text=f"Consultando NCM: {codigo} ({'CST/CClasTrib' if modo == 'cst_cclastrib' else 'Completo'})...")
        self.janela.update()
        
        # Limpar área de resultados
        self.resultado_texto.delete("1.0", tk.END)
        
        if modo == "cst_cclastrib":
            self.consultar_cst_cclastrib(codigo)
        else:
            self.consultar_completo(codigo)
    
    def consultar_cst_cclastrib(self, codigo):
        """Consulta apenas CST, CClasTrib e redução."""
        # Buscar os dados
        resultados = database.buscar_cst_cclastrib_reducao_ncm(codigo)
        
        if not resultados:
            self.exibir_sem_resultados(codigo)
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
        self.resultado_texto.insert(tk.END, f"✅ CONSULTA: NCM {codigo} (CST, CClasTrib e Redução)\n", "titulo")
        self.resultado_texto.insert(tk.END, "=" * 100 + "\n\n")
        
        if len(resultados_agrupados) == 1:
            self.resultado_texto.insert(tk.END, f"📋 1 COMBINAÇÃO ENCONTRADA\n\n", "subtitulo")
        else:
            self.resultado_texto.insert(tk.END, f"📋 {len(resultados_agrupados)} COMBINAÇÕES ENCONTRADAS\n\n", "subtitulo")
        
        for i, (chave, dados) in enumerate(resultados_agrupados.items(), 1):
            ncm_cd, sitr_cd, cltr_cd = chave
            
            self.resultado_texto.insert(tk.END, f"\n{i}. ", "subtitulo")
            self.resultado_texto.insert(tk.END, f"NCM: {ncm_cd}\n", "normal")
            
            # Descrição do NCM (completa)
            desc_ncm = dados['ncm_descricao']
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
            
            self.resultado_texto.insert(tk.END, "-" * 100 + "\n", "info")
        
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
    
    def exibir_sem_resultados(self, codigo):
        """Exibe mensagem quando não há resultados."""
        self.resultado_texto.insert(tk.END, f"🔍 CONSULTA: NCM {codigo}\n", "titulo")
        self.resultado_texto.insert(tk.END, "=" * 100 + "\n\n")
        self.resultado_texto.insert(tk.END, "❌ NENHUM RESULTADO ENCONTRADO\n\n", "destaque")
        self.resultado_texto.insert(tk.END, "Possíveis causas:\n", "subtitulo")
        self.resultado_texto.insert(tk.END, "1. O código NCM pode estar incorreto\n")
        self.resultado_texto.insert(tk.END, "2. O NCM pode não ter regras tributárias cadastradas\n")
        self.resultado_texto.insert(tk.END, "3. Verifique a formatação (ex: 30049099 em vez de 3004.90.99)\n")
        self.status_label.config(text=f"Nenhum resultado para NCM: {codigo}")
    
    def consultar_completo(self, codigo):
        """Consulta informações completas incluindo alíquotas e legislação."""
        # Buscar informações completas
        dados_ncm, resultados = database.buscar_informacoes_completas_ncm(codigo)
        
        if not dados_ncm:
            self.exibir_sem_resultados(codigo)
            return
        
        ncm_cd, ncm_desc, inicio_vig, fim_vig = dados_ncm
        
        # Exibir cabeçalho
        self.resultado_texto.insert(tk.END, f"✅ CONSULTA COMPLETA: NCM {codigo}\n", "titulo")
        self.resultado_texto.insert(tk.END, "=" * 120 + "\n\n")
        
        # Informações básicas do NCM
        self.resultado_texto.insert(tk.END, f"📦 INFORMAÇÕES DO NCM:\n", "subtitulo")
        self.resultado_texto.insert(tk.END, f"• Código: {ncm_cd}\n", "normal")
        self.resultado_texto.insert(tk.END, f"• Descrição: {ncm_desc}\n", "normal")
        self.resultado_texto.insert(tk.END, f"• Vigência: {inicio_vig} até {fim_vig if fim_vig else 'atual'}\n", "normal")
        self.resultado_texto.insert(tk.END, "\n")
        
        if not resultados:
            self.resultado_texto.insert(tk.END, "⚠️ Nenhuma regra tributária encontrada para este NCM.\n", "destaque")
            self.status_label.config(text=f"Nenhuma regra encontrada para NCM: {codigo}")
            return
        
        # Agrupar resultados por NCMA_ID (regra de aplicação)
        regras_agrupadas = {}
        for r in resultados:
            ncm_id = r[4]  # NCMA_ID
            if ncm_id not in regras_agrupadas:
                regras_agrupadas[ncm_id] = []
            regras_agrupadas[ncm_id].append(r)
        
        self.resultado_texto.insert(tk.END, f"📋 REGRAS TRIBUTÁRIAS ENCONTRADAS: {len(regras_agrupadas)}\n\n", "subtitulo")
        
        for i, (ncm_id, regras_grupo) in enumerate(regras_agrupadas.items(), 1):
            primeira_regra = regras_grupo[0]
            
            self.resultado_texto.insert(tk.END, f"\n{i}. REGRA (ID: {ncm_id}):\n", "subtitulo")
            self.resultado_texto.insert(tk.END, f"   • Vigência: {primeira_regra[5]} até {primeira_regra[6] if primeira_regra[6] else 'atual'}\n", "normal")
            
            # Classificação Tributária
            if primeira_regra[7]:  # CLTR_CD
                self.resultado_texto.insert(tk.END, f"   • Código Classificação: {primeira_regra[7]}\n", "normal")
                self.resultado_texto.insert(tk.END, f"   • Descrição: {primeira_regra[8]}\n", "normal")
                
                # Memória de cálculo
                memoria_calculo = primeira_regra[9]
                if memoria_calculo:
                    memoria_processada = database.processar_memoria_calculo(
                        memoria_calculo=memoria_calculo,
                        norma="LC 214/2025",
                        tratamento="Tributação integral"
                    )
                    self.resultado_texto.insert(tk.END, f"   • Memória de cálculo: {memoria_processada}\n", "info")
            
            # Situação Tributária (CST)
            if primeira_regra[16]:  # SITR_CD
                self.resultado_texto.insert(tk.END, f"   • CST: {primeira_regra[16]} - {primeira_regra[17]}\n", "destaque")
            
                # Anexo (Legislação)
                if primeira_regra[18]:  # ANXO_NUMERO
                    self.resultado_texto.insert(tk.END, f"   📚 LEGISLAÇÃO:\n", "legislacao")
                    self.resultado_texto.insert(tk.END, f"     • Anexo: {primeira_regra[18]}, Item: {primeira_regra[19]}\n", "legislacao")
                    if primeira_regra[20]:
                        texto_item = primeira_regra[20]
                        self.resultado_texto.insert(tk.END, f"     • Texto: {texto_item}\n", "legislacao")
            
            # Tributos e Alíquotas
            tributos_info = {}
            for regra in regras_grupo:
                if regra[21]:  # TBTO_SIGLA
                    sigla = regra[21]
                    if sigla not in tributos_info:
                        tributos_info[sigla] = {
                            'nome': regra[22],  # TBTO_NOME
                            'aliquotas': set(),
                            'reducoes': set()
                        }
                    
                    # Alíquotas
                    if regra[23]:  # ALRE_VALOR
                        aliquota_valor = regra[23]
                        aliquota_inicio = regra[24]
                        aliquota_fim = regra[25]
                        aliquota_info = f"{self.formatar_aliquota(aliquota_valor)} ({aliquota_inicio} até {aliquota_fim if aliquota_fim else 'atual'})"
                        tributos_info[sigla]['aliquotas'].add(aliquota_info)
                    
                    # Reduções
                    if regra[28]:  # PERE_VALOR
                        reducao_valor = regra[28]
                        reducao_inicio = regra[29]
                        reducao_fim = regra[30]
                        reducao_info = f"{self.formatar_reducao(reducao_valor)} ({reducao_inicio} até {reducao_fim if reducao_fim else 'atual'})"
                        tributos_info[sigla]['reducoes'].add(reducao_info)
            
            if tributos_info:
                self.resultado_texto.insert(tk.END, f"   💰 ALÍQUOTAS E REDUÇÕES:\n", "aliquota")
                for sigla, info in tributos_info.items():
                    self.resultado_texto.insert(tk.END, f"     • {sigla} ({info['nome']}):\n", "aliquota")
                    
                    if info['aliquotas']:
                        self.resultado_texto.insert(tk.END, f"       - Alíquotas: ", "normal")
                        for aliquota in info['aliquotas']:
                            self.resultado_texto.insert(tk.END, f"{aliquota}; ", "aliquota")
                        self.resultado_texto.insert(tk.END, "\n", "normal")
                    
                    if info['reducoes']:
                        self.resultado_texto.insert(tk.END, f"       - Reduções: ", "normal")
                        for reducao in info['reducoes']:
                            self.resultado_texto.insert(tk.END, f"{reducao}; ", "destaque")
                        self.resultado_texto.insert(tk.END, "\n", "normal")
            
            self.resultado_texto.insert(tk.END, "\n" + "-" * 120 + "\n", "info")
        
        # Resumo final
        self.resultado_texto.insert(tk.END, f"\n📊 RESUMO COMPLETO:\n", "subtitulo")
        self.resultado_texto.insert(tk.END, f"• Total de regras: {len(regras_agrupadas)}\n", "normal")
        
        # Contar tributos diferentes
        todos_tributos = set()
        for regras_grupo in regras_agrupadas.values():
            for regra in regras_grupo:
                if regra[21]:  # TBTO_SIGLA
                    todos_tributos.add(regra[21])
        
        if todos_tributos:
            self.resultado_texto.insert(tk.END, f"• Tributos aplicáveis: {', '.join(sorted(todos_tributos))}\n", "normal")
        
        # Verificar se tem ISS (Imposto Sobre Serviços)
        tem_iss = any('ISS' in tributo for tributo in todos_tributos)
        if tem_iss:
            self.resultado_texto.insert(tk.END, f"• ISS: Presente na tributação\n", "normal")
        else:
            self.resultado_texto.insert(tk.END, f"• ISS: Não aplicável a este NCM\n", "info")
        
        self.status_label.config(text=f"Consulta completa concluída para NCM: {codigo}")
    
    def buscar_ncms_por_descricao(self):
        """Busca NCMs por descrição e exibe na lista."""
        texto = self.entry_busca_desc.get().strip()
        
        if not texto:
            messagebox.showinfo("Informação", "Digite um termo para buscar na descrição dos NCMs.")
            return
        
        self.status_label.config(text=f"Buscando NCMs com: '{texto}'...")
        self.janela.update()
        
        # Limpar lista atual
        self.lista_ncms.delete(0, tk.END)
        
        # Buscar no banco de dados
        try:
            resultados = database.buscar_por_descricao(texto)
            
            if not resultados:
                self.lista_ncms.insert(tk.END, f"Nenhum NCM encontrado com: '{texto}'")
                self.label_info_lista.config(text=f"Nenhum resultado para: '{texto}'")
                self.status_label.config(text=f"Nenhum NCM encontrado com: '{texto}'")
                return
            
            # Adicionar resultados à lista
            for ncm_cd, ncm_desc in resultados:
                # Formatar para exibição: código + descrição (limitada para caber na lista)
                desc_curta = ncm_desc[:80] + "..." if len(ncm_desc) > 80 else ncm_desc
                item = f"{ncm_cd} - {desc_curta}"
                self.lista_ncms.insert(tk.END, item)
            
            self.label_info_lista.config(text=f"{len(resultados)} NCMs encontrados com: '{texto}'")
            self.status_label.config(text=f"{len(resultados)} NCMs encontrados com: '{texto}'")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar NCMs: {str(e)}")
            self.status_label.config(text="Erro na busca de NCMs")
    
    def listar_todos_ncms(self):
        """Lista todos os NCMs disponíveis no banco de dados."""
        self.status_label.config(text="Carregando todos os NCMs...")
        self.janela.update()
        
        # Limpar lista atual
        self.lista_ncms.delete(0, tk.END)
        
        # Limpar campo de busca
        self.entry_busca_desc.delete(0, tk.END)
        
        # Buscar todos os NCMs
        try:
            resultados = database.buscar_ncms()
            
            if not resultados:
                self.lista_ncms.insert(tk.END, "Nenhum NCM encontrado no banco de dados")
                self.label_info_lista.config(text="Nenhum NCM no banco de dados")
                self.status_label.config(text="Nenhum NCM encontrado")
                return
            
            total = len(resultados)
            
            # Adicionar TODOS os resultados à lista
            for i, (ncm_cd, ncm_desc) in enumerate(resultados):
                # Formatar para exibição: código + descrição (limitada para caber melhor)
                desc_curta = ncm_desc[:60] + "..." if len(ncm_desc) > 60 else ncm_desc
                item = f"{ncm_cd} - {desc_curta}"
                self.lista_ncms.insert(tk.END, item)
                
                # Atualizar status periodicamente para mostrar progresso
                if i % 500 == 0 and i > 0:
                    self.status_label.config(text=f"Carregando NCMs... {i}/{total}")
                    self.janela.update()
            
            self.label_info_lista.config(text=f"{total} NCMs carregados. Use busca para filtrar.")
            self.status_label.config(text=f"{total} NCMs carregados completos")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar NCMs: {str(e)}")
            self.status_label.config(text="Erro ao carregar NCMs")
    
    def selecionar_ncm_lista(self, event):
        """Quando um NCM é selecionado na lista, preenche o campo e executa consulta."""
        # Obter índice selecionado
        selecao = self.lista_ncms.curselection()
        
        if not selecao:
            return
        
        # Obter texto do item selecionado
        item_texto = self.lista_ncms.get(selecao[0])
        
        # Extrair código NCM (primeira parte antes do " - ")
        if " - " in item_texto:
            ncm_codigo = item_texto.split(" - ")[0].strip()
            
            # Verificar se é um código NCM válido (apenas dígitos)
            if ncm_codigo.isdigit():
                # Preencher campo de consulta
                self.entry_ncm.delete(0, tk.END)
                self.entry_ncm.insert(0, ncm_codigo)
                
                # Executar consulta automaticamente
                self.consultar_ncm()
                
                # Atualizar status
                self.label_info_lista.config(text=f"NCM {ncm_codigo} selecionado e consultado")
            else:
                self.label_info_lista.config(text="Seleção inválida - não é um código NCM")


def main():
    """Função principal que inicia a aplicação."""
    # Criar janela principal
    janela = tk.Tk()
    
    # Criar instância da calculadora tributária completa
    app = CalculadoraTributariaCompleta(janela)
    
    # Iniciar loop principal da interface
    janela.mainloop()


if __name__ == "__main__":
    main()
