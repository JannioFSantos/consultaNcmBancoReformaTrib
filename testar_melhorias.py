"""
Script para testar as melhorias implementadas no calculadora.py
"""
import database

def testar_descricoes_completas():
    """Testa se as descrições estão sendo retornadas completas."""
    print("=== Testando descrições completas ===")
    
    # Testar busca por NCM específico
    codigo = "100620"
    resultados = database.buscar_cst_cclastrib_reducao_ncm(codigo)
    
    if resultados:
        print(f"NCM {codigo} encontrado:")
        for resultado in resultados[:1]:  # Pegar apenas o primeiro para exemplo
            ncm_cd, ncm_desc, sitr_cd, sitr_desc, cltr_cd, cltr_desc, pere_valor, tbto_sigla, tbto_nome = resultado
            print(f"  Código: {ncm_cd}")
            print(f"  Descrição: {ncm_desc}")
            print(f"  Tamanho da descrição: {len(ncm_desc)} caracteres")
            
            # Verificar se a descrição não foi truncada
            if "..." in ncm_desc:
                print("  ⚠️  AVISO: Descrição contém '...' (pode estar truncada)")
            else:
                print("  ✅ Descrição completa (sem truncamento)")
    else:
        print(f"NCM {codigo} não encontrado")
    
    print()

def testar_busca_por_descricao():
    """Testa a busca de NCMs por descrição."""
    print("=== Testando busca por descrição ===")
    
    # Testar busca por termo comum
    termo = "trigo"
    resultados = database.buscar_por_descricao(termo)
    
    if resultados:
        print(f"Encontrados {len(resultados)} NCMs com '{termo}':")
        for ncm_cd, ncm_desc in resultados[:3]:  # Mostrar apenas 3 primeiros
            print(f"  {ncm_cd}: {ncm_desc[:60]}...")
    else:
        print(f"Nenhum NCM encontrado com '{termo}'")
    
    print()

def testar_listar_todos_ncms():
    """Testa a função de listar todos os NCMs."""
    print("=== Testando listagem de todos os NCMs ===")
    
    resultados = database.buscar_ncms()
    
    if resultados:
        print(f"Total de NCMs no banco: {len(resultados)}")
        
        # Mostrar alguns exemplos
        print("Primeiros 5 NCMs:")
        for ncm_cd, ncm_desc in resultados[:5]:
            print(f"  {ncm_cd}: {ncm_desc[:50]}...")
        
        # Verificar se há muitos resultados
        if len(resultados) > 100:
            print(f"⚠️  Muitos NCMs ({len(resultados)}). A interface limitará a 100.")
    else:
        print("Nenhum NCM encontrado no banco")
    
    print()

def testar_consultas_completas():
    """Testa as consultas completas de NCM."""
    print("=== Testando consultas completas ===")
    
    codigo = "30049099"
    dados_ncm, resultados = database.buscar_informacoes_completas_ncm(codigo)
    
    if dados_ncm:
        ncm_cd, ncm_desc, inicio_vig, fim_vig = dados_ncm
        print(f"NCM {codigo} encontrado:")
        print(f"  Descrição: {ncm_desc}")
        print(f"  Tamanho: {len(ncm_desc)} caracteres")
        
        if resultados:
            print(f"  {len(resultados)} regras tributárias encontradas")
            
            # Verificar memória de cálculo
            for resultado in resultados[:1]:  # Primeira regra
                memoria_calculo = resultado[9]  # CLTR_MEMORIA_CALCULO
                if memoria_calculo:
                    print(f"  Memória de cálculo: {memoria_calculo[:100]}...")
                    if "..." in memoria_calculo:
                        print("  ⚠️  AVISO: Memória de cálculo pode estar truncada")
                    else:
                        print("  ✅ Memória de cálculo completa")
        else:
            print("  Nenhuma regra tributária encontrada")
    else:
        print(f"NCM {codigo} não encontrado")
    
    print()

def main():
    """Função principal de teste."""
    print("🔍 TESTANDO MELHORIAS IMPLEMENTADAS NA CALCULADORA TRIBUTÁRIA")
    print("=" * 60)
    
    # Testar conexão com banco
    print("Testando conexão com banco de dados...")
    sucesso, mensagem = database.testar_conexao()
    if sucesso:
        print(f"✅ {mensagem}")
    else:
        print(f"❌ {mensagem}")
        return
    
    print()
    
    # Executar testes
    testar_descricoes_completas()
    testar_busca_por_descricao()
    testar_listar_todos_ncms()
    testar_consultas_completas()
    
    print("=" * 60)
    print("✅ Testes concluídos!")
    print("\nResumo das melhorias testadas:")
    print("1. Descrições completas (sem '...')")
    print("2. Busca de NCMs por descrição")
    print("3. Listagem de todos os NCMs")
    print("4. Consultas completas com todas as informações")

if __name__ == "__main__":
    main()
