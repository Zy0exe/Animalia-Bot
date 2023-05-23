from functions import *
from import_lib import *

# @Zyo

class ainject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1101301737761030205)
    async def ainject(self, ctx, user: discord.User, animal: str = None, gender: str = None, slot: int = None):
        if animal is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to specify an animal to inject.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if gender is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to specify a gender for the animal.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if slot is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You need to specify a slot to inject the animal in.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Retrieve the Discord ID of the mentioned user
        discord_id = user.id

        # Retrieve player data from the database
        player_data = get_player_data(discord_id)  # Replace with your own method to retrieve player data

        # Check if the player data exists
        if player_data is None:
            await ctx.send(f"{user.mention} has not linked their Steam ID.")
            return

        # Retrieve the Steam ID associated with the Discord ID
        steam_id = player_data["steam_id"]

        # Inject the animal into the game using the specified slot
        folder_name = "C:/servidores/animalia/AnimaliaSurvival/Saved/SaveGames/PlayerData/testLevel"
        file_name = f"C:/servidores/animalia/AnimaliaSurvival/Animalia-Bot/AnimalTemplates/{animal}_{gender}.sav"
        player_folder = os.path.join(folder_name, steam_id)
        new_file_name = f"{steam_id}_{slot-1}.sav"
        new_file_path = os.path.join(player_folder, new_file_name)

        # Check if the specified slot is valid
        if slot < 1 or slot > 10:
            embed = Embed(
                description="The specified slot is invalid. Please choose a number between 1 and 10."
            )
            await ctx.send(embed=embed)
            return

        if os.path.exists(new_file_path):
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"The slot {slot} is already occupied. Do you want to proceed with the injection and overwrite the existing animal data?",
                color=0xFF0000,
            )
            confirmation_msg = await ctx.send(embed=embed)
            await confirmation_msg.add_reaction("✅")  # Add a checkmark reaction to confirm
            await confirmation_msg.add_reaction("❌")  # Add a cross reaction to cancel

            def check(reaction, user):
                return (
                    user == ctx.author
                    and str(reaction.emoji) in ["✅", "❌"]
                    and reaction.message.id == confirmation_msg.id
                )

            try:
                reaction, _ = await ctx.bot.wait_for(
                    "reaction_add", timeout=60, check=check
                )
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="Kruger National Park 🤖",
                    description="Confirmation timed out.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

            if str(reaction.emoji) == "❌":
                embed = discord.Embed(
                    title="Kruger National Park 🤖",
                    description="Injection canceled.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

        try:
            shutil.copy(file_name, new_file_path)
            print(f"{file_name} copied to {new_file_path}")
        except FileNotFoundError:
            await ctx.send(f"File {file_name} not found.")
            return

        embed = Embed(
            title="Kruger National Park 🤖",
            description=f"{animal} has been injected into the game for {user.mention} using slot {slot}.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)
        print(f"Animal injected into slot {slot} for player {steam_id}")

async def setup(bot):
    await bot.add_cog(ainject(bot))