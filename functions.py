from functions import *
from import_lib import *

animals = {
    "Lion": {
        "price": 100,
        "image": ":lion_face:",
        "slot": "1",
        "quantity": 0,
        "gender": "",
    },
    "Tiger": {
        "price": 80,
        "image": ":tiger:",
        "slot": "2",
        "quantity": 0,
        "gender": "",
    },
    "Bear": {"price": 120, "image": ":bear:", "slot": "3", "quantity": 0, "gender": ""},
}

# Connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="kruger_park"
)

# Where the bot can be used
def in_animal_shop(ctx):
    return ctx.channel.name == "bot-testing"

# object hook
def object_hook(d):
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = tuple(value)
    return d


# Function to retrieve player data from the database
def get_player_data(discord_id):
    sql = "SELECT steam_id, coins, animals FROM players WHERE discord_id = %s"
    val = (str(discord_id),)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        player_data = {"steam_id": result[0], "coins": result[1], "animals": result[2]}
        return player_data
    else:
        return None

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