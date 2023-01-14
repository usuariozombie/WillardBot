import nextcord, asyncio, json, requests
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime
from nextcord.ext import activities, commands


class Ingame(commands.Cog, name="Ingame"):
	"""Muestra información sobre el servidor de Garry's Mod."""

	COG_EMOJI = "🎮"

	def __init__(self, client):
		self.client = client

	# Request a la API de Garry's Mod.
	def get_gmod_server_info(self):
		response = requests.get("https://api.battlemetrics.com/servers/16557024")
		# return data:{attributes:{players:[]}}
		return response.json()["data"]["attributes"]["players"]

	# Cambia el estado del bot cada 10 segundos.
	async def change_status(self):
		while True:
			# Obtenemos el numero de jugadores en el servidor.
			players = self.get_gmod_server_info()
			# Cambiamos el estado del bot cada 10 segundos.
			await self.client.change_presence(
				activity=nextcord.Game(name="Garry's Mod | " + f"{players} {'jugador' if players == 1 else 'jugadores'} en el servidor" if players > 0 else "No hay jugadores en el servidor"))
			await asyncio.sleep(10)

	@commands.Cog.listener()
	async def on_ready(self):
		print(
			f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Ingame enabled.\u001b[0m")
		# Iniciamos el cambio de estado y lo hacemos cada 10 segundos.
		self.client.loop.create_task(self.change_status())
	
	@nextcord.slash_command(name="ingame", description="Muestra información sobre el servidor de Garry's Mod.")
	async def _ingame(self, interaction: Interaction):
		# Usamos https://api.trackyserver.com/widget/index.php?id=2049539 para obtener la información del servidor.
		response = requests.get("https://api.trackyserver.com/widget/index.php?id=2049539")
		# Obtenemos el numero de jugadores en el servidor en ["playerslist"].
		for player in response.json()["playerslist"]:
			# Creamos una lista con los nombres de los jugadores.
			players = [player["name"] for player in response.json()["playerslist"]]
		# Creamos un embed con la información del servidor.
		embed = nextcord.Embed(
			color=nextcord.Color.blue()
		)
		# footer avatar server icon
		embed.set_author(name="Información del servidor", icon_url=interaction.guild.icon)
		embed.add_field(name="Nombre del servidor", value=response.json()["name"], inline=False)
		embed.add_field(name="Jugador(es) en el servidor", value=f"{response.json()['playerscount']}", inline=False)
		embed.add_field(name="Jugador(es)", value="\n".join(players) if players else "No hay jugadores en el servidor.", inline=False)
		embed.add_field(name="Mapa", value=response.json()["map"], inline=False)
		embed.add_field(name="IP", value=response.json()["ip"], inline=False)
		embed.add_field(name="Versión", value=response.json()["version"], inline=False)
		embed.add_field(name="Workshop", value="[Click aquí](https://steamcommunity.com/sharedfiles/filedetails/?id=2049539) (Será necesario tener los contenidos de CS:GO)", inline=False)
		embed.set_footer(text="Solicitado por " + interaction.user.name, icon_url=interaction.user.avatar)
		await interaction.response.send_message(embed=embed)
  
def setup(client):
	client.add_cog(Ingame(client))

    
