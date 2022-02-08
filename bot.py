import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import subprocess
import os
from storage import tstore

description = '''PiBot in Python'''
bot = commands.Bot(command_prefix='/', description=description)
TOKEN = tstore

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

bot.run(TOKEN)
