import discord

from main import *
from main import client
from functions import *
from discord_components import DiscordComponents, InteractionEventType, Button, ButtonStyle
import atributos

@client.event
async def on_ready():
    print(f"Bot ON\nUser: {client.user} | Name: {client.user.name} | ID: {client.user.id}")

    await client.change_presence(activity=discord.Game(name=f".help | Melhor Bot de RPG confia"))
    DiscordComponents(client)

    try: Connector(rules).execute("")
    except mysql.connector.errors.InterfaceError: print('Conexão não estabelecida')
    else: print('Conexão estabelecida')



@client.event
async def on_button_click(interaction):
    """
            {'version': 1, 'type': 3,
             'token': 'aW50ZXJhY3Rpb246OTM4MTQxMzA4MzIzNzc4NTkxOk0xbFVmc2FtempITzdVMjBpZmU2amxsSmQzNWozMmtKQzdNYVlkTEd1ZWRMZTVEclBjZTduUzJETHBFRXBEc3FmT3pZaGU2UWJKOTdRUDloYW1QWnJKM09KdFlyQVdTeEZQMUl1ZGVhQWNzT2c5R1RyZVpYTW0yQk9NT2duMm41',
             'message': {'type': 0, 'tts': False, 'timestamp': '2022-02-01T15:58:50.165000+00:00', 'pinned': False,
                         'mentions': [], 'mention_roles': [], 'mention_everyone': False, 'id': '938101095174139924', 'flags': 0,
                         'embeds': [], 'edited_timestamp': '2022-02-01T18:34:29.089000+00:00', 'content': 'funcionou?',
                         'components': [{'type': 1, 'components': [
                                 {'type': 2, 'style': 4, 'label': 'Golpe Da Morte', 'hash': '',
                                  'custom_id': 'btn_atc.monstro_teste.1d20.20.0'}]},
                            {'type': 1, 'components': [
                                 {'type': 2, 'style': 4, 'label': 'Golpe Que Mata', 'hash': '',
                                  'custom_id': 'btn_atc.monstro_teste.1d50.30.1'}]},
                            {'type': 1, 'components': [
                                 {'type': 2, 'style': 4, 'label': 'Golpe Mortifero', 'hash': '',
                                  'custom_id': 'btn_atc.monstro_teste.1d100.40.2'}]},
                            {'type': 1, 'components': [
                                 {'type': 2, 'style': 4, 'label': 'Espada', 'hash': '',
                                  'custom_id': 'btn_atc.monstro_teste.1d6.numtem.3'}]}],
                         'channel_id': '812327180423921684',
                         'author': {'username': 'Elixir', 'public_flags': 0, 'id': '873979047640711188',
                                    'discriminator': '0869', 'bot': True, 'avatar': '7f85b93905ced54a8f5c60bb8a324a93'},
                         'attachments': []}, 'member': {
                'user': {'username': 'Mestre dos magos', 'public_flags': 0, 'id': '675407695729131527', 'discriminator': '0112',
                         'avatar': '79015faabf4de8f4aedac15e1020d1bf'},
                'roles': ['811610862589968385', '829851857379131393', '818477283186573333', '871773357178249306',
                          '883578855535804476', '837652482506096670', '812306926737162303'], 'premium_since': None,
                'permissions': '1090921168631', 'pending': False, 'nick': 'Marijans| 13/50| 155/500|', 'mute': False,
                'joined_at': '2021-02-18T10:32:18.401000+00:00', 'is_pending': False, 'deaf': False,

    """

    if interaction.custom_id.startswith('mon'):
        custom_id = inteom_id[4:]
        print(custom_id)

        for comp in interaction.raw_data.get('message').get('components'):
            if comp.get('components')[0].get('custom_id') == interaction.custom_id: label = comp.get('components')[0].get('label')

        ctx = interaction.message



        if custom_id.startswith('btn_block'):
            token = custom_id.split('.')[1]
            await atributos.stre(ctx, token='monstro ' + token)
        if custom_id.startswith('btn_esquiv'):
            token = custom_id.split('.')[1]
            await atributos.dex(ctx, token='monstro ' + token)

        if custom_id.startswith('btn_atc'):
            properties = custom_id.split('.')
            dado = rolagemTag(properties[2])[0]
            contents = f'{properties[1].title()}: {label} = {properties[2]}\n{dado}'
            await ctx.reply(contents)

    elif interaction.custom_id.startswith('pla'):
        custom_id = interaction.custom_id[4:]

        for comp in interaction.raw_data['message']['components'][0]['components']:
            print(interaction.raw_data['message']['components'][0]['components'])
            print(comp)
            print(comp['custom_id'])
            print(interaction.custom_id)
            if comp['custom_id'] == interaction.custom_id:
                label = comp['label']

        ctx = interaction.message

        if custom_id.startswith('btn_block'):
            token = custom_id.split('.')[1]
            await atributos.stre(ctx, token=token)
        if custom_id.startswith('btn_esquiv'):
            token = custom_id.split('.')[1]
            await atributos.dex(ctx, token=token)

        if custom_id.startswith('btn_atc'):
            properties = custom_id.split('.')
            dado = rolagemTag(properties[2])[0]
            contents = f'{properties[1].title()}: {label} = {properties[2]}\n{dado}'
            await ctx.reply(contents)

    elif interaction.custom_id.startswith("help"):
        contents = interaction.custom_id.split('.')
        print(contents)
        ctx = interaction.message

        if int(contents[3]) != interaction.user.id:
            print(f'contents[3]: {contents[3]}')
            print(f"interaction.user.id: {interaction.user.id}")
            print('Retornou')
            return


        pages = [secao1(ctx), secao2(ctx), secao3(ctx), secao4(ctx), secao5(ctx)]

        if contents[1] == 'pass_left' and int(contents[2]) > 0:
            print("pá tras")
            print(f'contents[2]: {contents[2]}')
            page = int(contents[2]) - 1
        elif contents[1] == 'pass_right' and int(contents[2]) < len(pages):
            print('pá frente')
            print(f'contents[2]: {contents[2]}')
            page = int(contents[2]) + 1
            print(f'page: {page}')
        else:
            print('pá rado')
            print(f'contents[2]: {contents[2]}')
            print(f"len(pages): {len(pages)}")
            page = int(contents[2])
            print(f'page: {page}')

        buttons = [
            Button(style=ButtonStyle.blue, emoji="◀️", custom_id=f'help.pass_left.{page}.{interaction.user.id}'),
            Button(style=ButtonStyle.blue, emoji="▶️", custom_id=f'help.pass_right.{page}.{interaction.user.id}')
        ]
        await ctx.edit(embed=pages[page], components=[buttons])

    elif interaction.custom_id.startswith("server_info"):
        contents = interaction.custom_id.split('.')
        ctx = interaction.message
        if contents[1] == 'raphakawai':
            await ctx.reply('RAPHAEL KAWAAAIIIIIIIIIIII')
        if contents[1] == 'bolo':
            await ctx.reply('BOOOOOLOOOO :cake: :cake::cake: :cake: :birthday: :birthday: :birthday: ')
        if contents[1] == 'festim':
            await ctx.reply('É FEXXXTAAAA :tada: :partying_face: :tada: :partying_face: :tada: :partying_face:')
    else:
        return


