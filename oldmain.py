import discord
from discord import Embed
from discord import Game
from discord.ext import commands
from discord.ext.commands import cooldown

import steam

import mysql.connector

import json
import random
import os

# Set the status message for the bot
game = Game("")
# await client.change_presence(status=discord.Status.online, activity=game)


# Connect to the database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="kruger_park"
)

# Function to retrieve player data from the database
def get_player_data(discord_id):
    sql = "SELECT steam_id, balance FROM players WHERE discord_id = %s"
    val = (str(discord_id), )
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        player_data = {'steam_id': result[0], 'balance': result[1]}
        return player_data
    else:
        return None


def get_player_animals(discord_id):
    sql = "SELECT animals FROM players WHERE discord_id = %s"
    val = (str(discord_id), )
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        return json.loads(str(result[0]))
    else:
        return None


# Create a cursor object to interact with the database
cursor = db.cursor()

# Define the available animals as a dictionary
animals = {
    "Lion": {"price": 100, "image": ":lion_face:", "slot": "1"},
    "Elephant": {"price": 200, "image": ":elephant:", "slot": "2"},
    "Giraffe": {"price": 150, "image": ":giraffe:", "slot": "3"}
}

# Initialize a dictionary to store player data in memory
#players = {}

# Create a new Discord bot
bot = commands.Bot(command_prefix = '!', help_command=None, intents= discord.Intents.all())

def in_animal_shop(ctx):
    return ctx.channel.name == "bot-testing"

# @bot.command()
# async def playerdata(ctx):
#     player_data = players.get(ctx.author.id)
#     if not player_data:
#         await ctx.send("You don't have any player data.")
#     else:
#         await ctx.send(f"Player data: {player_data}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to provide a Steam ID to link your account." , color=0xff0000)
        embed.add_field(name="Example:", value="!link 00000000000000000", inline=False)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to be in the Animal Shop to use this command.", color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="An error occurred while running the command.", color=0xff0000)
        await ctx.send(embed=embed)

# Help command
@bot.command()
@commands.check(in_animal_shop)
async def help(ctx):
    embed = Embed(title="Kruger National Park �鴂�", color=0x00FF00)
    embed.add_field(name="!link [steam_id]", value="Link your Steam account to your Discord account.", inline=False)
    embed.add_field(name="!shop", value="Display the available animals for purchase.", inline=False)
    embed.add_field(name="!buy [animal]", value="Buy an animal from the shop.", inline=False)
    embed.add_field(name="!inject [animal] [slot]", value="Inject an animal into the game using a specified slot.", inline=False)
    embed.add_field(name="!cage", value="Display your current balance and owned animals.", inline=False)
    
    admin_role_id = 1011209441925943316
    if discord.utils.get(ctx.author.roles, id=admin_role_id) is not None:
        embed.add_field(name="Admin Commands:", value="!addcoins [amount] [user] - Add coins to a user's balance.\n!removecoins [amount] [user] - Remove coins from a user's balance.\n!setcoins [amount] [user] - Set a user's balance to a specific amount.\n!resetcage [user] - Remove all animals from a user's cage.", inline=False)

    await ctx.send(embed=embed)


# Define a command to link a player's Steam ID to their Discord account
@bot.command()
@commands.check(in_animal_shop)
async def link(ctx, steam_id):
    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )

    try:
        steam.steamid.SteamID(steam_id)
    except ValueError:
        await ctx.send("Invalid SteamID64 provided.")
        return
        
    # Create a cursor object to interact with the database
    cursor = db.cursor()

    # Get the user ID of the person who typed the command
    discord_id = ctx.author.id

    # Check if the discord_id already exists in the database
    cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()

    # If the discord_id already exists, update the steam_id
    if player_data is not None:
        cursor.execute("UPDATE players SET steam_id = %s WHERE discord_id = %s", (steam_id, discord_id))
        db.commit()
        embed = discord.Embed(title="Kruger National Park �鴂�", description="Your account has been successfully linked!", color=0x00ff00)
        await ctx.send(embed=embed)

    # If the discord_id does not exist, create a new row in the database
    else:
        try:
            cursor.execute("INSERT INTO players (discord_id, steam_id) VALUES (%s, %s)", (discord_id, steam_id))
            db.commit()
            embed = discord.Embed(title="Kruger National Park �鴂�", description="Your account has been successfully linked!", color=0x00ff00)
            await ctx.send(embed=embed)
        except mysql.connector.Error as error:
            print("An error occurred while linking the account:", error)

    # Close the database connection
    db.close()

