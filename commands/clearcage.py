from functions import *
from import_lib import *

class clearcage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1100915253501497505)
    async def clearcage(self, ctx, user: discord.Member):
        # Clear the player's animal inventory in the database
        if clear_player_animals(user.id):
            await ctx.send(f"{user.mention}'s animal inventory has been cleared!")
        else:
            await ctx.send(f"{user.mention} needs to link their Steam ID first using the !link command.")

async def setup(bot):
    await bot.add_cog(clearcage(bot))
