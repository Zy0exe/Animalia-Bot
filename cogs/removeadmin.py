from functions import *
from import_lib import *

class removeadmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def removeadmin(self, ctx, discord_id: int = None):
        # Check if the user has permission to use the command
        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You do not have permission to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            # await ctx.send("You do not have permission to use this command.")
            return

        # Check if there is an actual discord id
        if discord_id is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to provide a Discord ID to remove admin access.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the player exists in the database
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="kruger_park"
        )
        cursor = db.cursor()
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
        player_data = cursor.fetchone()
        if player_data is None or player_data[0] is None:
            await ctx.send("This player does not exist or has not linked their Steam ID.")
            return

        # Remove the Steam ID from the "AdminList" text file
        with open("AdminList.txt", "r") as f:
            admin_list = f.readlines()
        with open("AdminList.txt", "w") as f:
            for line in admin_list:
                if player_data[0] not in line:
                    f.write(line)
        user = bot.get_user(discord_id)
        if user:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"Admin List {user.mention} | has been removed to the admin list.",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"User with ID {discord_id} has been removed to the admin list.",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
        db.close()

async def setup(bot):
    await bot.add_cog(removeadmin(bot))
