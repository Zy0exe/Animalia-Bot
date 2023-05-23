from functions import *
from import_lib import *

animals = {
    "Lion": {
        "price": 30000,
        "image": "<:lionm:1102545517398986812>",
        "slot": "1",
        "quantity": 0,
        "gender": "",
        #"kind": "carn"
    },
    "Croc": {
        "price": 25000,
        "image": "<:Z_Croc:1102543258866958386>",
        "slot": "2",
        "quantity": 0,
        "gender": "",
        #"kind": "carn"
    },
    "Ele": {
        "price": 25000, 
        "image": "<a:elephants:1102543255540867163>", 
        "slot": "3", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Giraffe": {
        "price": 20000, 
        "image": "<:raffe:1102543262109147196>", 
        "slot": "4", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Hippo": {
        "price": 20000, 
        "image": "<:hippo:1102543257575104584>", 
        "slot": "5", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Hyena": {
        "price": 15000, 
        "image": "<:hyena_awwo:1102543253288525844>", 
        "slot": "6", 
        "quantity": 0, 
        "gender": "",
        #"kind": "carn"
    },
    "Leo": {
        "price": 20000, 
        "image": "<:leopardk:1102543260016185486>", 
        "slot": "7", 
        "quantity": 0, 
        "gender": "",
        #"kind": "carn"
    },
    "Meerkat": {
        "price": 3000, 
        "image": "<:meerkat:1102546538842046484>", 
        "slot": "8", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Rhino": {
        "price": 20000, 
        "image": "<:Rhino:1102543251547897968>", 
        "slot": "9", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "WB": {
        "price": 15000, 
        "image": "<:770291595232411678:1102543426718814248>", 
        "slot": "10", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Wilddog": {
        "price": 20000, 
        "image": "<:WildDog:1102543249316519986>", 
        "slot": "11", 
        "quantity": 0, 
        "gender": "",
        #"kind": "carn"
    },
    "Zebra": {
        "price": 15000, 
        "image": "<:Zebra:1102543263258386492>", 
        "slot": "12", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
}

# Connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="kruger_park"
)

# Where the bot can be used
def in_animal_shop(ctx):
    return ctx.channel.name == "🤖︱ʙᴏᴛ-ᴄᴏᴍᴍᴀɴᴅs"

# Where the bot can be used
def in_og_chan(ctx):
    return ctx.channel.name == "🤖︱ᴏɢ-ᴄᴏʟʟᴇᴄᴛ"

# object hook
def object_hook(d):
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = tuple(value)
    return d


# Function to retrieve player data from the database
# def get_player_data(discord_id):
#     sql = "SELECT steam_id, coins, animals FROM players WHERE discord_id = %s"
#     val = (str(discord_id),)
#     cursor.execute(sql, val)
#     result = cursor.fetchone()
#     if result:
#         player_data = {"steam_id": result[0], "coins": result[1], "animals": result[2]}
#         return player_data
#     else:
#         return None

# This was a pain in the ass
def get_player_data(discord_id):
    try:
        cursor.execute("SELECT * FROM players WHERE discord_id = %s", (discord_id,))
        result = cursor.fetchone()
    except mysql.connector.errors.OperationalError as e:
        # Attempt to reconnect to the MySQL server
        db.reconnect(attempts=3, delay=5)
        try:
            cursor.execute("SELECT * FROM players WHERE discord_id = %s", (discord_id,))
            result = cursor.fetchone()
        except Exception as e:
            print(f"DEBUG: Error during database query: {e}")
            result = None
    except Exception as e:
        print(f"DEBUG: Error during database query: {e}")
        result = None

    if result is None:
        return None

    player_data = {
        "steam_id": result[0],
        "discord_id": result[1],
        "coins": result[2],
        "animals": result[3],
    }
    print(f"DEBUG: {discord_id} has {player_data['coins']} coins.")
    return player_data



# Function to clear the players cage
def clear_player_animals(discord_id):
    # Retrieve player data from the database
    player_data = get_player_data(discord_id)
    if not player_data:
        return False

    # Clear the player's animal inventory in the database
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="kruger_park"
    )
    cursor = db.cursor()
    cursor.execute("UPDATE players SET animals = NULL WHERE discord_id = %s", (discord_id,))
    db.commit()

    return True

# Function to retrieve animals data from the database
def get_player_animals(discord_id):
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="kruger_park"
    )
    cursor = db.cursor()
    cursor.execute("SELECT animals FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None:
        return {}

    if player_data[0] is not None:
        try:
            player_animals = json.loads(player_data[0], object_hook=object_hook)
        except json.decoder.JSONDecodeError as e:
            traceback.print_exc()
            player_animals = {}
    else:
        player_animals = {}

    return player_animals

# Create a cursor object to interact with the database
cursor = db.cursor()