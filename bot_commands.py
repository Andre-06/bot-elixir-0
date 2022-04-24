# -------------BIBLIOTECAS---------#
import random
import time

import discord

import atributos
import functions
from functions import *
import data_base
import gsheet
from atributos import *
from data_base import *
import events
import math
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_components import InteractionEventType, Button, ButtonStyle

@client.command(aliases=['r'])
async def roll(ctx, *, dado):
    await ctx.send(rolagemTag(dado))

@client.command()
async def count(ctx, num, *, frase):
    x = 0
    if frase == 'x':
        numM = int(num) + 1
        while x < numM:
            print(x)
            await ctx.send(x)
            x = x + 1
    else:
        numM = int(num) + 1
        while x < numM:
            print(x)
            await ctx.send(frase)
            x = x + 1


@client.command()
async def xingar(ctx, nickA: discord.Member):
    nick = nickA.id
    xingamentos = ['você é um cara de mamão', 'você é um bananao', 'você é um fedido, ve se toma um banho',
                   'você é um intrometido, vai varrer uma calçada', 'voce é um bolsonarista',
                   'ado ado ado comi o cu de quem ta marcado',
                   'invejoso morre cedo']
    print(f'nome do xingado {nickA}')
    qualXingamento = None
    if nick == 873979047640711188:
        await ctx.send('Nao ouse xingar jorginho a lenda, mortal')
    else:
        qualXingamento = random.choice(xingamentos)
        await ctx.send(f'{nickA.mention}, {qualXingamento}')

@client.command()
async def button(ctx):
    embed = discord.Embed(title='Teste', description='none', color=discord.Color.red())
    await ctx.send(embed=embed, components=[Button(style=ButtonStyle.green, label="A green button", custom_id='btn_green'), Button(style=ButtonStyle.blue, label="A blue button", custom_id='btn_blue')])

@client.command(help='Comando Para testes')
async def teste(ctx):
    '''
    await ctx.send(ctx.guild.owner)
    members = ctx.guild.members
    for member in members:
      print(member)
      if member.guild_permissions.administrator:
        print('entro')
        await ctx.send(member)
      else:
        print('nn entro')

    # channel_id = get(ctx.guild.text_channels, position=0)
    # print(ctx.guild.text_channels)
    ticket = await channel.send(
        "_ _",
        components=[
            Button(label="YOUR NAME", style=ButtonStyle.blue, emoji="📬"),
        ]
    )
    await client.wait_for("button_click", check=lambda i: i.component.label.startswith("YOUR NAME"))
    await test.respond(content="hello") '''

@client.command()
async def ficha(ctx, token, link):
    if token.startswith("https"):
        await  ctx.send("Insira o nome do personagem antes do link")
        return

    if not link.startswith('https://docs.google.com/spreadsheets/'):
        await ctx.send("Insira um link válido")
        return

    if data_base.val_personagem_existe(token):
        id_ = data_base.id_name_db(name=token)
        data_base.script_sql(f"""UPDATE personagem SET urlplanilha = '{link}' WHERE idpersonagem = '{id_}' """)
    else:
        data_base.script_sql(f"""INSERT INTO personagem (nome, urlplanilha) VALUES ('{token}', '{link}')""")
    await ctx.send(f"Ficha de {token.title()} adicionada ao bot com sucesso")

@client.command()
async def planilha(ctx):
    await ctx.reply("Opa, aqui está o link da planilha: https://docs.google.com/spreadsheets/d/1VfS-zj3nG_nIyK-O56sRfdn7e7OHeORGVYK6-90TyB4/edit#gid=0\nFaça uma cópia da planilha para poder editá-la indo nos **Menus > Arquivo > Fazer uma Cópia**. E para adicionar a ficha no bot você deve compartilhar a cópia de sua planilha com o email **elixiraccount@bot-elixir.iam.gserviceaccount.com** dando a permissão de Editor e usar o comando `.ficha <personagem> <link>`\n`.help` para mais informações :)")

@client.command()
async def ficha_monstro(ctx, token, link):
    if token.startswith("https"):
        await  ctx.send("Insira o nome do personagem antes do link")
        return

    if not link.startswith('https://docs.google.com/spreadsheets/'):
        await ctx.send("Insira um link válido")
        return

    if data_base.val_personagem_existe(token):
        id_ = data_base.id_name_db(name=token)
        data_base.script_sql(f"""UPDATE personagem SET urlplanilha = '{link}' WHERE idpersonagem = '{id_}' """)
    else:
        data_base.script_sql(f"""INSERT INTO personagem (nome, urlplanilha) VALUES ('monstro {token}', '{link}')""")
    await ctx.send(f"Ficha de {token.title()} adicionada ao bot com sucesso")

@client.command(aliases=['conv'])
async def conversor(ctx, metro: int):
    convM = round(metro/3.281 - 0.5)
    convF = round(metro*3.281 - 0.5)

    await ctx.send(f"{metro} metros == {convF} pés\n{metro} pés == {convM} metros")

@client.command()
async def select(ctx, player: discord.Member, token):
    try: id_ = data_base.id_name_db(name=token)
    except IndexError:
        cursor.execute(f"INSERT INTO personagem(nome, iddiscord) VALUES ('{token}', '{player.id}')")
    else:
        cursor.execute(f"UPDATE personagem SET iddiscord = '{player.id}' WHERE (idpersonagem = '{id_}')")
    await ctx.send(f'Personagem {token} selecionado para {player.mention} ')

@client.command()
async def desselect(ctx, token):
    if token.startswith('<@!'): token = idPersonagem(token.id)[0]
    try: id_ = data_base.id_name_db(name=token)
    except IndexError:
        await ctx.send('Esse personagem não esta adicionado ou ja foi excluido')
    else:
        arroba = data_base.return_fetchall(f"select iddiscord from personagem where idpersonagem = '{id_}'")[0][0]
        cursor.execute(f"UPDATE personagem SET iddiscord = NULL WHERE (idpersonagem = '{id_}')")
        await ctx.send(f'Personagem {token.title()} não esta mais selecionado para <@!{arroba}> com sucecesso')

@client.command()
async def selectAtual(ctx, player):
    if player.startswith('<@!'):
        try:
            id_ = remover(player, ['<', '@', '!', '>', ' '])
            personagem = data_base.return_fetchall(f"select nome from personagem where iddiscord = '{id_}'")[0][0]
        except IndexError:
            await ctx.send('Nenhum personagem selecionado')
        else:
            await ctx.send(f'Personagem "{personagem}" selecionado para <@!{id_}>')
    else:
        try:
            id_ = id_name_db(name=player)
            id_discord = data_base.return_fetchall(f"select iddiscord from personagem where idpersonagem = '{id_}'")[0][0]
        except IndexError:
            await ctx.send('Nenhum personagem selecionado')
        else:
            await ctx.send(f'Personagem "{player.title()}" selecionado para <@!{id_discord}>')

@client.command(aliases=['limpIvt'])
async def limparInventario(ctx, token):
    id_ = data_base.id_name_db(name=token)
    cursor.execute(f"DELETE FROM inventario WHERE (idpersonagem = '{id_}')")
    await ctx.send(f'Inventário de {token} foi limpo com sucesso')


@client.command(aliases=['ivt', 'invent', 'addIvt'])
async def inventario(ctx, token, *, item):
    print(token)
    if data_base.val_personagem_existe(token) != True:
        await ctx.send('Insira um personagem válido')
        return

    if '-' in item:
        kilos = item.split('-')[1]
        item = item.split('-')[0]
        id_ = id_name_db(name=token)
        cursor.execute(
            f"INSERT INTO inventario(item, peso, idpersonagem) VALUES ('{item}', '{kilos}', '{id_}')")
        await ctx.send(f'"{item}" adicionado ao inventario de {token}')
    else:
        await ctx.send('Adicone o peso no final do comando depois de um "-"\nExemplo: 3 cadeiras gamer -5')

