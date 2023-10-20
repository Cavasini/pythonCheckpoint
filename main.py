import random

# Define os jogadores do jogo
def jogadores():
    while True:
        num_players = int(input("Digite a quantidade de jogadores (1 a 5): "))
        if 1 <= num_players <= 5:
            break
        print("Número inválido de jogadores. Tente novamente.")
    
    players = {}
    for _ in range(num_players):
        name = input("Digite o nome do jogador: ")
        players[name] = gerar_cartela_bingo()  # Gera cartela para cada jogador
    
    return players

# Gera uma cartela de bingo
def gerar_cartela_bingo():
    cartela = [] #cria lista cartela
    for _ in range(5): # cria um loop que vai até 5(de 0 até 4)
        coluna = [] #cria coluna
        for _ in range(5): # cria loop para numeros de numeros na coluna
            if len(coluna) == 0:
                # Para a primeira coluna, os números variam de 1 a 15
                numero = random.randint(1, 15)
            elif len(coluna) == 1:
                # Para a segunda coluna, os números variam de 16 a 30
                numero = random.randint(16, 30)
            elif len(coluna) == 2:
                # Para a terceira coluna, os números variam de 31 a 45
                numero = random.randint(31, 45)
            elif len(coluna) == 3:
                # Para a quarta coluna, os números variam de 46 a 60
                numero = random.randint(46, 60)
            else:
                # Para a quinta coluna, os números variam de 61 a 75
                numero = random.randint(61, 75)
            
            coluna.append(numero)
        cartela.append(coluna)

    return cartela

# Mostra as cartelas dos jogadores
def showCardsPlayers(players):
    for player, card in players.items():
        print(f"\nCartela de {player}:")
        for row in card:
            print(' '.join(str(num).rjust(2) if isinstance(num, int) else num for num in row))

# Se num for um número inteiro (representando um número da cartela), ele é convertido em uma string com str(num). Em seguida, rjust(2) é usado para justificar o número à direita em um espaço de 2 caracteres, preenchendo com espaços em branco à esquerda, para que os números sejam alinhados.
# Se num não for um número inteiro (como um marcador especial ou um espaço vazio), ele é mantido como está (é uma string ou outro tipo).
# join(...) é usado para combinar todos os elementos da linha em uma única string, separando-os por um espaço em branco.

# Atualiza as cartelas com os números sorteados
def update_cards(players, num):
    for player, card in players.items():
        for i in range(5):
            for j in range(5):
                if card[i][j] == num:
                    card[i][j] = "XX"
        if check_winner(card):
            return player
    return None

# Verifica se uma cartela é vencedora
def check_winner(card):
    # Verifica linhas, colunas e diagonais
    for i in range(5):
        #checa linha
        #checa coluna
        if all(cell == "XX" for cell in card[i]) or \
           all(card[j][i] == "XX" for j in range(5)):
            return True
        #chega diagona principal
        #chega diagonal secundaria
    if all(card[i][i] == "XX" for i in range(5)) or \
       all(card[i][4 - i] == "XX" for i in range(5)):
        return True
    return False

# Carrega o ranking a partir do arquivo
def load_ranking():
    try:
        with open("ranking.txt", "r") as file:
            lines = file.readlines()
            return {
                line.split(":")[0]: int(line.split(":")[1])
                for line in lines if ":" in line and line.split(":")[1].strip().isdigit()
            }
    except FileNotFoundError:
        return {}

# Salva o ranking atualizado no arquivo
def save_ranking(ranking):
    with open("ranking.txt", "w") as file:
        for player, score in ranking.items():
            file.write(f"{player}:{score}\n")

# Mostra o ranking atualizado
def players_ranking(ranking):
    print("\nRanking de Jogadores:")
    for player, score in sorted(ranking.items(), key=lambda x: x[1], reverse=True):
        print(f"{player}: {score} Vitória(s)")

# Lógica principal do jogo
def main_game():
    players = jogadores()
    ranking = load_ranking()
    drawn_numbers = []

    showCardsPlayers(players)
    print("\nIniciando o jogo! Pressione Enter para sortear números...")
    while True:
        input()
        while True:
            num = random.randint(1, 75)
            if num not in drawn_numbers:
                drawn_numbers.append(num)
                break
        
        print(f"\nNúmero sorteado: {num}")
        showCardsPlayers(players)
        winner = update_cards(players, num)
        if winner:
            print(f"\n{winner} ganhou! Aqui está a cartela vencedora:\n")
            showCardsPlayers({winner: players[winner]})
            ranking[winner] = ranking.get(winner, 0) + 1
            save_ranking(ranking)
            players_ranking(ranking)
            break

main_game()
