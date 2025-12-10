"""
Módulo de acesso ao banco de dados da Calculadora Tributária.
Contém todas as funções de consulta SQL.
"""

import sqlite3

DB_PATH = "calculadora.db"


def conectar():
    """Estabelece conexão com o banco de dados."""
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


def buscar_informacoes_completas_ncm(codigo):
    """
    Busca informações completas do NCM incluindo todas as regras tributárias, alíquotas e reduções.
    Usa uma consulta simplificada que sabemos que funciona.
    """
    conn = conectar()
    cur = conn.cursor()

    # 1. Buscar informações básicas do NCM
    cur.execute("""
        SELECT 
            NCM_CD,
            NCM_DESCRICAO,
            NCM_INICIO_VIGENCIA,
            NCM_FIM_VIGENCIA
        FROM NCM 
        WHERE NCM_CD = ?
    """, (codigo,))
    
    dados_ncm = cur.fetchone()
    
    if not dados_ncm:
        conn.close()
        return None, None
    
    # 2. Buscar todas as regras vinculadas ao NCM com informações completas
    # Consulta simplificada que garante que as reduções sejam retornadas
    cur.execute("""
        SELECT 
            -- Informações do NCM
            n.NCM_CD,
            n.NCM_DESCRICAO,
            n.NCM_INICIO_VIGENCIA,
            n.NCM_FIM_VIGENCIA,
            
            -- Informações da regra de aplicação
            na.NCMA_ID,
            na.NCMA_INICIO_VIGENCIA,
            na.NCMA_FIM_VIGENCIA,
            
            -- Classificação Tributária
            ct.CLTR_CD,
            ct.CLTR_DESCRICAO,
            ct.CLTR_MEMORIA_CALCULO,
            ct.CLTR_IN_APROPRIACAO_CREDITOS_ADQUIRENTES_CBS,
            ct.CLTR_IN_APROPRIACAO_CREDITOS_ADQUIRENTES_IBS,
            ct.CLTR_IN_CREDITO_PRESUMIDO_FORNECEDOR,
            ct.CLTR_IN_CREDITO_PRESUMIDO_ADQUIRENTE,
            ct.CLTR_TIPO_ALIQUOTA,
            ct.CLTR_NOMENCLATURA,
            
            -- Situação Tributária (CST)
            st.SITR_CD,
            st.SITR_DESCRICAO,
            
            -- Anexo
            a.ANXO_NUMERO,
            a.ANXO_NUMERO_ITEM,
            a.ANXO_TEXTO_ITEM,
            
            -- Tributos (CBS, IBSUF, IBSMun)
            t.TBTO_SIGLA,
            t.TBTO_NOME,
            
            -- Alíquotas de referência
            ar.ALRE_VALOR,
            ar.ALRE_INICIO_VIGENCIA,
            ar.ALRE_FIM_VIGENCIA,
            
            -- Alíquotas padrão
            ap.ALPA_VALOR,
            ap.ALPA_FORMA_APLICACAO,
            ap.ALPA_INICIO_VIGENCIA,
            ap.ALPA_FIM_VIGENCIA,
            
            -- Percentuais de Redução (CRÍTICO - usando JOIN direto que funciona)
            pr.PERE_VALOR,
            pr.PERE_INICIO_VIGENCIA,
            pr.PERE_FIM_VIGENCIA
            
        FROM NCM n
        -- JOIN principal: NCM -> NCM_APLICAVEL -> CLASSIFICACAO_TRIBUTARIA
        JOIN NCM_APLICAVEL na ON n.NCM_CD = na.NCMA_NCM_CD
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        
        -- JOINs opcionais para informações adicionais
        LEFT JOIN SITUACAO_TRIBUTARIA st ON ct.CLTR_SITR_ID = st.SITR_ID
        LEFT JOIN ANEXO a ON na.NCMA_ANXO_ID = a.ANXO_ID
        
        -- JOIN para tributos através de TRIBUTO_SITUACAO_TRIBUTARIA
        LEFT JOIN TRIBUTO_SITUACAO_TRIBUTARIA tst ON st.SITR_ID = tst.TRST_SITR_ID
        LEFT JOIN TRIBUTO t ON tst.TRST_TBTO_ID = t.TBTO_ID
        
        -- JOIN para alíquotas
        LEFT JOIN ALIQUOTA_REFERENCIA ar ON t.TBTO_ID = ar.ALRE_TBTO_ID
        LEFT JOIN ALIQUOTA_PADRAO ap ON ar.ALRE_ID = ap.ALPA_ALRE_ID
        
        -- JOIN CRÍTICO para reduções - usando LEFT JOIN para garantir que todas as regras sejam retornadas
        -- mesmo que não tenham reduções
        LEFT JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID 
            AND (pr.PERE_TBTO_ID IS NULL OR pr.PERE_TBTO_ID = t.TBTO_ID)
        
        WHERE n.NCM_CD = ?
        ORDER BY 
            na.NCMA_INICIO_VIGENCIA DESC,
            ct.CLTR_CD,
            t.TBTO_SIGLA,
            pr.PERE_VALOR DESC NULLS LAST
    """, (codigo,))
    
    resultados = cur.fetchall()
    conn.close()
    
    return dados_ncm, resultados


