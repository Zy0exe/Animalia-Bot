from functions import *
from import_lib import *

#this was the hardest for sure

class buy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(in_animal_shop)
    @commands.command()
    async def buy(self, ctx, animal=None, gender=None):
        if animal is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to specify an animal to buy.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the animal exists
        if animal not in animals:
            await ctx.send(f"{ctx.author.mention}, that animal does not exist.")
            return

        player_data = get_player_data(ctx.author.id)
        # Check if the player has linked their Steam ID
        if player_data is None or player_data["steam_id"] is None:
            await ctx.send(
                f"{ctx.author.mention}, you need to link your Steam ID first using the !link command."
            )
            return

        # Check if the player has enough coins to buy the animal
        animal_data = animals[animal]
        price = round(float(animal_data["price"]))  # convert price to float and round
        if player_data["coins"] < price:
            print(f"DEBUG: {ctx.author} does not have enough coins to buy {animal}.")
            print(f"DEBUG: {ctx.author} has {player_data['coins']} coins, but needs {price} coins.")
            await ctx.send(
                f"{ctx.author.mention}, you don't have enough coins to buy this animal."
            )
            return


        # Deduct the cost of the animal from the player's balance
        new_balance = player_data["coins"] - price
        cursor.execute(
            "UPDATE players SET coins = %s WHERE discord_id = %s",
            (new_balance, ctx.author.id),
        )
        db.commit()

        # Update the player's data with the new balance
        player_data["coins"] = new_balance

         # Add the animal to the player's collection
        player_animals = json.loads(player_data.get("animals") or "{}")
        if animal not in player_animals:
            player_animals[animal] = {
                "name": animal,
                "price": price,
                "quantity": 1,  # Set the initial quantity to 1
                "genders": [],  # Create an empty list to store genders
            }
        else:
            player_animals[animal]["quantity"] += 1  # Increment the quantity if the animal is already owned

        # Increment the quantity of the gender if provided
        if gender:
            gender_exists = False
            for gender_data in player_animals[animal]["genders"]:
                if gender_data["gender"] == gender:
                    gender_data["quantity"] += 1
                    gender_exists = True
                    break

            if not gender_exists:
                # Add the gender to the list of genders for this animal
                player_animals[animal]["genders"].append({"gender": gender, "quantity": 1})

        cursor.execute(
            "UPDATE players SET animals = %s WHERE discord_id = %s",
            (json.dumps(player_animals), ctx.author.id),
        )
        db.commit()

        embed = discord.Embed(
            title="Kruger National Park 🤖",
            description=f"{ctx.author.mention}, you have bought a {gender} {animal} for {price} coins.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(buy(bot))
