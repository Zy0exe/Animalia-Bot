from import_lib import *


# Connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="kruger_park"
)

# Create a new Discord bot
bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start("MTAwMDEyMzY1NjI3NTUxMzM4NA.GgPdrB.nwizaiJpUNt2DhQMH9ht0fBZ5ryixxFuAbxbw8")

asyncio.run(main())
