from functions import *
from import_lib import *

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(in_animal_shop)
    async def pay(self, ctx, member: discord.Member, amount: int):
        # Check if the amount is valid
        if amount <= 0:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="The amount must be greater than 0.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the user has enough coins
        sender_data = get_player_data(ctx.author.id)
        if sender_data is None or sender_data["coins"] < amount:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You do not have enough coins to complete this transaction.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Subtract coins from the sender's balance
        cursor.execute(
            "UPDATE players SET coins = coins - %s WHERE discord_id = %s",
            (amount, ctx.author.id),
        )
        db.commit()

        # Add coins to the recipient's balance
        recipient_data = get_player_data(member.id)
        if recipient_data is None:
            insert_player_data(member.id)
            recipient_data = get_player_data(member.id)

        cursor.execute(
            "UPDATE players SET coins = coins + %s WHERE discord_id = %s",
            (amount, member.id),
        )
        db.commit()

        # Send a confirmation message
        embed = discord.Embed(
            title="Kruger National Park 🤖",
            description=f"You paid {member.mention} {amount} coins.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    @pay.error
    async def pay_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="Please mention a valid user.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="Please use the command correctly: !pay {user} {amount}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"An error occurred: {str(error)}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Pay(bot))
