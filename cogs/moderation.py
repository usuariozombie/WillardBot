import nextcord, random, humanfriendly, time
from nextcord.ext import commands
from tools.global_functions import ban_msg, kick_msg
from datetime import datetime, timedelta
from nextcord.ext.commands import errors
from tools.utils import JSON



class BanConfirm(nextcord.ui.View):
    async def interaction_check(self,interaction):
        if self.ctx.author != interaction.user:
            await interaction.response.send_message('Este no es tu mensaje.', ephemeral=True)
            return False
        return True
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
    def __init__(self,ctx,**kwargs):
        super().__init__(timeout=60,**kwargs)
        self.value = None
        self.ctx = ctx




class Moderation(commands.Cog):

    """Algunos comandos de moderación."""
    
    COG_EMOJI = "🔨"


    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(self.client.user.id):
            send = message.channel.send



    @nextcord.slash_command(description="🚓 - Banea al usuario del servidor seleccionado.")
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, reason=None):
        if interaction.user.guild_permissions.ban_members == True:
        #ask name of the member in a modal
            if member == None:
                embed1 = nextcord.Embed(
                    color=nextcord.Color.red(),
                    description="Miembro a banear - No encontrado"
                )
                embed1.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=embed1)
            if member.id == interaction.user.id:
                embed69 = nextcord.Embed(
                    color=nextcord.Color.red(),
                    description="No te puedes banear a ti mismo, estúpido.",
                )
                embed69.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=embed69)
            elif interaction.user.top_role.position < member.top_role.position:
                em3 = nextcord.Embed(
                    color=nextcord.Color.red(),
                    description="El miembro tiene un rol **superior** a ti en la jerarquía de roles - Necesitas más permisos.",
                )
                em3.set_author(name=f"{interaction.client.user.name} · Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em3)
            elif interaction.user.top_role.position == member.top_role.position:
                em3 = nextcord.Embed(
                    color=nextcord.Color.red(),
                    description="El miembro tiene un rol **igual** a ti en la jerarquía de roles - Necesitas más permisos.",
                )
                em3.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em3)
            guild = interaction.guild
            banMsg = random.choice(ban_msg)
            banEmbed = nextcord.Embed(
                description=f"{member.mention} {banMsg} Razón: {reason}", color=nextcord.Color.red()
            )
            banEmbed.set_author(name=f"{interaction.client.user.name} · ¡Ban Completado!", icon_url=interaction.guild.icon)
            await interaction.send(embed=banEmbed)
            await member.send(f"Has sido baneado en **{guild}** | Razón: **{reason}**")
            await member.ban(reason=reason)
        else:
            embed2 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Necesitas el permiso ``Ban Members`` para usar este comando."
            )
            embed2.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed2, ephemeral=True)

    

    @nextcord.slash_command(description="🆓 - Desbanea un usuario por ID")

    async def unban(self, interaction: nextcord.Interaction, id: int):
        if interaction.user.guild_permissions.ban_members == False:
            embed2 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Necesitas el permiso ``Ban Members`` para usar este comando."
            )
            embed2.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            return await interaction.send(embed=embed2, ephemeral=True)
        else:
            user = await self.client.fetch_user(id)
            await interaction.guild.unban(user)
            em = nextcord.Embed(description=f"Has desbaneado a <@{id}>")
            em.set_author(name=f"{interaction.client.user.name} · ¡Desbaneo completado!", icon_url=interaction.guild.icon)
            await interaction.send(embed=em)
        
    @nextcord.slash_command(description="🚪 - Kickea al miembro de tu servidor.")
    async def kick(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, reason=None):
        if interaction.user.guild_permissions.kick_members == True:
            if member == None:
                embed1 = nextcord.Embed(
                    color=nextcord.Color.random(),
                    description="Miembro a banear - No encontrado."
                )
                embed1.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=embed1)
            if member.id == interaction.user.id:
                embed69 = nextcord.Embed(
                    color=nextcord.Color.random(),
                    description="Lamentablemente no puedes expulsarte a ti mismo...",
                )
                embed69.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=embed69)
            elif interaction.user.top_role.position < member.top_role.position:
                em3 = nextcord.Embed(
                    color=nextcord.Color.random(),
                    description="El miembro tiene un rol **superior** a ti en la jerarquía de roles - Necesitas más permisos.",
                )
                em3.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em3)
            elif interaction.user.top_role.position == member.top_role.position:
                em4 = nextcord.Embed(
                    color=nextcord.Color.random(),
                    description="El miembro tiene un rol **igual** a ti en la jerarquía de roles - Necesitas más permisos."
                )
                em4.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em4)
            guild = interaction.guild
            kickMsg = random.choice(kick_msg)
            kickEmbed = nextcord.Embed(
                color=nextcord.Color.random(),
                description=f"{member.mention} {kickMsg} **Razón:** {reason}"
            )
            kickEmbed.set_author(name=f"{interaction.client.user.name} · ¡Kick completado! ", icon_url=interaction.guild.icon)
            await interaction.send(embed=kickEmbed)
            await member.send(f"Se te ha expulsado de **{guild}** | Razón: **{reason}**")
            await member.kick(reason=reason)
        else:
            embed2 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Necesitas el permiso ``Kick Members`` para usar este comando."
            )
            embed2.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            return await interaction.send(embed=embed2, ephemeral=True)


    @nextcord.slash_command(name="clear", description="🗑️ - Borra un bloque de mensajes.")
    async def clear_slash(self, interaction: nextcord.Interaction, amount: int):
        if interaction.user.guild_permissions.manage_messages == False:
            em1 = nextcord.Embed(
                description="Necesitas el permiso ``Manage Messages`` para usar este comando.",
            )
            em1.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            return await interaction.send(embed=em1, ephemeral=True)
        else:
            amount = amount + 1
            if amount > 101:
                em1 = nextcord.Embed(
                    description="Has superado el límite - Más de 100 mensajes.",
                )
                em1.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em1, ephemeral=True)
            else:
                await interaction.channel.purge(limit=amount)
                msg = nextcord.Embed(
                )
                msg.set_author(name=f"{interaction.client.user.name} · ¡Limpieza completada! ", icon_url=interaction.guild.icon)
                msg.set_footer(text=f"Limpieza solicitada por {interaction.user}")
                await interaction.send(embed=msg)

            
    @nextcord.slash_command(name="slowmode", description="🐢 - Cambia el canal a modo lento.")
    async def slowmode_slash(self, interaction: nextcord.Interaction, time: int):
        if interaction.user.guild_permissions.manage_channels == False:
            em1 = nextcord.Embed(
                description="Necesitas el permiso ``Manage Channels`` para usar este comando.",
            )
            em1.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            return await interaction.send(embed=em1, ephemeral=True)
        else:
            try:
                if time == 0:
                    em1 = nextcord.Embed(
                        description="Modo lento desactivado."
                    )
                    em1.set_author(name=f"{interaction.client.user.name} · Modo lento.", icon_url=interaction.guild.icon)
                    await interaction.send(embed=em1, ephemeral=True)
                    await interaction.channel.edit(slowmode_delay=0)
                elif time > 21600:
                    em2 = nextcord.Embed(
                        description="Modo lento de más de 6 horas."
                    )
                    em2.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                    await interaction.send(embed=em2, ephemeral=True)
                else:   
                    await interaction.channel.edit(slowmode_delay=time)
                    em3 = nextcord.Embed(
                        description=f"El modo lento se ha habilitado con {time} segundos.",
                    )
                    em3.set_author(name=f"{interaction.client.user.name} · Modo lento.", icon_url=interaction.guild.icon)
                    await interaction.send(embed=em3, ephemeral=True)
            except Exception:   
                await interaction.send("Ha ocurrido un error, avisa al equipo de desarrollo.", ephemeral=True)
                print(Exception)
    
            
    @nextcord.slash_command(name="addrole", description="➕ - Le da a un miembro un rol concreto.")
    async def addrole_slash(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, role: nextcord.Role = None):
        if interaction.user.guild_permissions.manage_roles == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Manage Roles`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member is None:
                embed = nextcord.Embed(
                    description="¡Por favor menciona a un usuario para darle un rol!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.send(embed=embed, ephemeral=True)
                return
            if role is None:
                embed = nextcord.Embed(
                    description="¡Por favor menciona un rol para darle a {}!".format(
                        member.mention
                    ),
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.send(embed=embed, ephemeral=True)
                return
            if interaction.user.top_role.position < role.position:
                em = nextcord.Embed(
                    description="No tienes suficientes permisos para dar ese rol.",
                )
                em.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em, ephemeral=True)
            if interaction.guild.me.top_role.position < role.position:
                embed = nextcord.Embed(
                    description="Ese rol es muy alto en la jerarquía para poder darlo.",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                return await interaction.send(embed=embed, ephemeral=True)
            try:
                addRole = True
                for role_ in member.roles:
                    if role_ == role:
                        addRole = False
                        break
                if not addRole:
                    embed = nextcord.Embed(
                        description=f"{member.mention} ya tiene ese rol que intentar darle.",
                    )
                    embed.set_author(name=f"{interaction.client.user.name} · Error!", icon_url=interaction.guild.icon)
                    await interaction.send(embed=embed, ephemeral=True)
                    return
                else:
                    em = nextcord.Embed(
                        description=f"{member.mention} ha recibido el rol {role.mention}",
                    )
                    em.set_author(name=f"{interaction.client.user.name} · ¡Rol añadido!", icon_url=interaction.guild.icon)
                    await interaction.send(embed=em, ephemeral=True)
                    await member.add_roles(role)
                    return
            except Exception:
                print(Exception)

  
            
    @nextcord.slash_command(description="➖ - Elimina un rol específico de un usuario.")
    async def removerole(self, interaction: nextcord.Interaction, member: nextcord.Member = None, role: nextcord.Role = None, *, reason=None):
        if interaction.user.guild_permissions.manage_roles == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Manage Roles`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member is None:
                embed = nextcord.Embed(
                    description="¡Por favor, menciona a un usuario para quitarle ese rol!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.send(embed=embed, ephemeral=True)
                return
            if role is None:
                embed = nextcord.Embed(
                    description="Por favor menciona un rol para quitarle a {}!".format(
                        member.mention
                    ),
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.send(embed=embed, ephemeral=True)
                return
            if interaction.user.top_role.position < role.position:
                em = nextcord.Embed(
                    description="No tienes suficientes permisos para quitar ese rol.",
                )
                em.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                return await interaction.send(embed=em, ephemeral=True)
            if interaction.guild.me.top_role.position < role.position:
                embed = nextcord.Embed(
                    description="Ese rol es muy alto en la jerarquía para poder quitarlo.",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                return await interaction.send(embed=embed, ephemeral=True)
            try:
                roleRemoved = False
                for role_ in member.roles:
                    if role_ == role:
                        await member.remove_roles(role)
                        roleRemoved = True
                        break
                if not roleRemoved:
                    embed = nextcord.Embed(
                        description=f"{member.mention} ya tiene el rol que intentas entregarle.",
                    )
                    embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                    await interaction.send(embed=embed, ephemeral=True)
                    return
                else:
                    em = nextcord.Embed(
                        description=f"A {member.mention} se le ha quitado {role.mention}",
                    )
                    em.set_author(name=f"{interaction.client.user.name} · ¡Rol eliminado!", icon_url=interaction.guild.icon)
                    await interaction.send(embed=em, ephemeral=True)
                    return
            except Exception:
                print(Exception)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Moderation enabled.\u001b[0m")
    
        
    @nextcord.slash_command(name="mute", description="🔇 - Silencia usuarios con este comando.")
    async def mute(self, interaction: nextcord.Interaction , member: nextcord.Member, time=None, reason=None):
        if interaction.user.guild_permissions.manage_messages == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Mute users`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member == None:
                embed = nextcord.Embed(
                    description="¡Por favor menciona a un usuario para silenciarlo!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed)
                return
            if time == None:
                embed = nextcord.Embed(
                    description="¡Especifica cuanto tiempo quieres silenciarlo!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed)
                return
            if interaction.user.top_role.position < member.top_role.position:
                em = nextcord.Embed(
                    description="No tienes suficientes permisos para silenciar a este miembro.",
                )
                em.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=em)
                return
            else:
                time = humanfriendly.parse_timespan(time)
                await member.edit(timeout=nextcord.utils.utcnow() + timedelta(minutes=time))
                await member.send(f"Has sido silenciado en {interaction.guild} | Razón: {reason}")
                embed = nextcord.Embed(
                    description=f"{member.mention} ha sido silenciado por {time} minutos",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Silenciado!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed)
                return
    
        
    @nextcord.slash_command(name="unmute", description="🔊 - Elimina silencios de los usuarios con este comando.")
    async def unmute(self, interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
        if interaction.user.guild_permissions.manage_messages == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Mute users`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member == None:
                embed = nextcord.Embed(
                    description="¡Especifica un usuario para quitar el silencio!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed)
                return
            else:
                await member.edit(timeout=None)
                await member.send(f"Tu silecio en {interaction.guild} ha sido eliminado. | Reason: {reason}")
                embed = nextcord.Embed(
                    description=f"Se ha eliminado el silencio de {member.mention}",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Silencio eliminado!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed)
                return

    @commands.command(help = "🎚️ - Habilita o deshabilita los comandos en este servidor.")
    async def switch(self, ctx, *, command):
        if not ctx.author.id == 200391563346575361:
            await ctx.reply("Ni lo intentes, esto es un comando de desarrollo.")
            return
        command = self.get_command(command)
        if command == None:
            await ctx.reply("No se ha encontrado ese comando.")
        elif ctx.command == command:
            await ctx.send("No puedes desactivar este comando.")
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send (f"The {command.qualified_name} command is now {ternary}")
    
    @nextcord.slash_command(name="switch", description="🎚️ - Habilita o deshabilita los comandos en este servidor.")
    async def switch(self, interaction: nextcord.Interaction, *, command):
        if not interaction.author.id == 200391563346575361:
            await interaction.response.send_message("Ni lo intentes, esto es un comando de desarrollo.")
            return
        command = self.get_command(command)
        if command == None:
            await interaction.response.send_message("No se ha encontrado ese comando.")
        elif interaction.command == command:
            await interaction.response.send_message("No puedes desactivar este comando.")
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await interaction.response.send_message(f"The {command.qualified_name} command is now {ternary}")
            
    @nextcord.slash_command(name="warn", description="🚨 - Avisa a un usuario con este comando.")
    async def warn(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason=None):
        if interaction.user.guild_permissions.manage_messages == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Manage messages`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member == None:
                embed = nextcord.Embed(
                    description="¡Especifica un usuario para avisar!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            else:
                await member.send(f"Has sido advertido en {interaction.guild} | Razón: {reason}")
                embed = nextcord.Embed(
                    description=f"{member.mention} ha sido advertido por {reason}"
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Advertido!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed)
                # now save the warn in json file if not member in json file then create a new one and add the warn with the reason and interaction.client.user and member.id and name
                warn = {"member": member.name, "reason": reason, "moderator": interaction.user.name}
                warns = JSON.Read("json/warns.json")
                if str(member.id) in warns:
                    warns[str(member.id)].append(warn)
                else:
                    warns[str(member.id)] = [warn]
                JSON.Write("json/warns.json", warns)
                # notice in 1055870987020800071 in embed
                embed = nextcord.Embed(
                    title="Advertencia",
                    description=f"{member.mention} ha sido advertido por {interaction.user.mention}.",
                    color=nextcord.Color.red()
                )
                embed.add_field(name="Razón:", value=reason)
                await interaction.client.get_channel(1055870987020800071).send(embed=embed)
                # if user has 5 warns in json file then notice in 1055870987020800071
                if len(warns[str(member.id)]) == 5:
                    embed = nextcord.Embed(
                        title="Advertencia",
                        description=f"{member.mention} ha sido advertido 5 veces <@&1063285026684424323>.",
                        color=nextcord.Color.red()
                    )
                    await interaction.client.get_channel(1055870987020800071).send(embed=embed)
                return
            
            
    @nextcord.slash_command(name="warnlist", description="🚨 - Muestra las advertencias de un usuario.")
    async def warnlist(self, interaction: nextcord.Interaction, member: nextcord.Member):
        if interaction.user.guild_permissions.manage_messages == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Manage messages`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member == None:
                embed = nextcord.Embed(
                    description="¡Especifica un usuario para ver sus advertencias!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            else:
                warns = JSON.Read("json/warns.json")
                if str(member.id) in warns:
                    embed = nextcord.Embed(
                        title="Advertencias",
                        description=f"Estas son las advertencias de {member.mention}",
                        color=nextcord.Color.red()
                    )
                    for warn in warns[str(member.id)]:
                        embed.add_field(name=f"Warn: {warn['moderator']}", value=warn["reason"], inline=False)
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = nextcord.Embed(
                        description=f"{member.mention} no tiene advertencias.",
                    )
                    embed.set_author(name=f"{interaction.client.user.name} · Advertencias", icon_url=interaction.guild.icon)
                    await interaction.response.send_message(embed=embed)
                return
            
            
    @nextcord.slash_command(name="clearwarns", description="🚨 - Borra las advertencias de un usuario.")
    async def clearwarns(self, interaction: nextcord.Interaction, member: nextcord.Member):
        if interaction.user.guild_permissions.manage_messages == False:
            embed = nextcord.Embed(
                description="Necesitas el permiso ``Manage messages`` para usar este comando.",
            )
            embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member == None:
                embed = nextcord.Embed(
                    description="¡Especifica un usuario para borrar sus advertencias!",
                )
                embed.set_author(name=f"{interaction.client.user.name} · ¡Error!", icon_url=interaction.guild.icon)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            else:
                warns = JSON.Read("json/warns.json")
                if str(member.id) in warns:
                    del warns[str(member.id)]
                    JSON.Write("json/warns.json", warns)
                    embed = nextcord.Embed(
                        description=f"Se han borrado las advertencias de {member.mention}.",
                    )
                    embed.set_author(name=f"{interaction.client.user.name} · Advertencias", icon_url=interaction.guild.icon)
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = nextcord.Embed(
                        description=f"{member.mention} no tiene advertencias.",
                    )
                    embed.set_author(name=f"{interaction.client.user.name} · Advertencias", icon_url=interaction.guild.icon)
                    await interaction.response.send_message(embed=embed)
                return

def setup(client):
    client.add_cog(Moderation(client))