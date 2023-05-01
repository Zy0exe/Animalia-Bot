from functions import *
from import_lib import *

class cage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cage(self, ctx):
        # Retrieve player data from the database
        player_data = get_player_data(ctx.author.id)
        if not player_data:
            await ctx.send(
                f"{ctx.author.mention}, you need to link your Steam ID first using the !link command."
            )
            return

        # Retrieve player's animal inventory from the database
        player_animals = get_player_animals(ctx.author.id)
        print(player_animals)

        # Fix negative quantities
        for animal, data in player_animals.items():
            if data.get("quantity", 0) < 0:
                data["quantity"] = 0

        # Generate the inventory message
        inventory_embed = Embed(title=f"{ctx.author.display_name}'s cage")
        inventory_embed.add_field(
            name="Balance", value=f"{player_data['coins']} coins", inline=False
        )
        inventory_embed.add_field(name="Animals", value="\u200b", inline=False)

        if player_animals:
            for animal, data in player_animals.items():
                if "image" in data:
                    inventory_embed.add_field(
                        name=f"{data['image']} {animal}",
                        value=f"Quantity: {data.get('quantity', 'N/A')}",
                        inline=False,
                    )
                else:
                    inventory_embed.add_field(
                        name=animal,
                        value=f"Quantity: {data.get('quantity', 'N/A')}",
                        inline=False,
                    )
        else:
            inventory_embed.add_field(
                name="Kruger National Park 🤖",
                value="You don't have any animals yet.",
                inline=False,
            )
        await ctx.send(embed=inventory_embed)

async def setup(bot):
    await bot.add_cog(cage(bot))
