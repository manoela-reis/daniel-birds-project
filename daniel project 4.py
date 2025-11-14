import csv
import random
import math
import sys

# ==== CONFIGURAÇÕES DE GRUPOS (mesma lógica original) ====
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

def normalizar_caminho(caminho):
    caminho = caminho.strip()

    # Remove aspas duplas se existirem
    if caminho.startswith('"') and caminho.endswith('"'):
        caminho = caminho[1:-1]

    # Converte \ para / (funciona no Windows e no Linux)
    caminho = caminho.replace("\\", "/")

    return caminho


def carregar_csv(caminho_csv):
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        dados = list(reader)
    header = dados[0]
    linhas = dados[1:]
    return header, linhas

def contar_proporcao(linhas, col_id):
    total = len(linhas)
    if total == 0:
        return 0.0
    com_x = sum(1 for linha in linhas if linha[col_id - 1].strip().upper() == "X")
    return (com_x / total) * 100

def contar_proporcao_grupo(linhas, col_ids):
    total = len(linhas)
    if total == 0:
        return 0.0
    com_x = 0
    for linha in linhas:
        if any(linha[col - 1].strip().upper() == "X" for col in col_ids):
            com_x += 1
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
                print("⚠️ Entrada inválida. Use números decimais com ponto.")
    return proporcoes_grupos_input

def solicitar_tolerancia():
    while True:
        try:
            tolerancia = float(input("\nQual tolerância desejada (em %)? ").strip())
            if tolerancia < 0:
                print("❌ A tolerância deve ser positiva.")
                continue
            return tolerancia
        except ValueError:
            print("⚠️ Entrada inválida.")

def perguntar_modo_saida():
    while True:
        modo = input(
            "\nDeseja ver o resultado como:\n"
            "1. Baralho completo\n"
            "2. Apenas aves adicionadas além das obrigatórias\n"
            "3. Apenas as aves RETIRADAS do arquivo original\n"
            "Escolha 1, 2 ou 3: "
        ).strip()
        if modo in ["1", "2", "3"]:
            return modo
        print("⚠️ Opção inválida.")

def calcular_energia(baralho, proporcoes_alvo_caracteristica, total_aves):
    if len(baralho) != total_aves:
        return float('inf')
    energia = 0.0
    for col_id, desejada in proporcoes_alvo_caracteristica.items():
        prop_obtida = contar_proporcao(baralho, col_id)
        energia += abs(prop_obtida - desejada)
    for col_id in CARACTERISTICAS_INDIVIDUAIS:
        if contar_proporcao(baralho, col_id) <= 0.0:
            return float('inf')
    return energia

def inicializar_baralho(linhas, total_aves, proporcoes_alvo_caracteristica, must_include):
    baralho_set = set(tuple(l) for l in must_include)
    for col_id in CARACTERISTICAS_INDIVIDUAIS:
        candidatos = [linha for linha in linhas if linha[col_id - 1].strip().upper() == "X" and tuple(linha) not in baralho_set]
        if candidatos:
            baralho_set.add(tuple(random.choice(candidatos)))
    linhas_restantes = [linha for linha in linhas if tuple(linha) not in baralho_set]
    aves_faltando = total_aves - len(baralho_set)
    proporcoes_ordenadas = sorted(proporcoes_alvo_caracteristica.items(), key=lambda x: x[1], reverse=True)
    adicoes, idx = 0, 0
    while adicoes < aves_faltando and linhas_restantes:
        col_prioritaria = proporcoes_ordenadas[idx % len(proporcoes_ordenadas)][0]
        candidatos = [l for l in linhas_restantes if l[col_prioritaria - 1].strip().upper() == "X"]
        escolhido = random.choice(candidatos if candidatos else linhas_restantes)
        baralho_set.add(tuple(escolhido))
        linhas_restantes.remove(escolhido)
        adicoes += 1
        idx += 1
    baralho = [list(x) for x in baralho_set]
    random.shuffle(baralho)
    return baralho if len(baralho) == total_aves else None

def gerar_vizinho(baralho, todas_linhas_tuple, must_include_set):
    baralho_tuple = {tuple(l) for l in baralho}
    aves_incluidas = [l for l in baralho_tuple if l not in must_include_set]
    aves_nao = [l for l in todas_linhas_tuple if l not in baralho_tuple and l not in must_include_set]
    if not aves_incluidas or not aves_nao:
        return None
    removida = random.choice(aves_incluidas)
    adicionada = random.choice(aves_nao)
    novo = list((baralho_tuple - {removida}) | {adicionada} | must_include_set)
    return [list(l) for l in novo]

def verificar_resultado_final(baralho_final, proporcoes_alvo_caracteristica, tolerancia):
    for ids in GRUPOS.values():
        for col_id in ids:
            desejada = proporcoes_alvo_caracteristica.get(col_id, 0.0)
            if abs(contar_proporcao(baralho_final, col_id) - desejada) > tolerancia:
                return False
    for col_id in CARACTERISTICAS_INDIVIDUAIS:
        if contar_proporcao(baralho_final, col_id) <= 0.0:
            return False
    return True

