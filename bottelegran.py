import telebot 
from telebot import types
from chave import CHAVE_API 


bot = telebot.TeleBot(CHAVE_API)

class Dupla:
    def __init__(self, nome, prioridade):
        self.nome = nome
        self.prioridade = prioridade

    def __repr__(self):
        return f"Prioridade {self.prioridade}: {self.nome}"

class ListaDePrioridades:
    def __init__(self):
        self.duplas = []

    def adicionar_dupla(self, nome):
        prioridade = len(self.duplas) + 1
        novo_dupla = Dupla(nome, prioridade)
        self.duplas.append(novo_dupla)
        self.duplas.sort(key=lambda x: x.prioridade)
        return f"Dupla {nome} adicionada com prioridade {prioridade}."

    def retirar_dupla(self, indice):
        if not self.duplas:
            return "Não há duplas cadastradas."

        try:
            dupla_removida = self.duplas.pop(indice - 1)
            return f"Dupla '{dupla_removida}' removida com sucesso!"
        except IndexError:
            return "Índice inválido. Tente novamente."

    def definir_ganhador(self, ganhador, perdedor):
        for dupla in self.duplas:
            if dupla.nome == ganhador:
                dupla.prioridade = 3
                for t in self.duplas[4:]:
                    t.prioridade += 1
            if dupla.nome == perdedor:
                dupla.prioridade = len(self.duplas)

        self.duplas.sort(key=lambda x: x.prioridade)
        return f"Resultado atualizado: {ganhador} venceu {perdedor}."

    def pegar_proxima_dupla(self):
        if len(self.duplas) < 2:
            return "Não há duplas suficientes para uma partida."
        proxima_dupla = (self.duplas[0].nome, self.duplas[1].nome)
        for dupla in self.duplas:
            if dupla != self.duplas[0] and dupla != self.duplas[1]:
                dupla.prioridade -= 2
        self.duplas.sort(key=lambda x: x.prioridade)
        return proxima_dupla

    def listar_duplas(self):
        if not self.duplas:
            return "Nenhuma dupla cadastrada."
        return '\n'.join([f'{i+1}. Prioridade {dupla.prioridade}: {dupla.nome}' for i, dupla in enumerate(self.duplas)])

lista_de_prioridades = ListaDePrioridades()
proxima_dupla = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá, eu sou o bot do Futevôlei & Resenha. Use os comandos para interagir comigo.")

@bot.message_handler(commands=['adicionar_dupla'])
def add_dupla(message):
    msg = bot.send_message(message.chat.id, "Digite o nome da dupla:")
    bot.register_next_step_handler(msg, process_add_dupla_step)

def process_add_dupla_step(message):
    nome_dupla = message.text
    resposta = lista_de_prioridades.adicionar_dupla(nome_dupla)
    bot.reply_to(message, resposta)

@bot.message_handler(commands=['retirar_dupla'])
def remove_dupla(message):
    if not lista_de_prioridades.duplas:
        bot.reply_to(message, "Não há duplas cadastradas.")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i, dupla in enumerate(lista_de_prioridades.duplas):
            markup.add(types.KeyboardButton(f'{i+1}. {dupla.nome}'))
        msg = bot.send_message(message.chat.id, "Escolha a dupla a ser removida:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_remove_dupla_step)

def process_remove_dupla_step(message):
    try:
        indice = int(message.text.split('.')[0])
        resposta = lista_de_prioridades.retirar_dupla(indice)
    except (ValueError, IndexError):
        resposta = "Opção inválida. Tente novamente."
    bot.reply_to(message, resposta)

@bot.message_handler(commands=['listar_duplas'])
def list_duplas(message):
    resposta = lista_de_prioridades.listar_duplas()
    bot.reply_to(message, resposta)

@bot.message_handler(commands=['gerar_proximo_jogo'])
def generate_next_game(message):
    global proxima_dupla
    proxima_dupla = lista_de_prioridades.pegar_proxima_dupla()
    if isinstance(proxima_dupla, str):
        resposta = proxima_dupla
    else:
        resposta = f"Próxima dupla: {proxima_dupla[0]} x {proxima_dupla[1]}"
    bot.reply_to(message, resposta)

@bot.message_handler(commands=['definir_ganhador'])
def set_winner(message):
    if not proxima_dupla:
        bot.reply_to(message, "Nenhuma dupla selecionada para o jogo.")
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(proxima_dupla[0]), types.KeyboardButton(proxima_dupla[1]))
    msg = bot.send_message(message.chat.id, "Quem venceu?", reply_markup=markup)
    bot.register_next_step_handler(msg, process_set_winner_step)

def process_set_winner_step(message):
    global proxima_dupla
    ganhador = message.text
    if ganhador not in proxima_dupla:
        bot.reply_to(message, "Opção inválida. Tente novamente.")
        return
    perdedor = proxima_dupla[1] if ganhador == proxima_dupla[0] else proxima_dupla[0]
    resposta = lista_de_prioridades.definir_ganhador(ganhador, perdedor)
    bot.reply_to(message, resposta)
    proxima_dupla = None

def verificar(mensagem):
    return True

# Tela Inicial: 
@bot.message_handler(func= verificar)
def responder(mensagem):
    texto = """
        Olá, eu sou o bot do Futevolei e resenha

        Escolha uma opção para continuar (Clique no item):
        /adicionar_dupla 
        /retirar_dupla 
        /listar_duplas
        /gerar_proximo_jogo
        /definir_ganhador
        Responder qualquer outra coisa não vai funcionar, clique em uma das opções 
    """
    bot.reply_to(mensagem, texto)

bot.polling()
