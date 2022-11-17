import time
import telebot
from telebot import types
from MESSAGES import *


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot_username = self.bot.user.username
        self.bot_id = self.bot.user.id

    def send_special_message(self, chat_id, message_text):
        try:
            self.bot.send_message(chat_id, message_text, parse_mode='HTML')
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))

    def open_interface(self, chat_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        but_help = types.InlineKeyboardButton(text='Посмотреть справку', callback_data='help')
        but_del = types.InlineKeyboardButton(text='Закрыть интерфейс', callback_data='delete_message')
        but_ban = types.InlineKeyboardButton(text='Забанить пользователя', callback_data='ban_user')
        but_leave = types.InlineKeyboardButton(text='Выгнать бота из беседы', callback_data='leave')
        but_stats = types.InlineKeyboardButton(text='Получить информацию об участниках чата', callback_data='get_stats')
        but_test = types.InlineKeyboardButton(text='test', callback_data='test')
        markup.add(but_help, but_ban, but_leave, but_stats, but_del, but_test)
        self.bot.send_message(chat_id, 'Интерфейс для работы с ботом', reply_markup=markup)

    def reply_inline_call(self, call):
        if call.data == 'help':
            markup = types.InlineKeyboardMarkup()
            back_but = types.InlineKeyboardButton(text='Назад', callback_data='menu')
            markup.add(back_but)
            self.bot.edit_message_text(HELP_MESSAGE, call.message.chat.id, call.message.id, parse_mode='HTML')
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)
        elif call.data == 'leave':
            markup = types.InlineKeyboardMarkup()
            but_yes = types.InlineKeyboardButton(text='Да', callback_data='bot_leave')
            but_no = types.InlineKeyboardButton(text='Нет', callback_data='menu')
            markup.add(but_yes, but_no)
            self.bot.edit_message_text('Вы уверены, что хотите удалить бота из чата?', call.message.chat.id,
                                       call.message.id)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)
        elif call.data == 'get_stats':
            markup = types.InlineKeyboardMarkup()
            back_but = types.InlineKeyboardButton(text='Назад', callback_data='menu')
            markup.add(back_but)
            self.bot.edit_message_text(self.get_members_info_message(call.message.chat.id), call.message.chat.id,
                                       call.message.id)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)
        elif call.data == 'delete_message':
            self.bot.delete_message(call.message.chat.id, call.message.id)
        elif call.data == 'menu':
            markup = types.InlineKeyboardMarkup(row_width=1)
            but_help = types.InlineKeyboardButton(text='Посмотреть справку', callback_data='help')
            but_del = types.InlineKeyboardButton(text='Закрыть интерфейс', callback_data='delete_message')
            but_ban = types.InlineKeyboardButton(text='Забанить пользователя', callback_data='ban_user')
            but_unban = types.InlineKeyboardButton(text='Разбанить пользователя', callback_data='unban_user')
            but_kick = types.InlineKeyboardButton(text='Кикнуть пользователя', callback_data='kick_user')
            but_mute = types.InlineKeyboardButton(text='Замутить пользователя', callback_data='mute_user')
            but_leave = types.InlineKeyboardButton(text='Выгнать бота из беседы', callback_data='leave')
            but_stats = types.InlineKeyboardButton(text='Получить информацию об участниках чата',
                                                   callback_data='get_stats')
            markup.add(but_help, but_ban, but_leave, but_stats, but_del)
            self.bot.edit_message_text('Интерфейс для работы с ботом', call.message.chat.id, call.message.id)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)
        elif call.data == 'bot_leave':
            self.bot.delete_message(call.message.chat.id, call.message.id)
            self.leave(call.message.chat.id)
        elif call.data == 'ban_user':
            but_menu = types.InlineKeyboardButton(text='Назад', callback_data='menu')
            markup = types.InlineKeyboardMarkup()
            markup.add(but_menu)
            self.bot.edit_message_text('Выберите пользователя, которого хотите забанить', call.message.chat.id,
                                       call.message.id)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)
        elif call.data == 'test':
            but_menu = types.InlineKeyboardButton(text='Назад', callback_data='menu')
            markup = types.InlineKeyboardMarkup()
            buttons = [but_menu]
            for i in range(200):
                new_but = types.InlineKeyboardButton(text='but number'+str(i), callback_data='menu')
                buttons.append(new_but)
            markup.add(*buttons)
            self.bot.edit_message_text('test', call.message.chat.id, call.message.id)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)

    def get_admins_list(self, chat_id, id_or_username='id'):
        admins = set()
        if id_or_username == 'id':
            for admin in self.bot.get_chat_administrators(chat_id):
                admins.add(admin.user.id)
        elif id_or_username == 'username':
            for admin in self.bot.get_chat_administrators(chat_id):
                admins.add(admin.user.username)
        return admins

    def restrict_user(self, message, type_='kick', t=0):
        if len(message.text.split()) > 1:
            type_ = str(str(message.text.split()[1]))
        chat_id = message.chat.id
        attacker = message.from_user
        admins = self.get_admins_list(chat_id, id_or_username='id')
        if attacker.id not in admins:
            self.bot.send_message(chat_id, 'У вас недостаточно прав.')
            return
        if message.reply_to_message is None:
            self.bot.send_message(chat_id,
                                  'Укажите человека, которого необходимо кикнуть(забанить), ответив на его сообщение')
            return
        victim = message.reply_to_message.from_user
        if victim.id in admins:
            self.bot.send_message(chat_id, 'У вас недостаточно прав.')
        else:
            try:
                self.bot.get_chat_member(chat_id, victim.id)
            except Exception as e:
                self.bot.send_message(chat_id, 'Не удалось найти данного пользователя в чате.')
                print("{!s}\n{!s}".format(type(e), str(e)))

            try:
                if type_ == 'kick':
                    self.bot.kick_chat_member(chat_id=chat_id, user_id=victim.id)
                    self.bot.send_message(chat_id,
                                          'Пользователь @' + victim.username + ' был кикнут из чата по просьбе @' + attacker.username + ' .')
                elif type_ == 'ban':
                    self.bot.ban_chat_member(chat_id, victim.id, t)
                    self.bot.send_message(chat_id,
                                          'Пользователь @' + victim.username + ' был забанен по просьбе @' + attacker.username + ' .')
                elif type_ == 'mute':
                    self.bot.promote_chat_member(chat_id, victim.id, can_delete_messages=False, can_invite_users=False)
                    self.bot.send_message(chat_id,
                                          'Пользователь @' + victim.username + ' был замьючен (замучен) по просьбе @' + attacker.username + ' .')

            except Exception as e:
                self.bot.send_message(chat_id, 'Неизвестная ошибка')
                print("{!s}\n{!s}".format(type(e), str(e)))

    def unban_user(self, message):
        chat_id = message.chat.id
        attacker = message.from_user
        if attacker.id not in self.get_admins_list(chat_id):
            self.bot.send_message(chat_id, 'У вас недостаточно прав.')
        if message.reply_to_message is None:
            self.bot.send_message(chat_id, 'Укажите человека, которого необходимо разбанить, ответив на его сообщение')
            return
        victim = message.reply_to_message.from_user
        already_in = False
        if already_in:
            self.bot.send_message(chat_id, 'Данный пользователь уже находится в чате')
            return
        chat = self.bot.get_chat(chat_id)
        print(chat.invite_link)
        self.bot.unban_chat_member(chat_id, victim.id)
        self.bot.send_message(chat_id, 'Пользователь разбанен')

    def get_members_info_message(self, chat_id):
        all_users_count = self.bot.get_chat_member_count(chat_id)
        admins = self.bot.get_chat_administrators(chat_id)
        average_users_count = all_users_count - len(admins)
        real_admins = []
        bot_admins = []
        for admin in admins:
            if admin.user.is_bot:
                bot_admins.append(admin)
            else:
                real_admins.append(admin)
        return 'В этом чате ' + str(len(admins)) + ' админов (среди которых ' + str(
            len(bot_admins)) + ' ботов) и ' + str(average_users_count) + ' обычных пользователей'

    def send_members_info(self, chat_id):
        self.bot.send_message(chat_id, self.get_members_info_message(chat_id))

    def leave(self, chat_id):
        self.bot.send_message(chat_id, 'Я ухожу, я сделал всё, что мог')
        time.sleep(1)
        self.bot.leave_chat(chat_id)

    def start(self):
        self.bot.polling(none_stop=True, interval=0)
