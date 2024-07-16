import telebot 
from chave import CHAVE_API 


bot = telebot.TeleBot(CHAVE_API)

duplas = []

# Entrada de Dados: Tela para inserir as duplas
@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    while True:
        nome_dupla1 = input("Digite o nome da dupla 1: ")
        nome_dupla2 = input("Digite o nome da dupla 2: ")
        dupla = (nome_dupla1, nome_dupla2)
        duplas.append(dupla)
        resposta = input("Deseja adicionar outra dupla? (s/n): ")
        if resposta.lower() != "s":
            break
    return duplas


@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    pass

@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    pass

@bot.message_handler(commands=["opcao4"])
def opcao4(mensagem):
    pass



def verificar(mensagem):
    return True


# Tela Inicial: Escolha do método de jogo (Opção A ou B)
@bot.message_handler(func= verificar)
def responder(mensagem):
    texto = """
        Olá, eu sou o bot do Futevolei e resenha

        Escolha uma opção para continuar (Clique no item):
        /opcao1 Adicionar duplas
        /opcao2 Sai as duas duplas 
        /opcao3 Dupla ganhadora fica
        /opcao4 Dupla ganhadora volta no proximo jogo
        Responder qualquer outra coisa não vai funcionar, clique em uma das opções 
    """
    bot.reply_to(mensagem, texto)

bot.infinity_polling()

