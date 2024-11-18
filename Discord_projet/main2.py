import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord_components import DiscordComponents, Button, ComponentsBot, SelectOption, Select, ButtonStyle

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='*', intents=intents)
DiscordComponents(client)

# async et await = coroutines
@client.event
async def on_ready():
    print('Le bot est prêt')

@client.event
async def on_member_join(member):
    channel = client.get_channel(966695229468078155)
    embed=discord.Embed(title=f"Bienvenue {member.name} sur le serveur {member.guild.name}! 🎉",
                        description=f"Je m'appelle NEM le bot! 🤗Je vais gérer plein de petit évenements que je t'expliquerais en détail dans ta messagerie privée en tapant *dm."
                        "Ce serveur va rester actif donc tu pourras discuter avec d'autres éléves d'NSI et leurs demander des conceils.👍"
                        )
    embed.set_thumbnail(url=member.avatar_url) 
    await channel.send(embed=embed)

@client.event
async def on_command_error(ctx, error): #ctx = contexte
    if isinstance(error, commands.CommandNotFound):  #vérifie si la commande existe pas
        await ctx.send('! La commande n\'existe pas. Recommencer.')

@client.command()
async def dm(ctx):
    await ctx.author.send('Voici les détails: \n Ce serveur est uniquement crée pour un but éducatif au sein de la spécialité NSI.'
    'Donc il y a 2 régles principales : 1/ Pas d\'insultes entre éléves \n2/ On ne vole pas le projet des autres mais vous pouvez vous inspirer ou du moins présenter la source. \n'
    '! Attention ceux qui ne respectent pas ces régles peuvent êtres banis !\n'
    'Si vous y tenait a votre avenir dans le domaine informatique alors on compte sur vous 😊')


@client.command()
async def hello(ctx):
    await ctx.send("hello", components = [
        [Button(label="Hi", style="3", emoji = "👋🏼", custom_id="button1"), 
        Button(label="Bye", style="4", emoji = "😔", custom_id="button2")]#Le 2e crochet permet de mettre les bouttons 
        ])                                                                  #côte à côte et pas haut en bas
    interaction = await client.wait_for("button_click")

    await interaction.send(content = "Button clicked!", ephemeral=True)
    

@client.command(name='del')
async def delete(ctx, numbers_mess: int):
    message = await ctx.channel.history(limit=numbers_mess + 1).flatten()

    for each_message in message:
        await each_message.delete()

@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('! Vous devez précicer le nombre.')


@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, user:discord.User, *, reason =None):
    if reason is None:
        embed=discord.Embed(title=":warning: Erreur dans la commande de warn",
        description= "L'argument `reason` est requis",
        color =discord.Color.red())
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        embed = discord.Embed(title="Un utilisateur a recu un avertissement", 
        description= "un administrateura a donné un warn",
        color=discord.Color.orange())
        #embed.set_author(name="@system", url=ctx.autor.avatar_url)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/OOjs_UI_icon_alert-destructive.svg/2048px-OOjs_UI_icon_alert-destructive.svg.png")
        embed.add_field(name="membre averti:", value=user.name+"#"+str(user.discriminator))
        embed.add_field(name="Auteur:", value=ctx.author.name+"#"+str(ctx.author.discriminator),inline=True)
        embed.add_field(name="Raison", value=reason,inline=False)
        await ctx.send(embed=embed)



@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user:discord.User, *, reason =None):
    if reason is None:
        embed=discord.Embed(title=":warning: Erreur dans la commande kick",
        description= "L'argument `reason` est requis",
        color =discord.Color.blurple())
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        await ctx.guild.kick(user, reason=reason)
        embed = discord.Embed(title="Un utilisateur a été expulsé", 
        description= "un administrateura a expulsé un membre",
        color=discord.Color.red())
        #embed.set_author(name="@system", url=ctx.autor.avatar_url)
        embed.set_thumbnail(url="https://images.mydoorsign.com/img/lg/S/exit-entrance-sign-s-1257_sswhrd.png")
        embed.add_field(name="membre expulsé:", value=user.name+"#"+str(user.discriminator))
        embed.add_field(name="Auteur:", value=ctx.author.name+"#"+str(ctx.author.discriminator),inline=True)
        embed.add_field(name="Raison", value=reason,inline=False)
        await ctx.send(embed=embed)
        channel = client.get_channel(966695229468078155)

@client.command()
async def liens(ctx):
    await ctx.send("Voulez des liens qui pourront vous aidez pour les cours de NSI ?", 
    components = [
        [Button(label="YES", style="3", custom_id="button1"), 
        Button(label="NO", style="4", custom_id="button2")]
        ])
    interaction = await client.wait_for("button_click", 
    check = lambda i: i.custom_id == "button1")
    await interaction.send(content = "Voici des liens: https://developer.mozilla.org/fr/docs/Web/HTML \n https://www.editions-bordas.fr/cahier-nsi-1re-collection-30.html \n https://www.numerique-sciences-informatiques.fr/  ", ephemeral=False)
    interaction2 = await client.wait_for("button_click", 
    check = lambda i: i.custom_id == "button2")
    await interaction2.send(content = "OK. Bonne journée ", ephemeral=False)

