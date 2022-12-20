import nextcord, json, random, asyncio, humanfriendly
from nextcord.ext import commands
from global_functions import ban_msg, kick_msg
from datetime import datetime, timedelta
from main import BOT_USER_ID
from nextcord.ext.commands import errors



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

    @nextcord.ui.button(
        label="Confirmar", style=nextcord.ButtonStyle.green, custom_id="Si"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancelar", style=nextcord.ButtonStyle.red, custom_id="No")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()



class Moderation(commands.Cog):

    """Algunos comandos de moderación."""
    
    COG_EMOJI = "🔨"


    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.command(help="🚓 - Banea al usuario del servidor seleccionado.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Miembro a banear - No encontrado"
            )
            embed1.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="No te puedes banear a ti mismo, estúpido.",
            )
            embed69.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="El miembro tiene un rol **superior** a ti en la jerarquía de roles - Necesitas más permisos.",
            )
            em3.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="El miembro tiene un rol **igual** a ti en la jerarquía de roles - Necesitas más permisos.",
            )
            em3.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em3)
        guild = ctx.guild
        banMsg = random.choice(ban_msg)
        banEmbed = nextcord.Embed(
            description=f"{member.mention} {banMsg} Razón: {reason}", color=nextcord.Color.red()
        )
        banEmbed.set_author(name=f"{ctx.bot.user.name} · ¡Ban Completado!", icon_url=ctx.guild.icon)
        await ctx.send(embed=banEmbed)
        await member.send(f"Has sido baneado en **{guild}** | Razón: **{reason}**")
        await member.ban(reason=reason)


    @nextcord.slash_command(description="🚓 - Banea al usuario del servidor seleccionado.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, reason=None):
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


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes los permisos necesarios para banear :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(help="🆓 - Desbanea un usuario por ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        em = nextcord.Embed(description=f"Has desbaneado a <@{id}>")
        em.set_author(name=f"{ctx.bot.user.name} · ¡Desbaneo completado!", icon_url=ctx.guild.icon)
        await ctx.send(embed=em)
    

    @nextcord.slash_command(description="🆓 - Desbanea un usuario por ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: nextcord.Interaction, id: int):
        user = await self.client.fetch_user(id)
        await interaction.guild.unban(user)
        em = nextcord.Embed(description=f"Has desbaneado a <@{id}>")
        em.set_author(name=f"{interaction.client.user.name} · ¡Desbaneo completado!", icon_url=interaction.guild.icon)
        await interaction.send(embed=em)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes suficientes permisos :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)
        

    @commands.command(help="🚪 - Kickea al miembro de tu servidor.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Miembro a banear - No encontrado."
            )
            embed1.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed1)
        if not (ctx.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Necesito el permiso ``Kick Members`` para usar este comando - Faltan permisos.",
            )
            embed2.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed2)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Lamentablemente no puedes expulsarte a ti mismo...",
            )
            embed69.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="El miembro tiene un rol **superior** a ti en la jerarquía de roles - Necesitas más permisos.",
            )
            em3.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="El miembro tiene un rol **igual** a ti en la jerarquía de roles - Necesitas más permisos."
            )
            em4.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em4)
        guild = ctx.guild
        kickMsg = random.choice(kick_msg)
        kickEmbed = nextcord.Embed(
            color=nextcord.Color.random(),
            description=f"{member.mention} {kickMsg} **Razón:** {reason}"
        )
        kickEmbed.set_author(name=f"{ctx.bot.user.name} · ¡Kick completado! ", icon_url=ctx.guild.icon)
        await ctx.send(embed=kickEmbed)
        await member.send(f"Se te ha expulsado de **{guild}** | Razón: **{reason}**")
        await member.kick(reason=reason)
        
    @nextcord.slash_command(description="🚪 - Kickea al miembro de tu servidor.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Miembro a banear - No encontrado."
            )
            embed1.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            return await interaction.send(embed=embed1)
        if not (interaction.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Necesito el permiso ``Kick Members`` para usar este comando - Faltan permisos.",
            )
            embed2.set_author(name=f"{interaction.client.user.name} · ¡Error! ", icon_url=interaction.guild.icon)
            return await interaction.send(embed=embed2)
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


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes suficientes permisos :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)


    @commands.command(help="🗑️ - Borra un bloque de mensajes.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        amount = amount + 1
        if amount > 101:
            em1 = nextcord.Embed(
                description="Has superado el límite - Más de 100 mensajes.",
            )
            em1.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em1)
        else:
            await ctx.channel.purge(limit=amount)
            msg = nextcord.Embed(
            )
            msg.set_author(name=f"{ctx.bot.user.name} · ¡Limpieza completada! ", icon_url=ctx.guild.icon)
            msg.set_footer(text=f"Limpieza solicitada por {ctx.author}")
            await ctx.send(embed=msg)

    @nextcord.slash_command(name="clear", description="🗑️ - Borra un bloque de mensajes.")
    @commands.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: nextcord.Interaction, amount: int):
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


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos para este comando :face_with_raised_eyebrow: - Necesitas más permisos."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)


    @commands.command(help="🐢 - Cambia el canal a modo lento.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int):
        try:
            if time == 0:
                em1 = nextcord.Embed(
                    description="Modo lento desactivado."
                )
                em1.set_author(name=f"{ctx.bot.user.name} · Modo lento.", icon_url=ctx.guild.icon)
                await ctx.send(embed=em1)
                await ctx.channel.edit(slowmode_delay=0)
            elif time > 21600:
                em2 = nextcord.Embed(
                    description="Modo lento de más de 6 horas."
                )
                em2.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
                await ctx.send(embed=em2)
            else:
                await ctx.channel.edit(slowmode_delay=time)
                em3 = nextcord.Embed(
                    description=f"El modo lento se ha habilitado con {time} segundos.",
                )
                em3.set_author(name=f"{ctx.bot.user.name} · Modo lento.", icon_url=ctx.guild.icon)
                await ctx.send(embed=em3)
        except Exception:
            await ctx.send("Ha ocurrido un error, avisa al equipo de desarrollo.")
            print(Exception)
            
    @nextcord.slash_command(name="slowmode", description="🐢 - Cambia el canal a modo lento.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode_slash(self, interaction: nextcord.Interaction, time: int):
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
    
    
    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos para activar el modo lento :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(aliases=["giverole", "addr"], help="➕ - Le da a un miembro un rol concreto.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                description="¡Por favor menciona a un usuario para darle un rol!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                description="¡Por favor menciona un rol para darle a {}!".format(
                    member.mention
                ),
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                description="No tienes suficientes permisos para dar ese rol.",
            )
            em.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                description="Ese rol es muy alto en la jerarquía para poder darlo.",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed)
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
                embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    description=f"{member.mention} ha recibido el rol {role.mention}",
                )
                em.set_author(name=f"{ctx.bot.user.name} · ¡Rol añadido!", icon_url=ctx.guild.icon)
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)
            
    @nextcord.slash_command(name="addrole", description="➕ - Le da a un miembro un rol concreto.")
    @commands.has_permissions(manage_roles=True)
    async def addrole_slash(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, role: nextcord.Role = None):
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


    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos para dar roles :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(aliases=["takerole", "remover"], help="➖ - Elimina un rol específico de un usuario.",)
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx,
        member: nextcord.Member = None,
        role: nextcord.Role = None,
        *,
        reason=None,
    ):
        if member is None:
            embed = nextcord.Embed(
                description="¡Por favor, menciona a un usuario para quitarle ese rol!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                description="Por favor menciona un rol para quitarle a {}!".format(
                    member.mention
                ),
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                description="No tienes suficientes permisos para quitar ese rol.",
            )
            em.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                description="Ese rol es muy alto en la jerarquía para poder quitarlo.",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed)
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
                embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    description=f"A {member.mention} se le ha quitado {role.mention}",
                )
                em.set_author(name=f"{ctx.bot.user.name} · ¡Rol eliminado!", icon_url=ctx.guild.icon)
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)
            
    @nextcord.slash_command(description="➖ - Elimina un rol específico de un usuario.")
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, interaction: nextcord.Interaction, member: nextcord.Member = None, role: nextcord.Role = None, *, reason=None):
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
    

    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos para eliminar roles :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Moderation enabled.\u001b[0m")
    

    
    @commands.command(help = "🔇 - Silencia usuarios con este comando.")
    async def mute(self, ctx, member: nextcord.Member, time=None, reason=None):
        if member == None:
            embed = nextcord.Embed(
                description="¡Por favor menciona a un usuario para silenciarlo!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if time == None:
            embed = nextcord.Embed(
                description="¡Especifica cuanto tiempo quieres silenciarlo!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < member.top_role.position:
            em = nextcord.Embed(
                description="No tienes suficientes permisos para silenciar a este miembro.",
            )
            em.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em)
        else:
            time = humanfriendly.parse_timespan(time)
            await member.edit(timeout=nextcord.utils.utcnow() + timedelta(minutes=time))
            await member.send(f"Has sido silenciado en {ctx.guild} | Razón: {reason}")
            embed = nextcord.Embed(
                description=f"{member.mention} ha sido silenciado por {time}",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Silenciado!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        
    @nextcord.slash_command(name="mute", description="🔇 - Silencia usuarios con este comando.")
    async def mute(self, interaction: nextcord.Interaction , member: nextcord.Member, time=None, reason=None):
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
    
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos de mute :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)


    @commands.command(help = "🔊 - Elimina silencios de los usuarios con este comando.")
    async def unmute(self, ctx, member: nextcord.Member, reason=None):
        if member == None:
            await ctx.send("¡Especifica un usuario para quitar el silencio!")
        else:
            await member.edit(timeout=None)
            await member.send(f"Tu silecio en {ctx.guild} ha sido eliminado. | Reason: {reason}")
            embed = nextcord.Embed(
                description=f"Se ha eliminado el silencio de {member.mention}",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · ¡Silencio eliminado!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        
    @nextcord.slash_command(name="unmute", description="🔊 - Elimina silencios de los usuarios con este comando.")
    async def unmute(self, interaction: nextcord.Interaction, member: nextcord.Member, reason=None):
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

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos suficientes para eliminar el silencio :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

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
    
    
    @commands.command(help = "🚔 - Comando para que los moderadores baneen.")
    @commands.has_permissions(kick_members=True)
    async def modban(self, ctx, member: nextcord.Member, *, reason=None):
        if reason is None:
            reason = f"{ctx.author.name} ha baneado a {member.name}"
        else:
            reason = (
                f"{ctx.author.name} ha baneado a {member.name} por la razón {reason}"
            )
        if member == None:
            embed1 = nextcord.Embed(
                description="¡Miembro no encontrado!"
            )
            embed1.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                description="Lo siento, no puedes banearte a ti mismo."
            )
            embed69.set_author(name=f"{ctx.bot.user.name} · ¡Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed69)
        if ctx.author.top_role.position <= member.top_role.position:
            embed2 = nextcord.Embed(
                description="¡No puedes banear a alguien con un rol más alto en la jerarquía que tu!"
            )
            embed2.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed2)
        em = nextcord.Embed(
            description=f"**¿Estás seguro de querer banear a {member}?**\n Esta acción no puede deshacerse y debe ser consultada."
        )
        em.set_author(name=f"{ctx.bot.user.name} · ¿Estás seguro?", icon_url=ctx.guild.icon)
        view = BanConfirm(ctx)
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Se ha agotado el tiempo de espera.")
        elif view.value:
            guild = ctx.guild
            banMsg = random.choice(ban_msg)
            banEmbed = nextcord.Embed(
                description=f"{member.mention} {banMsg} | Razón: {reason}"
            )
            banEmbed.set_author(name=f"{ctx.bot.user.name} · Ha sido baneado.", icon_url=ctx.guild.icon)
            await ctx.author.send(embed=banEmbed)
            await member.ban(reason=reason)
            await member.send(f"Has sido baneado **{guild}** | Razón: **{reason}**")
        else:
            banEmbed = nextcord.Embed(
                description="El baneo ha sido cancelado."
            )
            banEmbed.set_author(name=f"{ctx.bot.user.name} · ¡Ban cancelado!", icon_url=ctx.guild.icon)
            await ctx.author.send(embed=banEmbed)

    @modban.error
    async def modban_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="No tienes permisos para banear :face_with_raised_eyebrow: - Petición rechazada."
            )
            em5.set_author(name=f"{ctx.bot.user.name} · ¡Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)



def setup(client):
    client.add_cog(Moderation(client))