def formatar_aliquota(valor):
    """Formata o valor da alíquota corretamente (0.9 → 0.90%)."""
    if valor is None:
        return "Não especificada"
    
    # Os valores no banco já estão em formato percentual (0.9 = 0.9%)
    # Não precisamos multiplicar por 100
    return f"{valor:.2f}%"


def processar_memoria_calculo(memoria_calculo, percentual_reducao=None, aliquota_ad_valorem=None, 
                             base_calculo=None, norma=None, tratamento=None, aliquota_ad_rem=None,
                             quantidade=None, unidade=None):
    """
    Substitui placeholders na memória de cálculo pelos valores reais.
    
    Args:
        memoria_calculo: Texto da memória de cálculo com placeholders
        percentual_reducao: Valor do percentual de redução
        aliquota_ad_valorem: Valor da alíquota ad valorem
        base_calculo: Valor da base de cálculo
        norma: Texto da norma legal
        tratamento: Texto do tratamento tributário
        aliquota_ad_rem: Valor da alíquota ad rem
        quantidade: Quantidade para cálculos ad rem
        unidade: Unidade de medida para cálculos ad rem
    
    Returns:
        Texto da memória de cálculo com placeholders substituídos
    """
    if not memoria_calculo:
        return "Memória de cálculo não disponível"
    
    resultado = memoria_calculo
    
    # Substituir placeholders comuns
    if percentual_reducao is not None:
        try:
            # Converter para float se for string
            if isinstance(percentual_reducao, str):
                percentual_reducao = float(percentual_reducao)
            resultado = resultado.replace('[percentual_reducao]', f'{percentual_reducao:.2f}')
        except (ValueError, TypeError):
            resultado = resultado.replace('[percentual_reducao]', str(percentual_reducao))
    
    if aliquota_ad_valorem is not None:
        try:
            # Converter para float se for string
            if isinstance(aliquota_ad_valorem, str):
                aliquota_ad_valorem = float(aliquota_ad_valorem)
            resultado = resultado.replace('[aliquota_ad_valorem]', f'{aliquota_ad_valorem:.2f}')
        except (ValueError, TypeError):
            resultado = resultado.replace('[aliquota_ad_valorem]', str(aliquota_ad_valorem))
    
    if base_calculo is not None:
        try:
            # Converter para float se for string
            if isinstance(base_calculo, str):
                base_calculo = float(base_calculo)
            resultado = resultado.replace('[base_calculo]', f'{base_calculo:.2f}')
        except (ValueError, TypeError):
            resultado = resultado.replace('[base_calculo]', str(base_calculo))
    
    if norma is not None:
        resultado = resultado.replace('[norma]', norma)
    
    if tratamento is not None:
        resultado = resultado.replace('[tratamento]', tratamento)
    
    if aliquota_ad_rem is not None:
        try:
            # Converter para float se for string
            if isinstance(aliquota_ad_rem, str):
                aliquota_ad_rem = float(aliquota_ad_rem)
            resultado = resultado.replace('[aliquota_ad_rem]', f'{aliquota_ad_rem:.2f}')
        except (ValueError, TypeError):
            resultado = resultado.replace('[aliquota_ad_rem]', str(aliquota_ad_rem))
    
    if quantidade is not None:
        try:
            # Converter para float se for string
            if isinstance(quantidade, str):
                quantidade = float(quantidade)
            resultado = resultado.replace('[quantidade]', f'{quantidade:.2f}')
        except (ValueError, TypeError):
            resultado = resultado.replace('[quantidade]', str(quantidade))
    
    if unidade is not None:
        resultado = resultado.replace('[unidade]', unidade)
    
    # Remover placeholders não substituídos
    import re
    resultado = re.sub(r'\[.*?\]', 'não especificado', resultado)
    
    return resultado


