from functions import *
from import_lib import *

class warn_player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="warn")
    async def warn_player(self, ctx, player: discord.Member = None, *, reason: str = None):
        if player is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to specify a player to warn!",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
            return

        if player == ctx.author:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You cannot warn yourself",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
            return

        if reason is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to specify a reason for the warning!",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
            return

        # Check if the player is already banned
        with open("C:/servidores/animalia/AnimaliaSurvival/banlist.txt", "r") as f:
            banned_players = [line.strip() for line in f.readlines()]
        if str(player.id) in banned_players:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"{player.mention} is already banned!",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
            return

        # Insert warning into database
        sql = "INSERT INTO warnings (player_id, reason, warning_date) VALUES (%s, %s, %s)"
        val = (str(player.id), reason, datetime.date.today())
        cursor.execute(sql, val)
        db.commit()

        # Get the number of warnings the player has
        cursor.execute(
            "SELECT COUNT(*) FROM warnings WHERE player_id = %s", (str(player.id),)
        )
        num_warnings = cursor.fetchone()[0]

        # Check if the player has reached the warning limit
        if num_warnings >= 2:
            await ctx.send(
                f"{player.mention} has reached the maximum number of warnings! They will now receive a strike."
            )
            await strike_player(ctx, player, reason="Received 2 warnings.")
        else:
            await ctx.send(
                f"{player.mention} has been warned | Reason: {reason}. They now have {num_warnings} warning(s) remaining."
            )

async def setup(bot):
    await bot.add_cog(warn_player(bot))
