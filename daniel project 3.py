import csv
import random
import math
import sys

#no export

# ==== CONFIGURAÇÕES DE GRUPOS ====
GRUPOS = {
    "TAMANHO E COR": [11, 12, 13],
    "TIPO DE NINHO": [14, 15, 16, 17],
    "2 PONTOS": [19, 20, 21, 22],
    "GEOGRAFIA": [23, 24],
    "HABITATS": [5, 6, 7]
}

# ==== CARACTERÍSTICAS INDIVIDUAIS (fora dos grupos) ====
CARACTERISTICAS_INDIVIDUAIS = [8, 9, 10, 18, 25, 26, 27, 28, 29, 30]

# ==== CONFIGURAÇÃO SIMULATED ANNEALING ====
SA_ITERATIONS = 50000  
SA_T_INITIAL = 1.0
SA_T_COOLING_RATE = 0.9999


# ==== LEITURA DO CSV ====
def carregar_csv(caminho_csv):
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        dados = list(reader)
    header = dados[0]
    linhas = dados[1:]
    return header, linhas


# ==== FUNÇÕES AUXILIARES ====
def contar_proporcao(linhas, col_id):
    total = len(linhas)
    if total == 0:
        return 0.0
    com_x = sum(1 for linha in linhas if linha[col_id - 1].strip().upper() == "X")
    return (com_x / total) * 100


def solicitar_proporcoes_alvo_grupos():
    proporcoes_grupos_input = {}
    print("\n--- Definição de PROPORÇÃO ALVO (%) por Grupo ---")
    for nome_grupo in sorted(GRUPOS.keys()):
        while True:
            try:
                prop = float(input(f"Proporção ALVO (%) para o GRUPO '{nome_grupo.upper()}' (IDs: {GRUPOS[nome_grupo]}): ").strip())
                if prop < 0 or prop > 100:
                    print("❌ A proporção deve ser entre 0 e 100.")
                    continue
                proporcoes_grupos_input[nome_grupo] = prop
                break
            except ValueError:
                print("⚠️ Entrada inválida. Use números decimais com ponto (ex: 20.5).")
    return proporcoes_grupos_input


def solicitar_tolerancia():
    while True:
        try:
            tolerancia = float(input("\nQual tolerância desejada (em %)? "))
            if tolerancia < 0:
                print("❌ A tolerância deve ser positiva.")
                continue
            return tolerancia
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número.")


def perguntar_modo_saida():
    while True:
        modo = input("\nDeseja ver o resultado como:\n1. Baralho completo\n2. Apenas aves adicionadas além das obrigatórias\nEscolha 1 ou 2: ").strip()
        if modo in ["1", "2"]:
            return modo
        print("⚠️ Opção inválida. Digite 1 ou 2.")


# ==== FUNÇÃO DE ENERGIA ====
def calcular_energia(baralho, proporcoes_alvo_caracteristica, total_aves):
    if len(baralho) != total_aves:
        return float('inf')
    energia_grupos = 0.0
    for col_id, desejada in proporcoes_alvo_caracteristica.items():
        prop_obtida = contar_proporcao(baralho, col_id)
        energia_grupos += abs(prop_obtida - desejada)
    for col_id in CARACTERISTICAS_INDIVIDUAIS:
        prop_obtida = contar_proporcao(baralho, col_id)
        if prop_obtida <= 0.0:
            return float('inf')
    return energia_grupos


# ==== INICIALIZAÇÃO ====
def inicializar_baralho(linhas, total_aves, proporcoes_alvo_caracteristica, must_include):
    baralho_set = set(tuple(l) for l in must_include)

    # garante presença de características individuais
    for col_id in CARACTERISTICAS_INDIVIDUAIS:
        candidatos = [linha for linha in linhas if linha[col_id - 1].strip().upper() == "X" and tuple(linha) not in baralho_set]
        if candidatos:
            baralho_set.add(tuple(random.choice(candidatos)))

    # completa o baralho até o tamanho total
    linhas_restantes = [linha for linha in linhas if tuple(linha) not in baralho_set]
    aves_faltando = total_aves - len(baralho_set)
    proporcoes_ordenadas = sorted(proporcoes_alvo_caracteristica.items(), key=lambda x: x[1], reverse=True)

    adicoes = 0
    while adicoes < aves_faltando and linhas_restantes:
        feature_prioritaria = proporcoes_ordenadas[0][0]
        candidatos_prioritarios = [linha for linha in linhas_restantes if linha[feature_prioritaria - 1].strip().upper() == "X"]
        if candidatos_prioritarios:
            escolhido = random.choice(candidatos_prioritarios)
        else:
            escolhido = random.choice(linhas_restantes)
        baralho_set.add(tuple(escolhido))
        linhas_restantes.remove(escolhido)
        adicoes += 1

    baralho = [list(x) for x in baralho_set]
    random.shuffle(baralho)
    return baralho if len(baralho) == total_aves else None


# ==== GERAR VIZINHO ====
def gerar_vizinho(baralho, todas_linhas_tuple, must_include_set):
    baralho_tuple = {tuple(l) for l in baralho}
    aves_incluidas = [l for l in baralho_tuple if l not in must_include_set]
    aves_nao_incluidas = [l for l in todas_linhas_tuple if l not in baralho_tuple and l not in must_include_set]

    if not aves_incluidas or not aves_nao_incluidas:
        return None

    removida = random.choice(aves_incluidas)
    adicionada = random.choice(aves_nao_incluidas)

    novo_baralho = list((baralho_tuple - {removida}) | {adicionada} | must_include_set)
    return [list(l) for l in novo_baralho]