def buscar_reducoes_ncm(codigo):
    """
    Busca especificamente as reduções para um NCM.
    Retorna uma lista de reduções encontradas.
    """
    conn = conectar()
    cur = conn.cursor()
    
    # Consulta especializada para encontrar reduções
    cur.execute("""
        SELECT 
            n.NCM_CD,
            ct.CLTR_CD,
            ct.CLTR_DESCRICAO,
            t.TBTO_SIGLA,
            t.TBTO_NOME,
            ar.ALRE_VALOR as ALIQUOTA,
            pr.PERE_VALOR as REDUCAO,
            pr.PERE_INICIO_VIGENCIA as REDUCAO_INICIO,
            pr.PERE_FIM_VIGENCIA as REDUCAO_FIM,
            ar.ALRE_INICIO_VIGENCIA as ALIQUOTA_INICIO,
            ar.ALRE_FIM_VIGENCIA as ALIQUOTA_FIM
        FROM NCM n
        JOIN NCM_APLICAVEL na ON n.NCM_CD = na.NCMA_NCM_CD
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID
        LEFT JOIN TRIBUTO t ON pr.PERE_TBTO_ID = t.TBTO_ID
        LEFT JOIN ALIQUOTA_REFERENCIA ar ON t.TBTO_ID = ar.ALRE_TBTO_ID
        WHERE n.NCM_CD = ?
          AND pr.PERE_VALOR IS NOT NULL
          AND pr.PERE_VALOR > 0
        ORDER BY ct.CLTR_CD, t.TBTO_SIGLA
    """, (codigo,))
    
    resultados = cur.fetchall()
    conn.close()
    
    return resultados


def obter_relacoes_tabelas_ncm(codigo):
    """
    Retorna informações sobre as tabelas e relações envolvidas na consulta de um NCM.
    
    Args:
        codigo: Código do NCM
        
    Returns:
        Lista de dicionários com informações das tabelas relacionadas
    """
    conn = conectar()
    cur = conn.cursor()
    
    # Consulta para obter informações sobre as tabelas relacionadas
    cur.execute("""
        SELECT DISTINCT
            'NCM' as tabela,
            n.NCM_CD as codigo,
            n.NCM_DESCRICAO as descricao,
            'Tabela principal' as tipo_relacao
        FROM NCM n
        WHERE n.NCM_CD = ?
        
        UNION ALL
        
        SELECT DISTINCT
            'NCM_APLICAVEL' as tabela,
            na.NCMA_ID as codigo,
            'Regra de aplicação NCM' as descricao,
            'Relação NCM -> Classificação Tributária' as tipo_relacao
        FROM NCM_APLICAVEL na
        WHERE na.NCMA_NCM_CD = ?
        
        UNION ALL
        
        SELECT DISTINCT
            'CLASSIFICACAO_TRIBUTARIA' as tabela,
            ct.CLTR_CD as codigo,
            ct.CLTR_DESCRICAO as descricao,
            'Classificação tributária aplicável' as tipo_relacao
        FROM NCM_APLICAVEL na
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        WHERE na.NCMA_NCM_CD = ?
        
        UNION ALL
        
        SELECT DISTINCT
            'SITUACAO_TRIBUTARIA' as tabela,
            st.SITR_CD as codigo,
            st.SITR_DESCRICAO as descricao,
            'Situação tributária (CST)' as tipo_relacao
        FROM NCM_APLICAVEL na
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        LEFT JOIN SITUACAO_TRIBUTARIA st ON ct.CLTR_SITR_ID = st.SITR_ID
        WHERE na.NCMA_NCM_CD = ? AND st.SITR_CD IS NOT NULL
        
        UNION ALL
        
        SELECT DISTINCT
            'ANEXO' as tabela,
            a.ANXO_NUMERO as codigo,
            a.ANXO_TEXTO_ITEM as descricao,
            'Anexo da legislação' as tipo_relacao
        FROM NCM_APLICAVEL na
        LEFT JOIN ANEXO a ON na.NCMA_ANXO_ID = a.ANXO_ID
        WHERE na.NCMA_NCM_CD = ? AND a.ANXO_NUMERO IS NOT NULL
        
        UNION ALL
        
        SELECT DISTINCT
            'TRIBUTO' as tabela,
            t.TBTO_SIGLA as codigo,
            t.TBTO_NOME as descricao,
            'Tributo aplicável' as tipo_relacao
        FROM NCM_APLICAVEL na
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        LEFT JOIN SITUACAO_TRIBUTARIA st ON ct.CLTR_SITR_ID = st.SITR_ID
        LEFT JOIN TRIBUTO_SITUACAO_TRIBUTARIA tst ON st.SITR_ID = tst.TRST_SITR_ID
        LEFT JOIN TRIBUTO t ON tst.TRST_TBTO_ID = t.TBTO_ID
        WHERE na.NCMA_NCM_CD = ? AND t.TBTO_SIGLA IS NOT NULL
        
        UNION ALL
        
        SELECT DISTINCT
            'ALIQUOTA_REFERENCIA' as tabela,
            'ALRE' as codigo,
            'Alíquotas de referência' as descricao,
            'Alíquotas aplicáveis' as tipo_relacao
        FROM NCM_APLICAVEL na
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        LEFT JOIN SITUACAO_TRIBUTARIA st ON ct.CLTR_SITR_ID = st.SITR_ID
        LEFT JOIN TRIBUTO_SITUACAO_TRIBUTARIA tst ON st.SITR_ID = tst.TRST_SITR_ID
        LEFT JOIN TRIBUTO t ON tst.TRST_TBTO_ID = t.TBTO_ID
        LEFT JOIN ALIQUOTA_REFERENCIA ar ON t.TBTO_ID = ar.ALRE_TBTO_ID
        WHERE na.NCMA_NCM_CD = ? AND ar.ALRE_VALOR IS NOT NULL
        
        UNION ALL
        
        SELECT DISTINCT
            'PERCENTUAL_REDUCAO' as tabela,
            'REDUCAO' as codigo,
            'Percentuais de redução' as descricao,
            'Reduções tributárias' as tipo_relacao
        FROM NCM_APLICAVEL na
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        LEFT JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID
        WHERE na.NCMA_NCM_CD = ? AND pr.PERE_VALOR IS NOT NULL
        
        ORDER BY tabela, codigo
    """, (codigo, codigo, codigo, codigo, codigo, codigo, codigo, codigo))
    
    resultados = cur.fetchall()
    conn.close()
    
    # Converter para lista de dicionários
    relacoes = []
    for tabela, codigo_rel, descricao, tipo_relacao in resultados:
        relacoes.append({
            'tabela': tabela,
            'codigo': codigo_rel,
            'descricao': descricao[:100] + '...' if descricao and len(descricao) > 100 else descricao,
            'tipo_relacao': tipo_relacao
        })
    
    return relacoes


