from random import randint
from socket import *


#Le o arquivo e separa ele em duas partes, tela e lista de palavras
def leArquivo():
    tela = ""
    palavras = ""
    ctrl = 0
    arq = open('facil.txt', 'r')
    for linha in arq:
        if linha == "PALAVRAS\n":
            ctrl = 1
        if ctrl == 0:
            tela = tela + linha
        else:
            palavras = palavras + linha
    arq.close()
    return tela, palavras


#Escolhe uma palavra da lista de palavras
def escolhePalavra(palavras):
    palavras = palavras.split("\n")
    palavraEscolhida = palavras[randint(1, len(palavras)-2)]
    return palavraEscolhida


#Compara letra a letra o chute com a palavra escolhida
def confere(chute, palavraEscolhida):
    if chute == palavraEscolhida:
        return len(palavraEscolhida)
    else:
        acertos = 0
        for x, y in zip(chute, palavraEscolhida):
            if x == y:
                acertos = acertos + 1
    return acertos


#Imprime o numero de acerto e a semelhanca das palavras
def tentativas(tent, acertos):
    linha = "# # # # # # # # # # # # # # # # # # # # # #\n"
    linha = linha + "# ENTRY DENID                             #\n"
    linha = linha + "# LIKENESS = " + str(acertos) + "                            #\n"
    linha = linha + "# " + str(tent) + " ATTEMPT(S) LEFT :"

    if tent == 1:
        linha = linha + " [X] [ ] [ ] [ ] "
    elif tent == 2:
        linha = linha + " [X] [X] [ ] [ ] "
    elif tent == 3:
        linha = linha + " [X] [X] [X] [ ] "
    linha = linha + "    #\n# # # # # # # # # # # # # # # # # # # # # #\n"

    return str.encode(linha)


#Imprime o cabelhaca
def cabecalho():
    linha = b"# # # # # # # # # # # # # # # # # # # # # #\n"
    linha = linha + b"# ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL #\n"
    linha = linha + b"# ENTER PASSWORD NOW ...                  #\n"
    linha = linha +	b"#                                         #\n"
    linha = linha +	b"# 4 ATTEMPT(S) LEFT : [X] [X] [X] [X]     #\n"
    linha = linha +	b"# # # # # # # # # # # # # # # # # # # # # #\n"
    return linha


def fimDeJogo(ctrl):
    linha = b"# # # # # # # # # # # # # # # # # # # # # #\n"
    linha = linha + b"# ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL #\n"
    
    if ctrl:
        linha = linha + b"# ENTRY DENID....                         #\n"
        linha = linha + b"# TERMINAL LOCK                           #\n"
    else:
        linha = linha + b"# ENTRY ACCEPT...                         #\n"
        linha = linha + b"# TERMINAL UNLOCK                         #\n"
    linha = linha + b"# # # # # # # # # # # # # # # # # # # # # #\n"
    return linha


def main():
    #configura o server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('127.0.0.1', 8000))
    serverSocket.listen(1)

    # configura variáveis para o game
    tent = 4
    texto = leArquivo()
    palavraEscolhida = escolhePalavra(texto[1])
    textoEscolhido = texto[0]

    #espera por conexões
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('conexão estabelecida com' + str(addr))

        connectionSocket.send(cabecalho())
        connectionSocket.send(str.encode(textoEscolhido))
        connectionSocket.send(b"INPUT:")

        #executa 4 tentativas
        while tent > 0:

            #recebe o chute do cliente e confere
            chute = str(connectionSocket.recv(10))
            #formata o chute
            chute = chute.replace("b'", "").replace("\\r\\n'", "")
            acertos = confere(chute, palavraEscolhida)

            #se acertou ou terminaram as chances termina o jogo, senão chuta de novo
            if (acertos == len(palavraEscolhida)):
                connectionSocket.send(fimDeJogo(False))
                break
            else:
                tent = tent - 1
                if tent == 0:
                    connectionSocket.send(fimDeJogo(True))
                else:
                    connectionSocket.send(tentativas(tent, acertos))
                    connectionSocket.send(b"INPUT:")

        tent = 4
        connectionSocket.close()
        print('conexão fechada')

main()