@client.command(aliases=['ivtR', 'inventR'])
async def inventarioRemove(ctx, token, *, item):
    if val_personagem_existe(token) != True:
        await ctx.send("Insira um personagem válido")

    itemRemovido = data_base.inventario(token, acharItem=item, idinventario=True)
    print(itemRemovido)
    print(f'leght {len(itemRemovido)}')
    if itemRemovido == []:
        await ctx.send('Esse item não existe na ficha')
    idRemovido = itemRemovido[0][1]
    print(idRemovido)
    data_base.script_sql(f'delete from inventario where idinventario = {idRemovido}')
    await ctx.send(f'{str(itemRemovido[0][0])} foi removido com sucesso')

# -------------NOVA ARMA---------#

@client.command(aliases=['atc', 'attack', 'a'])
async def atack(ctx, *, arma):
    print(f'arma: {arma}')
    armaName = arma
    if '<@!' in arma:
        id_ = int(arma.split('<@!')[1].split('>')[0])
        print(id_)
        token = idPersonagem(id_)
        arma = arma.replace(str(id_), '')
    else:
        token = idPersonagem(ctx.author.id)

    print(f'arma: {arma}')

    if token[1] == 1:
        await ctx.send(token[0])
    else:
        token = token[0]

    try:
        arma = gsheet.arma(token, acharArma=arma, damage=True)
    except AttributeError:
        await ctx.send(f"{token.title()}, não reconheci sua arma")
        return

    armaDano = arma[0]
    armaMod = ''

    sinal = qualSinal(armaDano)

    if sinal == IndexError:
        armaMod = ''
        sinal = ''
    else:
        armaMod = armaDano.split(sinal)[1]

    validaçãoAtributo = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'HAB', 'POD']
    convertAtb = {'STR' : 'FORÇA', 'DEX' : 'DESTREZA', 'INT' : 'INTELIGENCIA', 'CON' : 'CONSTITUIÇÃO', 'WIS' : 'SABEDORIA',
                  'CHA' : 'CARISMA', 'HAB' : 'PODER', 'POD' : 'PODER'}
    print(f'armaMod: {armaMod}')
    print(f'armaDano: {armaDano}')
    for atb in validaçãoAtributo:
        if str(armaMod).upper().replace(' ', '') in atb and armaMod != '':
            modificador = gsheet.atributo_gs(convertAtb[armaMod.upper().replace(' ', '')], token, get_mod=True)
            armaDano = armaDano.replace(armaMod, str(modificador))
    print(armaDano)

    rolarDado = rolagem(ctx, armaDano)

    await ctx.reply(f"{token.title()}: {armaName} = {armaDano}\n{rolarDado[2]}", mention_author=True)

# -------------NOVA ARMA---------#

@client.command(aliases=['addArma', 'novaArma', 'newA'])
async def nova_arma(ctx, token, *, arma):
    id_ = id_name_db(name=token)
    print("ASDKLAJFOAKFNANM FDAOISDFNAIOPHNFAFAPSOJNFA")
    print(id_)
    print("ASDKLAJFOAKFNANM FDAOISDFNAIOPHNFAFAPSOJNFA")
    temDado = False
    temPeso = False
    palavraS = arma.split(' ')
    print(palavraS)
    print(len(palavraS))
    count = 0
    # teste aaa aaa aa 1d20 2
    # 6
    # if len == 6 or == 5
    #
    while len(palavraS) > count:
        palavra = palavraS[count]
        print(f'palavra: {palavra}')
        cNums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if count >= len(palavraS) - 2 and any(chr.isdigit() for chr in palavra) or 'd' in palavra or '-' in palavra:
            try:
                print(palavra.replace('-', '').split('+')[0])
                rolagem(ctx, palavra.replace('-', '').split('+')[0])
            except (ValueError, IndexError):
                print('deu ruim 1')
                try:
                    peso = int(palavra.replace('-', ''))
                except:
                    print('deu ruim 2')
                else:
                    print('deu bom 2')
                    print(peso)
                    del (palavraS[count])
                    count = count - 1
                    temPeso = True
            else:
                print('deu bom 1')
                dado = palavra.replace('-', '').replace(' ', '')
                del (palavraS[count])
                count = count - 1
                print(palavraS)
                print(dado)
                temDado = True
        else:
            print('nem tinha hifen')
        count = count + 1
    if temPeso == False:
        await ctx.send('Adicone o peso no final do comando\nExemplo: espada 1d6 3')
    elif temDado == False:
        await ctx.send('Adicone o dano no final do comando\nExemplo: espada 1d6 5')
    else:
        palavraS = str(palavraS).replace("'", '').replace(',', '').replace('[', '').replace(']', '')
        print(palavraS)
        armaFicha = f'{palavraS} -{dado} -{peso}'
        print(armaFicha)
        data_base.script_sql(f"INSERT INTO armas(idpersonagem, item, peso, dano) VALUES ('{int(id_)}', '{palavraS}', '{peso}', '{dado}')")
        await ctx.send(f'Nova arma adicionada! {armaFicha}')


@client.command(aliases=['remArma'])
async def armaRemove(ctx, token, arma):
    if data_base.val_personagem_existe(token) != True:
        await ctx.send('Insira um personagem válido')

    armaRem = data_base.arma(token, arma, idarma=True)

    if armaRem == []:
        await ctx.send('Essa arma nao existe ou ja foi excluida')
        return

    try:
        data_base.script_sql(f"DELETE FROM armas WHERE idarmas = {int(armaRem[0][1])} ")
    except FileNotFoundError:
        await  ctx.send("Ocorreu um erro")
        return
    else:
        await ctx.send(f'"{str(armaRem[0][0])}" excluido com sucesso!')


# -------------CRIANDO NOVO ATRIBUTO---------#

@client.command(aliases=['compF'])
async def fichaCompleta(ctx, *, fichaInteira):
    await fichaCompletaCodigo(ctx, fichaInteira)

@client.command()
async def icon_user(ctx, user: discord.Member):
    await ctx.send(user.avatar_url)

# -------------EDITAR ATRIBUTOS---------#

# -------------COMANDO PARA ROLAGEM DE CADA ATRIBUTO---------#

@client.command()
async def editarFicha(ctx, token, color, imagem):
    id_ = data_base.id_name_db(name=token)
    cor = corConvert(color)
    if type(cor) == str:
        await ctx.send(cor)
    else:
        data_base.script_sql(f"""UPDATE personagem (embedCor, embedIcon) SET ('{color}', '{imagem}') 
                             WHERE (idpersonagem = '{id_}') """)
        await ctx.send(f'Cor alterada para {cor}({color}) e imagem alterada para {imagem}')