def buscar_cst_cclastrib_reducao_ncm(codigo):
    """
    Busca especificamente CST, CClasTrib e redução para um NCM.
    Retorna apenas os dados solicitados: NCM, CST, CClasTrib e redução.
    
    Args:
        codigo: Código do NCM
        
    Returns:
        Lista de tuplas com (NCM_CD, NCM_DESCRICAO, SITR_CD, SITR_DESCRICAO, 
                            CLTR_CD, CLTR_DESCRICAO, PERE_VALOR, TBTO_SIGLA, TBTO_NOME)
    """
    conn = conectar()
    cur = conn.cursor()
    
    # Consulta otimizada para buscar apenas CST, CClasTrib e redução
    cur.execute("""
        SELECT DISTINCT
            n.NCM_CD,
            n.NCM_DESCRICAO,
            st.SITR_CD,
            st.SITR_DESCRICAO,
            ct.CLTR_CD,
            ct.CLTR_DESCRICAO,
            pr.PERE_VALOR,
            t.TBTO_SIGLA,
            t.TBTO_NOME
        FROM NCM n
        JOIN NCM_APLICAVEL na ON n.NCM_CD = na.NCMA_NCM_CD
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        LEFT JOIN SITUACAO_TRIBUTARIA st ON ct.CLTR_SITR_ID = st.SITR_ID
        LEFT JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID
        LEFT JOIN TRIBUTO t ON pr.PERE_TBTO_ID = t.TBTO_ID
        WHERE n.NCM_CD = ?
        ORDER BY 
            ct.CLTR_CD,
            t.TBTO_SIGLA,
            pr.PERE_VALOR DESC NULLS LAST
    """, (codigo,))
    
    resultados = cur.fetchall()
    conn.close()
    
    return resultados


def testar_conexao():
    """Testa a conexão com o banco de dados."""
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM NCM")
        count = cur.fetchone()[0]
        conn.close()
        return True, f"Conexão bem-sucedida. {count} NCMs encontrados."
    except Exception as e:
        return False, f"Erro na conexão: {str(e)}"
