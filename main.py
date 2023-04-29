# Discord stuff
import discord
from discord import Embed
from discord import Game
from discord.ext import commands
from discord.ext.commands import cooldown

# Steam Stuff
import steam
from steam import steamid

#SQL Stuff
import mysql.connector

## More needed stuff
import json
import random
import os
import datetime
import traceback
import shutil


# Connect to the database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="kruger_park"
)

# Function to retrieve player data from the database
def get_player_data(discord_id):
    sql = "SELECT steam_id, coins, animals FROM players WHERE discord_id = %s"
    val = (str(discord_id), )
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        player_data = {'steam_id': result[0], 'coins': result[1], 'animals': result[2]}
        return player_data
    else:
        return None

# TODO: Animals table / injection not working yet
def get_player_animals(discord_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )
    cursor = db.cursor()
    cursor.execute("SELECT animals FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None:
        return {}

    try:
        player_animals = json.loads(player_data[0], object_hook=object_hook)
    except json.decoder.JSONDecodeError as e:
        traceback.print_exc()
        player_animals = {}

    return player_animals

def object_hook(d):
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = tuple(value)
    return d



# Create a cursor object to interact with the database
cursor = db.cursor()

# Define the available animals as a dictionary
animals = {
    "Lion": {"price": 100, "image": ":lion_face:", "slot": "1", "quantity": 0},
    "Tiger": {"price": 80, "image": ":tiger:", "slot": "2", "quantity": 0},
    "Bear": {"price": 120, "image": ":bear:", "slot": "3", "quantity": 0}
}

# Initialize a dictionary to store player data in memory
#players = {}

# Create a new Discord bot
bot = commands.Bot(command_prefix = '!', help_command=None, intents= discord.Intents.all())

#Where the bot can be used
def in_animal_shop(ctx):
    return ctx.channel.name == "bot-testing"

# @bot.command()
# async def playerdata(ctx):
#     player_data = players.get(ctx.author.id)
#     if not player_data:
#         await ctx.send("You don't have any player data.")
#     else:
#         await ctx.send(f"Player data: {player_data}")

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
    
    admin_role_id = 1100915253501497505
    if discord.utils.get(ctx.author.roles, id=admin_role_id) is not None:
        embed.add_field(name="Admin Commands:", value="!addcoins [amount] [user] - Add coins to a user's balance.\n!removecoins [amount] [user] - Remove coins from a user's balance.\n!setcoins [amount] [user] - Set a user's balance to a specific amount.\n!resetcage [user] - Remove all animals from a user's cage.", inline=False)

    await ctx.send(embed=embed)

#link discrd and steam command
@bot.command()
@commands.check(in_animal_shop)
async def link(ctx, steam_id: str = None):

    if steam_id is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to enter a steam id!", color=0xff0000)
        await ctx.send(embed=embed)
        return

     # Check if steam_id is exactly 17 characters long
    if len(steam_id) != 17:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="Steam ID must be exactly 17 characters long.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    # Verify that the SteamID64 is valid // Works finally :Zyo
    try:
        steam_id_obj = steam.steamid.SteamID(steam_id)
        if not steam_id_obj.is_valid():
            raise ValueError
    except ValueError:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="Invalid Steam ID format.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kruger_park"
    )

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

#Command to check the amount of coins
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


# Work command so player can get coins
@bot.command()
@cooldown(1, 7200, commands.BucketType.user) # Run command every 2 hours
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
    if current_balance is None:
        current_balance = 0
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

    # Get player's owned animals data
    owned_animals_data = get_player_animals(ctx.author.id)
    owned_animals = ", ".join([f"{animal.capitalize()} ({data['price']} :coin:)" for animal, data in owned_animals_data.items()]) if owned_animals_data else ""

    # Shop message
    shop_message = "Available animals for purchase:\n"
    for animal, data in animals.items():
        shop_message += f"{data['image']}{animal}: {data['price']} :coin:\n"
    embed = discord.Embed(title="Kruger National Park �鴂�", description=shop_message, color=0x00ff00)
    embed.add_field(name="Your coins", value=f":coin:`{current_balance}`", inline=False)

    if owned_animals:
        embed.add_field(name="Your owned animals", value=owned_animals, inline=False)

    embed.add_field(name="*How to Buy*", value=f"Example: !buy 20 M or !buy 20 F", inline=False)
    embed.add_field(name="*Subtitle*", value=f"M = Male \n F = Female", inline=False)

    await ctx.send(embed=embed)

