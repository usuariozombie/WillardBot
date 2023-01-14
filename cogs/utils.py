import time, sys, os, nextcord, requests, psutil
from inspect import getsource
from time import time
from datetime import datetime
from nextcord.ext import commands, tasks
from tools.global_functions import EMOJIS_TO_USE_FOR_CALCULATOR as etufc
from nextcord import ButtonStyle, Spotify
from nextcord.ui import button, View
from tools.utils import JSON


ConfigData = JSON.Read("json/config.json")
IPKEY = ConfigData["IpKey"]

us = 0
um = 0 
uh = 0
ud = 0


green_button_style = ButtonStyle.success
grey_button_style = ButtonStyle.secondary
blue_button_style = ButtonStyle.primary
red_button_style = ButtonStyle.danger

class CalculatorButtons(View):
    def __init__(self, owner, embed, message):
        self.embed = embed
        self.owner = owner
        self.message = message
        self.expression = ""
        super().__init__(timeout=300.0)

    @button(emoji=etufc['1'], style=grey_button_style, row=1)
    async def one_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "1"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['2'], style=grey_button_style, row=1)
    async def two_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "2"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['3'], style=grey_button_style, row=1)
    async def three_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "3"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['4'], style=grey_button_style, row=2)
    async def four_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "4"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['5'], style=grey_button_style, row=2)
    async def five_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "5"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['6'], style=grey_button_style, row=2)
    async def six_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "6"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['7'], style=grey_button_style, row=3)
    async def seven_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "7"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['8'], style=grey_button_style, row=3)
    async def eight_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "8"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['9'], style=grey_button_style, row=3)
    async def nine_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "9"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="00 ", style=grey_button_style, row=4)
    async def double_zero_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "00"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['0'], style=grey_button_style, row=4)
    async def zero_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "0"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['.'], style=grey_button_style, row=4)
    async def dot_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "."
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['x'], style=blue_button_style, row=1, custom_id="*")
    async def multiplication_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "x"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['÷'], style=blue_button_style, row=2, custom_id="/")
    async def division_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "÷"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['+'], style=blue_button_style, row=3)
    async def addition_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "+"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['-'], style=blue_button_style, row=4)
    async def subtraction_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "-"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="←", style=red_button_style, row=1)
    async def back_space_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression = self.expression[:-1]
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="Clear", style=red_button_style, row=2)
    async def clear_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression = ""
        self.embed.description = "Cleared Calculator"
        await interaction.response.edit_message(embed=self.embed)

    @button(label="Exit", style=red_button_style, row=3)
    async def exit_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        for child in self.children:
            child.disabled = True
        embed = nextcord.Embed(title="Calculator Stopped.", color=nextcord.Color.red())
        await interaction.response.edit_message(embed=embed, view=self)

    @button(label="=", style=green_button_style, row=4)
    async def equal_to_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        expression = self.expression
        expression = expression.replace("÷", "/").replace("x", "*")
        try:
            result = str(eval(expression))
            self.expression = result
        except:
            result = "An Error Occured."
        self.embed.description = result
        await interaction.response.edit_message(embed=self.embed)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        embed = nextcord.Embed(title="Calculator Timed Out.", color=nextcord.Color.red())
        await self.message.edit(embed=embed, view=self)