def exibir_resultados_sa(baralho_final, linhas_totais, proporcoes_grupos_input, proporcoes_alvo_caracteristica, tolerancia, modo_saida, must_include):
    print(f"\n✅ Baralho final gerado com {len(baralho_final)} aves!")
    bar_set = {tuple(l) for l in baralho_final}
    must_set = {tuple(l) for l in must_include}

    if modo_saida == "1":
        print("\n🕊️ Pássaros incluídos:")
        for l in baralho_final:
            print(f" - {l[0]}")
    elif modo_saida == "2":
        print("\n🪶 Pássaros adicionados além dos obrigatórios:")
        for l in baralho_final:
            if tuple(l) not in must_set:
                print(f" - {l[0]}")
    elif modo_saida == "3":
        print("\n🚫 Pássaros RETIRADOS do arquivo original:")
        removidos = [l for l in linhas_totais if tuple(l) not in bar_set]
        for l in removidos:
            print(f" - {l[0]}")

    print("\n--- RESULTADOS DE PROPORÇÕES ---")
    for nome, ids in GRUPOS.items():
        #alvo = proporcoes_grupos_input.get(nome, 0.0)
        #obtido = contar_proporcao_grupo(baralho_final, ids)
        #status = "✅ OK" if abs(obtido - alvo) <= tolerancia else "❌ FORA"
        print(f"\nGRUPO '{nome.upper()}'")
        for col in ids:
            dese = proporcoes_alvo_caracteristica[col]
            ob = contar_proporcao(baralho_final, col)
            st = "✅ OK" if abs(ob - dese) <= tolerancia else "❌ FORA"
            print(f" - feature {col}: {ob:.1f}% (alvo {dese:.1f}%) {st}")

def exportar_baralho_csv(header, baralho, nome_arquivo="baralho_final.csv"):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(baralho)
    print(f"\n💾 Arquivo '{nome_arquivo}' gerado com sucesso!")

def gerar_baralho(header, linhas, must_include_input, total_aves):
    tolerancia = solicitar_tolerancia()
    modo_saida = perguntar_modo_saida()
    proporcoes_grupos_input = solicitar_proporcoes_alvo_grupos()

    proporcoes_alvo_caracteristica = {
        col: proporcoes_grupos_input[nome]
        for nome, ids in GRUPOS.items()
        for col in ids
    }

    nomes_must = [m.strip().lower() for m in must_include_input if m.strip()]
    must_include = [l for l in linhas if l[0].strip().lower() in nomes_must]
    must_set = {tuple(l) for l in must_include}

    if len(must_include) > total_aves:
        print("❌ A lista obrigatória contém mais aves do que o limite.")
        return

    todas_tuple = [tuple(l) for l in linhas]

    bar_atual = inicializar_baralho(linhas, total_aves, proporcoes_alvo_caracteristica, must_include)
    if bar_atual is None:
        print("❌ Não foi possível inicializar o baralho.")
        return

    energia_atual = calcular_energia(bar_atual, proporcoes_alvo_caracteristica, total_aves)
    melhor = list(bar_atual)
    melhor_e = energia_atual
    T = SA_T_INITIAL

    for i in range(SA_ITERATIONS):
        vz = gerar_vizinho(bar_atual, todas_tuple, must_set)
        if vz is None:
            continue
        e_vz = calcular_energia(vz, proporcoes_alvo_caracteristica, total_aves)

        if e_vz < energia_atual or random.random() < math.exp(-(e_vz - energia_atual) / T):
            bar_atual = vz
            energia_atual = e_vz

        if energia_atual < melhor_e:
            melhor, melhor_e = list(bar_atual), energia_atual
            if verificar_resultado_final(melhor, proporcoes_alvo_caracteristica, tolerancia):
                print(f"\n🎉 Baralho ideal encontrado após {i+1} iterações.")
                exibir_resultados_sa(melhor, linhas, proporcoes_grupos_input, proporcoes_alvo_caracteristica, tolerancia, modo_saida, must_include)
                break

        T *= SA_T_COOLING_RATE
    else:
        print("\n⚠️ Nenhum baralho perfeito foi encontrado.")
        exibir_resultados_sa(melhor, linhas, proporcoes_grupos_input, proporcoes_alvo_caracteristica, tolerancia, modo_saida, must_include)

    if input("\nDeseja exportar o baralho final em CSV? (s/n): ").strip().lower() == "s":
        nome = input("Digite o nome (ENTER = baralho_final.csv): ").strip() or "baralho_final.csv"
        exportar_baralho_csv(header, melhor, nome)

if __name__ == "__main__":
    while True:
        print("\n===== 🕊️ BEM-VINDO AO PROJETO DANIEL BIRDS (com grupos) =====")
        caminho_raw = input("\nDigite o caminho completo do arquivo CSV com todas as aves: ").strip()
        caminho = normalizar_caminho(caminho_raw)

        try:
            header, linhas = carregar_csv(caminho)
        except FileNotFoundError:
            print("❌ Arquivo não encontrado.")
            continue

        print("\nCole abaixo os nomes das aves obrigatórias (uma por linha):")
        print("(Pressione ENTER vazio e depois CTRL+D / CTRL+Z para terminar)\n")
        aves_obrigatorias = sys.stdin.read().strip().splitlines()

        try:
            total = int(input("\nQuantas aves o baralho deve ter? ").strip())
        except ValueError:
            print("❌ Número inválido.")
            continue

        gerar_baralho(header, linhas, aves_obrigatorias, total)

        if input("\nDeseja rodar novamente? (s/n): ").strip().lower() != "s":
            print("\n🫶 Obrigada por usar! Foi feito com amor de presente para meu melhor amigo Dani <3 Até a próxima!")
            break