@client.command(aliases=['verF', 'verFicha'])
async def ver_ficha(ctx, *, token):
    try:
        id_ = id_name_db(name=token)
        url = data_base.get_link(token)
    except IndexError:
        await ctx.send('Essa ficha ainda não foi adicinado ao bot. Para adicioná-la utilize o comando `.ficha <nome do personagem> <link da palilha>` e compartilhe a planilha com este email elixiraccount@bot-elixir.iam.gserviceaccount.com')
        return
    except mysql.connector.errors.InterfaceError:
        await ctx.send('A conexão com o PC Batata do Maugrin foi perdida')
        return

    cor = return_fetchall(f'select p.embedCor from personagem as p where idpersonagem = {id_}')[0][0]
    icon = return_fetchall(f'select p.embedIcon from personagem as p where idpersonagem = {id_}')[0][0]

    if icon == 'ctx.guild.icon_url': icon = ctx.guild.icon_url
    cell_confirm = {'row' : 1, 'col' : 1}
    cell_hp = {'row' : 5, 'col' : 4}
    cell_loc = {'row' : 3, 'col' : 18}
    cell_carga = {'row' : 7, 'col' : 20}
    cell_mana = {'row' : 4, 'col' : 18}

    await ctx.send("Conectando...")
    try:
        confirm = gsheet.reader(url, cell=cell_confirm)
    except ValueError:
        await ctx.send('Não foi possivel se conectar a este tipo de planilha')
        return
    except TypeError:
        await  ctx.send("Essa ficha não foi adicinada ao bot")
        return
    except:
        await  ctx.send("Ocorreu um erro")
        return
    else:
        print(f'VerF {token}: Conectando...')
    if confirm == 'FICHA MONSTRO':
        await ctx.send('A ficha selecionada não esta disponível atraves desse comando')
        return
    hp = gsheet.reader(url, cell=cell_hp)
    locomoção = gsheet.reader(url, cell=cell_loc)
    carga = gsheet.reader(url, cell=cell_carga).replace(' ', '').replace('no', '').replace('si', '')
    mana = gsheet.reader(url, cell=cell_mana)

    if mana != None:
        fichaMana = f'\nMana: {mana}'
    else:
        fichaMana = ''

    title = f'Ficha de {token.title()}\nHP: {hp}{fichaMana}\nMovimento: {locomoção}\n'

    embedFicha = discord.Embed(
        title=title,
        description='',
        color=int(cor)
    )

    iconServer = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=iconServer)
    embedFicha.set_thumbnail(url=icon)

    atb_col1 = gsheet.reader(url, col=3)
    atb_col2 = gsheet.reader(url, col=13)

    per_name_col1 = gsheet.reader(url, col=4)
    per_val_col1 = gsheet.reader(url, col=6)

    per_name_col2 = gsheet.reader(url, col=11)
    per_val_col2 = gsheet.reader(url, col=10)

    print(f'======== atb_col1 ======== leng: {len(atb_col1)}')
    print(atb_col1)
    print(f'======== atb_col2 ======== leng: {len(atb_col2)}')
    print(atb_col2)
    print(f'======== per_name_col1 ======== leng: {len(per_name_col1)}')
    print(per_name_col1)
    print(f'======== per_val_col1 ======== leng: {len(per_val_col1)}')
    print(per_val_col1)
    print(f'======== per_name_col2 ======== leng: {len(per_name_col2)}')
    print(per_name_col2)
    print(f'======== per_val_col2 ======== leng: {len(per_val_col2)}')
    print(per_val_col2)

    cAtributos = ['STR', 'DEX', 'INT', 'WIS', 'CHA', 'CON', 'POD']
    convertAtb = {'STR' : 'FORÇA', 'DEX' : 'DESTREZA', 'CON' : 'CONSTITUIÇÃO', 'INT' : 'INTELIGENCIA',
                  'WIS' : 'SABEDORIA', 'CHA' : 'CARISMA', 'POD' : 'PODER'}
    convertEmoji = {'STR' : ':punch:', 'DEX' : ':bow_and_arrow:', 'CON' : ':shield:', 'INT' : ':brain:',
                  'WIS' : ':scales:', 'CHA' : ':zany_face:', 'POD' : ':medal:'}

    await ctx.send("Analisando Dados...")

    for atb in cAtributos:
        try:
            value_atb = atb_col1[atb_col1.index(convertAtb[atb])-3]
            mod_atb = atb_col1[atb_col1.index(convertAtb[atb])-4]
        except ValueError:
            value_atb = atb_col2[atb_col2.index(convertAtb[atb]) - 3]
            mod_atb = atb_col2[atb_col2.index(convertAtb[atb]) - 4]

        name = f"{convertEmoji[atb]} {atb} {value_atb}{mod_atb}"
        print(f'name: {name}')

        per_atb = {'Primeiros Socorros': 'INTELIGENCIA',
                   'Medicina': 'INTELIGENCIA', 'Psicologia': 'INTELIGENCIA', 'Arcanismo': 'INTELIGENCIA',
                   'Estudos': 'INTELIGENCIA', 'Crafting': 'INTELIGENCIA', 'Arremesso': 'DESTREZA',
                   'Acrobacia': 'DESTREZA',
                   'Furtividade': 'DESTREZA', 'Mãos Leves': 'DESTREZA', 'Pilotar': 'DESTREZA',
                   'Lutar': 'FORÇA', 'Atletismo': 'FORÇA', 'Lábia': 'CARISMA', 'Domesticar': 'CARISMA',
                   'Convencer': 'CARISMA',
                   'Percepção': 'SABEDORIA', 'Artes': 'SABEDORIA', 'Natureza': 'SABEDORIA',
                   'Uso de Armas' : ['DESTREZA', 'FORÇA']
                   }

        skills = []

        for s in per_atb:
            if convertAtb[atb] in per_atb[s]: skills.append(s)
        else:
            print(f'atb: {convertAtb[atb]}\nskills: {skills}')

        value_dict = dict()
        count = 1
        for name_skl in skills:

            try: value_skl = per_val_col1[per_name_col1.index(name_skl)]
            except ValueError: value_skl = per_val_col2[per_name_col2.index(name_skl)]

            mod_skl = round((int(value_skl)-10)/2)
            if mod_skl >= 0: mod_skl = '+' + str(mod_skl)

            value_dict[str(count)] = f'{name_skl}: {value_skl} ({mod_skl}) | '
            count = count + 1

        value = ''
        count = 1
        while count < len(value_dict):
            value = value + f'{value_dict[str(count)]}{value_dict[str(count + 1)]}{value_dict[str(count + 2)]}\n'
            count = count + 3

        if value == '': value = '---'

        embedFicha.add_field(name=name, value=value,
                             inline=False)

    await ctx.send("Criando embed...")

    itens = gsheet.reader(url, col=17)[8:28]
    damage = gsheet.reader(url, col=18)[8:28]
    weight = gsheet.reader(url, col=19)[8:28]

    while len(itens) > len(damage): damage.append('')
    while len(itens) > len(weight): weight.append('')

    print(f'======== itens ========')
    print(itens)
    print(f'======== damage ========')
    print(damage)
    print(f'======== weight ========')
    print(weight)

    inventario = []
    armas = []
    buttons = []

    count = 0

    for i in itens:
        if i.replace(' ', '') == '': break

        index = itens.index(i)

        if damage[index].replace(' ', '') == '' and weight[index].replace(' ', '') != '':
            inventario.append(f"{i.title()} | {weight[index]}kg")
        elif damage[index].replace(' ', '') != '' and weight[index].replace(' ', '') != '':
            armas.append(f"{i.title()} | {weight[index]}kg | {damage[index]}")
            buttons.append(Button(style=ButtonStyle.red, emoji='⚔️', label=i.title(),
                                  custom_id=f'pla.btn_atc.{token}.{damage[index]}.{count}'))
        else:
            inventario.append(f"{i.title()}")

        count = count + 1
    else:
        if inventario == []: inventario.append("Nenhum item no inventário")
        if armas == []: armas.append("Nenhuma arma no inventário")

    embedFicha.add_field(name=f':school_satchel: Inventario ({carga})', value='\n'.join(inventario), inline=False)
    embedFicha.add_field(name=f':dagger: Armas', value='\n'.join(armas), inline=False)

    buttons_1 = [
        Button(style=ButtonStyle.blue, emoji='🛡️', label="Bloquear", custom_id=f'pla.btn_block.{token}'),
        Button(style=ButtonStyle.blue, emoji='🤺', label="Esquiva", custom_id=f'pla.btn_esquiv.{token}'),
    ]

    await ctx.send(embed=embedFicha, components=[buttons_1])
    count = 0
    count_2 = 1
    while count < len(buttons):
        await ctx.send(content=f'**ATAQUES {count_2}**', components=[buttons[count:count+5]])
        count = count + 5
        count_2 = count_2 + 1

