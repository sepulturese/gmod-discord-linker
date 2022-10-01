import httplib
import botlib


# [ РЕАЛИЗАЦИЯ ОБРАБОТЧИКОВ HTTP ЗАПРОСОВ ОТ КЛИЕНТА ]
def get_all_discord_nicknames(context):
    return botlib.DISCORD_USERS_DATA


if __name__ == "__main__":
    # Запуск HTTP сервера в отдельном потоке.
    server = httplib.ValveHTTPRequestsHandler()
    server.add_handler("getAllDiscordPlayers", get_all_discord_nicknames)
    server.run()

    # Асинхронный запуск Discord бота
    intents = botlib.discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = botlib.Bot(intents=intents)
    client.run('MTAyNTY4ODU2ODMwNTI4NzIyOQ.G8auZ-.zhQ6Flnkf6FMtNqi5KJ_OQnzte_vWYpsbct__w')
