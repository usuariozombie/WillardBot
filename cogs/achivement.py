import nextcord, pytz, json, asyncio
from nextcord.ext import commands
from datetime import datetime, timedelta



achievements = {
    "Primeras palabras": {
        "description": "Manda tu primer mensaje en el servidor de discord",
        # This lambda function will always return True
        "requirement": lambda message: messageCount[str(message.author.id)] >= 1,
    },
    "Ciudadano ejemplar": {
        "description": "Manda 100 mensajes en el servidor de discord",
        #sends 5 messages
        "requirement": lambda message: messageCount[str(message.author.id)] >= 100,
    },
    "Superviviente de Black Mesa": {
        "description": "Dura mas de 30 dias en el servidor de discord",
        #offset naive datetime to UTC
        "requirement": lambda message: message.author.joined_at <= datetime.now(pytz.utc) - timedelta(days=30),
    },
    
    "Lealista": {
        "description": "Boostea el servidor de discord",
        "requirement": lambda message: message.author.premium_since is not None,
    },
    
    "¡Hay un Spy infiltrado!": {
        "description": "Cambia tu nombre a cualquier otra cosa que no sea tu nombre de usuario",
        "requirement": lambda message: message.author.display_name != message.author.name,
    },

    "VIP": {
        "description": "Compra el VIP Grado 1",
        "requirement": lambda message: nextcord.utils.get(message.author.roles, name="Un buen ciudadano - VIP Grado I") is not None or nextcord.utils.get(message.author.roles, name="Protector - VIP grado II") is not None or nextcord.utils.get(message.author.roles, name="Principe Gulanga - VIP Grado III") is not None,
    },
    
    "Incluso más importante": {
        "description": "Compra el VIP Grado 2",
        "requirement": lambda message: nextcord.utils.get(message.author.roles, name="Protector - VIP grado II") is not None or nextcord.utils.get(message.author.roles, name="Principe Gulanga - VIP Grado III") is not None,
    },
    
    "Príncipe Gulanga": {
        "description": "Compra el VIP Grado 3",
        "requirement": lambda message: nextcord.utils.get(message.author.roles, name="Principe Gulanga - VIP Grado III") is not None,
    }, 
    
    "Despierte y mire a su alrededor": {
        "description": "Que tu actividad principal en Discord sea Garry's Mod",
        "requirement": lambda message: message.author.activities != () and message.author.activities[0].name == "Garry's Mod",
    },
    
    "Vinculado con la vortesencia": {
        "description": "Vincula tu cuenta de Discord con el foro",
        "requirement": lambda message: None,
    }
}

# Leer el progreso de los usuarios en un JSON

with open("user_progress.json", "r") as f:
    user_progress = json.load(f)


#Leer el contador de mensajes en un JSON

with open("messageCount.json", "r") as f:
    messageCount = json.load(f)



