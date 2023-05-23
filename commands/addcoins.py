from functions import *
from import_lib import *

class addcoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1100915253501497505)
    async def addcoins(self, ctx, member: discord.Member = None, amount: int = 0):
        if amount < 0:
            await ctx.send("You cannot add a negative amount of coins.")
            return

        if member is None:
            member = ctx.author

        # Check if the user has linked their Steam ID
        player_data = get_player_data(member.id)
        if player_data is None:
            await ctx.send(f"{member.mention} has not linked their Steam ID, so coins cannot be added.")
            return

        # Update the user's balance in the database
        current_balance = player_data["coins"]
        new_balance = current_balance + amount
        cursor.execute(
            "UPDATE players SET coins = %s WHERE discord_id = %s",
            (new_balance, member.id),
        )
        db.commit()

        # Fetch the updated user data from the database
        player_data = get_player_data(member.id)

        # Send the command response with the updated user data
        embed = discord.Embed(
            title="Kruger National Park 🤖",
            description=f"{amount} :coin: added to {member.mention}'s balance. New balance is {player_data['coins']} :coin:.",
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
