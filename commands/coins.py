from functions import *
from import_lib import *

class coins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coins(self, ctx):
        try:
             #Check if the player exists in the database
            db = mysql.connector.connect(
                host="localhost", user="root", password="", database="kruger_park"
            )
            cursor = db.cursor()
            cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (ctx.author.id,))
            player_data = cursor.fetchone()
            if player_data is None or player_data[0] is None:
                embed = discord.Embed(
                    title="Kruger National Park 🤖",
                    description="You do not exist or have not linked your Steam ID. Please use the !link command to link your Steam account.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

            # Get the user's balance from the database
            db = mysql.connector.connect(
                host="localhost", user="root", password="", database="kruger_park"
            )
            cursor = db.cursor()
            cursor.execute(
                "SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,)
            )
            current_balance = cursor.fetchone()[0]

            # Send a message with the user's current balance
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"Your current balance is {current_balance} :coin:.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # If an error occurs, send a message with the error details
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"An error occurred while running the command:\n\n{str(e)}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(coins(bot))
