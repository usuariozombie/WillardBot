from symbol import parameters
import nextcord, aiofiles
from datetime import datetime
from nextcord.ext import commands
import asyncio


class Tickets(commands.Cog, name="Tickets"):
	"""Util para pedir ayuda a los administradores del servidor."""

	COG_EMOJI = "\U0001F3AB"

	def __init__(self, client):
		self.client = client
		self.client.ticket_configs = {}



	@commands.Cog.listener()
	async def on_ready(self):
		print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Tickets enabled.\u001b[0m")
		async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
			pass

		async with aiofiles.open("ticket_configs.txt", mode="r") as file:
			lines = await file.readlines()
			for line in lines:
				data = line.split(" ")
				self.client.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]
	
	@commands.command(help="🎫 - Configura el sistema de tickets del servidor.")
	async def configure_ticket(self, ctx, msg: nextcord.Message=None, category: nextcord.CategoryChannel=None):
		if msg is None or category is None:
			await ctx.channel.send("Se ha fallado al configurar el sistema de tickets, un argumento o varios eran inválidos.")
			return

		self.client.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] # this resets the configuration

		async with aiofiles.open("ticket_configs.txt", mode="r") as file:
			data = await file.readlines()

		async with aiofiles.open("ticket_configs.txt", mode="w") as file:
			await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

			for line in data:
				if int(line.split(" ")[0]) != ctx.guild.id:
					await file.write(line)
					
		await msg.add_reaction(u"\U0001F3AB")
		await ctx.channel.send("Se ha configurado exitosamente el sistema de tickets.")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.bot:
			pass
		else:
			if payload.channel_id == 871896095708565585:
				channel = self.client.get_channel(payload.channel_id)
				guild = await self.client.fetch_guild(payload.guild_id)
				member = await guild.fetch_member(payload.user_id)
				message = await channel.fetch_message(payload.message_id)
				if payload.message_id == 1011724754358648975:
					await message.remove_reaction(payload.emoji.name, member)
					role = nextcord.utils.find(lambda r: r.name == 'Anuncios', guild.roles)
					if role in member.roles:
						await member.remove_roles(guild.get_role(1004793088813834241))
					else:
						await member.add_roles(guild.get_role(1004793088813834241))
				elif payload.message_id == 1024380976438190100:
					await message.remove_reaction(payload.emoji.name, member)
					role = nextcord.utils.find(lambda r: r.name == 'GameNight', guild.roles)
					if role in member.roles:
						await member.remove_roles(guild.get_role(1023972661518417960))
					else:
						await member.add_roles(guild.get_role(1023972661518417960))

	



def setup(client):
    client.add_cog(Tickets(client))