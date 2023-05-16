from functions import *
from import_lib import *

class link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def link(self, ctx, steam_id: str = None):
        if steam_id is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to enter a steam id!",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if steam_id is exactly 17 characters long
        if len(steam_id) != 17:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="Steam ID must be exactly 17 characters long.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Verify that the SteamID64 is valid // Works finally :Zyo
        try:
            steam_id_obj = steam.steamid.SteamID(steam_id)
            if not steam_id_obj.is_valid():
                raise ValueError
        except ValueError:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="Invalid Steam ID format.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Connect to the database
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="kruger_park"
        )

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Get the user ID of the person who typed the command
        discord_id = ctx.author.id

        # Check if the discord_id already exists in the database
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
        player_data = cursor.fetchone()

        # If the discord_id already exists, update the steam_id
        if player_data is not None:
            cursor.execute(
                "UPDATE players SET steam_id = %s WHERE discord_id = %s",
                (steam_id, discord_id),
            )
            db.commit()
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="Your account has been successfully linked!",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)

        # If the discord_id does not exist, create a new row in the database
        else:
            try:
                cursor.execute(
                    "INSERT INTO players (discord_id, steam_id) VALUES (%s, %s)",
                    (discord_id, steam_id),
                )
                db.commit()
                embed = discord.Embed(
                    title="Kruger National Park 🤖",
                    description="Your account has been successfully linked!",
                    color=0x00FF00,
                )
                await ctx.send(embed=embed)
            except mysql.connector.Error as error:
                print("An error occurred while linking the account:", error)

        # Close the database connection
        db.close()

async def setup(bot):
    await bot.add_cog(link(bot))



