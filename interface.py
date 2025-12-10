"""
Módulo de interface gráfica da Calculadora Tributária.
Contém todas as funções relacionadas à interface Tkinter.
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


class CalculadoraTributaria:
    """Classe principal da interface da Calculadora Tributária."""
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📊 Banco de dados Calculadora.db - Consulta NCM")
        self.janela.geometry("1000x700")
        self.janela.configure(bg=COR_FUNDO)
        
        # Configurar tema
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Widgets principais
        self.resultado = None
        self.entry_codigo = None
        self.entry_desc = None
        self.lista_ncm = None
        self.status_label = None
        
        self.criar_widgets()
        self.configurar_eventos()
    
    def criar_widgets(self):
        """Cria todos os widgets da interface."""
        # Frame principal
        main_frame = tk.Frame(self.janela, bg=COR_FUNDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(titulo_frame, text="📊 CALCULADORA TRIBUTÁRIA", 
                 font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_PRIMARIA).pack()
        
        tk.Label(titulo_frame, text="Consulta completa de NCM para IBS, CBS e IS", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack()
        
        # Card de pesquisa - alinhado à esquerda
        card_pesquisa = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_pesquisa.pack(fill=tk.X, pady=(0, 15))
        
        frame_pesquisa = tk.Frame(card_pesquisa, bg=COR_CARD)
        frame_pesquisa.pack(padx=10, pady=15, fill=tk.X, anchor=tk.W)
        
        # Pesquisa por código NCM - alinhada à esquerda
        pesquisa_codigo_frame = tk.Frame(frame_pesquisa, bg=COR_CARD)
        pesquisa_codigo_frame.pack(fill=tk.X, pady=(0, 10), anchor=tk.W)
        
        tk.Label(pesquisa_codigo_frame, text="🔍 Pesquisar por Código NCM:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 5))
        
        entrada_codigo_frame = tk.Frame(pesquisa_codigo_frame, bg=COR_CARD)
        entrada_codigo_frame.pack(fill=tk.X, anchor=tk.W)
        
        self.entry_codigo = tk.Entry(entrada_codigo_frame, width=25, font=FONTE_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_codigo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_buscar = tk.Button(entrada_codigo_frame, text="Buscar", command=self.acao_buscar_codigo_com_status,
                           bg=COR_SECUNDARIA, fg="white", font=FONTE_SUBTITULO,
                           relief=tk.FLAT, padx=20, cursor="hand2")
        self.btn_buscar.pack(side=tk.LEFT)
        
        # Pesquisa por descrição - alinhada à esquerda
        pesquisa_desc_frame = tk.Frame(frame_pesquisa, bg=COR_CARD)
        pesquisa_desc_frame.pack(fill=tk.X, anchor=tk.W)
        
        tk.Label(pesquisa_desc_frame, text="📝 Pesquisar por Descrição:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 5))
        
        entrada_desc_frame = tk.Frame(pesquisa_desc_frame, bg=COR_CARD)
        entrada_desc_frame.pack(fill=tk.X, anchor=tk.W)
        
        self.entry_desc = tk.Entry(entrada_desc_frame, width=40, font=FONTE_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_desc.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_desc = tk.Button(entrada_desc_frame, text="Buscar Descrição", command=self.acao_buscar_descricao_com_status,
                         bg=COR_TERCIARIA, fg="white", font=FONTE_SUBTITULO,
                         relief=tk.FLAT, padx=15, cursor="hand2")
        self.btn_desc.pack(side=tk.LEFT)
        
        # Botão para consultar reduções específicas
        self.btn_reducoes = tk.Button(entrada_codigo_frame, text="Consultar Reduções", command=self.acao_consultar_reducoes,
                             bg="#e74c3c", fg="white", font=FONTE_SUBTITULO,
                             relief=tk.FLAT, padx=15, cursor="hand2")
        self.btn_reducoes.pack(side=tk.LEFT, padx=(10, 0))
        
        # Card de lista de NCMs
        card_lista = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_lista.pack(fill=tk.X, pady=(0, 15))
        
        frame_lista = tk.Frame(card_lista, bg=COR_CARD)
        frame_lista.pack(padx=20, pady=15)
        
        tk.Label(frame_lista, text="📋 Lista de NCMs:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 10))
        
        lista_container = tk.Frame(frame_lista, bg=COR_CARD)
        lista_container.pack(fill=tk.X, pady=(0, 10))
        
        self.lista_ncm = ttk.Combobox(lista_container, width=70, font=FONTE_NORMAL)
        self.lista_ncm.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_carregar = tk.Button(lista_container, text="Carregar Todos", command=self.carregar_lista_todos_com_status,
                             bg=COR_PRIMARIA, fg="white", font=FONTE_SUBTITULO,
                             relief=tk.FLAT, padx=15, cursor="hand2")
        self.btn_carregar.pack(side=tk.LEFT)
        
        # Card de resultados
        card_resultado = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_resultado.pack(fill=tk.BOTH, expand=True)
        
        frame_resultado = tk.Frame(card_resultado, bg=COR_CARD)
        frame_resultado.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_resultado, text="📄 Resultado da Consulta:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de resultado com scrollbar
        resultado_frame = tk.Frame(frame_resultado, bg=COR_CARD)
        resultado_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto com scroll
        self.resultado = tk.Text(resultado_frame, height=15, width=100, font=FONTE_MONO,
                                yscrollcommand=scrollbar.set, bg="#f8f9fa", fg=COR_TEXTO,
                                relief=tk.SOLID, bd=1, wrap=tk.WORD)
        self.resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.resultado.yview)
        
        # Configurar tags para formatação do texto
        self.resultado.tag_configure("titulo", font=("Segoe UI", 11, "bold"), foreground=COR_PRIMARIA)
        self.resultado.tag_configure("subtitulo", font=("Segoe UI", 10, "bold"), foreground=COR_SECUNDARIA)
        self.resultado.tag_configure("destaque", font=("Segoe UI", 10, "bold"), foreground=COR_DESTAQUE)
        self.resultado.tag_configure("normal", font=FONTE_MONO, foreground=COR_TEXTO)
        self.resultado.tag_configure("info", font=FONTE_MONO, foreground="#7f8c8d")
        
        # Status bar
        status_bar = tk.Frame(main_frame, bg=COR_PRIMARIA, height=25)
        status_bar.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(status_bar, text="Pronto para consultar", 
                                    bg=COR_PRIMARIA, fg="white", font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def configurar_eventos(self):
        """Configura os eventos dos widgets."""
        self.lista_ncm.bind("<<ComboboxSelected>>", self.acao_selecionar)
    
    def formatar_reducao(self, valor):
        """Formata o valor da redução corretamente."""
        if valor is None:
            return "Não especificada"
        
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
            # Vamos formatar de forma mais legível
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
    
    # Funções de ação
    def acao_buscar_codigo_com_status(self):
        """Busca NCM por código com atualização de status."""
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um NCM válido.")
            return
        
        self.status_label.config(text=f"Buscando NCM: {codigo}...")
        self.janela.update()
        
        ncm, regras_completas = database.buscar_informacoes_completas_ncm(codigo)
        self.exibir_resultado_completo(ncm, regras_completas)
        
        if ncm:
            self.status_label.config(text=f"Consulta concluída para NCM: {codigo}")
        else:
            self.status_label.config(text=f"NCM {codigo} não encontrado")
    
    def acao_buscar_descricao_com_status(self):
        """Busca NCM por descrição com atualização de status."""
        texto = self.entry_desc.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite um termo para busca.")
            return
        
        self.status_label.config(text=f"Buscando por: '{texto}'...")
        self.janela.update()
        
        ncms = database.buscar_por_descricao(texto)
        self.atualizar_lista(ncms)
        
        if ncms:
            self.status_label.config(text=f"Encontrados {len(ncms)} NCMs para: '{texto}'")
        else:
            self.status_label.config(text=f"Nenhum NCM encontrado para: '{texto}'")
    
    def acao_consultar_reducoes(self):
        """Consulta especificamente as reduções para o NCM informado."""
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um NCM válido para consultar reduções.")
            return
        
        self.status_label.config(text=f"Consultando reduções para NCM: {codigo}...")
        self.janela.update()
        
        # Buscar reduções específicas
        reducoes = database.buscar_reducoes_ncm(codigo)
        
        # Limpar área de resultados
        self.resultado.delete("1.0", tk.END)
        
        if not reducoes:
            self.resultado.insert(tk.END, f"🔍 CONSULTA DE REDUÇÕES - NCM: {codigo}\n")
            self.resultado.insert(tk.END, "=" * 80 + "\n\n")
            self.resultado.insert(tk.END, "❌ NENHUMA REDUÇÃO ENCONTRADA para este NCM.\n\n")
            self.resultado.insert(tk.END, "Possíveis causas:\n")
            self.resultado.insert(tk.END, "1. O NCM não possui reduções cadastradas\n")
            self.resultado.insert(tk.END, "2. As reduções podem estar fora da vigência\n")
            self.resultado.insert(tk.END, "3. Verifique se o código NCM está correto\n")
            self.status_label.config(text=f"Nenhuma redução encontrada para NCM: {codigo}")
            return
        
        # Exibir reduções encontradas
        self.resultado.insert(tk.END, f"✅ REDUÇÕES ENCONTRADAS - NCM: {codigo}\n")
        self.resultado.insert(tk.END, "=" * 80 + "\n\n")
        self.resultado.insert(tk.END, f"Total de reduções encontradas: {len(reducoes)}\n\n")
        
        # Agrupar por classificação tributária
        reducoes_agrupadas = {}
        for reducao in reducoes:
            cltr_cd = reducao[1]  # CLTR_CD
            if cltr_cd not in reducoes_agrupadas:
                reducoes_agrupadas[cltr_cd] = {
                    'descricao': reducao[2],  # CLTR_DESCRICAO
                    'tributos': []
                }
            
            reducoes_agrupadas[cltr_cd]['tributos'].append({
                'sigla': reducao[3],  # TBTO_SIGLA
                'nome': reducao[4],   # TBTO_NOME
                'aliquota': reducao[5],  # ALIQUOTA
                'reducao': reducao[6],   # REDUCAO
                'reducao_inicio': reducao[7],  # REDUCAO_INICIO
                'reducao_fim': reducao[8],     # REDUCAO_FIM
                'aliquota_inicio': reducao[9],  # ALIQUOTA_INICIO
                'aliquota_fim': reducao[10]     # ALIQUOTA_FIM
            })
        
        # Exibir reduções agrupadas
        for cltr_cd, dados in reducoes_agrupadas.items():
            self.resultado.insert(tk.END, f"📋 Classificação Tributária: {cltr_cd}\n")
            self.resultado.insert(tk.END, f"   Descrição: {dados['descricao']}\n\n")
            
            for tributo in dados['tributos']:
                self.resultado.insert(tk.END, f"   • Tributo: {tributo['sigla']} ({tributo['nome']})\n")
                
                # Formatar alíquota e redução
                aliquota_formatada = database.formatar_aliquota(tributo['aliquota'])
                reducao_formatada = self.formatar_reducao(tributo['reducao'])
                
                self.resultado.insert(tk.END, f"     - Alíquota: {aliquota_formatada}\n")
                self.resultado.insert(tk.END, f"       Vigência alíquota: {tributo['aliquota_inicio']} até {tributo['aliquota_fim'] if tributo['aliquota_fim'] else 'atual'}\n")
                self.resultado.insert(tk.END, f"     - Redução: {reducao_formatada}\n")
                self.resultado.insert(tk.END, f"       Vigência redução: {tributo['reducao_inicio']} até {tributo['reducao_fim'] if tributo['reducao_fim'] else 'atual'}\n")
                
                # Calcular alíquota efetiva
                if tributo['aliquota'] is not None and tributo['reducao'] is not None:
                    try:
                        aliquota_base = float(tributo['aliquota'])
                        reducao_valor = float(tributo['reducao'])
                        
                        if reducao_valor >= 10000:
                            aliquota_efetiva = 0.0
                        elif reducao_valor >= 100:
                            # Redução maior que 100% - tratar como isenção
                            aliquota_efetiva = 0.0
                        else:
                            aliquota_efetiva = aliquota_base * (1 - reducao_valor/100)
                        
                        aliquota_efetiva_formatada = database.formatar_aliquota(aliquota_efetiva)
                        self.resultado.insert(tk.END, f"     - Alíquota efetiva (com redução): {aliquota_efetiva_formatada}\n")
                    except (ValueError, TypeError):
                        pass
                
                self.resultado.insert(tk.END, "\n")
            
            self.resultado.insert(tk.END, "\n")
        
        self.status_label.config(text=f"Encontradas {len(reducoes)} reduções para NCM: {codigo}")
    
    def exibir_resultado_completo(self, ncm, regras_completas):
        """Exibe o resultado completo da consulta."""
        self.resultado.delete("1.0", tk.END)

        if not ncm:
            self.resultado.insert(tk.END, "NCM não encontrado.")
            return

        codigo, desc, inicio, fim = ncm

        # Primeiro, mostrar informações das relações/tabelas envolvidas
        self.resultado.insert(tk.END, f"📦 NCM: {codigo}\n")
        self.resultado.insert(tk.END, f"Descrição: {desc}\n")
        self.resultado.insert(tk.END, f"Início vigência: {inicio}\n")
        self.resultado.insert(tk.END, f"Fim vigência: {fim}\n\n")
        
        # Obter e exibir relações/tabelas envolvidas
        self.resultado.insert(tk.END, "🔗 RELAÇÕES DO BANCO DE DADOS ENVOLVIDAS:\n")
        self.resultado.insert(tk.END, "=" * 120 + "\n\n")
        
        try:
            relacoes = database.obter_relacoes_tabelas_ncm(codigo)
            if relacoes:
                # Agrupar por tabela
                tabelas_agrupadas = {}
                for relacao in relacoes:
                    tabela = relacao['tabela']
                    if tabela not in tabelas_agrupadas:
                        tabelas_agrupadas[tabela] = []
                    tabelas_agrupadas[tabela].append(relacao)
                
                for tabela, rels in tabelas_agrupadas.items():
                    self.resultado.insert(tk.END, f"📊 TABELA: {tabela}\n")
                    self.resultado.insert(tk.END, f"  Total de registros relacionados: {len(rels)}\n")
                    
                    # Mostrar apenas os primeiros 3 registros de cada tabela para não poluir
                    for rel in rels[:3]:
                        self.resultado.insert(tk.END, f"  • Código: {rel['codigo']}\n")
                        if rel['descricao']:
                            self.resultado.insert(tk.END, f"    Descrição: {rel['descricao']}\n")
                        self.resultado.insert(tk.END, f"    Tipo relação: {rel['tipo_relacao']}\n")
                    
                    if len(rels) > 3:
                        self.resultado.insert(tk.END, f"  • ... e mais {len(rels) - 3} registros\n")
                    
                    self.resultado.insert(tk.END, "\n")
            else:
                self.resultado.insert(tk.END, "Nenhuma relação específica encontrada.\n")
        except Exception as e:
            self.resultado.insert(tk.END, f"Erro ao obter relações: {str(e)}\n")
        
        self.resultado.insert(tk.END, "\n" + "=" * 120 + "\n\n")

        if not regras_completas:
            self.resultado.insert(tk.END, "Nenhuma regra tributária cadastrada.\n")
            return

        # Agrupar regras por NCMA_ID para evitar duplicações
        regras_agrupadas = {}
        for r in regras_completas:
            ncm_id = r[4]  # NCMA_ID
            if ncm_id not in regras_agrupadas:
                regras_agrupadas[ncm_id] = []
            regras_agrupadas[ncm_id].append(r)
        
        self.resultado.insert(tk.END, "📘 CLASSIFICAÇÃO TRIBUTÁRIA COMPLETA:\n")
        self.resultado.insert(tk.END, "=" * 120 + "\n\n")
        
        for i, (ncm_id, regras_grupo) in enumerate(regras_agrupadas.items(), 1):
            # Primeira regra do grupo contém informações comuns
            primeira_regra = regras_grupo[0]
            
            self.resultado.insert(tk.END, f"REGRA {i} (ID: {ncm_id}):\n")
            self.resultado.insert(tk.END, f"  • Vigência: {primeira_regra[5]} até {primeira_regra[6] if primeira_regra[6] else 'atual'}\n")
            
            # Classificação Tributária
            if primeira_regra[7]:  # CLTR_CD
                self.resultado.insert(tk.END, f"  • Código Classificação: {primeira_regra[7]}\n")
                self.resultado.insert(tk.END, f"  • Descrição: {primeira_regra[8]}\n")
                
                # Processar memória de cálculo com valores reais
                memoria_calculo = primeira_regra[9]
                if memoria_calculo:
                    # Obter valores para substituição
                    percentual_reducao = None
                    aliquota_ad_valorem = None
                    
                    # Buscar valores de redução e alíquota para esta classificação
                    # Garantir que pegamos apenas valores numéricos válidos
                    for regra in regras_grupo:
                        # Verificar se é um valor numérico válido para redução (não data)
                        if regra[28] is not None and isinstance(regra[28], (int, float)):
                            # Verificar se não é uma data (datas são strings no formato YYYY-MM-DD)
                            if not (isinstance(regra[28], str) and len(regra[28]) == 10 and regra[28][4] == '-' and regra[28][7] == '-'):
                                percentual_reducao = regra[28]
                        
                        # Verificar se é um valor numérico válido para alíquota
                        if regra[23] is not None and isinstance(regra[23], (int, float)):
                            aliquota_ad_valorem = regra[23]
                    
                    # Processar memória de cálculo
                    memoria_processada = database.processar_memoria_calculo(
                        memoria_calculo=memoria_calculo,
                        percentual_reducao=percentual_reducao,
                        aliquota_ad_valorem=aliquota_ad_valorem,
                        # Outros parâmetros podem ser adicionados conforme necessário
                        norma="LC 214/2025",  # Exemplo - poderia ser obtido do banco
                        tratamento="Tributação integral"  # Exemplo - poderia ser obtido do banco
                    )
                    self.resultado.insert(tk.END, f"  • Memória de cálculo: {memoria_processada}\n")
                else:
                    self.resultado.insert(tk.END, f"  • Memória de cálculo: Não disponível\n")
                
                # Informações de crédito
                credito_cbs = "SIM" if primeira_regra[10] == 1 else "NÃO"
                credito_ibs = "SIM" if primeira_regra[11] == 1 else "NÃO"
                credito_pres_forn = "SIM" if primeira_regra[12] == 1 else "NÃO"
                credito_pres_adq = "SIM" if primeira_regra[13] == 1 else "NÃO"
                
                self.resultado.insert(tk.END, f"  • Crédito CBS: {credito_cbs}\n")
                self.resultado.insert(tk.END, f"  • Crédito IBS: {credito_ibs}\n")
                self.resultado.insert(tk.END, f"  • Crédito Presumido Fornecedor: {credito_pres_forn}\n")
                self.resultado.insert(tk.END, f"  • Crédito Presumido Adquirente: {credito_pres_adq}\n")
                self.resultado.insert(tk.END, f"  • Tipo de Alíquota: {primeira_regra[14]}\n")
                self.resultado.insert(tk.END, f"  • Nomenclatura: {primeira_regra[15]}\n")
            
            # Situação Tributária (CST)
            if primeira_regra[16]:  # SITR_CD
                self.resultado.insert(tk.END, f"  • CST: {primeira_regra[16]} - {primeira_regra[17]}\n")
            
            # Anexo
            if primeira_regra[18]:  # ANXO_NUMERO
                self.resultado.insert(tk.END, f"  • Anexo: {primeira_regra[18]}, Item: {primeira_regra[19]}\n")
                self.resultado.insert(tk.END, f"  • Descrição: {primeira_regra[20]}\n")
            
            # Tributos, Alíquotas e Reduções - Agrupar para evitar duplicação
            tributos_aliquotas = {}
            for regra in regras_grupo:
                if regra[21]:  # TBTO_SIGLA
                    tributo_sigla = regra[21]
                    tributo_nome = regra[22]
                    aliquota_valor = regra[23]  # ALRE_VALOR
                    aliquota_inicio = regra[24]  # ALIQUOTA_INICIO
                    aliquota_fim = regra[25]  # ALIQUOTA_FIM
                    aliquota_padrao_valor = regra[26]  # ALPA_VALOR
                    aliquota_padrao_forma = regra[27]  # ALPA_FORMA_APLICACAO
                    percentual_reducao = regra[28]  # PERCENTUAL_REDUCAO
                    reducao_inicio = regra[29]  # REDUCAO_INICIO
                    reducao_fim = regra[30]  # REDUCAO_FIM
                    
                    if tributo_sigla not in tributos_aliquotas:
                        tributos_aliquotas[tributo_sigla] = {
                            'nome': tributo_nome,
                            'aliquotas': {},  # Usar dicionário para evitar duplicação por valor
                            'reducoes': {}    # Usar dicionário para evitar duplicação por valor
                        }
                    
                    # Adicionar informações de alíquota se existirem (evitar duplicação)
                    if aliquota_valor is not None:
                        # Converter para string para usar como chave
                        aliquota_valor_str = str(aliquota_valor)
                        aliquota_key = f"{aliquota_valor_str}_{aliquota_inicio}_{aliquota_fim}"
                        if aliquota_key not in tributos_aliquotas[tributo_sigla]['aliquotas']:
                            aliquota_info = {
                                'valor': aliquota_valor,
                                'inicio': aliquota_inicio,
                                'fim': aliquota_fim,
                                'padrao_valor': aliquota_padrao_valor,
                                'padrao_forma': aliquota_padrao_forma
                            }
                            tributos_aliquotas[tributo_sigla]['aliquotas'][aliquota_key] = aliquota_info
                    
                    # Adicionar informações de redução se existirem (evitar duplicação)
                    if percentual_reducao is not None:
                        # Converter para string para usar como chave
                        reducao_valor_str = str(percentual_reducao)
                        reducao_key = f"{reducao_valor_str}_{reducao_inicio}_{reducao_fim}"
                        if reducao_key not in tributos_aliquotas[tributo_sigla]['reducoes']:
                            reducao_info = {
                                'valor': percentual_reducao,
                                'inicio': reducao_inicio,
                                'fim': reducao_fim
                            }
                            tributos_aliquotas[tributo_sigla]['reducoes'][reducao_key] = reducao_info
            
            if tributos_aliquotas:
                self.resultado.insert(tk.END, f"  • Tributos, Alíquotas e Reduções Aplicáveis:\n")
                for sigla, info in tributos_aliquotas.items():
                    self.resultado.insert(tk.END, f"      - {sigla}: {info['nome']}\n")
                    
                    # Exibir alíquotas (agora são dicionários)
                    if info['aliquotas']:
                        for aliquota_key, aliquota in info['aliquotas'].items():
                            # Formatar alíquota corretamente
                            aliquota_formatada = database.formatar_aliquota(aliquota['valor'])
                            
                            # Alíquota de referência
                            self.resultado.insert(tk.END, f"        • Alíquota: {aliquota_formatada}\n")
                            self.resultado.insert(tk.END, f"          Vigência: {aliquota['inicio']} até {aliquota['fim'] if aliquota['fim'] else 'atual'}\n")
                            
                            # Alíquota padrão (se existir)
                            if aliquota['padrao_valor'] is not None:
                                aliquota_padrao_formatada = database.formatar_aliquota(aliquota['padrao_valor'])
                                self.resultado.insert(tk.END, f"        • Alíquota Padrão: {aliquota_padrao_formatada}\n")
                                if aliquota['padrao_forma']:
                                    self.resultado.insert(tk.END, f"          Forma de Aplicação: {aliquota['padrao_forma']}\n")
                    else:
                        self.resultado.insert(tk.END, f"        • Alíquota não especificada\n")
                    
                    # Exibir reduções (agora são dicionários)
                    if info['reducoes']:
                        for reducao_key, reducao in info['reducoes'].items():
                            reducao_formatada = self.formatar_reducao(reducao['valor'])
                            self.resultado.insert(tk.END, f"        • Redução: {reducao_formatada}\n")
                            self.resultado.insert(tk.END, f"          Vigência: {reducao['inicio']} até {reducao['fim'] if reducao['fim'] else 'atual'}\n")
                    
                    # Calcular e exibir alíquota efetiva se houver redução
                    if info['aliquotas'] and info['reducoes']:
                        # Para simplificar, pegar a primeira alíquota e primeira redução
                        aliquota_base = next(iter(info['aliquotas'].values()))['valor']
                        reducao = next(iter(info['reducoes'].values()))['valor']
                        if aliquota_base is not None and reducao is not None:
                            # Calcular alíquota efetiva: aliquota * (1 - reducao/100)
                            # Nota: reducao está em percentual (ex: 10000% = 100)
                            try:
                                aliquota_base_float = float(aliquota_base) if isinstance(aliquota_base, str) else aliquota_base
                                reducao_float = float(reducao) if isinstance(reducao, str) else reducao
                                
                                if reducao_float >= 10000:
                                    aliquota_efetiva = 0.0
                                elif reducao_float >= 100:
                                    # Redução maior que 100% - tratar como isenção
                                    aliquota_efetiva = 0.0
                                else:
                                    aliquota_efetiva = aliquota_base_float * (1 - reducao_float/100)
                                
                                aliquota_efetiva_formatada = database.formatar_aliquota(aliquota_efetiva)
                                self.resultado.insert(tk.END, f"        • Alíquota Efetiva (com redução): {aliquota_efetiva_formatada}\n")
                            except (ValueError, TypeError):
                                pass
            
            self.resultado.insert(tk.END, "\n" + "-" * 120 + "\n\n")
    
    def atualizar_lista(self, ncms):
        """Atualiza a lista de NCMs no combobox."""
        if not ncms:
            self.lista_ncm['values'] = []
            self.lista_ncm.set('')
            return
        
        # Formatar cada NCM para exibição
        valores = []
        for codigo, descricao in ncms:
            # Limitar descrição para não ficar muito longa
            desc_curta = descricao[:80] + "..." if len(descricao) > 80 else descricao
            valores.append(f"{codigo} - {desc_curta}")
        
        self.lista_ncm['values'] = valores
        self.lista_ncm.set('')
    
    def carregar_lista_todos_com_status(self):
        """Carrega todos os NCMs do banco de dados com atualização de status."""
        self.status_label.config(text="Carregando todos os NCMs...")
        self.janela.update()
        
        try:
            ncms = database.buscar_ncms()
            self.atualizar_lista(ncms)
            
            if ncms:
                self.status_label.config(text=f"Carregados {len(ncms)} NCMs")
            else:
                self.status_label.config(text="Nenhum NCM encontrado no banco de dados")
        except Exception as e:
            self.status_label.config(text=f"Erro ao carregar NCMs: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao carregar NCMs: {str(e)}")
    
    def acao_selecionar(self, event=None):
        """Ação executada quando um NCM é selecionado na lista."""
        selecionado = self.lista_ncm.get()
        if not selecionado:
            return
        
        # Extrair o código NCM da string selecionada
        partes = selecionado.split(' - ')
        if len(partes) > 0:
            codigo = partes[0].strip()
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.insert(0, codigo)
            
            # Executar busca automática
            self.acao_buscar_codigo_com_status()
