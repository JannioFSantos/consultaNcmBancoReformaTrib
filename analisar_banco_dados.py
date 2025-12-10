"""
Script para analisar todos os dados do banco de dados calculadora.db
"""
import sqlite3
import pandas as pd
from tabulate import tabulate

def analisar_estrutura_banco():
    """Analisa a estrutura completa do banco de dados."""
    conn = sqlite3.connect('calculadora.db')
    cursor = conn.cursor()
    
    print("🔍 ANÁLISE COMPLETA DO BANCO DE DADOS CALCULADORA.DB")
    print("=" * 100)
    
    # 1. Listar todas as tabelas
    print("\n📊 1. TABELAS DO BANCO DE DADOS:")
    print("-" * 50)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelas = cursor.fetchall()
    
    tabelas_info = []
    for tabela in tabelas:
        nome_tabela = tabela[0]
        
        # Contar registros
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
            count = cursor.fetchone()[0]
        except:
            count = 0
        
        # Obter colunas
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = cursor.fetchall()
        num_colunas = len(colunas)
        
        tabelas_info.append({
            'Tabela': nome_tabela,
            'Registros': count,
            'Colunas': num_colunas
        })
    
    # Exibir tabelas
    print(tabulate(tabelas_info, headers="keys", tablefmt="grid"))
    
    # 2. Analisar cada tabela em detalhe
    print("\n📋 2. ESTRUTURA DETALHADA DAS TABELAS:")
    print("=" * 100)
    
    for tabela_info in tabelas_info:
        nome_tabela = tabela_info['Tabela']
        
        print(f"\n📄 TABELA: {nome_tabela} ({tabela_info['Registros']} registros)")
        print("-" * 80)
        
        # Obter informações das colunas
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = cursor.fetchall()
        
        colunas_info = []
        for coluna in colunas:
            col_id, nome, tipo, not_null, default_val, pk = coluna
            colunas_info.append({
                'ID': col_id,
                'Nome': nome,
                'Tipo': tipo,
                'PK': '✓' if pk else '',
                'Not Null': '✓' if not_null else '',
                'Default': default_val if default_val else ''
            })
        
        print(tabulate(colunas_info, headers="keys", tablefmt="grid"))
        
        # Mostrar algumas linhas de exemplo
        if tabela_info['Registros'] > 0:
            print(f"\n📝 EXEMPLOS DE DADOS (primeiras 3 linhas):")
            try:
                cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3")
                exemplos = cursor.fetchall()
                
                # Obter nomes das colunas
                cursor.execute(f"PRAGMA table_info({nome_tabela})")
                nomes_colunas = [col[1] for col in cursor.fetchall()]
                
                exemplos_df = pd.DataFrame(exemplos, columns=nomes_colunas)
                print(tabulate(exemplos_df, headers="keys", tablefmt="grid", showindex=False))
            except Exception as e:
                print(f"  Erro ao ler dados: {e}")
    
    # 3. Analisar relações entre tabelas (chaves estrangeiras)
    print("\n🔗 3. RELAÇÕES ENTRE TABELAS (CHAVES ESTRANGEIRAS):")
    print("=" * 100)
    
    for tabela_info in tabelas_info:
        nome_tabela = tabela_info['Tabela']
        
        cursor.execute(f"PRAGMA foreign_key_list({nome_tabela})")
        fks = cursor.fetchall()
        
        if fks:
            print(f"\n🔗 Chaves estrangeiras na tabela {nome_tabela}:")
            fks_info = []
            for fk in fks:
                fks_info.append({
                    'De': fk[3],  # Coluna na tabela atual
                    'Para Tabela': fk[2],  # Tabela referenciada
                    'Para Coluna': fk[4],  # Coluna referenciada
                    'Ação Update': fk[5],
                    'Ação Delete': fk[6]
                })
            
            print(tabulate(fks_info, headers="keys", tablefmt="grid"))
    
    # 4. Análise específica para entender as reduções
    print("\n💰 4. ANÁLISE ESPECÍFICA DAS REDUÇÕES:")
    print("=" * 100)
    
    # Verificar tabela PERCENTUAL_REDUCAO
    print("\n📊 TABELA PERCENTUAL_REDUCAO:")
    print("-" * 50)
    
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(DISTINCT PERE_CLTR_ID) as classificacoes_distintas,
                COUNT(DISTINCT PERE_TBTO_ID) as tributos_distintos,
                MIN(PERE_VALOR) as reducao_minima,
                MAX(PERE_VALOR) as reducao_maxima,
                AVG(PERE_VALOR) as reducao_media
            FROM PERCENTUAL_REDUCAO
            WHERE PERE_VALOR > 0
        """)
        
        stats = cursor.fetchone()
        print(f"  Total de reduções: {stats[0]}")
        print(f"  Classificações distintas: {stats[1]}")
        print(f"  Tributos distintos: {stats[2]}")
        print(f"  Redução mínima: {stats[3]}")
        print(f"  Redução máxima: {stats[4]}")
        print(f"  Redução média: {stats[5]:.2f}")
        
        # Verificar valores específicos
        print(f"\n  📈 DISTRIBUIÇÃO DOS VALORES DE REDUÇÃO:")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN PERE_VALOR >= 10000 THEN 'Isenção total (≥10000)'
                    WHEN PERE_VALOR >= 100 THEN 'Redução alta (100-9999)'
                    WHEN PERE_VALOR >= 50 THEN 'Redução média (50-99)'
                    WHEN PERE_VALOR > 0 THEN 'Redução baixa (1-49)'
                    ELSE 'Sem redução'
                END as faixa,
                COUNT(*) as quantidade,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM PERCENTUAL_REDUCAO WHERE PERE_VALOR > 0), 2) as percentual
            FROM PERCENTUAL_REDUCAO
            WHERE PERE_VALOR > 0
            GROUP BY faixa
            ORDER BY quantidade DESC
        """)
        
        distribuicao = cursor.fetchall()
        for faixa, qtd, perc in distribuicao:
            print(f"    {faixa}: {qtd} registros ({perc}%)")
        
        # Exemplos de reduções
        print(f"\n  📝 EXEMPLOS DE REDUÇÕES:")
        cursor.execute("""
            SELECT 
                pr.PERE_ID,
                pr.PERE_VALOR,
                pr.PERE_INICIO_VIGENCIA,
                pr.PERE_FIM_VIGENCIA,
                ct.CLTR_CD,
                t.TBTO_SIGLA
            FROM PERCENTUAL_REDUCAO pr
            LEFT JOIN CLASSIFICACAO_TRIBUTARIA ct ON pr.PERE_CLTR_ID = ct.CLTR_ID
            LEFT JOIN TRIBUTO t ON pr.PERE_TBTO_ID = t.TBTO_ID
            WHERE pr.PERE_VALOR > 0
            ORDER BY pr.PERE_VALOR DESC
            LIMIT 5
        """)
        
        exemplos = cursor.fetchall()
        for exemplo in exemplos:
            print(f"    ID: {exemplo[0]}, Redução: {exemplo[1]}%, Classificação: {exemplo[4]}, Tributo: {exemplo[5]}")
            print(f"      Vigência: {exemplo[2]} até {exemplo[3] if exemplo[3] else 'atual'}")
            
    except Exception as e:
        print(f"  Erro ao analisar tabela PERCENTUAL_REDUCAO: {e}")
    
    # 5. Verificar NCMs com reduções
    print("\n📦 5. NCMs COM REDUÇÕES:")
    print("-" * 50)
    
    try:
        cursor.execute("""
            SELECT 
                n.NCM_CD,
                n.NCM_DESCRICAO,
                COUNT(DISTINCT pr.PERE_ID) as total_reducoes,
                GROUP_CONCAT(DISTINCT t.TBTO_SIGLA) as tributos
            FROM NCM n
            JOIN NCM_APLICAVEL na ON n.NCM_CD = na.NCMA_NCM_CD
            JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
            JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID
            LEFT JOIN TRIBUTO t ON pr.PERE_TBTO_ID = t.TBTO_ID
            WHERE pr.PERE_VALOR > 0
            GROUP BY n.NCM_CD
            ORDER BY total_reducoes DESC
            LIMIT 10
        """)
        
        ncms_com_reducoes = cursor.fetchall()
        
        if ncms_com_reducoes:
            print(f"  Top 10 NCMs com mais reduções:")
            for ncm in ncms_com_reducoes:
                print(f"    NCM: {ncm[0]} - {ncm[1][:50]}...")
                print(f"      Reduções: {ncm[2]}, Tributos: {ncm[3]}")
        else:
            print(f"  Nenhum NCM encontrado com reduções usando JOIN direto.")
            
            # Tentar método alternativo
            print(f"\n  🔍 Tentando método alternativo de busca...")
            cursor.execute("""
                SELECT DISTINCT n.NCM_CD, n.NCM_DESCRICAO
                FROM NCM n
                WHERE EXISTS (
                    SELECT 1 FROM NCM_APLICAVEL na
                    JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
                    JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID
                    WHERE na.NCMA_NCM_CD = n.NCM_CD
                    AND pr.PERE_VALOR > 0
                )
                LIMIT 10
            """)
            
            ncms_alternativo = cursor.fetchall()
            if ncms_alternativo:
                print(f"  NCMs encontrados com método alternativo:")
                for ncm in ncms_alternativo:
                    print(f"    NCM: {ncm[0]} - {ncm[1][:50]}...")
            else:
                print(f"  Nenhum NCM encontrado com nenhum método.")
                
    except Exception as e:
        print(f"  Erro ao buscar NCMs com reduções: {e}")
    
    # 6. Verificar a consulta que deveria funcionar
    print("\n🔍 6. TESTE DA CONSULTA QUE DEVERIA RETORNAR REDUÇÕES:")
    print("-" * 50)
    
    ncm_teste = '100620'  # Arroz - sabemos que tem reduções
    
    print(f"  Testando NCM: {ncm_teste}")
    
    # Consulta simplificada que DEVERIA funcionar
    consulta = """
        SELECT 
            n.NCM_CD,
            ct.CLTR_CD,
            t.TBTO_SIGLA,
            pr.PERE_VALOR,
            pr.PERE_INICIO_VIGENCIA,
            pr.PERE_FIM_VIGENCIA
        FROM NCM n
        JOIN NCM_APLICAVEL na ON n.NCM_CD = na.NCMA_NCM_CD
        JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
        JOIN PERCENTUAL_REDUCAO pr ON ct.CLTR_ID = pr.PERE_CLTR_ID
        LEFT JOIN TRIBUTO t ON pr.PERE_TBTO_ID = t.TBTO_ID
        WHERE n.NCM_CD = ?
          AND pr.PERE_VALOR > 0
    """
    
    cursor.execute(consulta, (ncm_teste,))
    resultados = cursor.fetchall()
    
    if resultados:
        print(f"  ✅ CONSULTA SIMPLIFICADA FUNCIONOU!")
        print(f"  Total de reduções encontradas: {len(resultados)}")
        for i, resultado in enumerate(resultados[:3]):
            print(f"    {i+1}. Classificação: {resultado[1]}, Tributo: {resultado[2]}, Redução: {resultado[3]}%")
    else:
        print(f"  ❌ CONSULTA SIMPLIFICADA NÃO RETORNOU RESULTADOS")
        
        # Verificar se o NCM existe
        cursor.execute("SELECT NCM_CD, NCM_DESCRICAO FROM NCM WHERE NCM_CD = ?", (ncm_teste,))
        ncm_info = cursor.fetchone()
        
        if ncm_info:
            print(f"  NCM existe: {ncm_info[0]} - {ncm_info[1]}")
            
            # Verificar se tem NCM_APLICAVEL
            cursor.execute("SELECT COUNT(*) FROM NCM_APLICAVEL WHERE NCMA_NCM_CD = ?", (ncm_teste,))
            count_ncm_aplicavel = cursor.fetchone()[0]
            print(f"  Registros em NCM_APLICAVEL: {count_ncm_aplicavel}")
            
            # Verificar as classificações vinculadas
            cursor.execute("""
                SELECT DISTINCT ct.CLTR_CD, ct.CLTR_DESCRICAO
                FROM NCM_APLICAVEL na
                JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
                WHERE na.NCMA_NCM_CD = ?
            """, (ncm_teste,))
            
            classificacoes = cursor.fetchall()
            print(f"  Classificações vinculadas: {len(classificacoes)}")
            for cltr in classificacoes:
                print(f"    - {cltr[0]}: {cltr[1][:50]}...")
                
                # Verificar se esta classificação tem reduções
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM PERCENTUAL_REDUCAO 
                    WHERE PERE_CLTR_ID = (
                        SELECT CLTR_ID FROM CLASSIFICACAO_TRIBUTARIA WHERE CLTR_CD = ?
                    ) AND PERE_VALOR > 0
                """, (cltr[0],))
                
                count_reducoes = cursor.fetchone()[0]
                print(f"      Reduções para esta classificação: {count_reducoes}")
        else:
            print(f"  NCM {ncm_teste} não encontrado na tabela NCM")
    
    conn.close()
    
    print("\n" + "=" * 100)
    print("✅ ANÁLISE DO BANCO DE DADOS CONCLUÍDA")

if __name__ == "__main__":
    analisar_estrutura_banco()