@client.command(aliases=['mon'])
async def monstro(ctx, *, token):
    try: url = data_base.get_link(f'monstro {token}')
    except IndexError:
        await ctx.send('A ficha desse inimigo ainda não foi adicinado ao bot. Para adicioná-la utilize o comando `.ficha monstro <numero do monstro> <link da palilha>` e compartilhe a planilha com este email elixiraccount@bot-elixir.iam.gserviceaccount.com')
        return

    await  ctx.send('Conectando...')
    cell_confirm = {'row' : 1, 'col' : 1}
    cell_hp = {'row' : 2, 'col' : 10}
    cell_mana = {'row' : 3, 'col' : 10}
    if gsheet.reader(url, cell=cell_confirm) != 'FICHA MONSTRO':
        await ctx.send('Não foi possível abrir este tipo de ficha')
        return

    hp = gsheet.reader(url, cell=cell_hp)
    mana = gsheet.reader(url, cell=cell_mana)

    if mana != None:
        fichaMana = f'\nMana: {mana}'
    else:
        fichaMana = ''

    title = f'Ficha de {token.title()}\nHP: {hp}{fichaMana}\n'

    embedFicha = discord.Embed(
        title=title,
        description='',
        color=discord.Color.green()
    )

    iconServer = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=iconServer)
    embedFicha.set_thumbnail(url=iconServer)

    atb_col1 = gsheet.reader(url, col=3)
    atb_col2 = gsheet.reader(url, col=11)

    per_name_col1 = gsheet.reader(url, col=4)
    per_val_col1 = gsheet.reader(url, col=6)

    per_name_col2 = gsheet.reader(url, col=9)
    per_val_col2 = gsheet.reader(url, col=8)

    print(f'======== atb_col1 ======== leng: {len(atb_col1)}')
    print(atb_col1)
    print(f'======== atb_col2 ======== leng: {len(atb_col2)}')
    print(atb_col2)
    print(f'======== per_name_col1 ======== leng: {len(per_name_col1)}')
    print(per_name_col1)
    print(f'======== per_val_col1 ======== leng: {len(per_val_col1)}')
    print(per_val_col1)
    print(f'======== per_name_col2 ======== leng: {len(per_name_col2)}')
    print(per_name_col2)
    print(f'======== per_val_col2 ======== leng: {len(per_val_col2)}')
    print(per_val_col2)

    cAtributos = ['STR', 'DEX', 'INT', 'WIS', 'CHA', 'CON', 'POD']
    convertAtb = {'STR': 'FORÇA', 'DEX': 'DESTREZA', 'CON': 'CONSTITUIÇÃO', 'INT': 'INTELIGENCIA',
                  'WIS': 'SABEDORIA', 'CHA': 'CARISMA', 'POD': 'PODER'}
    convertEmoji = {'STR': ':punch:', 'DEX': ':bow_and_arrow:', 'CON': ':shield:', 'INT': ':brain:',
                    'WIS': ':scales:', 'CHA': ':zany_face:', 'POD': ':medal:'}

    await ctx.send("Analisando Dados...")

    for atb in cAtributos:
        try:
            value_atb = atb_col1[atb_col1.index(convertAtb[atb]) - 3]
            mod_atb = atb_col1[atb_col1.index(convertAtb[atb]) - 4]
        except ValueError:
            value_atb = atb_col2[atb_col2.index(convertAtb[atb]) - 3]
            mod_atb = atb_col2[atb_col2.index(convertAtb[atb]) - 4]

        name = f"{convertEmoji[atb]} {atb} {value_atb}{mod_atb}"
        print(f'name: {name}')

        per_atb = {'Primeiros Socorros': 'INTELIGENCIA',
                   'Medicina': 'INTELIGENCIA', 'Psicologia': 'INTELIGENCIA', 'Arcanismo': 'INTELIGENCIA',
                   'Estudos': 'INTELIGENCIA', 'Crafting': 'INTELIGENCIA', 'Arremesso': 'DESTREZA',
                   'Acrobacia': 'DESTREZA',
                   'Furtividade': 'DESTREZA', 'Mãos Leves': 'DESTREZA', 'Pilotar': 'DESTREZA',
                   'Lutar': 'FORÇA', 'Atletismo': 'FORÇA', 'Lábia': 'CARISMA', 'Domesticar': 'CARISMA',
                   'Convencer': 'CARISMA',
                   'Percepção': 'SABEDORIA', 'Artes': 'SABEDORIA', 'Natureza': 'SABEDORIA',
                   'Uso de Armas': ['DESTREZA', 'FORÇA']
                   }

        skills = []

        for s in per_atb:
            if convertAtb[atb] in per_atb[s]: skills.append(s)
        else:
            print(f'atb: {convertAtb[atb]}\nskills: {skills}')

        value_dict = dict()
        count = 1
        for name_skl in skills:

            try:
                value_skl = per_val_col1[per_name_col1.index(name_skl)]
            except ValueError:
                value_skl = per_val_col2[per_name_col2.index(name_skl)]

            mod_skl = round((int(value_skl) - 10) / 2)
            if mod_skl >= 0: mod_skl = '+' + str(mod_skl)

            value_dict[str(count)] = f'{name_skl}: {value_skl} ({mod_skl}) | '
            count = count + 1

        value = ''
        count = 1
        while count < len(value_dict):
            value = value + f'{value_dict[str(count)]}{value_dict[str(count + 1)]}{value_dict[str(count + 2)]}\n'
            count = count + 3

        if value == '': value = '---'

        embedFicha.add_field(name=name, value=value,
                             inline=False)

    await ctx.send("Criando embed...")

    itens = gsheet.reader(url, col=15)[6:26]
    damage = gsheet.reader(url, col=16)[6:26]
    manna = gsheet.reader(url, col=17)[6:26]

    while len(itens) > len(damage): damage.append('')
    while len(itens) > len(manna): manna.append('')

    print(f'======== itens ========')
    print(itens)
    print(f'======== damage ========')
    print(damage)
    print(f'======== weight ========')
    print(manna)

    attacks = list()

    buttons_1 = [
        Button(style=ButtonStyle.blue, label="Bloquear", custom_id=f'mon.btn_block.{token}'),
        Button(style=ButtonStyle.blue, label="Esquiva", custom_id=f'mon.btn_esquiv.{token}'),
    ]

    buttons = []
    count = 0
    for i in itens:
        if i.replace(' ', '') == '': break

        index = itens.index(i)

        if manna[index].replace(' ', '') != '':
            attacks.append(i.title() + ' | ' + damage[index])
            buttons.append(Button(style=ButtonStyle.red, label=i.title(),
                                  custom_id=f'mon.btn_atc.{token}.{damage[index]}.{count}'))
        else:
            attacks.append(i.title() + ' | ' + damage[index])
            buttons.append(Button(style=ButtonStyle.red, label=i.title(),
                                  custom_id=f'mon.btn_atc.{token}.{damage[index]}.{count}'))
        count = count + 1

    embedFicha.add_field(name=f':dagger: Ataques', value='\n'.join(attacks), inline=False)
    await ctx.send(embed=embedFicha, components=[buttons_1])
    count = 0
    count_2 = 1
    while count < len(buttons):
        await ctx.send(content=f'**ATAQUES {count_2}**', components=[buttons[count:count+5]])
        count = count + 5
        count_2 = count_2 + 1

@client.command(aliases=['iconServer'])
async def icon_server(ctx):
    await ctx.send(ctx.guild.icon_url)

