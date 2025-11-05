import csv
import random
import math
import sys

# ==== CONFIGURAÇÕES GERAIS ====
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
def contar_proporcao(linhas, col_ids):
    total = len(linhas)
    if total == 0:
        return 0.0
    com_x = 0
    for linha in linhas:
        if any(linha[col - 1].strip().upper() == "X" for col in col_ids):
            com_x += 1
    return (com_x / total) * 100


def solicitar_grupos(header):
    grupos = {}
    print("\n--- Criação dos grupos de características ---")
    print("Digite os IDs das colunas que pertencem ao mesmo grupo, separados por vírgula.")
    print("Exemplo: 2,3,5")
    print("Deixe em branco e pressione ENTER quando terminar.\n")

    while True:
        nome = input("Nome do grupo (ou ENTER para finalizar): ").strip()
        if not nome:
            break
        ids = input(f"IDs das colunas que compõem '{nome}': ").strip()
        try:
            colunas = [int(x.strip()) for x in ids.split(",") if x.strip()]
            grupos[nome] = colunas
        except ValueError:
            print("⚠️ Entrada inválida. Tente novamente.")
    return grupos


def solicitar_proporcoes_alvo(grupos):
    proporcoes_alvo = {}
    print("\n--- Defina a proporção ALVO (%) para cada grupo ---")
    for nome in grupos:
        while True:
            try:
                prop = float(input(f"{nome}: "))
                if prop < 0 or prop > 100:
                    print("❌ A proporção deve estar entre 0 e 100.")
                    continue
                proporcoes_alvo[nome] = prop
                break
            except ValueError:
                print("⚠️ Entrada inválida. Digite um número.")
    return proporcoes_alvo


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


# ==== SIMULATED ANNEALING ====
def calcular_energia(baralho, grupos, proporcoes_alvo, total_aves):
    if len(baralho) != total_aves:
        return float('inf')
    energia = 0.0
    for nome, col_ids in grupos.items():
        desejada = proporcoes_alvo[nome]
        prop_obtida = contar_proporcao(baralho, col_ids)
        energia += abs(prop_obtida - desejada)
    return energia


def gerar_vizinho(baralho, todas_linhas_tuple):
    baralho_tuple = {tuple(l) for l in baralho}
    aves_incluidas = list(baralho_tuple)
    aves_nao_incluidas = [l for l in todas_linhas_tuple if l not in baralho_tuple]
    if not aves_incluidas or not aves_nao_incluidas:
        return None
    removida = random.choice(aves_incluidas)
    adicionada = random.choice(aves_nao_incluidas)
    novo_baralho = list(baralho_tuple - {removida} | {adicionada})
    return [list(l) for l in novo_baralho]


# ==== EXPORTAR CSV ====
def exportar_baralho_csv(header, baralho):
    nome_arquivo = "baralho_final.csv"
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(baralho)
    print(f"\n💾 Arquivo '{nome_arquivo}' gerado com sucesso!")


# ==== FUNÇÃO PRINCIPAL ====
def gerar_baralho(header, linhas, aves_obrigatorias, total_aves):
    print("\n⚙️ Configurando parâmetros...")
    grupos = solicitar_grupos(header)
    proporcoes_alvo = solicitar_proporcoes_alvo(grupos)
    tolerancia = solicitar_tolerancia()
    modo_saida = perguntar_modo_saida()

    must_include = [l for l in linhas if l[0].strip().lower() in [a.strip().lower() for a in aves_obrigatorias]]
    restantes = [l for l in linhas if l not in must_include]

    if len(must_include) > total_aves:
        print("❌ A lista obrigatória contém mais aves do que o limite do baralho.")
        return

    baralho_atual = list(must_include)
    while len(baralho_atual) < total_aves:
        baralho_atual.append(random.choice(restantes))

    todas_linhas_tuple = [tuple(l) for l in linhas]
    energia_atual = calcular_energia(baralho_atual, grupos, proporcoes_alvo, total_aves)
    melhor_baralho = list(baralho_atual)
    melhor_energia = energia_atual
    T = SA_T_INITIAL

    for i in range(SA_ITERATIONS):
        vizinho = gerar_vizinho(baralho_atual, todas_linhas_tuple)
        if vizinho is None:
            continue
        energia_vizinho = calcular_energia(vizinho, grupos, proporcoes_alvo, total_aves)
        if energia_vizinho < energia_atual or random.random() < math.exp(-(energia_vizinho - energia_atual) / T):
            baralho_atual = vizinho
            energia_atual = energia_vizinho
        if energia_atual < melhor_energia:
            melhor_energia = energia_atual
            melhor_baralho = list(baralho_atual)
        T *= SA_T_COOLING_RATE

    print(f"\n✅ Baralho final gerado com {len(melhor_baralho)} aves!")
    baralho_final_set = {tuple(l) for l in melhor_baralho}
    must_include_set = {tuple(l) for l in must_include}

    if modo_saida == "1":
        print("\n🕊️ Pássaros incluídos:")
        for linha in melhor_baralho:
            print(f" - {linha[0]}")
    else:
        print("\n🪶 Pássaros adicionados além dos obrigatórios:")
        adicionais = [linha for linha in melhor_baralho if tuple(linha) not in must_include_set]
        for linha in adicionais:
            print(f" - {linha[0]}")

    print("\n--- RESULTADOS DE PROPORÇÕES ---")
    for nome, col_ids in grupos.items():
        alvo = proporcoes_alvo[nome]
        obtida = contar_proporcao(melhor_baralho, col_ids)
        status = "✅ OK" if abs(obtida - alvo) <= tolerancia else "❌ FORA"
        print(f"  - {nome}: {obtida:.1f}% (alvo {alvo:.1f}%) {status}")

    # ==== Exportação opcional ====
    exportar = input("\nDeseja exportar o baralho final em CSV? (s/n): ").strip().lower()
    if exportar == "s":
        exportar_baralho_csv(header, melhor_baralho)


# ==== EXECUÇÃO ====
if __name__ == "__main__":
    print("\n===== 🕊️ BEM-VINDO AO PROJETO DANIEL BIRDS 3.0 =====")
    caminho = input("\nDigite o caminho completo do arquivo CSV com todas as aves: ").strip()
    try:
        header, linhas = carregar_csv(caminho)
    except FileNotFoundError:
        print("❌ Arquivo não encontrado. Verifique o caminho e tente novamente.")
        exit()

    print("\nCole abaixo (direto do Excel) os nomes das aves obrigatórias (uma por linha):")
    print("(Quando terminar, pressione ENTER em branco e depois CTRL+D no Linux/macOS ou CTRL+Z no Windows)\n")
    aves_obrigatorias = sys.stdin.read().strip().splitlines()

    total = int(input("\nQuantas aves o baralho deve ter no total? "))
    gerar_baralho(header, linhas, aves_obrigatorias, total)
