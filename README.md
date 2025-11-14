# 🪶 Projeto Daniel Birds

Um programa em Python criado por **Manu e Dani (com apoio de Rick 💗)** para gerar um baralho ideal de aves baseado em proporções definidas por grupos de características.
O sistema usa **Recozimento Simulado (Simulated Annealing)** para buscar automaticamente uma combinação equilibrada de aves que respeite as proporções desejadas.

---

## 🎁 Sobre este presente

Este projeto foi feito com muito carinho como um **presente para o meu melhor amigo Dani**,
uma pessoa apaixonada por **passarinhos**, por **Wingspan**, e por tudo o que envolve mundos construídos com cuidado e beleza.

É um programinha que traduz o amor dele por aves em código — e o meu carinho por ele e pelo Ric em cada detalhe. 💛
![20250709_002139](https://github.com/user-attachments/assets/e11868a7-3f8f-46ac-964a-b9a9fe394bba)


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
* Compatível com caminhos de arquivo **copiados exatamente como o Windows fornece**, incluindo:

  * Aspas (`" "`)
  * Barras invertidas (`\`)
  * Espaços
    O programa normaliza tudo automaticamente.
* Geração de um **baralho ideal** que respeita as proporções definidas para cada grupo.
* Possibilidade de incluir uma **lista personalizada de aves obrigatórias**, copiando e colando diretamente do Excel.
* Inclusão obrigatória automática das **características individuais essenciais**.
* Ajuste fino de tolerância de proporções (%).
* Opção de visualizar:

  * O **baralho completo**
  * Apenas as **aves adicionadas além das obrigatórias**
  * As **aves retiradas** do conjunto original
* Feedback detalhado das proporções alcançadas por subcaracterísticas dentro de cada grupo.
* Opção de **exportar o baralho final em CSV**.
* E agora:
  **O programa pergunta automaticamente se o usuário deseja rodar novamente**, facilitando testar vários cenários sem precisar reiniciar.

---

## 🧩 Estrutura dos grupos

O programa trabalha com **grupos de características**, onde cada grupo é composto por vários IDs de colunas do CSV.

### **Grupos de características**

| Grupo         | IDs de Características |
| ------------- | ---------------------- |
| TAMANHO E COR | 11, 12, 13             |
| TIPO DE NINHO | 14, 15, 16, 17         |
| 2 PONTOS      | 19, 20, 21, 22         |
| GEOGRAFIA     | 23, 24                 |
| HABITATS      | 5, 6, 7                |

### **Características individuais obrigatórias**

Além dos grupos, o código também exige a presença de pelo menos uma ave com cada uma das seguintes características:

`8, 9, 10, 18, 25, 26, 27, 28, 29, 30`

### **Aves obrigatórias (Must Include)** — *Novidade!*

Agora o usuário pode colar uma lista de nomes de aves (uma por linha) vindas direto do Excel.
Essas aves sempre estarão presentes no baralho final.

---

## 🖥️ Como usar

### 1. Executar o programa

```bash
python "daniel project 4.py"
```

### 2. Inserir o caminho do arquivo CSV

O programa aceita **exatamente o caminho copiado do Windows**, incluindo:

```
"C:\Users\Manoela\Downloads\passarinhos.csv"
```

Ele automaticamente:

* remove as aspas
* converte `\` em `/`
* limpa caracteres extras

### 3. Informar aves obrigatórias

Cole os nomes das aves, uma por linha.

Para terminar a lista:

* **ENTER vazio + CTRL+D** (Mac/Linux)
* **ENTER vazio + CTRL+Z** (Windows)

### 4. Informar quantidade total de aves

### 5. Definir tolerância (%)

### 6. Selecionar o modo de saída

```
1. Baralho completo
2. Apenas aves adicionadas além das obrigatórias
3. Aves retiradas do arquivo original
```

### 7. Definir proporções alvo para cada grupo

### 8. Repetição automática

No final, o programa pergunta:

```
Deseja rodar novamente? (s/n)
```

Assim você pode criar quantos cenários quiser sem reiniciar.

---

## 📊 Saída

O programa exibirá:

* 🎉 Mensagem de sucesso (ou aviso se não encontrou uma solução perfeita)
* 🕊️ A lista de aves conforme o modo selecionado
* 📈 Proporções alcançadas dentro de cada subcaracterística dos grupos
* ⚠️ Quais ficaram fora da tolerância
* 💾 E a opção final de exportar para CSV

---

## 🧠 Como o algoritmo funciona

O programa utiliza **Simulated Annealing**, ajustando o baralho iterativamente:

* Calcula uma função de energia com base nos desvios das proporções alvo.
* Substitui aves gradualmente, aceitando pioras iniciais para evitar mínimos locais.
* Resfria a temperatura a cada iteração.
* Encerra quando:

  * Todas as condições são atendidas dentro da tolerância, **ou**
  * As `50.000` iterações são concluídas.

---

## 🧾 Estrutura do CSV

O arquivo deve conter:

* Primeira coluna: **nome da ave**
* Demais colunas: `"X"` ou vazio

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
* Nenhuma biblioteca externa (apenas `csv`, `math`, `random`, `sys`)

---

## 📂 Estrutura do projeto

```
daniel project 4.py
README.md
```

