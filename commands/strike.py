from functions import *
from import_lib import *

class strike_player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="strike")
    async def strike_player(self, ctx, player: discord.Member = None, *, reason: str = None):
        # "Adds a strike to a player's record and bans them if they have 2 strikes."""
        # Check if the user invoking the command has the required permissions
        if not ctx.author.guild_permissions.administrator:
            embed = Embed(description="You do not have permission to use this command.")
            return await ctx.send(embed=embed)

        # Check if the bot has permission to ban members
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = Embed(description="I don't have permission to ban members.")
            return await ctx.send(embed=embed)

        if player is None:
            embed = Embed(description="You need to specify a player to warn!")
            await ctx.send(embed=embed)
            return

        if player == ctx.author:
            embed = Embed(description="You cannot warn yourself!")
            await ctx.send(embed=embed)
            return

        if reason is None:
            embed = Embed(description="You need to specify a reason for the warning!")
            await ctx.send(embed=embed)
            return

        # Get the player's Steam ID from the database
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (player.id,))
        result = cursor.fetchone()
        if result is None:
            embed = Embed(description="This player is not registered in the database.")
            return await ctx.send(embed=embed)

        steam_id = result[0]

        # Check if the player already has 2 strikes
        cursor.execute(
            "SELECT COUNT(*) FROM strikes WHERE player_steam_id = %s", (steam_id,)
        )
        result = cursor.fetchone()
        strike_count = result[0]

        if strike_count >= 2:
            await ctx.send(
                f"{player.display_name} already has 2 strikes and cannot be given another."
            )
            return

        # Insert the strike into the database
        sql = "INSERT INTO strikes (admin_id, player_steam_id) VALUES (%s, %s)"
        val = (str(ctx.author.id), steam_id)
        cursor.execute(sql, val)
        db.commit()

        # Check if the player now has 2 strikes
        cursor.execute(
            "SELECT COUNT(*) FROM strikes WHERE player_steam_id = %s", (steam_id,)
        )
        result = cursor.fetchone()
        strike_count = result[0]

        if strike_count == 2:
            # Ban the player and add their Steam ID to the banlist.txt file
            with open("C:\servidores/animalia/AnimaliaSurvival/Saved/SaveGames/banlist.txt", "a") as f:
                f.write(steam_id + "\n")
            await ctx.send(f"{player.display_name} has been banned for reaching 2 strikes.")
        else:
            await ctx.send(
                f"{player.display_name} has been given a strike. They now have {strike_count} strikes."
            )

async def setup(bot):
    await bot.add_cog(strike_player(bot))
