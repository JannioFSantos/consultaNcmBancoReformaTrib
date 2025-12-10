import sqlite3

def explorar_banco():
    conn = sqlite3.connect('calculadora.db')
    cursor = conn.cursor()
    
    # Listar todas as tabelas
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name')
    tables = cursor.fetchall()
    
    print("Tabelas no banco de dados:")
    for table in tables:
        table_name = table[0]
        print(f"\n=== TABELA: {table_name} ===")
        
        # Obter informações das colunas
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = cursor.fetchall()
        
        print(f"Colunas ({len(columns)}):")
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            print(f"  - {col_name} ({col_type}) {'PK' if pk else ''} {'NOT NULL' if not_null else ''}")
        
        # Contar registros
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            count = cursor.fetchone()[0]
            print(f"Total de registros: {count}")
            
            # Mostrar algumas linhas de exemplo para tabelas importantes
            if table_name in ['NCM', 'CLASSIFICACAO_TRIBUTARIA', 'SITUACAO_TRIBUTARIA', 'PERCENTUAL_REDUCAO']:
                cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
                rows = cursor.fetchall()
                if rows:
                    print(f"Exemplo de registros (primeiros 3):")
                    for row in rows:
                        print(f"  {row}")
        except Exception as e:
            print(f"Erro ao consultar tabela: {e}")
    
    # Explorar relações específicas
    print("\n\n=== EXPLORAÇÃO ESPECÍFICA ===")
    
    # Verificar se temos CST (Código de Situação Tributária)
    print("\n1. CST (Código de Situação Tributária):")
    try:
        cursor.execute("SELECT * FROM SITUACAO_TRIBUTARIA LIMIT 5")
        csts = cursor.fetchall()
        if csts:
            print("Primeiros 5 CSTs:")
            for cst in csts:
                print(f"  {cst}")
        else:
            print("Tabela SITUACAO_TRIBUTARIA vazia ou não existe")
    except Exception as e:
        print(f"Erro ao consultar CST: {e}")
    
    # Verificar CClasTrib (Classificação Tributária)
    print("\n2. CClasTrib (Classificação Tributária):")
    try:
        cursor.execute("SELECT CLTR_CD, CLTR_DESCRICAO FROM CLASSIFICACAO_TRIBUTARIA LIMIT 5")
        clastribs = cursor.fetchall()
        if clastribs:
            print("Primeiras 5 classificações tributárias:")
            for cl in clastribs:
                print(f"  Código: {cl[0]}, Descrição: {cl[1]}")
        else:
            print("Tabela CLASSIFICACAO_TRIBUTARIA vazia ou não existe")
    except Exception as e:
        print(f"Erro ao consultar Classificação Tributária: {e}")
    
    # Verificar Reduções
    print("\n3. Reduções (PERCENTUAL_REDUCAO):")
    try:
        cursor.execute("SELECT * FROM PERCENTUAL_REDUCAO LIMIT 5")
        reducoes = cursor.fetchall()
        if reducoes:
            print("Primeiras 5 reduções:")
            for red in reducoes:
                print(f"  {red}")
        else:
            print("Tabela PERCENTUAL_REDUCAO vazia ou não existe")
    except Exception as e:
        print(f"Erro ao consultar Reduções: {e}")
    
    # Verificar relação entre NCM e Classificação Tributária
    print("\n4. Relação NCM -> Classificação Tributária:")
    try:
        cursor.execute("""
            SELECT n.NCM_CD, n.NCM_DESCRICAO, ct.CLTR_CD, ct.CLTR_DESCRICAO
            FROM NCM n
            JOIN NCM_APLICAVEL na ON n.NCM_CD = na.NCMA_NCM_CD
            JOIN CLASSIFICACAO_TRIBUTARIA ct ON na.NCMA_CLTR_ID = ct.CLTR_ID
            LIMIT 5
        """)
        relacoes = cursor.fetchall()
        if relacoes:
            print("Primeiras 5 relações NCM -> Classificação Tributária:")
            for rel in relacoes:
                print(f"  NCM: {rel[0]} ({rel[1][:30]}...) -> CClasTrib: {rel[2]} ({rel[3][:30]}...)")
        else:
            print("Nenhuma relação encontrada")
    except Exception as e:
        print(f"Erro ao consultar relações: {e}")
    
    conn.close()

if __name__ == "__main__":
    explorar_banco()
