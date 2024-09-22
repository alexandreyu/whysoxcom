from commands import *


@bot.event
async def on_ready():
    print(bot.commands)
    print(f"{bot.user} is online")


@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    guild = channel.guild
    guild_name = guild.name if guild else "Private Message"
    current_time = datetime.now().strftime("%H:%M")
    print(f"[{current_time}] {guild_name}/#{channel.name}/@{author.name}: {message.content}")


bot.run(os.getenv("TOKEN"))
