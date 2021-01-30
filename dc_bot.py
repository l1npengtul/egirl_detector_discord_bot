import sys

from discord.ext.commands import Bot
from pathlib import Path
import requests, time, base64, json, traceback, calendar, dotenv, os, discord
import tensorflow as tf
import numpy as np

'''
Runs a discord bot with a trained tensorflow model to detect e-girls
l1npengtul Rho (C) 2020-2021
This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''



# The reason we have a cache is because Mojang's API to get the Skin Data is rate limited to 1 unique search per minute
# per user, so we want to cache these with a timestamp and remove any that are out of date(lets consider it 300 seconds)
# This cache-clear will happen in the on_ready
# Format: key = uuid, values are tuples (image_url, timestamp, gender)
cache = {}

model = tf.keras.models.load_model('trained_models/good_shit/model_1587992893.h5')

env_path = Path('.') / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

global DISC_API
DISC_API = os.getenv('DISCORD_TOKEN')

global BOT_PREFIX
BOT_PREFIX = '!'
client = Bot(command_prefix=BOT_PREFIX)


def get_player_uuid(name):
    # old code from my other project
    # gets the UUID of a player from their username
    try:
        uuid_player = requests.get(
            "https://api.mojang.com/users/profiles/minecraft/" + str(name) + "?at=" + str(int(time.time()))).json()
        return uuid_player['id']
    except:  # in case name is invalid
        return ""


def get_skin_detect(uuid):
    print(uuid)
    # use Mojang's API to get a base64 String then convert it into JSON(python treats JSON as a dictionary, which is
    # good because we dont need any fancy libraries).
    # then that JSON contains the URL for the skin, which we can then grab, put into pre-trained TF Model to get gender
    # then return that gender
    player_json = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()

    # The JSON tag 'properties' contains a list containing more JSON Values
    if uuid in cache:
        print("Wow! Cache Hit!")
        return cache[str(uuid)][2], cache[str(uuid)][0]
    else:
        if uuid != "":
            try:
                print(player_json['properties'][0]['value'])
                print(base64.b64decode(player_json['properties'][0]['value']))
                skindata_url_json = json.loads(base64.b64decode(player_json['properties'][0]['value']))
                print(skindata_url_json["textures"]["SKIN"]["url"])
                skin_url = skindata_url_json["textures"]["SKIN"]["url"]

                if skin_url != "":
                    imagerequest_s1 = requests.get(skin_url)
                    with open(f'bot_img_download/aaaaa.png', 'wb') as out_file:
                        out_file.write(imagerequest_s1.content)
                        out_file.close()

                    img = tf.keras.preprocessing.image.load_img("bot_img_download/aaaaa.png", target_size=(64, 64),
                                                                color_mode='rgba')
                    img_arr = tf.keras.preprocessing.image.img_to_array(img)
                    img_arr = np.array([img_arr])
                    prediction = model.predict(img_arr, batch_size=1, steps=1)
                    # ok i will be honest i really don't know what is happening here
                    # but when prediction[0] is negative, it is female skin
                    # if it is positive it thinks it is male or other
                    # the more negative or positive the number the more "sure" it is

                    if prediction > 0:
                        current_time = calendar.timegm(time.gmtime())
                        cache[str(uuid)] = (skin_url, current_time, "Male or Other")
                        return "Male or Other", skin_url
                    elif prediction < 0:
                        current_time = calendar.timegm(time.gmtime())
                        cache[str(uuid)] = (skin_url, current_time, "Female")
                        return "Female", skin_url
                    else:
                        current_time = calendar.timegm(time.gmtime())
                        cache[str(uuid)] = (skin_url, current_time, "Default")
                        return "Default(Steve or Alex)", skin_url
                else:
                    return "",""
            except:
                print(traceback.format_exc(10))
                return "","",str(sys.exc_info()[0])
        else:
            return "","","Missing UUID Error (Most likely invalid name, or Mojang APIs may be down!)"


async def clean_cache():
    for key in cache:
        current_time = calendar.timegm(time.gmtime())
        print(f"Checking key: {key}")
        if (current_time - cache[key][1]) > 300:
            print(f"Removing key {key} and values {cache[key]}")
            cache.pop(key, None)


@client.command()
async def detect(ctx, name):
    data = get_skin_detect(get_player_uuid(name))
    if data[0] == "" or data[1] == "":
        await ctx.send("There was an error processing your request!")
        await ctx.send(f"Error: {data[2]}")
        if data[2].lower() == "typeerror":
            await ctx.send(f"The service was most likely rate-limited!")
    else:
        await ctx.send(f"{data[1]}\n{name} is most likely using a {data[0]} skin")


@client.event
async def on_ready():
    game = discord.Game("BIG BRAIN TENSORFLOW")
    await client.change_presence(status=discord.Status.online, activity=game)
    await clean_cache()
    print("""
    egirl_detect_dc_bot dc_bot  Copyright (C) 2020-2021  l1npengtul Rho
        This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
        This is free software, and you are welcome to redistribute it
        under certain conditions; type `show c' for details.
    """)


client.run(DISC_API)
