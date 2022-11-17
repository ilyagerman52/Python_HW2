# from bot import Bot


# bot_username = Bot.bot_username

bot_username = 'geoguessr_banner_bot'

ADVICE_MESSAGE = f"Для вывода справки напишите <code> @{bot_username} help </code>."

HELP_MESSAGE = "Справка.\n\n" \
               f"<code>@{bot_username} help</code> — команда для вывода справки. \n" \
               f"<code>@{bot_username} ban [time]</code> — команда для бана пользователя на время [time]. " \
               "По умолчанию пользователь будет кикнут." \
               "Необходимо ответить на сообщение пользователя этой командой, чтобы он был забанен. \n" \
               f"<code>@{bot_username} kick</code> — команда для кика пользователя." \
               "Необходимо ответить на сообщение пользователя этой командой, чтобы он был кикнут. \n" \
               f"<code>@{bot_username} mute</code> — команда для мута пользователя." \
               f"<code>@{bot_username} unban</code> — команда для разбана пользователя. \n" \
               f"<code>@{bot_username} leave</code> — команда для выхода бота из чата. \n" \
               f"<code>@{bot_username} get_chat_info</code> — команда для получения статистики чата. \n" \
               f"<code>@{bot_username} open_interface</code> — команда для получения интерфейса для работы с ботом"

MISUNDERSTAND_MESSAGE = f"Я не понял вашу команду. Для вывода справки напишите \n <code>@{bot_username} help</code>"

HELLO_NEW_MEMBER_MESSAGE = f"Мы рады привествовать вас в нашем чате. Вилкой в глаз или что-то другое выберешь?"

HELLO_MESSAGE =  f"Рад всех приветствовать. Для вывода справки напишите \n <code>@{bot_username} help</code>"
