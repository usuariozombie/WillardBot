# -*- coding: utf-8 -*-

import nextcord, os
from nextcord.ext import commands
from utils import Debug, JSON, ClearScreen, PurgeCache, TextClearer

ConfigData = JSON.Read("config.json")

ClearScreen(True)
Debug.Info("Connecting...")

client = commands.Bot(case_insensitive = True, command_prefix = ConfigData["Prefix"], intents = nextcord.Intents.all())
client.remove_command("help")

for cog in os.listdir("./cogs"):
	if cog.endswith(".py"):
		try: client.load_extension(f"cogs.{cog[:-3]}")
		except Exception as Error: Debug.Error(f"An error has occured while loading the cog: \"{cog}\"\n{Error}")

@client.event
async def on_ready():
	Debug.Good(f"Connected as {client.user.name}#{client.user.discriminator} ({client.user.id})!")
	Debug.Line(f"Currently in {str(len(client.guilds))} servers using \"{ConfigData['Prefix']}\" as prefix.")
	Debug.Line(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions={ConfigData['Permissions']}&scope=applications.command%20bot")

@client.command()
async def load(ctx, cog):
	if ctx.author.id in JSON.Read("config.json")["Whitelist"]:
		try:
			client.load_extension(f"cogs.{cog}")
			await ctx.send(f"> **Cog \"{TextClearer(cog)}\" loaded successfully!")
		except Exception as Error: await ctx.send(f"> **An error has occurred while loading \"{TextClearer(cog)}\": ```\n{Error}```")

@client.command()
async def reload(ctx, cog):
	if ctx.author.id in JSON.Read("config.json")["Whitelist"]:
		try:
			client.reload_extension(f"cogs.{cog}")
			await ctx.send(f"> **Cog \"{TextClearer(cog)}\" reloaded successfully!")
		except Exception as Error: await ctx.send(f"> **An error has occurred while reloading \"{TextClearer(cog)}\": ```\n{Error}```")

@client.command()
async def unload(ctx, cog):
	if ctx.author.id in JSON.Read("config.json")["Whitelist"]:
		try:
			client.unload_extension(f"cogs.{cog}")
			await ctx.send(f"> **Cog \"{TextClearer(cog)}\" unloaded successfully!")
		except Exception as Error: await ctx.send(f"> **An error has occurred while unloading \"{TextClearer(cog)}\": ```\n{Error}```")

client.run(ConfigData["BotToken"])