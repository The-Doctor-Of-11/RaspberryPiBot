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

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
slash = SlashCommand(bot)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

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
async def M911(ctx, num=1):

    d = feedparser.parse("https://www.monroecounty.gov/911/rss.php")
    entry = d.entries[num]

    i = 0
    while i < num:
        response = "```\n----------- Event Title -------------\n\n" + d['entries'][i]['title'] + "\n"
        response += "\n---------- Event Date --------------\n\n" + d['entries'][i]['published'] + "\n"
        response += "\n---------- Description -------------\n\n" + d['entries'][i]['summary'] + "\n```"
        i += 1
        await ctx.send(response)

bot.run(storage.tstore)