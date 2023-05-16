from functions import *
from import_lib import *

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = Embed(title="Kruger National Park 🤖", color=0xf1c40f)
        embed.add_field(
            name="!link [steam_id]",
            value="Link your Steam account to your Discord account.",
            inline=False,
        )
        embed.add_field(
            name="!shop", value="Display the available animals for purchase.", inline=False
        )
        embed.add_field(
            name="!buy [animal]", value="Buy an animal from the shop.", inline=False
        )
        embed.add_field(
            name="!inject [animal] [slot]",
            value="Inject an animal into the game using a specified slot.",
            inline=False,
        )
        embed.add_field(
            name="!cage",
            value="Display your current balance and owned animals.",
            inline=False,
        )

        admin_role_id = 1100915253501497505
        if discord.utils.get(ctx.author.roles, id=admin_role_id) is not None:
            embed.add_field(
                name="Admin Commands:",
                value="!addcoins [amount] [user] - Add coins to a user's balance.\n!removecoins [amount] [user] - Remove coins from a user's balance.\n!resetcage [user] - Remove all animals from a user's cage.\n !addadmin [discord_id] - grant admin to a user in game.\n !removeadmin [discord_id] - remove admin from a user in game.\n !ban [discord_id] - ban a player in game.\n !warn [discord_id] [reason] - warn a player.\n !strike [discord_id] [reason] - give a strike to a player (2 strikes makes the player banned in-game)",
                inline=False,
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))