@client.command()
async def projet(ctx):
    embed = discord.Embed(title='Lien projet de NSI',
    description="Vous allez reçevoir un lien drive dans votre messagerie privé, dans lequel se trouve des projets d'anciens élèves de NSI qui pourront peut-être vous aidez")
    await ctx.send(embed=embed, 
    components=[Button(label='Reçevoir', 
    custom_id="test-id", style=ButtonStyle.green)])
    interaction = await client.wait_for("button_click", 
    check=lambda inter: inter.custom_id == "test-id")

@client.event
async def on_button_click(interaction):
    await interaction.respond(type=6)
    await interaction.author.send("https://drive.google.com/drive/u/3/my-drive")



@client.command()
async def quiz(ctx):
    await ctx.send("Quelle commande permet d'afficher une chaîne de caractère ? \n A: import() \n B: input() \n C: print()", 
            components = [
        Select(
            placeholder = "Choisi",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B"),
                SelectOption(label="C", value="C")
            ]
        )
    ])

    select_interaction = await client.wait_for("select_option")
    await select_interaction.send(content = f"{select_interaction.values[0]} sélectionné", 
    ephemeral = False)
    if select_interaction.values[0] == "A":
        await ctx.send("Faux. Bonne réponse: C")
    elif select_interaction.values[0] == "B":
        await ctx.send("Faux. Bonne réponse: C")
    elif select_interaction.values[0] == "C":
        await ctx.send("Bravo, c'est la bonne réponse")

    await ctx.send("Quel est le nom du type de variables des nombres entiers ? \n A: Integer \n B: String \n C: Floats", 
    components = [
        Select(
            placeholder = "Choisi",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B"),
                SelectOption(label="C", value="C")
            ]
        )
    ])

    select_interaction = await client.wait_for("select_option")
    await select_interaction.send(content = f"{select_interaction.values[0]} sélectionné", 
    ephemeral = False)
    if select_interaction.values[0] == "A":
        await ctx.send("Bravo, c'est la bonne réponse")
    elif select_interaction.values[0] == "B":
        await ctx.send("Faux. Bonne réponse: A")
    elif select_interaction.values[0] == "C":
        await ctx.send("Faux. Bonne réponse: A")

    await ctx.send("Quel élément HTML représente un paragraphe de texte ? \n A: <h> \n B: <ol> \n C: <p>", components = [
        Select(
            placeholder = "Choisi",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B"),
                SelectOption(label="C", value="C")
            ]
        )
    ])

    select_interaction = await client.wait_for("select_option")
    await select_interaction.send(content = f"{select_interaction.values[0]} sélectionné", ephemeral = False)
    if select_interaction.values[0] == "A":
        await ctx.send("aux. Bonne réponse: C")
    elif select_interaction.values[0] == "B":
        await ctx.send('Faux. Bonne réponse: C')
    elif select_interaction.values[0] == "C":
        await ctx.send("Bravo, c'est la bonne réponse")


    await ctx.send("Que signifie HTML ? \n A: Hypertext Market Language \n B: Hypertext Markup Language \n C: Hypertext Markup Launch", components = [
        Select(
            placeholder = "Choisi",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B"),
                SelectOption(label="C", value="C")
            ]
        )
    ])

    select_interaction = await client.wait_for("select_option")
    await select_interaction.send(content = f"{select_interaction.values[0]} sélectionné", ephemeral = False)
    if select_interaction.values[0] == "A":
        await ctx.send("Faux. Bonne réponse: B")
    elif select_interaction.values[0] == "B":
        await ctx.send("Bravo, c'est la bonne réponse")
    elif select_interaction.values[0] == "C":
        await ctx.send("Faux. Bonne réponse: B")
        
    await ctx.send("Linux est... \n A: Un programme \n B: Un système d'exploitation \n C: Une application", components = [
        Select(
            placeholder = "Choisi",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B"),
                SelectOption(label="C", value="C")
            ]
        )
    ])

    select_interaction = await client.wait_for("select_option")
    await select_interaction.send(content = f"{select_interaction.values[0]} sélectionné", ephemeral = False)
    if select_interaction.values[0] == "A":
        await ctx.send("Faux. Bonne réponse: B")
    elif select_interaction.values[0] == "B":
        await ctx.send("Bravo, c'est la bonne réponse")
    elif select_interaction.values[0] == "C":
        await ctx.send("Faux. Bonne réponse: B")


client.run(os.getenv('TOKEN'))