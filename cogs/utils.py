from distutils.log import error
from multiprocessing.sharedctypes import Value
import time, sys, os, nextcord, requests, aiohttp, psutil, json, asyncio, urllib.parse, random
from inspect import getsource
from time import time
from datetime import datetime
from nextcord.ext import commands, tasks
from io import BytesIO
from main import IPKEY, APIKEY
from global_functions import EMOJIS_TO_USE_FOR_CALCULATOR as etufc
from nextcord import ButtonStyle, Spotify
from nextcord.ui import button, View, Button
from pytube import YouTube
from weather import *

API_TOKEN = 'a2qc6acZ3PswJEEr5FF5P08vGZvC1TsgFxKgjOuH'

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


    @commands.command(help = "🧑‍💻 - Muestra la información de usuario.")
    async def userinfo(self, ctx, *, user: nextcord.Member = None):  # b'\xfc'
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
    

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(876845404786946099):
            send = message.channel.send
    
    
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
    
    @commands.command(help="🌡️ - Muestra la temperatura de una ciudad.")
    async def weather(self ,ctx, *, location):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={APIKEY}&units=metric'
        try:
            data=json.loads(requests.get(url).content)
            data = parse_data(json.loads(requests.get(url).content)['main'])
            await ctx.send(embed=weather_message(data, location))
        except KeyError:
            await ctx.send(embed=error_message(location))
    
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

   

def setup(client):
    client.add_cog(Utils(client))