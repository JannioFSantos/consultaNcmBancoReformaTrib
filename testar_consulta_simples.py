"""
Teste simples da função de consulta de CST, CClasTrib e redução.
"""

import database

def testar_consulta():
    """Testa a consulta com alguns NCMs de exemplo."""
    exemplos = ["100620", "04011010", "220710", "847130", "851712"]
    
    for codigo in exemplos:
        print(f"\n{'='*80}")
        print(f"Testando NCM: {codigo}")
        print(f"{'='*80}")
        
        resultados = database.buscar_cst_cclastrib_reducao_ncm(codigo)
        
        if not resultados:
            print(f"Nenhum resultado para NCM: {codigo}")
            continue
        
        # Mostrar os primeiros resultados
        print(f"Total de registros encontrados: {len(resultados)}")
        print("\nPrimeiros 3 registros:")
        for i, resultado in enumerate(resultados[:3], 1):
            ncm_cd, ncm_desc, sitr_cd, sitr_desc, cltr_cd, cltr_desc, pere_valor, tbto_sigla, tbto_nome = resultado
            
            print(f"\n{i}. NCM: {ncm_cd}")
            print(f"   Descrição: {ncm_desc[:80]}..." if len(ncm_desc) > 80 else f"   Descrição: {ncm_desc}")
            print(f"   CST: {sitr_cd} - {sitr_desc}")
            print(f"   CClasTrib: {cltr_cd} - {cltr_desc}")
            
            if pere_valor is not None:
                # Formatar redução
                try:
                    if isinstance(pere_valor, (int, float)):
                        if pere_valor >= 10000:
                            reducao_fmt = "Isenção total (100%)"
                        elif pere_valor >= 100:
                            reducao_fmt = f"{pere_valor:.2f}% (fator especial)"
                        else:
                            reducao_fmt = f"{pere_valor:.2f}%"
                    else:
                        reducao_fmt = str(pere_valor)
                except:
                    reducao_fmt = str(pere_valor)
                
                tributo = f"{tbto_sigla} ({tbto_nome})" if tbto_sigla else "Tributo não especificado"
                print(f"   Redução: {reducao_fmt} para {tributo}")
            else:
                print(f"   Redução: Sem redução")
        
        # Resumo
        print(f"\nResumo para NCM {codigo}:")
        print(f"  - CSTs distintos: {len(set(r[2] for r in resultados))}")
        print(f"  - CClasTribs distintos: {len(set(r[4] for r in resultados))}")
        print(f"  - Reduções com valor > 0: {len([r for r in resultados if r[6] is not None and float(r[6]) > 0])}")
    
    print(f"\n{'='*80}")
    print("Teste concluído!")
    print(f"{'='*80}")

if __name__ == "__main__":
    # Testar conexão
    sucesso, mensagem = database.testar_conexao()
    print(mensagem)
    
    if sucesso:
        testar_consulta()
    else:
        print("Erro: Não foi possível conectar ao banco de dados.")
