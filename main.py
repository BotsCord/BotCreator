from InquirerPy import inquirer
import asyncio
import json
import os
from discord.ext import commands
import discord
import traceback
import emoji
import requests
import dotenv

PLUGINS_REPO = "https://raw.githubusercontent.com/BotsCord/plugins/main/plugins.json"

config = {
    "token": "",
    "extensions": [x for x in os.listdir("extensions") if x.endswith(".py")],
    "prefix": "!",
}

bot = commands.Bot(
    command_prefix=config["prefix"], intents=discord.Intents.all())

print("Ready to start bot maker from " + __file__)


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
    if choice == "Edit envoirnement variables":
        env_choice = inquirer.select(message="What do you want to do?", choices=[
                                     "Edit", "Add", "Delete"]).execute()
        if env_choice == "Edit":
            env = open(".env", "r")
            env_content = env.read()
            env_keys = env_content.split("\n")
            env_values = [x.split("=") for x in env_keys]
            data = {}
            for a in env_values:
                data[a[0]] = a[1]
            to_edit = inquirer.select(message="What do you want to edit?", choices=[
                                      x[0] for x in env_values]).execute()
            edited = inquirer.text(
                message="Enter your new value for "+to_edit).execute()

            env_content = env_content.replace(
                to_edit+"="+data[to_edit], to_edit+"="+edited)
            env.close()
            env = open(".env", "w")
            env.write(env_content)
            env.close()
        if env_choice == "Add":
            key = inquirer.text(message="Enter your key").execute()
            value = inquirer.text(message="Enter your value").execute()
            env = open(".env", "a")
            env.write("\n"+key+"="+value)
            env.close()
        if env_choice == "Delete":
            env = open(".env", "r")
            env_content = env.read()
            env_keys = env_content.split("\n")
            env_values = [x.split("=") for x in env_keys]
            data = {}
            for a in env_values:
                data[a[0]] = a[1]
            to_delete = inquirer.select(message="What do you want to edit?", choices=[
                                      x[0] for x in env_values]).execute()
            env.close()
            env = open(".env", "w")
            env.write("\n".join([x[0]+"="+data[x[0]] for x in env_values if x[0] != to_delete]))
            env.close()
    if choice == "Run":
        dotenv.load_dotenv(dotenv_path=".env")
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

        plugins = json.loads(r.text)

        to_install = inquirer.checkbox(message="Select the plugins you want to install", choices=[
                                       x["name"] for x in plugins]).execute()
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
        choices=["Choose token", "Choose extensions", "Install plugins",
                 "Edit envoirnement variables", "Run", "Exit"],
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