# .ini call, inimigo 1, inimigo 2, bruxas-3
@client.command(aliases=['ini'])
async def iniciativa(ctx, *, iniciativa):
    # cria uma lista com o que passram na iniciativa e seta as variaveis
    jogador = iniciativa.split(',')
    ordem = []
    ordemToNext = list()
    print(f'jogador: {jogador}')

    # verifica se estao pedindo uma iniciativa com a galera da call
    if 'call' in iniciativa:
        # deleta call da lista e acha a call em que a pessoa esta conectada
        del (jogador[item_lista(jogador, 'call')])
        idCanal = ctx.author.voice.channel.id
        print(idCanal)
        canal = client.get_guild(ctx.guild.id).get_channel(idCanal)
        print(canal.members[3].nick)
        for member in canal.members:
            # ignora se o nick da pessoa nn estiver jogando
            validaçãoEspec = ['MESTRE', 'ESPECTADOR', 'ESPECTANDO', 'OUVINTE', 'OUVINDO']
            if member.nick == None or '|' not in member.nick or 'MESTRE' in member.nick.upper() or 'ESPECTANDO' in member.nick.upper() or 'ESPECTADOR' in member.nick.upper() or 'OUVINTE' in member.nick.upper() or 'OUVINDO' in member.nick.upper():
                a = ''
            else:
                jogador.append(acharNoNick(member.nick, 'nome').replace(' |', '').replace('|', ''))


    # verifica se tem mais de um elemebnto e coloca a quantiade que tiver
    if '-' in iniciativa:
        count = 0
        while count < len(jogador):
            print('AAAAAAAAAAAAAAAAAAA' + jogador[count])
            if '-' in jogador[count]:
                inmigos = jogador[count]
                quantidade = int(jogador[count].split('-')[1])
                print(quantidade)
                countinho = 0
                del (jogador[count])
                while countinho < quantidade:
                    jogador.append(f'{inmigos.split("-")[0]} {countinho + 1}')
                    countinho = countinho + 1
            else:
                count = count + 1

    # remove os espaços que tem no inicio e final e também remove os caracteres especiais
    for i in range(0, len(jogador)):
        player = jogador[0]
        print(f"player: {player}")
        p = player
        player = functions.remover(player, ['all'])
        del(jogador[jogador.index(p)])
        jogador.append(player)
        print(f"jogador: {jogador}")
    # definia a ordem de iniciativa aleatoriamente sem deixar que se repita
    print(f'jogador: {jogador}')
    ini = dict()

    for i in range(0, len(jogador)):
        i = jogador[0]
        print(f'i: {i}')
        try:
            dex = await atributos.dex(ctx, token=i.title().replace(' ', ''))
            print(f"dex: {dex.content.split('|')[1].split('⟵')[0].replace('`', '')}")
            ini[i] = int(dex.content.split('|')[1].split('⟵')[0].replace('`', ''))
        except IndexError:
            await dex.delete()
            dex = await ctx.reply(i.title() + ':\n' + functions.rolagemTag('1d20')[0], mention_author=False)
            print(f"dex: {dex.content.split(i.title() + ':')[1].split('⟵')[0].replace('`', '')}")
            ini[i] = int(dex.content.split(':\n')[1].split('⟵')[0].replace('`', ''))

        del(jogador[jogador.index(i)])
        jogador.append("passou")
        print(f'jogador: {jogador}')

    print(f'jogador: {jogador}')
    print(f'ini: {ini}')
    ordem_list = list()
    maior = 0
    count = 0
    for i in range(0, len(ini)):
        for i in ini:
            print(f"i: {i}")
            if ini[i] > maior and 'passou' not in i:
                maior = ini[i]
                name = i
                print(f'name: {name}')

        ordem.append(f'{name.title()} ({ini[name]}), ')
        ordemToNext.append(f'{name.title()} \n')
        print(f'ordem_list: {ordem}')

        ini['passou' + str(count)] = 0
        del ini[name]
        print(f"ini: {ini}")

        maior = 0
        count += 1

    # muda o ultimo item para '.' ao inves de ','
    ordem[len(ordem) - 1] = ordem[len(ordem) - 1].replace(',', '.')

    # coloca, em negritro, a ordem de iniciativa no docs
    ordinha = ''.join(ordem)
    arq = open('iniciativa temp.txt', 'a')
    arq.truncate(0)
    celula = ordemToNext[0]
    caracter = len(celula) - 2
    ordemToNext[0] = f'**{celula[:caracter]}** \n'
    arq.writelines(ordemToNext)

    # envia a ordem de iniciativa
    await ctx.reply(f'Ordem de iniciativa: {str(ordinha)}', mention_author=True)

@client.command(aliases=['v'])
async def view(ctx):
    arq = open('iniciativa temp.txt').readlines()
    msg = 'Ordem de iniciativa:  ' + ', '.join(arq).replace('\n', '') + '.'
    await ctx.send(msg)

@client.command(aliases=['addIni'])
async def addIniciativa(ctx, *, player):
    player = player.title()
    arq = open('iniciativa temp.txt', 'a')
    arq2 = open('iniciativa temp.txt')
    lista = arq2.readlines()

    if 'aleatorio:sim' in player.lower().replace(" ", ''):
        player = player.lower().replace('aleatorio:sim', '').title()
        count = random.randint(0, len(lista))
        lista.insert(count, player + ' \n')
        arq.truncate(0)
        arq.writelines(lista)
    else:
        arq.writelines(player + ' \n')
    await ctx.send('**' + player + '**' + ' adicionado a iniciativa')

@client.command(aliases=['remIni'])
async def remIniciativa(ctx, *, playerRemove):
    arq = open('iniciativa temp.txt', 'r')
    iniciativa = arq.readlines()
    count = 0
    while count < len(iniciativa):
        print(iniciativa[count].upper())
        print(playerRemove.upper())
        if playerRemove.lower().replace(' ', '') in iniciativa[count].lower().replace(' ', ''):
            if '**' in iniciativa[count]:
                print('tava com **')
                await Next(ctx)
                iniciativa = open('iniciativa temp.txt', 'r').readlines()
                removido = iniciativa[count].replace('\n', '')
                del(iniciativa[count])
                break
            else:
                removido = '**' + iniciativa[count].replace('\n', '') + '**'
                del(iniciativa[count])
                break
        else:
            count = count + 1
            print('num achei nn')
    arq2 = open('iniciativa temp.txt', 'w')
    arq2.truncate(0)
    arq2.writelines(iniciativa)
    await ctx.send(f"{removido} foi removido")


@client.command()
async def paror(ctx):
    await ctx.send('parorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr meoooooooooooooooooooooooooooo')


@client.command()
async def eéaqui(ctx):
    await ctx.send(
        'E é aqui.........................................................................................................................................................................')


@client.command(aliases=['dltF'])
async def deleteFicha(ctx, token):
    deuRuim = 0
    try:
        os.remove(f"ficha {token}.txt")
    except FileNotFoundError:
        await ctx.send(
            f'{token} ja foi para o Pós-Vida ou nunca nem saiu de lá. Por favor selecione um personagem que esteja entre os mortais')
    else:
        try:
            os.remove(f"embedFicha {token}.txt")
        except FileNotFoundError:
            deuRuim = deuRuim + 1
        try:
            os.remove(f"ficha arma {token}.txt")
        except FileNotFoundError:
            deuRuim = deuRuim + 1
        try:
            os.remove(f"inventario {token}.txt")
        except FileNotFoundError:
            deuRuim = deuRuim + 1
        await ctx.send(f'Adeus {token}, que sua jornada ao além seja gloriosa\nPress F for respect')

@client.command()
async def hm(ctx):
    await ctx.send(
        'HUMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')


@client.command()
async def analise(ctx):
    await ctx.send('Ué, Analisekkkkkk')