# ==== VERIFICAÇÃO FINAL ====
def verificar_resultado_final(baralho_final, proporcoes_alvo_caracteristica, tolerancia):
    sucesso_grupos = True
    for ids in GRUPOS.values():
        for col_id in ids:
            desejada = proporcoes_alvo_caracteristica.get(col_id, 0.0)
            prop_obtida = contar_proporcao(baralho_final, col_id)
            if abs(prop_obtida - desejada) > tolerancia:
                sucesso_grupos = False
                break
        if not sucesso_grupos:
            break

    todas_presentes = True
    for col_id in CARACTERISTICAS_INDIVIDUAIS:
        prop_obtida = contar_proporcao(baralho_final, col_id)
        if prop_obtida <= 0.0:
            todas_presentes = False
            break
    return sucesso_grupos and todas_presentes


# ==== EXIBIÇÃO ====
def exibir_resultados(baralho_final, linhas_totais, proporcoes_grupos_input, proporcoes_alvo_caracteristica, tolerancia, modo_saida, must_include):
    print(f"\n✅ Baralho final gerado com {len(baralho_final)} aves!")
    baralho_final_set = {tuple(l) for l in baralho_final}
    must_include_set = {tuple(l) for l in must_include}

    if modo_saida == "1":
        print("\n🕊️ Pássaros incluídos:")
        for linha in baralho_final:
            print(f" - {linha[0]}")
    else:
        print("\n🪶 Pássaros adicionados além dos obrigatórios:")
        adicionais = [linha for linha in baralho_final if tuple(linha) not in must_include_set]
        for linha in adicionais:
            print(f" - {linha[0]}")

    print("\n--- RESULTADOS DE PROPORÇÕES ---")
    for nome, ids in GRUPOS.items():
        prop_grupo_alvo = proporcoes_grupos_input.get(nome, 0.0)
        print(f"\nGRUPO '{nome.upper()}' (Alvo por Feature: {prop_grupo_alvo:.2f}%):")
        for col_id in ids:
            desejada = proporcoes_alvo_caracteristica.get(col_id, 0.0)
            prop_obtida = contar_proporcao(baralho_final, col_id)
            status_check = "✅ OK" if abs(prop_obtida - desejada) <= tolerancia else "❌ FORA"
            print(f"  - {col_id}: {prop_obtida:.1f}% (alvo {desejada:.1f}%) {status_check}")


# ==== GERAÇÃO DO BARALHO ====
def gerar_baralho(header, linhas, must_include, total_aves):
    tolerancia = solicitar_tolerancia()
    modo_saida = perguntar_modo_saida()
    proporcoes_grupos_input = solicitar_proporcoes_alvo_grupos()
    proporcoes_alvo_caracteristica = {col_id: prop for nome, prop in proporcoes_grupos_input.items() for col_id in GRUPOS[nome]}

    todas_linhas_tuple = [tuple(l) for l in linhas]
    must_include_set = {tuple(l) for l in must_include}

    baralho_atual = inicializar_baralho(linhas, total_aves, proporcoes_alvo_caracteristica, must_include)
    if baralho_atual is None:
        print("❌ Não foi possível inicializar o baralho.")
        return

    energia_atual = calcular_energia(baralho_atual, proporcoes_alvo_caracteristica, total_aves)
    melhor_baralho = list(baralho_atual)
    melhor_energia = energia_atual
    T = SA_T_INITIAL

    for i in range(SA_ITERATIONS):
        vizinho = gerar_vizinho(baralho_atual, todas_linhas_tuple, must_include_set)
        if vizinho is None:
            continue
        energia_vizinho = calcular_energia(vizinho, proporcoes_alvo_caracteristica, total_aves)
        if energia_vizinho < energia_atual or random.random() < math.exp(-(energia_vizinho - energia_atual) / T):
            baralho_atual = vizinho
            energia_atual = energia_vizinho
        if energia_atual < melhor_energia:
            melhor_energia = energia_atual
            melhor_baralho = list(baralho_atual)
            if verificar_resultado_final(melhor_baralho, proporcoes_alvo_caracteristica, tolerancia):
                print(f"\n🎉 Baralho ideal encontrado após {i+1} iterações.")
                return exibir_resultados(melhor_baralho, linhas, proporcoes_grupos_input, proporcoes_alvo_caracteristica, tolerancia, modo_saida, must_include)
        T *= SA_T_COOLING_RATE

    print("\n⚠️ Nenhum baralho perfeito foi encontrado.")
    exibir_resultados(melhor_baralho, linhas, proporcoes_grupos_input, proporcoes_alvo_caracteristica, tolerancia, modo_saida, must_include)


# ==== EXECUÇÃO ====
if __name__ == "__main__":
    print("\n===== 🕊️ BEM-VINDO AO PROJETO DANIEL BIRDS 2.1 =====")
    caminho = input("\nDigite o caminho completo do arquivo CSV com todas as aves: ").strip()

    try:
        header, linhas = carregar_csv(caminho)
    except FileNotFoundError:
        print("❌ Arquivo não encontrado. Verifique o caminho e tente novamente.")
        exit()

    print("\nCole abaixo (direto do Excel) os nomes das aves obrigatórias (uma por linha):")
    print("(Quando terminar, pressione ENTER em branco e depois CTRL+D no Linux/macOS ou CTRL+Z no Windows)\n")
    aves_obrigatorias = sys.stdin.read().strip().splitlines()

    must_include = [l for l in linhas if l[0].strip().lower() in [a.strip().lower() for a in aves_obrigatorias]]

    total = int(input("\nQuantas aves o baralho deve ter no total? "))
    gerar_baralho(header, linhas, must_include, total)