class Achivements(commands.Cog, name="Achievements"):
    """Logros para el servidor."""
    COG_EMOJI = "\U0001F3AB"
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):

        author = str(message.author.id)
        if message.author.bot:
            return
        
    
        #store the message count in a JSON file
        if author not in messageCount:
            messageCount[author] = 0
        messageCount[author] += 1
        with open("messageCount.json", "w") as f:
            json.dump(messageCount, f, indent=4)
    
        
        # Check if the message author is in the user_progress dict and if it is don't duplicate the achievements
        for achievement in achievements:
            
            if str(message.author.id) not in user_progress:
                user_progress[str(message.author.id)] = {}
                user_progress[str(message.author.id)][achievement] = False
                with open("user_progress.json", "w") as f:
                    json.dump(user_progress, f, indent=4)
            
            elif achievement not in user_progress[str(message.author.id)]:
                user_progress[str(message.author.id)][achievement] = False
                with open("user_progress.json", "w") as f:
                    json.dump(user_progress, f, indent=4)
            elif achievement in user_progress[str(message.author.id)] and user_progress[str(message.author.id)][achievement] == False and achievements[achievement]["requirement"](message):
                user_progress[str(message.author.id)][achievement] = True
                with open("user_progress.json", "w") as f:
                    json.dump(user_progress, f, indent=4)
                embed = nextcord.Embed(color=nextcord.Color.green())
                embed.set_author(name=message.author.name ,url=message.author.avatar)
                embed.add_field(name="Logro desbloqueado", value=f"¡Felicidades! Has desbloqueado el logro **{achievement}**")
                await message.author.send(embed=embed)
            else:
                continue
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id not in user_progress:
            user_progress[member.id] = {}
            
        for achievement in achievements:
            if achievement not in user_progress[member.id]:
                user_progress[member.id][achievement] = False
                open("user_progress.json", "w").write(json.dumps(user_progress, indent=4))
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.id in user_progress:
            del user_progress[member.id]
            
    @nextcord.slash_command(name="achievements", description="Muestra los logros disponibles del servidor en una tabla.")
    async def achievements(self, interaction: nextcord.Interaction):
        """Muestra los logros del servidor."""
        embed = nextcord.Embed(color=nextcord.Color.blue())
        embed.set_author(name="Logros disponibles", icon_url=self.client.user.avatar)
        for achievement in achievements:
            embed.add_field(name=achievement, value=achievements[achievement]["description"], inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    

    @nextcord.slash_command(name="progress", description="Muestra el progreso de los logros del servidor en una tabla.")
    async def progress(self, interaction: nextcord.Interaction):
        with open("user_progress.json", "r") as f:
            user_progress = json.load(f)
        embed = nextcord.Embed(color=nextcord.Color.blue())
        embed.set_author(name=f"Logros  ·  {interaction.user.name}", icon_url=interaction.user.avatar)
        for achievement in achievements:
            if user_progress[str(interaction.user.id)][achievement]:
                embed.add_field(name=achievement, value=":white_check_mark:", inline=False)
            else:
                if achievement == "Ciudadano ejemplar":
                    embed.add_field(name=achievement, value=f"<a:loader:867179026246008892> **{messageCount[str(interaction.user.id)]}**/100 mensajes", inline=False)
                if achievement == "Superviviente de Black Mesa":
                    days_left = 30 - (datetime.now(pytz.utc) - interaction.user.joined_at).days
                    embed.add_field(name=achievement, value=f"<a:loader:867179026246008892> **{days_left}** días restantes", inline=False)
                else:
                    if achievement != "Ciudadano ejemplar" and achievement != "Superviviente de Black Mesa":
                        embed.add_field(name=achievement, value=":x:", inline=False) 
        await interaction.response.send_message(embed=embed, ephemeral=True)
                                
    #Usa ephemeral para que el mensaje solo se vea por el usuario que ejecutó el comando
    #Busca el nombre del usuario en el historial de mensajes del canal 875529893893509120 si aparece, le da el logro "Vinculado con la vortesencia"

    @nextcord.slash_command(name="vincular", description="Vincula tu cuenta de Discord con la del foro.")
    async def vincular(self, interaction: nextcord.Interaction):
        channel = self.client.get_channel(875529893893509120)
        async for message in channel.history(limit=100):
            if interaction.user.mention in message.content:
                user_progress[str(interaction.user.id)]["Vinculado con la vortesencia"] = True
                with open("user_progress.json", "w") as f:
                    json.dump(user_progress, f, indent=4)
                embed = nextcord.Embed(color=nextcord.Color.green())
                embed.set_author(name="¡Felicidades! Has desbloqueado el logro · Vinculado con la vortesencia", icon_url=self.client.user.avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        embed = nextcord.Embed(color=nextcord.Color.red())
        embed.set_author(name="ERROR - No tienes vinculada tu cuenta de Discord con la del foro", icon_url=self.client.user.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @nextcord.slash_command(name="leaderboard", description="Muestra el top 10 de usuarios con más logros desbloqueados.")
    async def leaderboard(self, interaction: nextcord.Interaction):
        with open("user_progress.json", "r") as f:
            user_progress = json.load(f)
        embed = nextcord.Embed(color=nextcord.Color.blue())
        embed.set_author(name="Top 10 de usuarios con más logros desbloqueados", icon_url=self.client.user.avatar)
        leaderboard = {}
        for user in user_progress:
            count = 0
            for achievement in user_progress[user]:
                if user_progress[user][achievement]:
                    count += 1
            leaderboard[user] = count
        leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
        count = 1
        for user in leaderboard:
            if count <= 10:
                embed.add_field(name=f"{count}. {self.client.get_user(int(user)).name}", value=f"**{leaderboard[user]}** logros desbloqueados", inline=False)
                count += 1
        await interaction.response.send_message(embed=embed, ephemeral=True)

        
        
    
    
            
def setup(client):
    client.add_cog(Achivements(client))