@bot.command()
async def coins(ctx):
    try:
        # Get the user's balance from the database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kruger_park"
        )
        cursor = db.cursor()
        cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
        current_balance = cursor.fetchone()[0]

        # Send a message with the user's current balance
        # await ctx.send(f"Your current balance is {current_balance} coins.")

        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"Your current balance is {current_balance} :coin:.", color=0x00ff00)
        await ctx.send(embed=embed)
    except Exception as e:
        # If an error occurs, send a message with the error details
        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"An error occurred while running the command:\n\n{str(e)}", color=0xff0000)
        await ctx.send(embed=embed)


# Work command
@bot.command()
@cooldown(1, 7200, commands.BucketType.user)
async def work(ctx):
    # Generate a random amount of coins between 500-2000
    coins_earned = random.randint(500, 2000)

    # Update the user's balance in the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )
    cursor = db.cursor()
    cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
    current_balance = cursor.fetchone()[0]
    new_balance = current_balance + coins_earned
    cursor.execute("UPDATE players SET coins = %s WHERE discord_id = %s", (new_balance, ctx.author.id))
    db.commit()

    #await ctx.send(f"You earned {coins_earned} coins! Your new balance is {new_balance} coins.")

    embed = discord.Embed(title="Kruger National Park �鴂�", description=f"You earned {coins_earned} :coin:! Your new balance is {new_balance} :coin:.", color=0x00ff00)
    await ctx.send(embed=embed)

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You can use this command again in {error.retry_after:.0f} seconds.")


# Define a command to display the available animals for purchase
@bot.command()
@commands.check(in_animal_shop)
async def shop(ctx):

     # Check if the player has linked their Steam ID
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )

    cursor = db.cursor()
    cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
    current_balance = cursor.fetchone()[0]

    # Shop message
    shop_message = "Available animals for purchase:\n"
    for animal, data in animals.items():
        shop_message += f"{data['image']}{animal}: {data['price']} :coin:\n"
    embed = discord.Embed(title="Kruger National Park �鴂�", description=shop_message, color=0x00ff00)
    embed.add_field(name="Your coins", value=f":coin:`{current_balance}`", inline=False)

    embed.add_field(name="*How to Buy*", value=f"Example: !buy 20 M or !buy 20 F", inline=False)
    embed.add_field(name="*Subtile*", value=f"M = Male \n F = Female", inline=False)


    await ctx.send(embed=embed)

