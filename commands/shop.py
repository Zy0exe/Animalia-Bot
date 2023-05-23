from functions import *
from import_lib import *

class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(in_animal_shop)
    async def shop(self, ctx):
        # Check if the player has linked their Steam ID
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="kruger_park"
        )

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
        shop_message = "Available animals for purchase:\n"
        for animal, data in animals.items():
            shop_message += f"{data['image']}{animal}: {data['price']} :coin:\n"
        embed = discord.Embed(
            title="Kruger National Park 🤖", description=shop_message, color=0xf1c40f
        )
        embed.add_field(name="Your coins", value=f":coin:`{current_balance}`", inline=False)

        if owned_animals:
            embed.add_field(name="Your owned animals", value=owned_animals, inline=False)

        embed.add_field(
            name="*How to Buy*", value=f"Example: !buy animal M or !buy animal F", inline=False
        )
        embed.add_field(name="*Note*", value=f"The animal name *NEEDS* to be the exact same as its shown in the shop!", inline=False)
        embed.add_field(name="*Genders*", value=f"M = Male \n F = Female", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(shop(bot))