@client.event
async def on_member_join(member: discord.Member):
    embed = discord.Embed(
        title=f'Olá {member.name} :man_mage:',
        description=f'Seja muito bem vindo ao reino de Impéria, {member.mention}\num lugar mágico criado por <@621664265907994624>.\nSinta-se a vontade para explorar o sevidor.\nQualquer dúvida fique livre para perguntar, \nsempre tem gente online para responder\n',
        color=corConvert('roxo')
    )

    embed.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text='Meu criador: Mestre dos magos#0112 (que não ganhou meio centavo pra faze esse bot cof cof mextre cof cof)')
    embed.set_image(
        url="https://media3.giphy.com/media/3oriNPdeu2W1aelciY/giphy.gif?cid=790b7611fe70bf47d18dd4dd5b087742f07aaee586385d44&rid=giphy.gif&ct=g")
    channel = client.get_guild(member.guild.id).get_channel(get(member.guild.text_channels, position=0).id)
    print(channel)
    print(embed)
    await channel.send(embed=embed)
    """
    if member.bot:
      print('não coisou')
      return
    else:
      print('coisou')
      await channel.send(embed=embed)
    """

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    convert_dict = {'FORÇA': ['str', 'str', 'for', 'força'], 'DESTREZA': ['dex', 'des', 'destreza'],
                    'CARISMA': ['cha', 'carisma', 'car'], 'SABEDORIA': ['wis', 'sab', 'sabedoria'],
                    'PODER': ['hab', 'habilidade', 'poder', 'pod'], 'CONSTITUIÇÃO': ['con', 'constituição'],
                    'INTELIGENCIA': ['inte', 'int', 'inteligencia']}

    if message.content == 'm!xingar <@873979047640711188>':
        await ctx.send('Nao ouse xingar jorginho a lenda, mortal')

    if message.content.startswith('.'):
        await client.process_commands(message)

    elif message.content.lower().startswith('desv'):
        dado = message.content.lower().replace('desv ', '')

        rolarDado = rolagemTag(dado)
        rolarDado1 = rolagemTag(dado)
        primeiro = rolarDado[1]
        segundo = rolarDado1[1]
        primeiroCtx = rolarDado[0]
        segundoCtx = rolarDado1[0]

        if segundo < primeiro:
            primeiroCtx = f'~~{primeiroCtx}~~'
        elif primeiro < segundo:
            segundoCtx = f'~~{segundoCtx}~~'

        await message.reply(primeiroCtx + '\n' + segundoCtx)

    elif message.content.lower().startswith('van'):
        dado = message.content.lower().replace('van ', '')

        rolarDado = rolagemTag(dado)
        rolarDado1 = rolagemTag(dado)
        primeiro = rolarDado[1]
        segundo = rolarDado1[1]
        primeiroCtx = rolarDado[0]
        segundoCtx = rolarDado1[0]

        if segundo > primeiro:
            primeiroCtx = f'~~{primeiroCtx}~~'
        elif primeiro > segundo:
            segundoCtx = f'~~{segundoCtx}~~'

        await message.reply(primeiroCtx + '\n' + segundoCtx)


    elif 'd' in message.content.lower() and len(message.content) <= 32 and any(
            chr.isdigit() for chr in message.content):
        try:
            print('*************** ' + str(message.channel) + ' *****************')
            print('*************** ' + str(message.guild.name) + ' *****************')
            dado = rolagemTag(message.content.lower())[0]
        except ValueError: return
        else:
            if message.author.id == 621664265907994624: add = ''
            else: add = ''

            await message.reply(dado + add, mention_author=True)