# Define a command to allow players to buy an animal
@bot.command()
@commands.check(in_animal_shop)
async def buy(ctx, animal=None):
    if animal is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to specify an animal to buy.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    
    # Check if the animal exists
    if animal not in animals:
        await ctx.send(f"{ctx.author.mention}, that animal does not exist.")
        return

    # Check if the player has linked their Steam ID
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )
    cursor = db.cursor()
    discord_id = ctx.author.id
    cursor.execute("SELECT steam_id, balance, FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None or player_data[0] is None:
        await ctx.send(f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.")
        return

    # Check if the player has enough coins to buy the animal
    animal_data = animals[animal]
    price = animal_data["price"]
    if player_data[1] < price:
        await ctx.send(f"{ctx.author.mention}, you don't have enough coins to buy this animal.")
        return

    # Deduct the cost of the animal from the player's balance
    new_balance = player_data[1] - price
    cursor.execute("UPDATE players SET balance = %s WHERE discord_id = %s", (new_balance, discord_id))
    db.commit()

    # Add the animal to the player's collection
    player_animals = json.loads(str(player_data[2]))
    if animal not in player_animals:
        player_animals[animal] = {
            "name": animal,
            "price": price
        }
    cursor.execute("UPDATE players = %s WHERE discord_id = %s", (json.dumps(player_animals), discord_id))
    db.commit()

    # Save file to player's folder
    steam_id = player_data[0]
    file_path = f"C:/Users/Dylan/Desktop/Discord-Bots/ParkGame{steam_id}/{animal}.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(f"This is your {animal} file!")
    
    await ctx.send(f"{ctx.author.mention}, you have bought a {animal} for {price} coins.")



# Define a command to allow players to inject an animal into the game
@bot.command()
@commands.check(in_animal_shop)
async def inject(ctx, animal: str, slot: int):
    # Check if the player has linked their Steam ID
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )
    cursor = db.cursor()
    discord_id = ctx.author.id
    cursor.execute("SELECT steam_id, animals FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None or player_data[0] is None:
        await ctx.send(f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.")
        return

    # Check if the player has the animal
    player_animals = json.loads(str(player_data[1]))
    animal_data = player_animals.get(animal)
    if not animal_data:
        await ctx.send(f"{ctx.author.mention}, you don't have a {animal}.")
        return

    # Check if the specified slot is valid
    if slot < 1 or slot > 3:
        await ctx.send(f"{ctx.author.mention}, the specified slot is invalid.")
        return

    # Inject the animal into the game using the specified slot
    # TODO: Make the bot place the files that would be place holders provided by us inside the correct player folder
           # This can be achived by telling the bot to look for the folder with the same steam_id from the person that executed the command.
    embed = Embed(title="Kruger National Park �鴂�",
                  description=f"{ctx.author.mention} has injected a {animal} into the game using slot {slot}.",
                  color=0x00FF00)
    embed.set_image(url=animal_data["image"])
    await ctx.send(embed=embed)


# Define a command to show the player's balance and owned animals
@bot.command()
@commands.check(in_animal_shop)
async def cage(ctx):
    # Retrieve player data from the database
    player_data = get_player_data(ctx.author.id)
    if not player_data:
        await ctx.send(f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.")
        return

    inventory_message = f"{ctx.author.mention}'s cage:\n"
    inventory_message += f"Balance: {player_data['balance']} coins\n"

    animals_data = get_player_animals(ctx.author.id)
    if animals_data:
        inventory_message += "Animals:\n"
        for animal, data in animals_data.items():
            inventory_message += f"{animal}: {data['image']}\n"

    await ctx.send(inventory_message)

@bot.command()
async def giveadmin(ctx, discord_id: int=None):
    # Check if the user has permission to use the command
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You do not have permission to use this command.", color=0xff0000)
        await ctx.send(embed=embed)
        # await ctx.send("You do not have permission to use this command.")
        return
    
    # Check if there is an actual discord id
    if discord_id is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to provide a Discord ID to give admin access.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    # Check if the player exists in the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )
    cursor = db.cursor()
    cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None or player_data[0] is None:
        await ctx.send("This player does not exist or has not linked their Steam ID.")
        return

    # Add the Steam ID to the "AdminList" text file
    with open("AdminList.txt", "a") as f:
        f.write(player_data[0] + "\n")
    user = bot.get_user(discord_id)
    if user:
        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"Admin List {user.mention} | has been added to the admin list.", color=0x2ecc71)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"User with ID {discord_id} has been added to the admin list.", color=0x2ecc71)
        await ctx.send(embed=embed)
    db.close()

@bot.command()
async def removeadmin(ctx, discord_id: int=None):
    # Check if the user has permission to use the command
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You do not have permission to use this command.", color=0xff0000)
        await ctx.send(embed=embed)
        # await ctx.send("You do not have permission to use this command.")
        return

    # Check if there is an actual discord id
    if discord_id is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to provide a Discord ID to remove admin access.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    # Check if the player exists in the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )
    cursor = db.cursor()
    cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None or player_data[0] is None:
        await ctx.send("This player does not exist or has not linked their Steam ID.")
        return

    # Remove the Steam ID from the "AdminList" text file
    with open("AdminList.txt", "r") as f:
        admin_list = f.readlines()
    with open("AdminList.txt", "w") as f:
        for line in admin_list:
            if player_data[0] not in line:
                f.write(line)
    user = bot.get_user(discord_id)
    if user:
        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"Admin List {user.mention} | has been removed to the admin list.", color=0x2ecc71)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"User with ID {discord_id} has been removed to the admin list.", color=0x2ecc71)
        await ctx.send(embed=embed)
    db.close()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help"))

    #await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
    # Bot ready message
    print("Bot is ready!")

# Run the bot
bot.run("MTAwMDEyMzY1NjI3NTUxMzM4NA.GOt4oq.4_Up_06SRa4Ub8ABRms7I2jU_oyozPCOSGv3-s")