@client.command()
async def Next(ctx):
    arq = open('iniciativa temp.txt', 'r')
    lerArq = arq.readlines()
    print(lerArq)

    count = 0
    while count < len(lerArq):
        if f"**" in lerArq[count]:
            print(f'entramnos {lerArq[count]}')
            vezAtual = count
            count = count + len(lerArq) + 1
        else:
            print(lerArq[count])
            count = count + 1
            vezAtual = 0

    vezProx = vezAtual + 1
    print(vezAtual)
    lerArq[vezAtual] = lerArq[vezAtual].replace('*', '')
    print(vezProx)
    if vezAtual >= len(lerArq) - 1:
        vezAtual = 0
        vezProx = 0

    celula = lerArq[vezProx]
    caracter = len(celula) - 2
    lerArq[vezProx] = f'**{celula[:caracter]}** \n'
    print(lerArq)
    arq = open('iniciativa temp.txt', 'a')
    count = 0
    ordemToNext = list()
    ordemToNext.append(lerArq)
    arq.truncate(0)
    arq.writelines(lerArq)
    ordem = ''.join(lerArq)
    while count < len(lerArq):
        celula = lerArq[count]
        caracter = len(celula) - 2
        lerArq[count] = f'{celula[:caracter]}, '
        count = count + 1
    print(lerArq)
    lerArq[len(lerArq) - 1] = lerArq[len(lerArq) - 1].replace(',', '.')
    await ctx.reply(
        f"Ordem de Iniciativa: {''.join(lerArq)} \nVez Passada: {''.join(lerArq[vezAtual]).replace(',', '').replace('*', '')}\nVez Atual: {''.join(lerArq[vezProx]).replace(',', '')}",
        mention_author=True)


@client.command(pass_context=True)
async def end(ctx):
    arq = open('iniciativa temp.txt', 'a')
    arq.truncate(0)
    await ctx.send("Combate encerrado")


@client.command(pass_context=True, aliases=['d'])
async def dano(ctx, dado, member: discord.Member):
    print(member)
    rolarDado = rolagem(ctx, dado)
    danoDado = rolarDado[1]
    nickAtual = member.nick

    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpSubtraido = int(hpAtual) - int(danoDado)
    hpFinal = f" {hpSubtraido}/{hpTotal}|"
    flechas = acharNoNick(nickAtual, 'flechas')
    mana = acharNoNick(nickAtual, 'mana')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    print(nickFinal)

    if hpSubtraido < -6:
        await ctx.reply(
            f"**Dano:** {rolarDado[2]} \n **HP:** {hpAtual} - {danoDado} = **{hpSubtraido}**\n*Press F to pay respect*")
    else:
        await ctx.reply(f"**Dano:** {rolarDado[2]} \n **HP:** {hpAtual} - {danoDado} = **{hpSubtraido}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        if member.id != ctx.guild.owner.id and member.bot != True:
            await member.edit(mute=True)
            await ctx.send(f'{member.nick} calou a boquinha com sucesso')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['desmute'])
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        await member.edit(mute=False)
        await ctx.send(f'{member.nick} voltou a falar merda com sucesso')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True)
async def muteAll(ctx):
    print(ctx.guild.voice_channels)
    canal = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    print(canal.members)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        for member in canal.members:
            if member.id != ctx.guild.owner.id and member.bot != True:
                await member.edit(mute=True)
        else:
            await ctx.send('Todo mundo ficou com a boquinha calada')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['desmuteall'])
async def unmuteAll(ctx):
    canal = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        for member in canal.members:
            await member.edit(mute=False)
        else:
            await ctx.send('Todo mundo voltou a falar merda')
    else:
        await ctx.send('Quem você pensa que é?')


"""
  count = 0
  while count < len(canal.members):
    if salvos in member:
      count = count + 1
    else:
      await member.edit(mute=True)
      count = count + 1
"""


@client.command(pass_context=True, aliases=['c'])
async def cura(ctx, dado, member: discord.Member):
    rolarDado = rolagem(ctx, dado)
    danoDado = rolarDado[1]
    nickAtual = member.nick
    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpAdicionado = int(hpAtual) + int(danoDado)
    hpFinal = f" {hpAdicionado}/{hpTotal}|"
    mana = acharNoNick(nickAtual, 'mana')
    flechas = acharNoNick(nickAtual, 'flechas')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    print(nickFinal)

    if int(hpAdicionado) >= int(hpTotal):
        hpFinal = f" {hpTotal}/{hpTotal}|"
        nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
        print(nickFinal)
        await ctx.reply(f"**Cura:** {rolarDado[2]} \n **HP:** {hpAtual} + {danoDado} = **{hpAdicionado}**")
    else:
        await ctx.reply(f"**Cura:** {rolarDado[2]} \n **HP:** {hpAtual} + {danoDado} = **{hpAdicionado}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True)
async def hp(ctx, dano, member: discord.Member = None):

    if member == None: member = ctx.author
    nickAtual = member.nick

    if 'd' in dano:
        if dano.startswith('-'):
            dano = dano[1:]
            print(dano)
            sinal = '-'
            rolarDado = rolagemTag(dano)
            danoDado = rolarDado[1] * -1
        else:
            sinal = '+'
            rolarDado = rolagemTag(dano[1:])
            danoDado = rolarDado[1]
        ctxReturn = rolarDado[0]
    else:
        danoDado = eval(dano)
        sinal = qualSinal(str(danoDado))
        if sinal == IndexError: sinal = '+'
        ctxReturn = str(danoDado).replace(sinal, '')

    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) |f flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpSubtraido = int(hpAtual) + int(danoDado)
    if hpSubtraido > int(hpTotal): hpSubtraido = int(hpTotal)
    hpFinal = f" {hpSubtraido}/{hpTotal}|"
    flechas = acharNoNick(nickAtual, 'flechas')
    mana = acharNoNick(nickAtual, 'mana')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    if hpSubtraido <= 0:
        await ctx.reply(f"**HP:** {hpAtual} {sinal} {ctxReturn} = **{hpSubtraido}**\n*Press F to pay respect*")
    else:
        await ctx.reply(f"**HP:** {hpAtual} {sinal} {ctxReturn} = **{hpSubtraido}**")

    await member.edit(nick=nickFinal)

@client.command(pass_context=True, aliases=['ml'])
async def magiaLeve(ctx, nick: discord.Member = None):
    print(nick)
    rolarDado = rolagem(ctx, '2d10')
    manaGasta = rolarDado[1]
    c1d6 = [1, 2, 3, 4, 5]
    c1d8 = [6, 7, 8, 9, 10]
    c1d10 = [11, 12, 13, 14, 15]
    c2d8 = [16, 17, 18, 19, 20]
    if manaGasta in c1d6:
        dadoMagia = '1d6'
        estagio = '1/4'
    if manaGasta in c1d8:
        dadoMagia = '1d8'
        estagio = '2/4'
    if manaGasta in c1d10:
        dadoMagia = '1d10'
        estagio = '3/4'
    if manaGasta in c2d8:
        dadoMagia = '2d8'
        estagio = '**4/4**'

    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        print('entrei')
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f"{int(manaAtual) - int(manaGasta)}/{manaTotal}|"
    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} = **{int(manaAtual) - int(manaGasta)}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['mm'])
