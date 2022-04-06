# WRITTEN BY AIDAN LEMAY
# aidanlemay.com
# admin@aidanlemay.com for more details

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import subprocess
import storage
import feedparser
import json
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import requests
from requests.exceptions import HTTPError

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
slash = SlashCommand(bot)

# Sync Functions

def get_source():
    try:
        session = HTMLSession()
        response = session.get("https://www.monroecounty.gov/incidents911.rss")
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_feed():
    response = get_source()

    df = pd.DataFrame()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text
            
            description = item.find('description', first=True).text

            row = {'title': title, 'description': description}
            df = df.append(row, ignore_index=True)

    return df

# End Sync Functions

# Async Commands

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')

@bot.command()
async def help(ctx):
    """Gets Status of RPI Server"""
    await ctx.send("```\nRaspberryPiBot Discord Bot Help!\n\nCreated by Aidan LeMay using Discord.py\nhttps://github.com/The-Doctor-Of-11/RaspberryPiBot\n\n__Command Help:__\n/help: Display this help window\n/status or /stat: show status of Raspberry Pi Server\n/M911 [X#: Optional Quantity]: Returns X# of Monroe County 911 Events from https://www.monroecounty.gov/incidents911.rss\n\nVisit the creator here! https://aidanlemay.com/```")

@bot.command()
async def status(ctx):
    """Gets Status of RPI Server"""
    stats = subprocess.run(["mpstat -P ALL"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    mem = subprocess.run(["vmstat -w -S m"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    proc = subprocess.run(["ps aux | head -5"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    apache = subprocess.run(["systemctl status apache2 | head -5"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    await ctx.send("```\n---------- CPU Status -------------\n\n" + stats + "\n```")
    await ctx.send("```\n---------- Memory Status ----------\n\n" + mem + "\n```")
    await ctx.send("```\n---------- Top Processes ----------\n\n" + proc + "\n```")
    await ctx.send("```\n---------- Apache Status ----------\n\n" + apache + "\n```")

@bot.command()
async def stat(ctx):
    """Gets Status of RPI Server"""
    stats = subprocess.run(["mpstat -P ALL"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    mem = subprocess.run(["vmstat -w -S m"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    proc = subprocess.run(["ps aux | head -5"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')
    apache = subprocess.run(["systemctl status apache2 | head -5"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf8')

    await ctx.send("```\n---------- CPU Status -------------\n\n" + stats + "\n```")
    await ctx.send("```\n---------- Memory Status ----------\n\n" + mem + "\n```")
    await ctx.send("```\n---------- Top Processes ----------\n\n" + proc + "\n```")
    await ctx.send("```\n---------- Apache Status ----------\n\n" + apache + "\n```")

@bot.command()
async def m911(ctx, num=1):

    df = get_feed()
    await ctx.send(df.head(num))

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def Ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    """A global error handler cog."""

    if isinstance(error, commands.CommandNotFound):
        message = "Sorry, this command was not found. Please check your input and try again!"
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        message = "Something about your input was wrong, please check your input and try again!"
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.send(message, delete_after=5)
    await ctx.message.delete(delay=5)

bot.run(storage.tstore)