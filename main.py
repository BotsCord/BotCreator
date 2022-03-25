from InquirerPy import inquirer
import asyncio
import os
from discord.ext import commands
import discord
import traceback
import emoji
import requests

PLUGINS_REPO = "http://localhost:8080/plugins"

config = {
    "token": "",
    "extensions": [x for x in os.listdir("extensions") if x.endswith(".py")],
    "prefix": "!",
}

bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())

print("Ready to start raid tool from " + __file__)


def run_choices(choice):
    if choice == "Choose token":
        token = inquirer.secret(message="Enter your token").execute()
        config["token"] = token

    if choice == "Choose extensions":
        extensions = inquirer.checkbox(
            message="Choose extensions", choices=config["extensions"]
        ).execute()
        config["extensions"] = extensions

    if choice == "Choose prefix":
        prefix = inquirer.text(message="Enter your prefix").execute()
        config["prefix"] = prefix
        bot.commands_prefix = config["prefix"]

    if choice == "Run":
        if config["token"] == "":
            print("You need to enter a token")
            menu()
        try:
            bot.run(config["token"])
        except discord.LoginFailure:
            print("Invalid token")
        except:
            pass
    
    if choice == "Install plugins":
        r = requests.get(PLUGINS_REPO)
        
        data = r.json()
        plugins = data["plugins"]
        to_install = inquirer.checkbox(message="Select the plugins you want to install", choices=[x["name"] for x in plugins]).execute()
        urls = [x["url"] for x in plugins if x["name"] in to_install]
        for x in range(len(urls)):
            f = open(f"extensions/{to_install[x]}.py", "wb")
            re = requests.get(urls[x])
            f.write(re.content)
            
    
    if choice == "Exit":
        exit()


def menu():
    choice = inquirer.select(
        message="What do you want to do? arrow keys to move and enter to select",
        choices=["Choose token", "Choose extensions", "Install plugins", "Run", "Exit"],
        amark=emoji.emojize(":check_mark: "),
    ).execute()
    return run_choices(choice)



@bot.event
async def on_ready():
    print("Bot succesfully started! Loading extensions...")
    print(discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(8)))
    for a in config["extensions"]:
        try:
            bot.load_extension(f"extensions.{a[:-3]}")
        except Exception as e:
            print(f"Failed to load extension {a[:-3]}")
            traceback.print_exc()

    print("All extensions loaded!")
    print("Guilds the bot is in:")
    for x in bot.guilds:
        print(f"    - {x.name}")


if __name__ == "__main__":
    while True:
        try:
            menu()
        except (KeyboardInterrupt, EOFError):
            break
    
