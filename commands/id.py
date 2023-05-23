from functions import *
from import_lib import *
import discord

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def player(self, ctx, member: discord.Member):
        # Check if the user has a valid entry in the database
        player_data = get_player_data(member.id)
        if player_data is None:
            await ctx.send("That user does not have a valid entry in the database.")
            return

        # Retrieve player's coins and Steam ID
        coins = player_data.get('coins', 0)
        steam_id = player_data.get('steam_id', 'Not available')

        embed = discord.Embed(title="Player Information", color=discord.Color.blue())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Steam ID", value=steam_id, inline=False)
        embed.add_field(name="Coins", value=coins, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))
