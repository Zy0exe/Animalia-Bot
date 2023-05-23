from functions import *
from import_lib import *

class ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1100915253501497505)
    @commands.check(in_animal_shop)
    async def ban(self, ctx, member: discord.Member):
        # Check if the user has a valid entry in the database
        player_data = get_player_data(member.id)
        if player_data is None:
            await ctx.send("That user does not have a valid entry in the database.")
            return

        # Ask the admin to confirm the ban
        embed = discord.Embed(
            title="Ban Confirmation",
            description=f"Are you sure you want to ban {member.mention}? React with \u2705 to confirm or \u274c to cancel.",
            color=discord.Color.red(),
        )
        confirmation_message = await ctx.send(embed=embed)
        await confirmation_message.add_reaction("\u2705")  # Check mark
        await confirmation_message.add_reaction("\u274c")  # X mark

        # Wait for the admin to react
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\u2705", "\u274c"]
        reaction, _ = await self.bot.wait_for("reaction_add", check=check)

        # If the admin confirmed the ban, add the user's Steam ID to the ban list
        if str(reaction.emoji) == "\u2705":
            with open("C:/servidores/animalia/AnimaliaSurvival/banlist.txt", "a") as f:
                f.write(f"{player_data['steam_id']}\n")
            await ctx.send(f"{member.mention} has been banned from the game.")

        # Otherwise, cancel the ban
        else:
            await ctx.send(f"{member.mention} has not been banned from the game.")
            
async def setup(bot):
    await bot.add_cog(ban(bot))
