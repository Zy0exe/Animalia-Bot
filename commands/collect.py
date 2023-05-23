from functions import *
from import_lib import *

class collect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collect_cooldown = commands.CooldownMapping.from_cooldown(1, 10800, commands.BucketType.user)

    @commands.command()
    @commands.has_role(1101321118436036719)
    @commands.check(in_og_chan)
    async def collect(self, ctx):
        # Check if the player exists in the database
        player_data = get_player_data(ctx.author.id)
        if player_data is None or player_data.get("steam_id") is None:
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description="You do not exist or have not linked your Steam ID. Please use the !link command to link your Steam account.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the user is on cooldown
        bucket = self.collect_cooldown.get_bucket(ctx.message)
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
        coins_earned = random.randint(350, 2000)

        # Update the user's balance in the database
        current_balance = player_data.get("coins", 0)
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

    @collect.error
    async def collect_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Kruger National Park 🤖",
                description=f"You can use this command again in {error.retry_after:.0f} seconds.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(collect(bot))
