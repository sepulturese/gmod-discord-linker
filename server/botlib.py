import discord


DISCORD_USERS_DATA = []


class Bot(discord.Client):
    async def on_ready(self):
        print("I'm ready to work.")

    async def on_message(self, message):
        # ограничитель для тестирования
        if str(message.author) == "Подольск#7675":
            if message.content == "!update":
                async for member in message.guild.fetch_members():
                    DISCORD_USERS_DATA.append({
                        "uid": member.id,
                        "nick": member.nick,
                        "name": member.name,
                        "avatar": member.display_avatar.url
                    })
