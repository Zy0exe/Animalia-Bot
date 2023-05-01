from functions import *
from import_lib import *

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(in_animal_shop)
    @cooldown(1, 7200, commands.BucketType.user)
    async def work(self, ctx):
        # Generate a random amount of coins between 500-2000
        coins_earned = random.randint(500, 2000)

        # Update the user's balance in the database
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="kruger_park"
        )
        cursor = db.cursor()
        cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
        current_balance = cursor.fetchone()[0]
        if current_balance is None:
            current_balance = 0
        new_balance = current_balance + coins_earned
        cursor.execute(
            "UPDATE players SET coins = %s WHERE discord_id = %s",
            (new_balance, ctx.author.id),
        )
        db.commit()

        # await ctx.send(f"You earned {coins_earned} coins! Your new balance is {new_balance} coins.")

        embed = discord.Embed(
            title="Kruger National Park 🤖",
            description=f"You earned {coins_earned} :coin:! Your new balance is {new_balance} :coin:.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You can use this command again in {error.retry_after:.0f} seconds."
            )

async def setup(bot):
    await bot.add_cog(work(bot))



