import discord
from discord.ext import commands, ipc

class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="360noscope")

    async def on_ready(self):
        print("Bot is ready")
    
    async def on_ipc_ready(self):
        print("Ipc server is ready")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

my_bot = MyBot(command_prefix = "$$", intents=discord.Intents.all())

@my_bot.ipc.route()
async def get_guild_count(data):
    return len(my_bot.guilds)

@my_bot.ipc.route()
async def get_guild_ids(data):
    final = []
    for guild in my_bot.guilds:
        final.append(guild.id)
    return final

@my_bot.ipc.route()
async def get_guild(data):
    guild = my_bot.get_guild(data.guild_id)
    if guild is None:
        return None
    
    guild_data = {
        "name": guild.name,
        "id": guild.id,
        "prefix" : "$$"
    }
    return guild_data

@my_bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.mention}(or {ctx.author.name}#{ctx.author.discriminator})")

my_bot.ipc.start()
my_bot.run("OTUyNjEwNzIwODY3MDI5MDMy.GUxqD8.zpH8kM-XYFS5K2DiJha0ymqjknt1d31HlMk088")