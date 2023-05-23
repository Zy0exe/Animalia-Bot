from functions import *
from import_lib import *

# Replace with your Steam API key
api_key = "256873BDF8D008E44A7D26C1C9B222A3"

# Replace with the Steam ID of the player you want to fetch information for
player_steam_id = "76561199346987549"

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# never got this to work was supposed to show the amount of players in the server
    @commands.command()
    async def server(self, ctx):
        try:
            # Fetch player information
            player_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={player_steam_id}"
            player_data = requests.get(player_url).json()
            player_info = player_data['response']['players'][0]
            game_id = player_info.get('gameid', '0')

            if game_id != '0':
                # The player is currently playing a game
                print("Game ID:", game_id)

                # Fetch server details
                server_url = f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={api_key}&filter=gameaddr&addr={player_info['gameserverip']}"
                server_data = requests.get(server_url).json()
                print("Server Data:", server_data)

                if 'servers' in server_data and len(server_data['servers']) > 0:
                    # At least one server was found
                    server = server_data['servers'][0]
                    server_name = server['name']
                    players_online = server['players']
                    max_players = server['max_players']
                    server_ping = server['ping']

                    # Create an embed to display the server information
                    embed = discord.Embed(title="Server Information", color=discord.Color.green())
                    embed.add_field(name="Server Name", value=server_name, inline=False)
                    embed.add_field(name="Players Online", value=f"{players_online}/{max_players}", inline=False)
                    embed.add_field(name="Server Ping", value=server_ping, inline=False)

                    await ctx.send(embed=embed)
                else:
                    # No server information available
                    embed = discord.Embed(title="Server Information", description="No server information available.",
                                        color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                # The player is not currently playing any game
                embed = discord.Embed(title="Server Information", description="The player is not currently playing any game.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)

        except Exception as e:
            # Handle any exceptions that occur during server data retrieval
            embed = discord.Embed(title="Server Information", description="Failed to fetch server information.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            print(f"Error: {str(e)}")


async def setup(bot):
    await bot.add_cog(Server(bot))
