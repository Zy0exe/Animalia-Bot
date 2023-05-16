from functions import *
from import_lib import *

class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx, discord_id: int = None):
        # Check if the player exists in the database
        # db = mysql.connector.connect(
        #     host="localhost", user="root", password="", database="kruger_park"
        # )
        # cursor = db.cursor()
        # cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
        # player_data = cursor.fetchone()
        # if player_data is None or player_data[0] is None:
        #     embed = discord.Embed(
        #         title="Kruger National Park 🤖",
        #         description="This player does not exist or has not linked their Steam ID.",
        #         color=0xFF0000,
        #     )
        #     await ctx.send(embed=embed)
        #     return

        cursor = db.cursor()
        cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
        result = cursor.fetchone()
        if result is not None:
            current_balance = result[0]
        else:
            current_balance = 0

        # Get player's owned animals data
        owned_animals_data = get_player_animals(ctx.author.id)
        owned_animals = (
            ", ".join(
                [
                    f"{animal.capitalize()} ({data['price']} :coin:)"
                    for animal, data in owned_animals_data.items()
                ]
            )
            if owned_animals_data
            else ""
        )

         # Shop message
        herb = ""
        carn = ""
        for animal, data in animals.items():
            animal_message = f"{data['image']}{animal}: {data['price']} :coin:\n"
            if data["kind"] == "herb":
                herb += animal_message
            else:
                carn += animal_message
        
        embed = discord.Embed(title="Kruger National Park 🤖", color=0xf1c40f)
        embed.add_field(name="*Carnivores:*", value=carn, inline=True)
        embed.add_field(name="*Herbivores:*", value=herb, inline=True)
        embed.add_field(name="Your coins", value=f":coin:`{current_balance}`", inline=False)
        embed.add_field(name="*How to Buy*", value=f"Example: !buy 20 M or !buy 20 F", inline=False)
        embed.add_field(name="*Subtitle*", value=f"M = Male \n F = Female", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(shop(bot))
