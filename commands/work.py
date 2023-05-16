from functions import *
from import_lib import *

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.work_cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    @commands.command()
    async def work(self, ctx):

        # Check if the player exists in the database
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="kruger_park"
        )
        cursor = db.cursor()
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (ctx.author.id,))
        player_data = cursor.fetchone()
        if player_data is None or player_data[0] is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You do not exist or have not linked your Steam ID. Please use the !link command to link your Steam account.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the user is on cooldown
        bucket = self.work_cooldown.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"You can use this command again in {retry_after:.0f} seconds.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Generate a random amount of coins between 500-2000
        coins_earned = random.randint(500, 2000)

        # Update the user's balance in the database
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

        embed = discord.Embed(
            title="Kruger National Park 🤖",
            description=f"You earned {coins_earned} :coin:! Your new balance is {new_balance} :coin:.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"You can use this command again in {error.retry_after:.0f} seconds.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(work(bot))
