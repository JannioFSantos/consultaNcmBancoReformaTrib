"""
Calculadora Tributária Simplificada
Interface com apenas um campo de busca que mostra todas as informações vinculadas ao NCM
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


class CalculadoraTributariaSimplificada:
    """Classe principal da interface simplificada."""
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📊 Calculadora Tributária - Consulta NCM")
        self.janela.geometry("1200x800")
        self.janela.configure(bg=COR_FUNDO)
        
        # Configurar tema
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Widgets principais
        self.resultado = None
        self.entry_codigo = None
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
        
        tk.Label(titulo_frame, text="Consulta completa de NCM com todas as informações vinculadas", 
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack()
        
        # Card de pesquisa
        card_pesquisa = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_pesquisa.pack(fill=tk.X, pady=(0, 15))
        
        frame_pesquisa = tk.Frame(card_pesquisa, bg=COR_CARD)
        frame_pesquisa.pack(padx=20, pady=15, fill=tk.X)
        
        tk.Label(frame_pesquisa, text="🔍 Digite o código NCM:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 10))
        
        entrada_frame = tk.Frame(frame_pesquisa, bg=COR_CARD)
        entrada_frame.pack(fill=tk.X)
        
        self.entry_codigo = tk.Entry(entrada_frame, width=30, font=FONTE_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_codigo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_buscar = tk.Button(entrada_frame, text="Buscar Informações Completas", 
                           command=self.acao_buscar_completo,
                           bg=COR_SECUNDARIA, fg="white", font=FONTE_SUBTITULO,
                           relief=tk.FLAT, padx=20, cursor="hand2")
        self.btn_buscar.pack(side=tk.LEFT)
        
        # Card de resultados
        card_resultado = tk.Frame(main_frame, bg=COR_CARD, relief=tk.RAISED, bd=1)
        card_resultado.pack(fill=tk.BOTH, expand=True)
        
        frame_resultado = tk.Frame(card_resultado, bg=COR_CARD)
        frame_resultado.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_resultado, text="📄 RESULTADO COMPLETO DA CONSULTA:", 
                 font=FONTE_SUBTITULO, bg=COR_CARD, fg=COR_PRIMARIA).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de resultado com scrollbar
        resultado_frame = tk.Frame(frame_resultado, bg=COR_CARD)
        resultado_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto com scroll
        self.resultado = tk.Text(resultado_frame, height=20, width=120, font=FONTE_MONO,
                                yscrollcommand=scrollbar.set, bg="#f8f9fa", fg=COR_TEXTO,
                                relief=tk.SOLID, bd=1, wrap=tk.WORD)
        self.resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.resultado.yview)
        
        # Status bar
        status_bar = tk.Frame(main_frame, bg=COR_PRIMARIA, height=25)
        status_bar.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(status_bar, text="Pronto para consultar", 
                                    bg=COR_PRIMARIA, fg="white", font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def configurar_eventos(self):
        """Configura os eventos dos widgets."""
        # Permitir buscar com Enter
        self.entry_codigo.bind("<Return>", lambda event: self.acao_buscar_completo())
    
    def converter_para_numero(self, valor):
        """Converte um valor para número (float) se for string."""
        if valor is None:
            return None
        
        try:
            if isinstance(valor, str):
                # Remover caracteres não numéricos se necessário
                valor = valor.replace(',', '.')
                return float(valor)
            elif isinstance(valor, (int, float)):
                return float(valor)
            else:
                return None
        except (ValueError, TypeError):
            return None
    
    def formatar_reducao(self, valor):
        """Formata o valor da redução corretamente."""
        if valor is None:
            return "Não especificada"
        
        # Converter para número primeiro
        valor_num = self.converter_para_numero(valor)
        if valor_num is None:
            return str(valor)
        
        if valor_num >= 10000:
            return "Isenção total (100%)"
        elif valor_num >= 100:
            return f"{valor_num:.2f}% (fator especial)"
        else:
            return f"{valor_num:.2f}%"
    
    def acao_buscar_completo(self):
        """Busca todas as informações do NCM, incluindo reduções."""
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um código NCM válido.")
            return
        
        self.status_label.config(text=f"Buscando informações completas para NCM: {codigo}...")
        self.janela.update()
        
        # Limpar área de resultados
        self.resultado.delete("1.0", tk.END)
        
        # Buscar informações completas
        ncm, regras_completas = database.buscar_informacoes_completas_ncm(codigo)
        
        if not ncm:
            self.resultado.insert(tk.END, f"❌ NCM {codigo} não encontrado no banco de dados.\n")
            self.status_label.config(text=f"NCM {codigo} não encontrado")
            return
        
        # Exibir informações básicas do NCM
        codigo_ncm, desc, inicio, fim = ncm
        
        self.resultado.insert(tk.END, f"📦 INFORMAÇÕES DO NCM\n")
        self.resultado.insert(tk.END, "=" * 100 + "\n")
        self.resultado.insert(tk.END, f"Código: {codigo_ncm}\n")
        self.resultado.insert(tk.END, f"Descrição: {desc}\n")
        self.resultado.insert(tk.END, f"Vigência: {inicio} até {fim if fim else 'atual'}\n\n")
        
        if not regras_completas:
            self.resultado.insert(tk.END, "⚠️ Nenhuma regra tributária vinculada a este NCM.\n")
            self.status_label.config(text=f"NCM {codigo} encontrado, mas sem regras tributárias")
            return
        
        # Agrupar regras por NCMA_ID para evitar duplicações
        regras_agrupadas = {}
        for r in regras_completas:
            ncm_id = r[4]  # NCMA_ID
            if ncm_id not in regras_agrupadas:
                regras_agrupadas[ncm_id] = []
            regras_agrupadas[ncm_id].append(r)
        
        self.resultado.insert(tk.END, f"📘 REGRAS TRIBUTÁRIAS VINCULADAS\n")
        self.resultado.insert(tk.END, "=" * 100 + "\n\n")
        
        total_regras = len(regras_agrupadas)
        self.resultado.insert(tk.END, f"Total de regras encontradas: {total_regras}\n\n")
        
        for i, (ncm_id, regras_grupo) in enumerate(regras_agrupadas.items(), 1):
            primeira_regra = regras_grupo[0]
            
            self.resultado.insert(tk.END, f"📋 REGRA {i} (ID: {ncm_id})\n")
            self.resultado.insert(tk.END, "-" * 80 + "\n")
            self.resultado.insert(tk.END, f"Vigência da regra: {primeira_regra[5]} até {primeira_regra[6] if primeira_regra[6] else 'atual'}\n\n")
            
            # Classificação Tributária
            if primeira_regra[7]:  # CLTR_CD
                self.resultado.insert(tk.END, f"📊 CLASSIFICAÇÃO TRIBUTÁRIA\n")
                self.resultado.insert(tk.END, f"Código: {primeira_regra[7]}\n")
                self.resultado.insert(tk.END, f"Descrição: {primeira_regra[8]}\n")
                
                # Memória de cálculo
                memoria_calculo = primeira_regra[9]
                if memoria_calculo:
                    # Buscar valores para substituição
                    percentual_reducao = None
                    aliquota_ad_valorem = None
                    
                    for regra in regras_grupo:
                        if regra[28] is not None:  # PERCENTUAL_REDUCAO
                            percentual_reducao = regra[28]
                        if regra[23] is not None:  # ALRE_VALOR
                            aliquota_ad_valorem = regra[23]
                    
                    memoria_processada = database.processar_memoria_calculo(
                        memoria_calculo=memoria_calculo,
                        percentual_reducao=percentual_reducao,
                        aliquota_ad_valorem=aliquota_ad_valorem,
                        norma="LC 214/2025",
                        tratamento="Tributação integral"
                    )
                    self.resultado.insert(tk.END, f"Memória de cálculo: {memoria_processada}\n")
                else:
                    self.resultado.insert(tk.END, f"Memória de cálculo: Não disponível\n")
                
                # Informações de crédito
                self.resultado.insert(tk.END, f"\n💳 INFORMAÇÕES DE CRÉDITO\n")
                credito_cbs = "SIM" if primeira_regra[10] == 1 else "NÃO"
                credito_ibs = "SIM" if primeira_regra[11] == 1 else "NÃO"
                credito_pres_forn = "SIM" if primeira_regra[12] == 1 else "NÃO"
                credito_pres_adq = "SIM" if primeira_regra[13] == 1 else "NÃO"
                
                self.resultado.insert(tk.END, f"Crédito CBS: {credito_cbs}\n")
                self.resultado.insert(tk.END, f"Crédito IBS: {credito_ibs}\n")
                self.resultado.insert(tk.END, f"Crédito Presumido Fornecedor: {credito_pres_forn}\n")
                self.resultado.insert(tk.END, f"Crédito Presumido Adquirente: {credito_pres_adq}\n")
                self.resultado.insert(tk.END, f"Tipo de Alíquota: {primeira_regra[14]}\n")
                self.resultado.insert(tk.END, f"Nomenclatura: {primeira_regra[15]}\n")
            
            # Situação Tributária (CST)
            if primeira_regra[16]:  # SITR_CD
                self.resultado.insert(tk.END, f"\n🏷️ SITUAÇÃO TRIBUTÁRIA (CST)\n")
                self.resultado.insert(tk.END, f"Código: {primeira_regra[16]} - {primeira_regra[17]}\n")
            
            # Anexo
            if primeira_regra[18]:  # ANXO_NUMERO
                self.resultado.insert(tk.END, f"\n📄 ANEXO\n")
                self.resultado.insert(tk.END, f"Número: {primeira_regra[18]}, Item: {primeira_regra[19]}\n")
                self.resultado.insert(tk.END, f"Descrição: {primeira_regra[20]}\n")
            
            # Informações detalhadas de alíquotas e reduções
            self.resultado.insert(tk.END, f"\n💰 INFORMAÇÕES DETALHADAS DE ALÍQUOTAS E REDUÇÕES\n")
            self.resultado.insert(tk.END, "-" * 80 + "\n")
            
            # Agrupar informações por tributo
            tributos_info = {}
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
                    
                    if tributo_sigla not in tributos_info:
                        tributos_info[tributo_sigla] = {
                            'nome': tributo_nome,
                            'aliquotas': [],
                            'reducoes': []
                        }
                    
                    # Adicionar informações de alíquota se existirem
                    if aliquota_valor is not None:
                        aliquota_info = {
                            'valor': aliquota_valor,
                            'inicio': aliquota_inicio,
                            'fim': aliquota_fim,
                            'padrao_valor': aliquota_padrao_valor,
                            'padrao_forma': aliquota_padrao_forma
                        }
                        # Verificar se já não existe uma alíquota igual
                        if aliquota_info not in tributos_info[tributo_sigla]['aliquotas']:
                            tributos_info[tributo_sigla]['aliquotas'].append(aliquota_info)
                    
                    # Adicionar informações de redução se existirem
                    if percentual_reducao is not None:
                        reducao_info = {
                            'valor': percentual_reducao,
                            'inicio': reducao_inicio,
                            'fim': reducao_fim
                        }
                        # Verificar se já não existe uma redução igual
                        if reducao_info not in tributos_info[tributo_sigla]['reducoes']:
                            tributos_info[tributo_sigla]['reducoes'].append(reducao_info)
            
            # Exibir informações dos tributos
            if tributos_info:
                for sigla, info in tributos_info.items():
                    self.resultado.insert(tk.END, f"\n  📊 TRIBUTO: {sigla} - {info['nome']}\n")
                    
                    # Exibir alíquotas
                    if info['aliquotas']:
                        for i, aliquota in enumerate(info['aliquotas'], 1):
                            self.resultado.insert(tk.END, f"    {i}. Alíquota: {database.formatar_aliquota(aliquota['valor'])}\n")
                            if aliquota['inicio']:
                                self.resultado.insert(tk.END, f"       Vigência: {aliquota['inicio']} até {aliquota['fim'] if aliquota['fim'] else 'atual'}\n")
                            if aliquota['padrao_valor'] is not None:
                                self.resultado.insert(tk.END, f"       Alíquota Padrão: {database.formatar_aliquota(aliquota['padrao_valor'])}\n")
                                if aliquota['padrao_forma']:
                                    self.resultado.insert(tk.END, f"       Forma de Aplicação: {aliquota['padrao_forma']}\n")
                    else:
                        self.resultado.insert(tk.END, f"    Alíquota: Não especificada\n")
                    
                    # Exibir reduções
                    if info['reducoes']:
                        for i, reducao in enumerate(info['reducoes'], 1):
                            self.resultado.insert(tk.END, f"    {i}. Redução: {self.formatar_reducao(reducao['valor'])}\n")
                            if reducao['inicio']:
                                self.resultado.insert(tk.END, f"       Vigência: {reducao['inicio']} até {reducao['fim'] if reducao['fim'] else 'atual'}\n")
                            
                            # Calcular alíquota efetiva se houver alíquota
                            if info['aliquotas']:
                                for aliquota in info['aliquotas']:
                                    if aliquota['valor'] is not None:
                                        # Converter valores usando a função auxiliar
                                        aliquota_base = self.converter_para_numero(aliquota['valor'])
                                        reducao_valor = self.converter_para_numero(reducao['valor'])
                                        
                                        if aliquota_base is not None and reducao_valor is not None:
                                            if reducao_valor >= 10000:
                                                aliquota_efetiva = 0.0
                                            elif reducao_valor >= 100:
                                                # Redução maior que 100% - tratar como isenção total
                                                aliquota_efetiva = 0.0
                                            else:
                                                aliquota_efetiva = aliquota_base * (1 - reducao_valor/100)
                                            
                                            aliquota_efetiva_formatada = database.formatar_aliquota(aliquota_efetiva)
                                            self.resultado.insert(tk.END, f"       Alíquota Efetiva (com redução): {aliquota_efetiva_formatada}\n")
                                        else:
                                            self.resultado.insert(tk.END, f"       Alíquota Efetiva: Cálculo não disponível\n")
                                        break
                    else:
                        self.resultado.insert(tk.END, f"    Redução: Não aplicável\n")
                    
                    self.resultado.insert(tk.END, "\n")
            else:
                self.resultado.insert(tk.END, "  Nenhum tributo vinculado a esta regra.\n")
            
            self.resultado.insert(tk.END, "\n" + "=" * 100 + "\n\n")
        
        self.status_label.config(text=f"Consulta concluída para NCM: {codigo} - {total_regras} regras encontradas")


def main():
    """Função principal para iniciar a aplicação."""
    janela = tk.Tk()
    app = CalculadoraTributariaSimplificada(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