async def magiaModerada(ctx, nick: discord.Member = None):
    print(nick)
    rolarDado = rolagem(ctx, '2d30')
    manaGasta = rolarDado[1]

    c1d8 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    c1d10 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    c2d8 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    c2d10 = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    c2d12 = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    c4d8 = [51, 52, 53, 54, 55, 56]
    c2d20 = [57, 58, 59, 60]
    if manaGasta in c1d8:
        dadoMagia = '1d8'
        estagio = '1/7'
    elif manaGasta in c1d10:
        dadoMagia = '1d10'
        estagio = '2/7'
    elif manaGasta in c2d8:
        dadoMagia = '2d8'
        estagio = '3/7'
    elif manaGasta in c2d10:
        dadoMagia = '2d10'
        estagio = '4/7'
    elif manaGasta in c2d12:
        dadoMagia = '2d12'
        estagio = '5/7'
    elif manaGasta in c4d8:
        dadoMagia = '4d8'
        estagio = '6/7'
    elif manaGasta in c2d20:
        dadoMagia = '2d20'
        estagio = '**7/7**'
    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f"{int(manaAtual) - int(manaGasta)}/{manaTotal}|"

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} = **{int(manaAtual) - int(manaGasta)}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['me'])
async def magiaExtrema(ctx, nick: discord.Member = None):
    rolarDado = rolagem(ctx, '2d50')
    manaGasta = rolarDado[1]

    c2d8menos15 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    c2d12menos10 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    c2d16menos10 = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    c2d20menos5 = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    c2d20mais5 = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    c2d20mais7 = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
    c2d20mais10 = [81, 82, 83, 84, 85, 86, 87, 88, 89]
    c1d50menos15 = [90, 91, 92, 93, 94, 95]
    c1d100menos25 = [96, 97, 98, 99, 100]

    if manaGasta in c2d8menos15:
        dadoMagia = '2d8'
        manaExtrema = 15
        estagio = '1/9'
    elif manaGasta in c2d12menos10:
        dadoMagia = '2d12'
        manaExtrema = 10
        estagio = '2/9'
    elif manaGasta in c2d16menos10:
        dadoMagia = '2d16'
        manaExtrema = 10
        estagio = '3/9'
    elif manaGasta in c2d20menos5:
        dadoMagia = '2d20'
        manaExtrema = 5
        estagio = '4/9'
    elif manaGasta in c2d20mais5:
        dadoMagia = '2d20+5'
        manaExtrema = 0
        estagio = '5/9'
    elif manaGasta in c2d20mais7:
        dadoMagia = '2d20+7'
        manaExtrema = 0
        estagio = '6/9'
    elif manaGasta in c2d20mais10:
        dadoMagia = '2d20+10'
        manaExtrema = 0
        estagio = '7/9'
    elif manaGasta in c1d50menos15:
        dadoMagia = '5d10'
        manaExtrema = 15
        estagio = '8/9'
    elif manaGasta in c1d100menos25:
        dadoMagia = '5d20'
        manaExtrema = 25
        estagio = '**9/9**'

    if manaExtrema == 0:
        streManaExtrema = ''
    else:
        streManaExtrema = f'**- {manaExtrema}**'

    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f" {int(manaAtual) - int(manaGasta) - manaExtrema}/{manaTotal}|"

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} {streManaExtrema} = **{int(manaAtual) - int(manaGasta) - manaExtrema}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)

@client.command(aliases=['f'])
async def flecha(ctx, quantidade):
    nickAtual = ctx.message.author.nick

    flechaAtual = acharNoNick(nickAtual, 'flechasAtual')
    flechasTotal = acharNoNick(nickAtual, 'flechasTotal')
    nome = acharNoNick(nickAtual, 'nome')
    hp = acharNoNick(nickAtual, 'hp')
    mana = acharNoNick(nickAtual, 'mana')

    flechaOperada = int(flechaAtual) + int(quantidade)
    print(f'flecha operdaa: {flechaOperada}')
    if flechaOperada > int(flechasTotal.replace('f', '')) and int(flechaAtual) >= int(
            flechasTotal.replace('f', '')) and quantidade.count('+') == 1:
        flechaOperada = flechasTotal.replace('f', '')
        await ctx.reply('Sua aljava ja esta cheia')
    elif flechaOperada < 0 and int(flechaAtual) <= 0 and quantidade.count('-') == 1:
        await ctx.reply('Ops, acabaram-se as flechas, taca o arco mesmo')
    else:
        if flechaOperada < 0:
            flechaOperada = 0
        elif flechaOperada > int(flechasTotal.replace('f', '')):
            flechaOperada = int(flechasTotal.replace('f', ''))

        flechaFinal = f' {flechaOperada}/{flechasTotal}'
        nickFinal = f"{nome}{hp}{mana}{flechaFinal}"
        print(nickFinal)
        await ctx.reply(f'{quantidade} flecha na sua aljava\n{flechaAtual}{quantidade} = {flechaOperada}')
        await member.edit(nick=nickFinal)

@client.command()
async def full(ctx, token: discord.Member = ''):
    if token == '':
        nickAtual = ctx.message.author.nick
        nickEditar = ctx.message.author
    else:
        nickAtual = token.nick
        nickEditar = token

    nome = acharNoNick(nickAtual, 'nome')
    hp = acharNoNick(nickAtual, 'hp')
    mana = acharNoNick(nickAtual, 'mana')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    manaAtual = acharNoNick(nickAtual, 'manaAtual')
    manaTotal = acharNoNick(nickAtual, 'manaTotal')
    flecha = acharNoNick(nickAtual, 'flechas')

    if hp != '' and mana != '':
        nick = f"{nome} {hpTotal.replace(' ', '')}/{hpTotal}| {manaTotal.replace(' ', '')}/{manaTotal}|{flecha}"
        final = f'Elixir esta enchendo sua HP e mana `glub glub glub`\nHP: {hpAtual} + {int(hpTotal) - int(hpAtual)} = {hpTotal}\nMana: {manaAtual} + {int(manaTotal) - int(manaAtual)} = {manaTotal}'
    elif hp != '' and mana == '':
        nick = f"{nome} {hpTotal.replace(' ', '')}/{hpTotal}|{mana}{flecha}"
        final = f'Elixir esta enchendo sua HP `glub glub glub`\nHP: {hpAtual} + {int(hpTotal) - int(hpAtual)} = {hpTotal}'
    elif hp == '' and mana == '':
        nick1 = f'HP e Mana nao estao em seu nick'
        await ctx.send(nick1)
    print(nickEditar)
    try:
        await nickEditar.edit(nick=nick)
    except discord.errors.Forbidden:
        await ctx.send('Sou fraco, me falta permissão')
    else:
        await ctx.reply(final)


@client.command(aliases=['tr'])
async def tdasRolagens(ctx, token = None):
    await atributos.stre(ctx, token=token)
    await atributos.dex(ctx, token=token)
    await atributos.con(ctx, token=token)
    await atributos.wis(ctx, token=token)
    await atributos.inte(ctx, token=token)
    await atributos.cha(ctx, token=token)
    await atributos.hab(ctx, token=token)
"""

# ------------------- TESTES DE ATRIBUTOS ----------------#

# ------------------- TESTES DE PERÍCIA DE ATRIBUTOS ----------------#

@client.command(aliases=['pstr', 'pfor', 'pforça'])
async def pstre(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'stre', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pdes', 'pdestreza'])
async def pdex(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'dex', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pconstituição'])
async def pcon(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'con', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pint', 'pinteligencia'])
async def pinte(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'int', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['psab', 'psabedoria'])
async def pwis(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'wis', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pcarisma', 'pcar'])
async def pcha(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'cha', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['ppod', 'phabilidade', 'ppoder'])
async def phab(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'hab', 'p')
    if token[1] == 1:
        await ctx.send(token[0])

"""

@client.command()
async def van(ctx, teste):
    if teste.lower().startswith('p') and teste.lower() != 'pod':
        pericia = 'p'
        teste = teste[1:][:3].upper()
    else:
        pericia = 'o'
        teste = teste[:3].upper()

    token = idPersonagem(ctx.author.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], teste, pericia, 'sim')
    if token[1] == 1:
        await ctx.send(token[0])

