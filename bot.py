from Bot import *

# from MESSAGES import *

TOKEN = '5774814883:AAEzanp5Vs63lcnclWmVMMrgLrRtVt5mG04'
Bot = Bot(TOKEN)


@Bot.bot.message_handler(commands=['help'])
def help(message):
    Bot.send_special_message(message.chat.id, HELP_MESSAGE)


@Bot.bot.message_handler(chat_types=['supergroup'], commands=['get_stats'])
def get_stats(message):
    Bot.send_members_info(message.chat.id)


@Bot.bot.message_handler(chat_types=['supergroup'], commands=['unban'])
def restrict_user(message):
    Bot.restrict_user(message, 'unban')


@Bot.bot.message_handler(chat_types=['supergroup'], commands=['ban'])
def restrict_user(message):
    Bot.restrict_user(message, 'ban', 2)


@Bot.bot.message_handler(commands=['show_interface'])
def show_interface(message):
    Bot.open_interface(message.chat.id)


@Bot.bot.message_handler(chat_types=['supergroup', 'group'], commands=['restrict'])
def restrict(message):
    Bot.restrict_user(message)

@Bot.bot.message_handler(content_types=['text'])
def reply_message(message):
    mes_text = message.text.split()
    if mes_text[0] != '@geoguessr_banner_bot':
        return
    if len(mes_text) == 1:
        Bot.send_special_message(message.chat.id, ADVICE_MESSAGE)
    elif mes_text[1] == 'open_interface':
        Bot.open_interface(message.chat.id)
    elif mes_text[1] in ('ban', 'kick', 'mute'):
        t = 0
        if len(mes_text) > 2:
            try:
                t = int(mes_text[2])
            except Exception as e:
                pass
        Bot.restrict_user(message, mes_text[1], t)
    elif mes_text[1] == 'unban':
        Bot.unban_user(message)
    elif mes_text[1] == 'leave':
        Bot.leave(message.chat.id)
    elif mes_text[1] == 'get_chat_info':
        Bot.send_members_info(message.chat.id)
    elif mes_text[1] == 'help':
        Bot.send_special_message(message.chat.id, HELP_MESSAGE)
    else:
        Bot.send_special_message(message.chat.id, MISUNDERSTAND_MESSAGE)


@Bot.bot.message_handler(content_types=['new_chat_members'])
def say_hello(new_member):
    Bot.send_special_message(new_member, HELLO_NEW_MEMBER_MESSAGE)


@Bot.bot.callback_query_handler(func=lambda call: True)
def reply_callback_query(call):
    Bot.reply_inline_call(call)


Bot.start()
