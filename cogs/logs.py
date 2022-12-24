import nextcord
from datetime import datetime
from nextcord.ext import commands


class Reactions(commands.Cog, name="Reactions"):
	"""Util para realizar tareas a partir de reacciones y logs."""

	COG_EMOJI = "\U0001F3AB"

	def __init__(self, client):
		self.client = client



	@commands.Cog.listener()
	async def on_ready(self):
		print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Reactions enabled.\u001b[0m")
	

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
				elif payload.message_id == 1025431376922673323:
					await message.remove_reaction(payload.emoji.name, member)
					role = nextcord.utils.find(lambda r: r.name == 'GameNight', guild.roles)
					if role in member.roles:
						await member.remove_roles(guild.get_role(1023972661518417960))
					else:
						await member.add_roles(guild.get_role(1023972661518417960))
    

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.author.bot:
			pass
		else:
			channel = self.client.get_channel(1055866232194207774)
			embed = nextcord.Embed(title="Mensaje borrado", description=f"**Autor:** {message.author.mention} ({message.author})\n**Canal:** {message.channel.mention}\n**Contenido:** {message.content}", color=0xff0000)
			await channel.send(embed=embed)
	
 
	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if before.author.bot:
			pass
		else:
			channel = self.client.get_channel(1055866232194207774)
			embed = nextcord.Embed(title="Mensaje editado", description=f"**Autor:** {before.author.mention} ({before.author})\n**Canal:** {before.channel.mention}\n**Antes:** {before.content}\n**Después:** {after.content}", color=0xff0000)
			await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if member.bot:
			pass
		else:
			channel = self.client.get_channel(1055867543736291348)
			if before.channel is None and after.channel is not None:
				embed = nextcord.Embed(title="Se ha conectado a un canal de voz", description=f"**Usuario:** {member.mention} ({member})\n**Canal:** {after.channel.mention}", color=0x00ff00)
				await channel.send(embed=embed)
			elif before.channel is not None and after.channel is None:
				embed = nextcord.Embed(title="Se ha desconectado de un canal de voz", description=f"**Usuario:** {member.mention} ({member})\n**Canal:** {before.channel.mention}", color=0xff0000)
				await channel.send(embed=embed)
			elif before.channel ==  after.channel:
				pass
			else:
				embed = nextcord.Embed(title="Se ha cambiado de canal de voz", description=f"**Usuario:** {member.mention} ({member})\n**Antes:** {before.channel.mention}\n**Después:** {after.channel.mention}", color=0xffff00)
				await channel.send(embed=embed)


#member join log
	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = self.client.get_channel(1055868047044386936)
		embed = nextcord.Embed(title="Se ha unido un nuevo miembro", description=f"**Usuario:** {member.mention} ({member})\n**ID:** {member.id}", color=0x00ff00)
		await channel.send(embed=embed)
		#welcome message and image with avatar and banners

#member leave log
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = self.client.get_channel(1055868047044386936)
		embed = nextcord.Embed(title="Se ha ido un miembro", description=f"**Usuario:** {member.mention} ({member})\n**ID:** {member.id}", color=0xff0000)
		await channel.send(embed=embed)


#member ban log
	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		channel = self.client.get_channel(1055870987020800071)
		embed = nextcord.Embed(title="Se ha baneado a un miembro", description=f"**Usuario:** {user.mention} ({user})\n**ID:** {user.id}", color=0xff0000)
		await channel.send(embed=embed)


#member unban log
	@commands.Cog.listener()
	async def on_member_unban(self, guild, user):
		channel = self.client.get_channel(1055870987020800071)
		embed = nextcord.Embed(title="Se ha desbaneado a un miembro", description=f"**Usuario:** {user.mention} ({user})\n**ID:** {user.id}", color=0x00ff00)
		await channel.send(embed=embed)

#member role add log and who added it
	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.roles != after.roles:
			channel = self.client.get_channel(1055871514462932992)
			embed = nextcord.Embed(title="Se ha añadido un rol a un miembro", description=f"**Usuario:** {after.mention} ({after})\n**Rol:** {after.roles[-1]}", color=0x00ff00)
			await channel.send(embed=embed)


#member role remove log
	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.roles != after.roles:
			channel = self.client.get_channel(1055871514462932992)
			embed = nextcord.Embed(title="Se ha quitado un rol a un miembro", description=f"**Usuario:** {after.mention} ({after})\n**Rol:** {before.roles[-1]}", color=0xff0000)
			await channel.send(embed=embed)
   
   
#member kick log
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = self.client.get_channel(1055870987020800071)
		embed = nextcord.Embed(title="Se ha expulsado a un miembro", description=f"**Usuario:** {member.mention} ({member})\n**ID:** {member.id}", color=0xff0000)
		await channel.send(embed=embed)
	
 
def setup(client):
    client.add_cog(Reactions(client))