@client.command()
async def desv(ctx, teste):
    if teste.lower().startswith('p') and teste.lower() != 'pod':
        pericia = 'p'
        teste = teste[1:][:3].upper()
    else:
        pericia = 'o'
        teste = teste[:3].upper()

    token = idPersonagem(ctx.author.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], teste, pericia, 'no', 'sim')
    if token[1] == 1:
        await ctx.send(token[0])

@client.command(aliases=['s'])
async def sorte(ctx):
    coiso = rolagem(ctx, '1d20')
    dado = int(coiso[1])
    dadoRolagem = coiso[2]
    if dado >= 10:
        await ctx.reply(f'Teste de Sorte\n\nSucesso | {dadoRolagem}', mention_author=True)
    elif dado < 10:
        await ctx.reply(f'Teste de Sorte\n\nFracasso | {dadoRolagem}', mention_author=True)
    else:
        await ctx.reply('uékkkkkk', mention_author=True)

@client.command()
async def calc(ctx, *, conta):
    await ctx.send(f'{conta} = `{eval(conta)}`')

#@client.command()
#async def invite(ctx):
#    await ctx.send(
#        'Convide o Elixir para seu servidor com este link\nhttps://discord.com/api/oauth2/authorize?client_id=873979047640711188&permissions=8&scope=bot')

@client.command()
async def novaMesa(ctx, *, todos):
    guild = ctx.guild
    guildSend = client.get_guild(ctx.guild.id)

    todosA = todos.split(', ')
    print(todosA)
    campanha = todosA[0]
    try: qntPlayer = int(todos.split('player:')[1].split(",")[0])
    except IndexError:
        ctx.send(
            'A quantidade de players não foi estabelecida, determine a quantidade utilizando "player:<quantidade>", digite o comando como o exemplo abaixo:\n.novaMesa nome:Nova Campanha, player:5, posicao:3'
        )
        return
    except ValueError:
        ctx.send('Não consegui reconhecer a quantidade de player, digite o comando conforme o exemplo abaixo:\n.novaMesa nome:Nova Campanha, player:5, posicao:3')
        return

    try: campanha = todos.split('nome:')[1].split(",")[0]
    except IndexError:
        ctx.send(
            'O nome da mesa não foi estabelecido, determine o nome utilizando "nome:<nome da campanha>", digite o comando como o exemplo abaixo:\n.novaMesa nome:Nova Campanha, player:5, posicao:3'
        )
        return

    try: posicao = int(todos.split('posicao:')[1]) + 1
    except IndexError:
        ctx.send(
            'A posição de onde a categoria vai ficar no servidor não foi estabelecida, determine a posição utilizando "posicao:<numero>", digite o comando como o exemplo abaixo:\n.novaMesa nome:Nova Campanha, player:5, posicao:3'
        )
        return

    except ValueError:
        ctx.send('Não consegui reconhecer a posição, digite o comando conforme o exemplo abaixo:\n.novaMesa nome:Nova Campanha, player:5, posicao:3')
        return

    ficha = """▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
NOME: 
IDADE: 
JOGADOR: @ 
GÊNERO: 
Ex. Magica: 
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
ATRIBUTOS
Força: val (+mod)
Destreza: val (+mod)
Constituição: val (+mod)
Inteligência: val (+mod)
Sabedoria: val (+mod)
Carisma: val (+mod)
Poder: val (+mod)
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Pericias:
►acrobacia (dex); {val}
►arcanismo (int); {val}
►arremesso (dex); {val}
►artes (wis); {val} [ex]
►atletismo (str); {val}
►convencer (cha); {val}
►crafting (int); {val}
►domesticar (cha); {val}
►estudo (int); {val} [ex]
►furtividade (dex); {val}
►lábia (cha); {val}
►medicina (int); {val}
►natureza (wis); {val}
►percepção (wis); {val}
►pilotar (int); {val} [ex]
►primeiros socorros (int); {val}
►psicologia (int); {val}
►trapaça (dex); {val}
►uso de armas (str); {val}
►uso de armas (dex); {val}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Mandato:
►
►
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Aparência
Cor do olhos: 
Cor da pele: 
Cor cabelo: 
Altura: 
Roupa completa/vestimentas:
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Bag/Mochila;
► item -peso
►
► 
► 
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Armas;
► arma -dano -peso
► 
► 
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Back History:"""
    await guild.create_category(name=campanha, position=posicao)
    categoriaCampanha = get(ctx.guild.categories, name=campanha)
    count = 0
    while count < qntPlayer:
        await guild.create_text_channel(name=f'personagem-{count + 1}', category=categoriaCampanha)
        channel_id = get(guild.text_channels, name=f'personagem-{count + 1}')
        print(channel_id)
        channel = client.get_guild(ctx.guild.id).get_channel(channel_id.id)
        await channel.send(ficha)
        await channel.send("https://docs.google.com/spreadsheets/d/1VfS-zj3nG_nIyK-O56sRfdn7e7OHeORGVYK6-90TyB4/edit#gid=0")
        count += 1
    await ctx.send(
        f'Nova Campanha: **{campanha}** foi criada com sucesso. {qntPlayer} modelos de fichas novas foram enviados ')


@client.command(aliasses=['peticao'])
async def petição(ctx, *, peticao):
    msg = await ctx.send(f"@everyone {peticao}")
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@client.command()
async def RELIQUIAS(ctx):
    await ctx.send('ELE DISSE RELIQUIAS???????????????')

@client.command(aliases=['sf'])
async def server_info(ctx):
    embed = discord.Embed(title=f'Informações do Server xeroso:',
        description=f'Esse server bonito tem {len(ctx.guild.text_channels)} canais de texto e {len(ctx.guild.voice_channels)} canais de voz. Tem ao total {len(ctx.guild.members)} membros. Foi criado aos exatos {ctx.guild.created_at}. Ao todo tem {len(ctx.guild.roles)} cargos\n\n__***"{ctx.guild.description}"***__ - Descrição do server\nAtual Monarca: {ctx.guild.owner.mention}',
        color=discord.Color.blue())

    icon = ctx.guild.icon_url
    nome = ctx.guild.name
    embed.set_author(name=nome, icon_url=icon)
    embed.set_thumbnail(url=icon)
    for channel in ctx.guild.text_channels[:6]:
        embed.add_field(name=channel.name, value=f'categoria: {channel.category} | data de criação: {channel.created_at}')
    for category in ctx.guild.categories[:6]:
        embed.add_field(name=category.name, value=f"n° canais texto: {len(category.text_channels)}| n° canais voz: {len(category.voice_channels)} | data de criação: {category.created_at}")
    emoji = get(ctx.message.guild.emojis, name='raphaelkawaii')
    buttons = [Button(style=ButtonStyle.red, emoji=emoji, custom_id='server_info.raphakawai'), Button(style=ButtonStyle.blue, emoji='🍰', custom_id='server_info.bolo'), Button(style=ButtonStyle.green, emoji='🎉', custom_id='server_info.festim')]
    await ctx.send(embed=embed, components=[buttons])

def comando(ctx, helpComando):
    return ctx.send('aaaaa')

@client.command()
async def help(ctx, helpComando=None):
    contents = [secao1(ctx), secao2(ctx), secao3(ctx), secao4(ctx), secao5(ctx)]

    buttons = [
        Button(style=ButtonStyle.blue, emoji="◀️", custom_id=f'help.pass_left.0.{ctx.author.id}'),
        Button(style=ButtonStyle.blue, emoji="▶️", custom_id=f'help.pass_right.0.{ctx.author.id}')
    ]

    msg = await ctx.send(embed=contents[0], components=[buttons])

TOKEN = key.get_token()

client.run(TOKEN)
