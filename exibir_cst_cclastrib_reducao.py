"""
Script para exibir CST, CClasTrib e redução por NCM.
Conforme solicitado pelo usuário: "pegar apenas cst, cclasstrib e redução do banco de dados, pelo ncm, apenas isso, e exibir na tela"
"""

import database

def formatar_reducao(valor):
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

def exibir_cst_cclastrib_reducao(codigo_ncm):
    """
    Exibe CST, CClasTrib e redução para um NCM específico.
    
    Args:
        codigo_ncm: Código do NCM a ser consultado
    """
    print(f"\n{'='*80}")
    print(f"CONSULTA: CST, CClasTrib e Redução para NCM: {codigo_ncm}")
    print(f"{'='*80}")
    
    # Buscar os dados usando a nova função
    resultados = database.buscar_cst_cclastrib_reducao_ncm(codigo_ncm)
    
    if not resultados:
        print(f"Nenhum resultado encontrado para NCM: {codigo_ncm}")
        print("Verifique se o código NCM está correto.")
        return
    
    # Agrupar resultados por classificação tributária para melhor organização
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
            reducao_formatada = formatar_reducao(pere_valor)
            tributo_info = f"{tbto_sigla} ({tbto_nome})" if tbto_sigla else "Tributo não especificado"
            resultados_agrupados[chave]['reducoes'].append({
                'valor': pere_valor,
                'formatado': reducao_formatada,
                'tributo': tributo_info
            })
    
    # Exibir resultados agrupados
    for i, (chave, dados) in enumerate(resultados_agrupados.items(), 1):
        ncm_cd, sitr_cd, cltr_cd = chave
        
        print(f"\n{i}. NCM: {ncm_cd}")
        print(f"   Descrição: {dados['ncm_descricao'][:100]}..." if len(dados['ncm_descricao']) > 100 else f"   Descrição: {dados['ncm_descricao']}")
        print(f"   CST: {sitr_cd} - {dados['sitr_descricao']}")
        print(f"   CClasTrib: {cltr_cd} - {dados['cltr_descricao']}")
        
        if dados['reducoes']:
            print(f"   Reduções aplicáveis:")
            for reducao in dados['reducoes']:
                print(f"     • {reducao['tributo']}: {reducao['formatado']}")
        else:
            print(f"   Redução: Sem redução cadastrada")
    
    print(f"\n{'='*80}")
    print(f"Total de combinações encontradas: {len(resultados_agrupados)}")
    print(f"{'='*80}")

def menu_principal():
    """Menu principal para interação com o usuário."""
    while True:
        print("\n" + "="*60)
        print("CONSULTA DE CST, CClasTrib E REDUÇÃO POR NCM")
        print("="*60)
        print("1. Consultar por código NCM")
        print("2. Testar com exemplos pré-definidos")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            codigo = input("Digite o código NCM (ex: 100620, 04011010): ").strip()
            if codigo:
                exibir_cst_cclastrib_reducao(codigo)
            else:
                print("Código NCM não pode ser vazio.")
        
        elif opcao == "2":
            # Exemplos de NCMs para teste
            exemplos = ["100620", "04011010", "220710", "847130", "851712"]
            print("\nTestando com exemplos pré-definidos:")
            for exemplo in exemplos:
                exibir_cst_cclastrib_reducao(exemplo)
                input("\nPressione Enter para continuar...")
        
        elif opcao == "3":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    # Testar conexão com o banco de dados
    print("Testando conexão com o banco de dados...")
    sucesso, mensagem = database.testar_conexao()
    print(mensagem)
    
    if sucesso:
        menu_principal()
    else:
        print("Não foi possível conectar ao banco de dados. Verifique se o arquivo calculadora.db existe.")
