from functions import *
from import_lib import *

class addcoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1100915253501497505)
    async def addcoins(self, ctx, member: discord.Member, amount: int):
        if amount < 0:
            await ctx.send("You cannot add a negative amount of coins.")
            return
        
        # Check if the user has linked their Steam ID
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="kruger_park"
        )
        cursor = db.cursor()
        cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (member.id,))
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f"{member.mention} has not linked their Steam ID, so coins cannot be added.")
            return

        # Update the user's balance in the database
        current_balance = result[0]
        new_balance = current_balance + amount
        cursor.execute(
            "UPDATE players SET coins = %s WHERE discord_id = %s",
            (new_balance, member.id),
        )
        db.commit()

        embed = discord.Embed(
            title="Kruger National Park 🤖",
            description=f"{amount} :coin: added to {member.mention}'s balance. New balance is {new_balance} :coin:.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    @addcoins.error
    async def addcoins_error(ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Sorry, only admins can use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please use the command correctly: !addcoins {user} {amount}")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(addcoins(bot))