class Utils(commands.Cog):

    """Comandos miscelaneos."""

    def __init__(self, client):
        self.client = client
        self.clientuptime.start()

    COG_EMOJI = "🧰"

    @commands.command(help="📇 - Calculadora bastante útil.")
    async def calculator(self, ctx):
        message = await ctx.send("Cargando....")
        embed = nextcord.Embed(
            title=f"Calculadora de {ctx.author.name}",
            color=nextcord.Color.green(),
            description="¡Ya puedes utilizarla!",
        )
        view = CalculatorButtons(ctx.author, embed, message)
        await message.edit(content=None, embed=embed, view=view)
    
    @nextcord.slash_command(name="calculator", description="Calculadora bastante útil.")
    async def _calculator(self, interaction: nextcord.Interaction):
        message = await interaction.send("Cargando....")
        embed = nextcord.Embed(
            title=f"Calculadora de {interaction.user.name}",
            color=nextcord.Color.green(),
            description="¡Ya puedes utilizarla!",
        )
        view = CalculatorButtons(interaction.user, embed, message)
        await message.edit(content=None, embed=embed, view=view)

    @commands.command(help = "🧑‍💻 - Muestra la información de usuario.")
    async def userinfo(self, ctx, *, user: nextcord.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Se unió en", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Usuario número", value=str(members.index(user) + 1))
        embed.add_field(name="Registrado", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_paginator = commands.Paginator(prefix="```diff", max_size=1000)
        for p in user.guild_permissions:
            perm_paginator.add_line(
                f"{'+' if p[1] else '-'} {str(p[0]).replace('_', ' ').title()}"
            )
        embed.add_field(
            name="Permisos", value=f"{perm_paginator.pages[0]}", inline=False
        )
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        return await ctx.send(embed=embed)
    
    @nextcord.slash_command(name="userinfo", description="Muestra la información de usuario.")
    async def _userinfo(self, interaction: nextcord.Interaction, user: nextcord.Member = None):
        if user is None:
            user = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Se unió en", value=user.joined_at.strftime(date_format))
        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Usuario número", value=str(members.index(user) + 1))
        embed.add_field(name="Registrado", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_paginator = commands.Paginator(prefix="```diff", max_size=1000)
        for p in user.guild_permissions:
            perm_paginator.add_line(
                f"{'+' if p[1] else '-'} {str(p[0]).replace('_', ' ').title()}"
            )
        embed.add_field(
            name="Permisos", value=f"{perm_paginator.pages[0]}", inline=False
        )
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        return await interaction.send(embed=embed)

    @commands.command(help = "🖥️ - Muestra la información del servidor.")
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embed2 = nextcord.Embed(
            timestamp=ctx.message.created_at, color=ctx.author.color
        )
        embed2.add_field(name="Nombre", value=f"{ctx.guild.name}", inline=False)
        embed2.add_field(
            name="Nivel de verificación",
            value=str(ctx.guild.verification_level),
            inline=True,
        )
        embed2.add_field(name="Rol más alto", value=ctx.guild.roles[-1], inline=True)
        embed2.add_field(name="Número de roles", value=str(role_count), inline=True)
        embed2.add_field(
            name="Número de miembros", value=ctx.guild.member_count, inline=True
        )
        embed2.add_field(
            name="Creado el",
            value=ctx.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=True,
        )
        embed2.add_field(name="Bots:", value=(", ".join(list_of_bots)), inline=False)
        embed2.set_thumbnail(url=ctx.guild.icon.url)
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed2.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed2)

    @nextcord.slash_command(name="serverinfo", description="Muestra la información del servidor.")
    async def _serverinfo(self, interaction: nextcord.Interaction):
        role_count = len(interaction.guild.roles)
        list_of_bots = [bot.mention for bot in interaction.guild.members if bot.bot]

        embed2 = nextcord.Embed(
            timestamp=datetime.utcnow(), color=interaction.user.color
        )
        embed2.add_field(name="Nombre", value=f"{interaction.guild.name}", inline=False)
        embed2.add_field(
            name="Nivel de verificación",
            value=str(interaction.guild.verification_level),
            inline=False,
        )
        embed2.add_field(name="Rol más alto", value=interaction.guild.roles[-1], inline=False)
        embed2.add_field(name="Número de roles", value=str(role_count), inline=False)
        embed2.add_field(
            name="Número de miembros", value=interaction.guild.member_count, inline=False
        )
        embed2.add_field(
            name="Creado el",
            value=interaction.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=False,
        )
        embed2.add_field(name="Bots:", value=(", ".join(list_of_bots)), inline=False)
        embed2.set_thumbnail(url=interaction.guild.icon.url)
        embed2.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
        embed2.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await interaction.send(embed=embed2)

    @commands.command(
        aliases=["cs", "ci", "channelinfo"], help = "📈 - Muestra las estadísticas e información del canal."
    )
    async def channelstats(self, ctx, channel: nextcord.TextChannel = None):
        if channel == None:
            channel = ctx.channel

        embed = nextcord.Embed(
            title=f"{channel.name}",
            description=f"{'Categoría - `{}`'.format(channel.category.name) if channel.category else '`Este canal no tiene categoría.`'}",
        )
        embed.add_field(name="Servidor", value=ctx.guild.name, inline=True)
        embed.add_field(name="Id del canal", value=channel.id, inline=True)
        embed.add_field(
            name="Tema del canal",
            value=f"{channel.topic if channel.topic else 'No tiene tema'}",
            inline=False,
        )
        embed.add_field(name="Posición del canal", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Canal de anuncios", value=channel.is_news(), inline=True)
        embed.add_field(
            name="Permisos del canal", value=channel.permissions_synced, inline=True
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)


    @nextcord.slash_command(name="channelinfo", description="Muestra la información del canal.")
    async def _channelinfo(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        if channel == None:
            channel = interaction.channel

        embed = nextcord.Embed(
            title=f"{channel.name}",
            description=f"{'Categoría - `{}`'.format(channel.category.name) if channel.category else '`Este canal no tiene categoría.`'}",
        )
        embed.add_field(name="Servidor", value=interaction.guild.name, inline=True)
        embed.add_field(name="Id del canal", value=channel.id, inline=True)
        embed.add_field(
            name="Tema del canal",
            value=f"{channel.topic if channel.topic else 'No tiene tema'}",
            inline=False,
        )
        embed.add_field(name="Posición del canal", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Canal de anuncios", value=channel.is_news(), inline=True)
        embed.add_field(
            name="Permisos del canal", value=channel.permissions_synced, inline=True
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await interaction.send(embed=embed)


    @commands.command(help="🏓 - Muestra el ping del bot")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ping(self, ctx):
        em = nextcord.Embed(colour=nextcord.Colour.random())
        em.set_author(
            name=f"Actualmente mi latencia es: {round(self.client.latency*1000)} ms", icon_url=self.client.user.display_avatar
        )
        em.set_footer(
            text=f"Ping solicitado por {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
        
    @nextcord.slash_command(name="ping", description="Muestra el ping del bot")
    async def _ping(self, interaction: nextcord.Interaction):
        em = nextcord.Embed(colour=nextcord.Colour.random())
        em.set_author(
            name=f"Actualmente mi latencia es: {round(self.client.latency*1000)} ms", icon_url=self.client.user.display_avatar
        )
        em.set_footer(
            text=f"Ping solicitado por {interaction.user}", icon_url=interaction.user.display_avatar
        )
        await interaction.send(embed=em)
        
        
    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif not var_length:
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (
            variable
            if (len(f"{variable}") <= 1000)
            else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>"
        )

    def prepare(self, string):
        arr = (
            string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        )
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(
        pass_context=True,
        aliases=["eval", "exec", "evaluate"],
        help = "✏️ - Evalúa el código entregado.",
    )
    async def _eval(self, ctx, *, code: str):
        if not ctx.author.id == 200391563346575361:
            ctx.reply("Esto es un comando de desarrollo.")
            return
        silent = "-s" in code

        code = self.prepare(code.replace("-s", ""))
        args = {
            "nextcord": nextcord,
            "sauce": getsource,
            "sys": sys,
            "os": os,
            "imp": __import__,
            "this": self,
            "ctx": ctx,
            "member": ctx.author,
            "client": self.client,
        }

        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, nextcord.Message):
                em = nextcord.Embed(
                    title="Eval Success!",
                    description="```Code ran without any errors```",
                )
                await ctx.send(embed=em)
                del args, code
                return
            em = nextcord.Embed(
                title="Eval Success without problems!",
                description=f"```py\n{self.resolve_variable(response)}```",
            )
            em.set_footer(
                text=f"`{type(response).__name__} | {(time() - a) / 1000} ms`"
            )
            await ctx.send(embed=em)
        except Exception as e:
            em = nextcord.Embed(
                title="Eval Error!",
                description=f"```{type(e).__name__}: {str(e)}```",
            )
            await ctx.send(embed=em)

        del args, code, silent

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Utils enabled.\u001b[0m")
    
    
    @tasks.loop(seconds=2.0)
    async def clientuptime(self):
        global uh, us, um, ud
        us += 2
        if us == 60:
            us = 0
            um += 1
            if um == 60:
                um = 0
                uh += 1
                if uh == 24:
                    uh = 0
                    ud += 1

    @clientuptime.before_loop
    async def before_clientuptime(self):
        await self.client.wait_until_ready()

    @commands.command(
        help="📟 - Información y estado del bot."
    )

    @commands.cooldown(1, 15, commands.BucketType.user)
    async def status(self, ctx):
        global ud, um, uh, us
        em = nextcord.Embed(title="\u200b")
        em.set_author(name=f"Estado de la VPS.", icon_url=ctx.guild.icon)
        em.add_field(name="Días:", value=ud)
        em.add_field(name="Horas:", value=uh)
        em.add_field(name="Minutos:", value=um)
        em.add_field(name="Segundos:", value=us)
        em.add_field(name="Uso del CPU:", value=f"{psutil.cpu_percent()}%")
        em.add_field(name="Uso de RAM:", value=f"{psutil.virtual_memory()[2]}%")
        em.set_footer(
            text=f"Estado solicitado por {ctx.author.name}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
    
    @nextcord.slash_command(description="📟 - Información y estado del bot.")
    async def status(self, interaction: nextcord.Interaction):
        global ud, um, uh, us
        em = nextcord.Embed(title="\u200b")
        em.set_author(name=f"Estado de la VPS.", icon_url=interaction.guild.icon)
        em.add_field(name="Días:", value=ud)
        em.add_field(name="Horas:", value=uh)
        em.add_field(name="Minutos:", value=um)
        em.add_field(name="Segundos:", value=us)
        em.add_field(name="Uso del CPU:", value=f"{psutil.cpu_percent()}%")
        em.add_field(name="Uso de RAM:", value=f"{psutil.virtual_memory()[2]}%")
        em.set_footer(
            text=f"Estado solicitado por {interaction.user.name}", icon_url=interaction.user.display_avatar
        )
        await interaction.response.send_message(embed=em)
    

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(876845404786946099):
            send = message.channel.send
        
        #if channel id == 876845404786946099:
        if message.channel.id == 1054111038427123842:
            #delete all messages
            try: 
                await message.delete()
            except:
                pass
    
    
    @commands.command(help = "📶 - Te da la información sobre una IP.")
    async def iplookup(self, ctx, *, ipaddr: str = "9.9.9.9"):
        r = requests.get(f"http://extreme-ip-lookup.com/json/{ipaddr}?key={IPKEY}")
        geo = r.json()
        em = nextcord.Embed()
        fields = [
            {'name': 'IP Address', 'value': geo['query']},
            {'name': 'Country', 'value': geo['country']},
            {'name': 'City', 'value': geo['city']},
            {'name': 'Region', 'value': geo['region']},
            {'name': 'Latitude', 'value': geo['lat']},
            {'name': 'Longitude', 'value': geo['lon']},
            {'name': 'ISP', 'value': geo['isp']},
            {'name': 'Status', 'value': geo['status']},
            {'name': 'Organization', 'value': geo['org']},
            {'name': 'Country Code', 'value': geo['countryCode']},
            {'name': 'IP Type', 'value': geo['ipType']},
            {'name': 'Continent', 'value': geo['continent']},
        ]
        for field in fields:
            if field['value']:
                em.set_footer(text=f"IP requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                em.add_field(name=field['name'], value=field['value'])
                em.set_author(name=f"IP Lookup", icon_url=ctx.guild.icon)
        
        await ctx.send(embed=em)
        c = nextcord.Client()
        return await c.close()
    
    @nextcord.slash_command(description="📶 - Te da la información sobre una IP.")
    async def iplookup(self, interaction: nextcord.Interaction, *, ipaddr: str = "9.9.9.9"):
        r = requests.get(f"http://extreme-ip-lookup.com/json/{ipaddr}?key={IPKEY}")
        geo = r.json()
        em = nextcord.Embed()
        fields = [
            {'name': 'IP Address', 'value': geo['query']},
            {'name': 'Country', 'value': geo['country']},
            {'name': 'City', 'value': geo['city']},
            {'name': 'Region', 'value': geo['region']},
            {'name': 'Latitude', 'value': geo['lat']},
            {'name': 'Longitude', 'value': geo['lon']},
            {'name': 'ISP', 'value': geo['isp']},
            {'name': 'Status', 'value': geo['status']},
            {'name': 'Organization', 'value': geo['org']},
            {'name': 'Country Code', 'value': geo['countryCode']},
            {'name': 'IP Type', 'value': geo['ipType']},
            {'name': 'Continent', 'value': geo['continent']},
        ]
        for field in fields:
            if field['value']:
                em.set_footer(text=f"IP requested by: {interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.timestamp = datetime.utcnow()
                em.add_field(name=field['name'], value=field['value'])
                em.set_author(name=f"IP Lookup", icon_url=interaction.guild.icon)
        
        await interaction.response.send_message(embed=em)
        c = nextcord.Client()
        return await c.close()


    @commands.command(help = "🎵 - Información sobre lo que escucha un usuario en Spotify.")
    async def spotify(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author

        spotify_result = next((activity for activity in user.activities if isinstance(activity, nextcord.Spotify)), None)
        if spotify_result == None:
            await ctx.reply(f'{user.name} No está escuchando nada en Spotify.')

        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    url=(f'https://open.spotify.com/track/{spotify_result.track_id}')
                    embed = nextcord.Embed(
                        title = f"Spotify de {user.name}",
                        description = f"Está escuchando: [{activity.title}]({url})",
                        color = 0xC902FF,
                        timestamp=datetime.utcnow() )
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artista", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon)
                    await ctx.send(embed=embed)
         
                    
    @nextcord.slash_command(description="🎵 - Información sobre lo que escucha un usuario en Spotify.")
    async def spotify(self, interaction: nextcord.Interaction, user: nextcord.Member = None):
        if not user:
            user = interaction.user

        spotify_result = next((activity for activity in user.activities if isinstance(activity, nextcord.Spotify)), None)
        if spotify_result == None:
            await interaction.response.send_message(f'{user.name} No está escuchando nada en Spotify.')

        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    url=(f'https://open.spotify.com/track/{spotify_result.track_id}')
                    embed = nextcord.Embed(
                        title = f"Spotify de {user.name}",
                        description = f"Está escuchando: [{activity.title}]({url})",
                        color = 0xC902FF,
                        timestamp=datetime.utcnow() )
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artista", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon)
                    await interaction.response.send_message(embed=embed)
    
    @commands.command(help="🤳 - Muestra el avatar de un usuario.")
    async def avatar(self, ctx, *, member : nextcord.Member = None):
        if member == None:
            member = ctx.author

        memberAvatar = member.avatar

        avaEmbed = nextcord.Embed(color=nextcord.Color.random())
        avaEmbed.set_image(url = memberAvatar)
        avaEmbed.set_author(name=f"Avatar de {member.name}", icon_url=member.avatar)
        avaEmbed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed = avaEmbed)
    
    
    @nextcord.slash_command(description="Muestra el avatar de un usuario.")
    async def avatar(self, interaction: nextcord.Interaction, member : nextcord.Member = None):
        if member == None:
            member = interaction.user

        memberAvatar = member.avatar

        avaEmbed = nextcord.Embed(color=nextcord.Color.random())
        avaEmbed.set_image(url = memberAvatar)
        avaEmbed.set_author(name=f"Avatar de {member.name}", icon_url=member.avatar)
        avaEmbed.set_footer(text=f"Solicitado por {interaction.user}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed = avaEmbed)
    
    @commands.command(help="📃 - General bot info.")
    async def info(self, ctx):
        info = nextcord.Embed(color = nextcord.Colour.random(), description = "¡Soy WillardBot, dispuesto a ayudarte en todo lo que necesites!")
        info.set_author(name = "➜ Sobre WillardBot.", icon_url="https://media.discordapp.net/attachments/931640602490187866/993197355341971456/ezgif-1-7404e335a6.gif")
        info.add_field(name = "`🤖| Estadísticas e Información.`", value = f"""
        🧟 - ``Mi desarrollador es`` ➜ [Usuariozombie#9110](https://discord.com/users/200391563346575361).
        🥳 - ``Fui creado el`` <t:1629064800:D>.
        🖥️ - ``Desarrollado en Python, usando Nextcord.``
        ✏️ - ``Versión 1.0 Estable.``
        🗃️ - ``Trabajando en {len(self.client.guilds)} servers.``
        💬 - ``Ayudando a {len(self.client.users)} usuarios.``""", inline = False)
        info.set_footer(text="Owned by Willard Networks.")
        await ctx.reply(embed=info)


    @nextcord.slash_command(description="📃 - Información general del bot.")
    async def info(self, interaction: nextcord.Interaction):
        info = nextcord.Embed(color = nextcord.Colour.random(), description = "¡Soy WillardBot, dispuesto a ayudarte en todo lo que necesites!")
        info.set_author(name = "➜ Sobre WillardBot.", icon_url="https://media.discordapp.net/attachments/931640602490187866/993197355341971456/ezgif-1-7404e335a6.gif")
        info.add_field(name = "`🤖| Estadísticas e Información.`", value = f"""
        🧟 - ``Mi desarrollador es`` ➜ [Usuariozombie#9110](https://discord.com/users/200391563346575361).
        🥳 - ``Fui creado el`` <t:1629064800:D>.
        🖥️ - ``Desarrollado en Python, usando Nextcord.``
        ✏️ - ``Versión 1.0 Estable.``
        🗃️ - ``Trabajando en {len(self.client.guilds)} servers.``
        💬 - ``Ayudando a {len(self.client.users)} usuarios.``""", inline = False)
        info.set_footer(text="Owned by Willard Networks.")
        await interaction.response.send_message(embed=info)

    
    @nextcord.slash_command(name = "ticket", description="🎫 - Abre un ticket.")
    async def _ticket(self, interaction: nextcord.Interaction, type: str = nextcord.SlashOption(name="hilo", choices={"Público":"pub", "Privado":"pri"})):
        
        #if a thread with the same name exists, send a message and return
        if type == "pri": 
            if any(thread.name == f"ticket-{interaction.user.name}" for thread in interaction.channel.threads):
                await interaction.send("Ya tienes un ticket abierto.", ephemeral=True)
                return
            elif interaction.channel.id == 1054111038427123842:
                #create a thread with user name
                thread = await interaction.channel.create_thread(name=f"ticket-{interaction.user.name}", type=nextcord.ChannelType.private_thread)
                #send a message in the thread
                await thread.send(f"Ticket creado por {interaction.user.mention} -- *usa /close para cerrar el ticket cuando se resuelva tu duda*")
                #send a message in the channel
                await interaction.send(f"Ticket creado en {thread.mention}", ephemeral=True)
                #notify admins in channel 1046191747451068517
                await self.client.get_channel(1046191747451068517).send(f"Ticket creado por {interaction.user.mention} en {thread.mention}")
            else:
                await interaction.send("No puedes crear un ticket aquí, prueba en <#1054111038427123842>.", ephemeral=True)
        elif type == "pub":
            if any(thread.name == f"ticket-{interaction.user.name}" for thread in interaction.channel.threads):
                await interaction.send("Ya tienes un ticket abierto.", ephemeral=True)
                return
            elif interaction.channel.id == 1054111038427123842:
                #create a thread with user name
                thread = await interaction.channel.create_thread(name=f"ticket-{interaction.user.name}", type=nextcord.ChannelType.public_thread)
                #send a message in the thread
                await thread.send(f"Ticket creado por {interaction.user.mention}")
                #send a message in the channel
                await interaction.send(f"Ticket creado en {thread.mention}", ephemeral=True)
                #notify admins in channel 1046191747451068517
                await self.client.get_channel(1046191747451068517).send(f"Ticket creado por {interaction.user.mention} en {thread.mention}")
            else:
                await interaction.send("No puedes crear un ticket aquí, prueba en <#1054111038427123842>.", ephemeral=True)
        
    @nextcord.slash_command(name = "close", description="🔒 - Cierra un ticket.")
    async def _close(self, interaction: nextcord.Interaction):
        #if the channel is not a thread, send a message and return
        if interaction.channel.name != f"ticket-{interaction.user.name}":
            await interaction.send("Este no es tu ticket.", ephemeral=True)
            return
        else:
            #send a message in the thread
            await interaction.channel.send(f"Ticket cerrado por {interaction.user.mention}")
            #delete the thread
            await interaction.channel.delete()
            #send a message in the channel
            await interaction.send("Ticket cerrado.", ephemeral=True)
            #notify admins in channel 1046191747451068517
            await self.client.get_channel(1046191747451068517).send(f"Ticket de {interaction.user.mention} **cerrado**")

        
    @nextcord.slash_command(name = "help", description="📃 - Lista de comandos.")
    async def _commandlist(self, interaction: nextcord.Interaction, page: str = nextcord.SlashOption(name="category", choices={"Útiles":"utl", "Moderación":"mod"})):
        if page == "utl":
            embedutils = nextcord.Embed(title="Comandos de WillardBot", description="Comandos útiles.", color=nextcord.Colour.random())
            embedutils.add_field(name="💤 - AFK", value="``/afk - Avisa de que estás afk``", inline=False)
            embedutils.add_field(name="🎵 - Spotify", value="``/spotify - Información sobre lo que escucha un usuario en Spotify.``", inline=False)
            embedutils.add_field(name="🤳 - Avatar", value="``/avatar - Muestra el avatar de un usuario.``", inline=False)
            embedutils.add_field(name="🌡️ - Weather", value="``/weather - Muestra la temperatura de una ciudad.``", inline=False)
            embedutils.add_field(name="📃 - Info", value="``/info - Información general del bot.``", inline=False)
            embedutils.add_field(name="🧑‍💻 - Userinfo", value="``/userinfo - Muestra la información de usuario.``", inline=False)
            embedutils.add_field(name="✏️ - Eval", value="``/eval - Evalúa código. (comando de desarrollador)``", inline=False)
            embedutils.add_field(name="📶 - Iplookup", value="``/iplookup - Muestra información sobre una IP.``", inline=False)
            embedutils.add_field(name="📟 - Status", value="``/status - Información y estado del bot.``", inline=False)
            embedutils.add_field(name="📈 - Channelstats", value="``/channelstats - Muestra estadísticas de un canal.``", inline=False)
            embedutils.add_field(name="🏓 - Ping", value="``/ping - Muestra el ping del bot.``", inline=False)
            embedutils.add_field(name="🖥️ - Serverinfo", value="``/serverinfo - Muestra información del servidor.``", inline=False)
            embedutils.add_field(name="📇 - Calculator", value="``/calculator - Calculadora.``", inline=False)
            embedutils.add_field(name="🗃 - Activities", value="``/activities - Muestra las actividades para realizar en grupo en discord.``", inline=False)
            embedutils.add_field(name="🎖️ - Achievements", value="``/achievements - Muestra los logros del servidor.``", inline=False)
            embedutils.add_field(name="📜 - Progress", value="``/progress - Muestra tu progreso en los logros del servidor.``", inline=False)
            embedutils.add_field(name="🏆 - Leaderboard", value="``/leaderboard - Muestra el top de usuarios con más logros.``", inline=False)
            embedutils.add_field(name="📬 - Ticket", value="``/ticket - Crea un ticket.``", inline=False)
            embedutils.add_field(name="🔒 - Close", value="``/close - Cierra un ticket.``", inline=False)
            embedutils.add_field(name="ℹ️ - Ingame", value="``/ingame - Muestra información sobre el servidor de Garry's Mod``", inline=False)
            embedutils.set_footer(text="Página de Útiles.")
            await interaction.response.send_message(embed=embedutils, ephemeral=True)
        elif page == "mod":
            embedutils2 = nextcord.Embed(title="Comandos de WillardBot", description="Comandos de moderación.", color=nextcord.Colour.random())
            embedutils2.add_field(name="🔨 - Ban", value="``/ban - Banea a un usuario.``", inline=False)
            embedutils2.add_field(name="🔧 - Unban", value="``/unban - Desbanea a un usuario.``", inline=False)
            embedutils2.add_field(name="🐢 - Slowmode", value="``/slowmode - Establece el slowmode de un canal.``", inline=False)
            embedutils2.add_field(name="🔇 - Mute", value="``/mute - Silencia a un usuario.``", inline=False)
            embedutils2.add_field(name="🔊 - Unmute", value="``/unmute - Quita el silencio a un usuario.``", inline=False)
            embedutils2.add_field(name="🦵 - Kick", value="``/kick - Expulsa a un usuario.``", inline=False)
            embedutils2.add_field(name="🗑️ - Clear", value="``/clear - Borra mensajes.``", inline=False)
            embedutils2.add_field(name="➕ - Addrole", value="``/addrole - Añade un rol a un usuario.``", inline=False)
            embedutils2.add_field(name="➖ - Removerole", value="``/removerole - Quita un rol a un usuario.``", inline=False)
            embedutils2.add_field(name="🎚️ - Switch", value="``/switch - Habilita o deshabilita comandos``", inline=False)
            embedutils2.add_field(name="❗ - Warn", value="``/warn - Avisa a un usuario.``", inline=False)
            embedutils2.add_field(name="📋 - Warnlist", value="``/warns - Muestra los avisos de un usuario.``", inline=False)
            embedutils2.add_field(name="📋 - Clearwarns", value="``/clearwarns - Borra los avisos de un usuario.``", inline=False)
            embedutils2.set_footer(text="Página de Moderación.")
            await interaction.response.send_message(embed=embedutils2, ephemeral=True)
        else:
            await interaction.response.send_message("Página no encontrada.", ephemeral=True)
        
        
        
            

        
   

def setup(client):
    client.add_cog(Utils(client))