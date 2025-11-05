# daniel-birds-project

# 🪶 Projeto Daniel Birds

Um programa em Python criado por **Manu e Dani (com apoio de Rick 💗)** para gerar um baralho ideal de aves baseado em proporções definidas por grupos de características.
O sistema usa **Recozimento Simulado (Simulated Annealing)** para buscar automaticamente uma combinação equilibrada de aves que respeite as proporções desejadas.

---

## 🎲 Sobre o projeto

Este programa foi desenvolvido inspirado nas **regras e mecânicas do jogo de tabuleiro *Wingspan***, criado por **Elizabeth Hargrave** e publicado pela **Stonemaier Games**.

**Wingspan** é um jogo estratégico de construção de motores, em que os jogadores competem para atrair e cuidar das aves mais incríveis em seus habitats naturais.
Cada ave possui **características específicas**, como tipo de ninho, alimentação, habitat e efeitos especiais, que influenciam diretamente o equilíbrio do ecossistema e a pontuação final.

O propósito deste código é **simular a montagem equilibrada de um baralho de aves**, respeitando as proporções de características conforme as regras e a distribuição original do jogo.

🪶 A base de dados com as aves e suas características pode ser obtida neste link oficial do **BoardGameGeek**:
👉 [Wingspan – Spreadsheet (Bird Cards, Bonus Cards, End of Round Goals)](https://boardgamegeek.com/filepage/193164/wingspan-spreadsheet-bird-cards-bonus-cards-end-of)

Essa planilha contém todas as informações originais das aves do jogo, utilizadas para gerar os baralhos equilibrados neste programa.

---

## ⚙️ Funcionalidades

* Leitura de um arquivo `.csv` com os dados das aves e suas características.
* Geração de um **baralho ideal** que respeita as proporções definidas para cada grupo.
* Inclusão obrigatória de **aves específicas**, colando seus nomes diretamente do **Excel** — a lista de `must_include`.
* Ajuste fino de **tolerância** de proporções (%).
* Opção de visualizar:

  * O **baralho final completo**, ou
  * As **aves adicionadas além das obrigatórias**.
* Feedback detalhado das proporções alcançadas por grupo.
* 💾 **Exportação opcional em CSV** com o baralho final.

---

## 🧩 Estrutura dos grupos

O programa trabalha com **grupos de características** definidos por IDs de coluna no arquivo CSV:

| Grupo         | IDs de Características |
| ------------- | ---------------------- |
| TAMANHO E COR | 11, 12, 13             |
| TIPO DE NINHO | 14, 15, 16, 17         |
| 2 PONTOS      | 19, 20, 21, 22         |
| GEOGRAFIA     | 23, 24                 |
| HABITATS      | 5, 6, 7                |

Além disso, o código também exige a presença das seguintes **características individuais** (IDs fixos):
`8, 9, 10, 18, 25, 26, 27, 28, 29, 30`.

---

## 🖥️ Como usar

### 1. Executar o programa

No terminal, rode:

```bash
python "daniel project_3.1_with_export.py"
```

### 2. Inserir o caminho do arquivo CSV

Digite o **caminho completo** (ou apenas o nome, se estiver na mesma pasta):

```
Digite o caminho completo do arquivo CSV com todas as aves:  
> /Users/Manoela/Downloads/passarinhos.csv
```

### 3. Adicionar aves obrigatórias (must_include)

Copie e cole diretamente do Excel os nomes das aves que **devem obrigatoriamente** estar no baralho final.
Quando terminar, pressione **ENTER** em branco e depois **CTRL+D** (Linux/macOS) ou **CTRL+Z** (Windows):

```
Cole abaixo (direto do Excel) os nomes das aves obrigatórias (uma por linha):  
Coruja-das-torres  
Pica-pau-verde  
Beija-flor  

(ENTER + CTRL+D para continuar)
```

Essas aves serão incluídas automaticamente no baralho final.

---

## 🔢 Etapas de interação

Durante a execução, o programa solicitará:

1. **Tolerância (%)**
   Exemplo: `1.0` → permite até ±1% de diferença nas proporções.

2. **Modo de saída**

   * `1` → Mostrar o **baralho final completo**
   * `2` → Mostrar **apenas as aves adicionadas além das obrigatórias**

3. **Proporção alvo (%)** para cada grupo de características.
   Exemplo:

   ```
   Proporção ALVO (%) para o GRUPO 'HABITATS' (IDs: [5, 6, 7]): 20
   ```

4. **Número total de aves** no baralho.

5. **Deseja exportar o resultado em CSV?**
   Ao final, o programa perguntará se você quer gerar automaticamente um arquivo `.csv` com o baralho final.

---

## 📊 Saída

O programa exibirá:

* ✅ As aves incluídas ou adicionadas além das obrigatórias
* 📈 O resultado das proporções alcançadas por grupo
* 🐦 As aves obrigatórias garantidas no baralho
* ⚠️ Alertas se alguma característica ficou fora da tolerância
* 🎉 Mensagem de sucesso se todas as condições forem cumpridas
* 💾 Geração opcional de um arquivo `baralho_final.csv`

---

## 🧠 Como o algoritmo funciona

O método de **Recozimento Simulado** (*Simulated Annealing*) busca otimizar a composição do baralho com base em:

* **Função de energia:** mede o desvio entre as proporções obtidas e as desejadas.
* **Trocas aleatórias controladas:** aves são substituídas gradualmente para reduzir o erro total.
* **Taxa de resfriamento:** controla a probabilidade de aceitar piores soluções no início para evitar mínimos locais.

O processo termina quando:

* A energia mínima é atingida dentro da tolerância, ou
* As iterações (`SA_ITERATIONS = 50.000`) são concluídas.

---

## 🧾 Estrutura do CSV

O arquivo deve conter:

* A primeira coluna com o **nome da ave**.
* As colunas seguintes contendo `"X"` ou vazio (`""`) para indicar a presença ou ausência da característica.

Exemplo:

| Bird Name | Col5 | Col6 | Col7 | ... | Col30 |
| --------- | ---- | ---- | ---- | --- | ----- |
| Bird_001  | X    |      | X    | ... |       |
| Bird_002  |      | X    |      | ... | X     |

---

## 🪄 Créditos

**Desenvolvido por:**
🕊️ Manu
🦅 Dani
🦜 Apoio moral: Rick

> Projeto feito com amor, improviso e alguns pombos aleatórios Pruu.

---

## 🧰 Requisitos

* Python 3.8+
* Nenhuma biblioteca externa (apenas `csv`, `math`, `random` e `sys`)

---

## 💬 Exemplo de execução

```
Digite o caminho completo do arquivo CSV com todas as aves:  
> passarinhos.csv  

Cole abaixo (direto do Excel) os nomes das aves obrigatórias (uma por linha):  
Coruja-das-torres  
Beija-flor  

(ENTER + CTRL+D para continuar)  

Quantas aves o baralho deve ter no total? 120  

Qual tolerância desejada (em %)? 1.0  

Deseja ver o resultado como:  
1. Baralho ideal completo  
2. Apenas aves adicionadas além das obrigatórias  
Escolha 1 ou 2: 1  
```

Saída esperada:

```
🎉 Baralho ideal encontrado após 4389 iterações.  
✅ Baralho final gerado com 120 aves!  
🐦 Aves obrigatórias incluídas com sucesso.  
🕊️ Pássaros incluídos:  
 - Bird_001  
 - Bird_054  
 - Bird_302  
 ...  

--- RESULTADOS DE PROPORÇÕES ---  
GRUPO 'HABITATS' (Alvo 20.00%)  
  - 5: 19.8% (alvo 20.0%) ✅ OK  
  - 6: 20.1% (alvo 20.0%) ✅ OK  

💾 Arquivo 'baralho_final.csv' gerado com sucesso!  
```

---

## 📂 Estrutura do projeto

```
daniel project_3.1_with_export.py  
README.md  
```

---

## ✨ Novidades da Versão 3.1

🐦 **Lista `must_include`** — agora é possível colar diretamente do Excel os nomes das aves que devem obrigatoriamente estar no baralho final.
💾 **Exportação em CSV** — ao final da execução, o programa oferece a opção de gerar automaticamente um arquivo `.csv` com o baralho resultante.
📊 **Mesma lógica original dos grupos** — mantida a estrutura de balanceamento por grupos de características e proporções alvo.
💬 **Melhorias gerais na interação** — mensagens mais claras, interface de terminal revisada e execução mais fluida.