# Define a command to allow players to buy an animal
@bot.command()
@commands.check(in_animal_shop)
async def buy(ctx, animal=None, gender=None):
    if animal is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to specify an animal to buy.", color=0xff0000)
        await ctx.send(embed=embed)
        return    

    # Check if the animal exists
    if animal not in animals:
        await ctx.send(f"{ctx.author.mention}, that animal does not exist.")
        return

    # Check if the player has linked their Steam ID
    player_data = get_player_data(ctx.author.id)
    if player_data is None or player_data['steam_id'] is None:
        await ctx.send(f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.")
        return

    # Check if the player has enough coins to buy the animal
    animal_data = animals[animal]
    price = animal_data["price"]
    if player_data['coins'] < price:
        await ctx.send(f"{ctx.author.mention}, you don't have enough coins to buy this animal.")
        return

    # Deduct the cost of the animal from the player's balance
    new_balance = player_data['coins'] - price
    cursor.execute("UPDATE players SET coins = %s WHERE discord_id = %s", (new_balance, ctx.author.id))
    db.commit()

    # Add the animal to the player's collection
    player_animals = json.loads(player_data.get('animals') or '{}')
    if animal not in player_animals:
        player_animals[animal] = {
            "name": animal,
            "price": price,
            "quantity": 0,  # Set the initial quantity to 0
            "gender": None  # Set the initial gender to None
        }
    if gender is None:
        await ctx.send(f"{ctx.author.mention}, please specify the gender of the {animal} you want to buy.")
        return
    else:
        player_animals[animal]["gender"] = gender
        
    if player_animals[animal]["quantity"] == 0:  # Check if the player doesn't already own the animal
        player_animals[animal]["quantity"] += 1  # Increment the quantity if the animal is already owned
    cursor.execute("UPDATE players SET animals = %s WHERE discord_id = %s", (json.dumps(player_animals), ctx.author.id))
    db.commit()

    await ctx.send(f"{ctx.author.mention}, you have bought a {gender} {animal} for {price} coins.")






# Define a command to allow players to inject an animal into the game
@bot.command()
@commands.check(in_animal_shop)
async def inject(ctx, animal: str = None, slot: int = None):
    if animal is None:
        embed = discord.Embed(title="Kruger National Park",
                              description="You need to specify an animal to inject.",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return

    if slot is None:
        embed = discord.Embed(title="Kruger National Park",
                              description="You need to specify a slot to inject the animal in.",
                              color=0xff0000)
        await ctx.send(embed=embed)
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
    cursor.execute("SELECT steam_id, animals FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None or player_data[0] is None:
        await ctx.send(f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.")
        return

    steam_id = player_data[0]

    # Check if the player has the animal
    player_animals = {}
    if player_data[1] is not None:
        try:
            player_animals = json.loads(player_data[1])
        except json.decoder.JSONDecodeError as e:
            traceback.print_exc()
            await ctx.send(f"{ctx.author.mention}, there was an error decoding your animal data. Please contact an administrator.")
            return

    animal_data = player_animals.get(animal)
    if animal_data is None:
        await ctx.send(f"{ctx.author.mention}, you don't have a {animal}.")
        return

    if animal_data["quantity"] < 1:
        await ctx.send(f"{ctx.author.mention}, you don't have any {animal} left.")
        return

    # Check if the specified slot is valid
    if slot < 1 or slot > 10:
        await ctx.send(f"{ctx.author.mention}, the specified slot is invalid. Please choose a number between 1 and 10.")
        return

    # Inject the animal into the game using the specified slot
    file_name = f"{animal}_M.sav"
    new_file_name = f"{steam_id}_{slot-1}.sav"
    try:
        shutil.copyfile(file_name, new_file_name)
    except FileNotFoundError:
        await ctx.send(f"File {file_name} not found.")
        return

    # Move the file to the correct folder
    folder_name = "PlayerData"
    player_folder = os.path.join(folder_name, steam_id)
    if not os.path.exists(player_folder):
        os.makedirs(player_folder)
    try:
        shutil.move(new_file_name, os.path.join(player_folder, new_file_name))
    except FileNotFoundError:
        await ctx.send(f"File {new_file_name} not found.")
        return

    # Update the player's inventory in the database
    player_animals[animal]["quantity"] -= 1
    player_animals_json = json.dumps(player_animals)
    cursor.execute("UPDATE players SET animals = %s WHERE discord_id = %s", (player_animals_json, discord_id))
    db.commit()

    embed = Embed(title="Kruger National Park",
                  description=f"{ctx.author.mention} has injected a {animal} into the game using slot {slot}.",
                  color=0x00FF00)
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

    # Retrieve player's animal inventory from the database
    player_animals = get_player_animals(ctx.author.id)
    print(player_animals)

    # Fix negative quantities
    for animal, data in player_animals.items():
        if data.get("quantity", 0) < 0:
            data["quantity"] = 0

    # Generate the inventory message
    inventory_message = f"{ctx.author.mention}'s cage:\n"
    inventory_message += f"Balance: {player_data['coins']} coins\n"
    inventory_message += "Animals:\n"
    if player_animals:
        for animal, data in player_animals.items():
            if 'image' in data:
                inventory_message += f"{data['image']} {animal} (quantity: {data.get('quantity', 'N/A')})\n"
            else:
                inventory_message += f"{animal} (quantity: {data.get('quantity', 'N/A')})\n"

    else:
        inventory_message += "You don't have any animals yet.\n"

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
        embed = discord.Embed(title="Kruger National Park �鴂�", description="This player does not exist or has not linked their Steam ID.", color=0xff0000)
        await ctx.send(embed=embed)
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

@bot.command(name='warn')
async def warn_player(ctx, player: discord.Member = None, *, reason: str = None):
    if player is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to specify a player to warn!", color=0x2ecc71)
        await ctx.send(embed=embed)      
        return
    if player == ctx.author:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You cannot warn your self", color=0x2ecc71)
        await ctx.send(embed=embed) 
        return
    if reason is None:
        embed = discord.Embed(title="Kruger National Park �鴂�", description="You need to specify a reason for the warning!", color=0x2ecc71)
        await ctx.send(embed=embed) 
        return

    # Check if the player is already banned
    with open("banlist.txt", "r") as f:
        banned_players = [line.strip() for line in f.readlines()]
    if str(player.id) in banned_players:
        embed = discord.Embed(title="Kruger National Park �鴂�", description=f"{player.mention} is already banned!", color=0x2ecc71)
        await ctx.send(embed=embed) 
        return

    # Insert warning into database
    sql = "INSERT INTO warnings (player_id, reason, warning_date) VALUES (%s, %s, %s)"
    val = (str(player.id), reason, datetime.date.today())
    cursor.execute(sql, val)
    db.commit()

    # Get the number of warnings the player has
    cursor.execute("SELECT COUNT(*) FROM warnings WHERE player_id = %s", (str(player.id),))
    num_warnings = cursor.fetchone()[0]

    # Check if the player has reached the warning limit
    if num_warnings >= 2:
        await ctx.send(f"{player.mention} has reached the maximum number of warnings! They will now receive a strike.")
        await strike_player(ctx, player, reason="Received 2 warnings.")
    else:
        await ctx.send(f"{player.mention} has been warned | Reason: {reason}. They now have {num_warnings} warning(s) remaining.")

@bot.command(name='strike')
async def strike_player(ctx, player: discord.Member = None, *, reason: str = None):
    #"Adds a strike to a player's record and bans them if they have 2 strikes."""
    # Check if the user invoking the command has the required permissions
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send('You do not have permission to use this command.')

    # Check if the bot has permission to ban members
    if not ctx.guild.me.guild_permissions.ban_members:
        return await ctx.send("I don't have permission to ban members.")

    if player is None:
        await ctx.send("You need to specify a player to warn!")
        return

    if player == ctx.author:
        await ctx.send("You cannot warn yourself!")
        return

    if reason is None:
        await ctx.send("You need to specify a reason for the warning!")
        return

    # Get the player's Steam ID from the database
    cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (player.id,))
    result = cursor.fetchone()
    if result is None:
        return await ctx.send('This player is not registered in the database.')

    steam_id = result[0]

    # Check if the player already has 2 strikes
    cursor.execute("SELECT COUNT(*) FROM strikes WHERE player_steam_id = %s", (steam_id,))
    result = cursor.fetchone()
    strike_count = result[0]

    if strike_count >= 2:
        await ctx.send(f'{player.display_name} already has 2 strikes and cannot be given another.')
        return

    # Insert the strike into the database
    sql = "INSERT INTO strikes (admin_id, player_steam_id) VALUES (%s, %s)"
    val = (str(ctx.author.id), steam_id)
    cursor.execute(sql, val)
    db.commit()

    # Check if the player now has 2 strikes
    cursor.execute("SELECT COUNT(*) FROM strikes WHERE player_steam_id = %s", (steam_id,))
    result = cursor.fetchone()
    strike_count = result[0]

    if strike_count == 2:
        # Ban the player and add their Steam ID to the banlist.txt file
        with open('banlist.txt', 'a') as f:
            f.write(steam_id + '\n')
        await ctx.send(f'{player.display_name} has been banned for reaching 2 strikes.')
    else:
        await ctx.send(f'{player.display_name} has been given a strike. They now have {strike_count} strikes.')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help"))
    print("Bot is ready!")

# Run the bot
bot.run("MTEwMDkxMjExMzg2NzgyNTE4NA.Gf_AQu.5dRa4CN1pzyTtgDp_LGX_b3FGbO2tTU9xuognU")