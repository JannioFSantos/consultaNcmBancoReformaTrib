import database

def testar_ncm_com_reducao():
    """Testa a consulta de um NCM que sabemos ter reduções."""
    codigo_ncm = "29362290"  # cocarboxilase reduzid 60% - sabemos que tem reduções
    
    print(f"Testando NCM: {codigo_ncm}")
    print("=" * 60)
    
    # Buscar informações completas
    ncm, regras_completas = database.buscar_informacoes_completas_ncm(codigo_ncm)
    
    if not ncm:
        print("NCM não encontrado!")
        return
    
    codigo, desc, inicio, fim = ncm
    print(f"NCM: {codigo}")
    print(f"Descrição: {desc}")
    print(f"Vigência: {inicio} até {fim}")
    print()
    
    if not regras_completas:
        print("Nenhuma regra tributária encontrada!")
        return
    
    print(f"Total de registros retornados: {len(regras_completas)}")
    print()
    
    # Verificar se há informações de redução
    tem_reducoes = False
    for i, regra in enumerate(regras_completas[:5]):  # Analisar apenas as primeiras 5
        print(f"Regra {i+1}:")
        print(f"  NCMA_ID: {regra[4]}")
        print(f"  Tributo: {regra[21]} ({regra[22]})")
        print(f"  Alíquota: {regra[23]}")
        print(f"  Percentual Redução: {regra[28]}")
        print(f"  Início Redução: {regra[29]}")
        print(f"  Fim Redução: {regra[30]}")
        print()
        
        if regra[28] is not None:
            tem_reducoes = True
    
    if tem_reducoes:
        print("✓ REDUÇÕES ENCONTRADAS!")
    else:
        print("✗ Nenhuma redução encontrada nas primeiras regras.")
    
    # Testar outro NCM sem redução
    print("\n" + "=" * 60)
    print("Testando NCM sem redução (exemplo: 87032100)")
    print("=" * 60)
    
    codigo_ncm2 = "87032100"
    ncm2, regras2 = database.buscar_informacoes_completas_ncm(codigo_ncm2)
    
    if ncm2 and regras2:
        print(f"NCM: {ncm2[0]}")
        print(f"Descrição: {ncm2[1][:50]}...")
        
        # Verificar reduções
        tem_reducoes2 = False
        for regra in regras2[:3]:
            if regra[28] is not None and regra[28] > 0:
                tem_reducoes2 = True
                print(f"  Redução encontrada: {regra[28]}% para tributo {regra[21]}")
        
        if not tem_reducoes2:
            print("  Nenhuma redução encontrada (como esperado)")

if __name__ == "__main__":
    testar_ncm_com_reducao()
