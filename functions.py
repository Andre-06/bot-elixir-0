import mysql.connector.errors

import bot_commands
import data_base
from main import *
import random
from bot_commands import *
from data_base import *
from gsheet import *

def rolagemTag(dado):

    dado = dado.replace(" ", '')
    finalFinal = []
    resultadoFinal = []
    monteDeDadosSFinal = []
    limite = f"` XXXX ` ⟵  [Limite Alcançado]"

    if '#' in dado:
        rollSeparado = int(dado.split("#")[0])
        dado = dado.split('#')[1]
        if rollSeparado > 100: return limite
    else:
        rollSeparado = 1

    for i in range(0, rollSeparado):

        ###################### PRIMEIRA PARTE SÓ ############

        dadoS = []
        dadoM = []
        soma = []
        min = []

        dados = dado.split('+')
        print(f'dados: {dados}')
        for d in dados:
            print(f'd: {d}')
            if 'd' in d and '-' not in d:
                print('entrou 1: dado puro')
                dadoS.append(d)
            elif '-' in d:
                newDados = d.split('-')
                print(f'newDados: {newDados}')
                if 'd' in newDados[0]:
                    print('entrou 2: primeiro dado do split -')
                    dadoS.append(newDados[0])
                elif newDados[0] != '':
                    print('entrou 3: primeiro numero do split -')
                    soma.append(int(d.split('-')[0]))
                del(newDados[0])
                print(f"newDados new: {newDados}")
                for newD in newDados:
                    print(f'newD: {newD}')
                    if newD == '':
                        print('entrou 4: vazio antes do split -')
                        pass
                    elif 'd' in newD:
                        print('entrou 5: dado puro negativo')
                        dadoM.append(newD)
                    else:
                        print('entrou 6: numero negativo')
                        min.append(int(newD))
            else:
                print('entrou 7: numero positivo')
                soma.append(int(d))

        if len(dadoS) > 10 or len(dadoM) > 10:
            return limite

        #######################   ROLAGEM RANDOMICA   ######################

        monteDeDadosS = []
        monteDeDadosM = []

        if dadoS != []:
            for d in dadoS:
                qntD = d.split('d')[0]
                if qntD == '': qntD = 1
                else: qntD = int(qntD)
                numD = int(d.split('d')[1])

                if qntD > 100 or numD > 500: return limite

                for i in range(0, qntD):
                    ran = random.randint(1, numD)
                    if ran == numD:
                        monteDeDadosS.append(ran + 10000)
                    else:
                        monteDeDadosS.append(ran)
            else:
                monteDeDadosS.sort(reverse=True)

        if dadoM != []:
            for d in dadoM:
                qntD = d.split('d')[0]
                if qntD == '': qntD = 1
                else: qntD = int(qntD)
                numD = int(d.split('d')[1])

                if qntD > 100 or numD > 500: return limite

                for i in range(0, qntD):
                    ran = random.randint(1, numD)
                    if ran == numD:
                        monteDeDadosM.append(ran + 10000)
                    else:
                        monteDeDadosM.append(ran)
            else:
                monteDeDadosM.sort(reverse=True)

        print(f'monteDeDadosS: {monteDeDadosS}')
        print(f'monteDeDadosM: {monteDeDadosM}')
        print(f'sum: {soma}')
        print(f'min: {min}')

        #######################  TOTAIS  ######################

        totalS = 0
        for i in monteDeDadosS:
            if i > 10000:
                totalS = totalS + i - 10000
            else:
                totalS = totalS + i

        totalM = 0
        for i in monteDeDadosM:
            if i > 10000:
                totalM = totalM + i - 10000
            else:
                totalM = totalM + i

        totalSum = sum(soma)

        totalMin = sum(min)

        resultado = totalS - totalM + totalSum - totalMin

        #######################  STR DO SUM E MIN  ######################

        sumStrComp = []
        if soma == []:
            sumStrComp = ''
        else:
            for i in soma:
                sumStrComp.append(str(i))

        minStrComp = []
        if min == []:
            minStrComp = ''
        else:
            for i in min:
                minStrComp.append(str(i))

        #######################  EXTREMO DESASTRE  ######################

        count = 0
        while count < len(monteDeDadosM):
            i = monteDeDadosM[count]
            try:
                if i > 10000:
                    monteDeDadosM[count] = '**' + str(i - 10000) + '**'
                elif i == 1:
                    monteDeDadosM[count] = '**' + str(i) + '**'
            except TypeError:
                pass
            count = count + 1

        count = 0
        while count < len(monteDeDadosS):
            i = monteDeDadosS[count]
            try:
                if i > 10000:
                    monteDeDadosS[count] = '**' + str(i - 10000) + '**'
                elif i == 1:
                    monteDeDadosS[count] = '**' + str(i) + '**'
            except TypeError:
                pass
            count = count + 1

        #######################  FINALIZAÇÕES  ######################

        if totalSum != 0:
            finalSoma = f" + {' + '.join(sumStrComp)}"
        else:
            finalSoma = ''

        if totalMin != 0:
            finalMenos = f" - {' - '.join(minStrComp)}"
        else:
            finalMenos = ''

        if totalM != 0:
            finalDadosNegativos = f" - {monteDeDadosM} {'-'.join(dadoM)}"
        else:
            finalDadosNegativos = ''

        if totalS != 0:
            finalBasico = f"{monteDeDadosS} {'+'.join(dadoS)}"
        else:
            finalBasico = ''

        final = f"` {resultado} ` ⟵  " + finalBasico + finalDadosNegativos + finalSoma + finalMenos
        resultadoFinal.append(resultado)
        monteDeDadosSFinal.append(monteDeDadosS)
        finalFinal.append(final)

    return('\n'.join(finalFinal), sum(resultadoFinal), monteDeDadosSFinal, resultadoFinal)

def sum(list_):
    total = 0
    for i in list_:
        total = total + i
    else:
        return total

def rolagem(ctx, dado):
    print(ctx)
    if '+' in dado:
        posicao = dado.split('d')
        print(posicao)
        print(posicao[0])
        print(posicao[1])
        separa = posicao[1].split('+')
        soma = int(separa[1])
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(separa[0])
        print(type(x))
        print(x)
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while x > count:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu
                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)

        resultado = maisDeUmDado + soma
        print(separa)


    elif '-' in dado:
        posicao = dado.split('d')
        separa = posicao[1].split('-')
        soma = int(separa[1])
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(separa[0])
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while x > count:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu
                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)

        resultado = int(maisDeUmDado) - soma
        print(separa)

    else:
        soma = 0
        posicao = dado.split('d')
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(posicao[1])
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while count < x:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu

                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)
            resultado = int(maisDeUmDado)

    if ctx != '1':
        print(posicao)
        if type(todosOsDados) == str:
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            finalNal = ctx.reply(final, mention_author=True)
            return (finalNal, resultado, final, deu)
        else:
            todosOsDados.sort(reverse=True)
            print(todosOsDados)
            count = 0
            while count < len(todosOsDados):
                if todosOsDados[count] == 1 or todosOsDados[count] == y:
                    todosOsDados[count] = f'**{todosOsDados[count]}**'
                    print(todosOsDados[count])
                else:
                    count = count + 1
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            finalNal = ctx.reply(final, mention_author=True)
            return (finalNal, resultado, final, todosOsDados, maisDeUmDado)
    if ctx == '1':
        print(posicao)
        if type(todosOsDados) == str:
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            return (resultado, final, deu)
        else:
            todosOsDados.sort(reverse=True)
            print(todosOsDados)
            count = 0
            while count < len(todosOsDados):
                if todosOsDados[count] == 1 or todosOsDados[count] == y:
                    todosOsDados[count] = f'**{todosOsDados[count]}**'
                    print(todosOsDados[count])
                else:
                    count = count + 1
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            return (resultado, final, todosOsDados, maisDeUmDado)


def acharLinha(arquivo, variavel):
    lerArq = open(arquivo, 'r').readlines()
    count = 0
    while count < len(lerArq):
        if variavel in lerArq[count]:
            return count
            count = count + len(lerArq) + 1
        else:
            count = count + 1
    return IndexError


def item_lista(lista, itemAchar):
    count = 0
    for item in lista:
        if str(itemAchar).lower() in str(item).lower():
            return count
        else:
            count = count + 1
    else:
        return IndexError


def qualSinal(atribute):
    if '+' in atribute and '-' in atribute:
        return 'Ih rapaz'
    elif '+' in atribute:
        return '+'
    elif '-' in atribute:
        return '-'
    elif '>' in atribute:
        return '>'
    elif '<' in atribute:
        return '<'
    elif '+' in atribute:
        return '+'
    elif '*' in atribute:
        return '*'
    elif '/' in atribute:
        return '/'
    elif '^' in atribute:
        return '^'
    else:
        return IndexError


def acharAtributo(player, atributo):
    arq = open(f'ficha {player}.txt', 'r')
    ficha = arq.readlines()
    for atributoFicha in ficha:
        if atributo.upper() in atributoFicha.upper():
            return atributoFicha
        else:
            pass


def id_by_name(name_channel, guild):
    for channel in guild:
        print(channel.name)
        if channel.name == name_channel:
            return channel.id
            print(channel.id)


def corConvert(color):
    if color == 'verde':
        cor = 32768
    elif color == 'azul':
        cor = 255
    elif color == 'roxo':
        cor = 6950317
    elif color == 'rosa':
        cor = 16718146
    elif color == 'preto':
        cor = 000000
    elif color == 'branco':
        cor = 16777215
    elif color == 'laranja':
        cor = 16753920
    elif color == 'amarelo':
        cor = 16776960
    elif color == 'vermelho':
        cor = 16711680
    elif color == 'ciano':
        cor = 3801067

    else:
        cor = 'Desculpe, não achei essa cor. Tente colocar o código decimal. \nSite para a conversão de decimal: https://convertingcolors.com/'

    return cor


def acharNoNick(nick, achar):
    print('---INICIO-----------INICIO-------------INICIO--------------------INICIO---------')

    if "|" in nick:
        partesNick = nick.split('|')
        print(partesNick)
    elif 'I' in nick:
        partesNick = nick.split('I')
        print(partesNick)
    elif 'l' in nick:
        partesNick = nick.split('l')
        print(partesNick)
    else:
        return None

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = partesNick[0] + '|'
    hp = partesNick[1] + '|'
    hpAtual = partesNick[1].split('/')[0]
    hpTotal = partesNick[1].split('/')[1]
    flechas = ''
    flechasAtual = ''
    flechasTotal = ''
    manaTotal = ''
    manaAtual = ''
    mana = ''

    count = 0
    while count < len(partesNick):
        print(f"parte do nick analisado: {partesNick[count]}")
        if partesNick[count].replace(' ', '') == '':
            del (partesNick[count])
            print(f'nick tava vazio')
            count = count + 1
        else:
            print(f'nick nn tava vaio')
            count = count + 1

    if len(partesNick) == 3:
        # Maugrin Maugrin , 40/40 , 500/500
        # Maugrin Maugrin , 40/40 , f 20/20

        if 'f' in partesNick[2]:
            # Maugrin Maugrin , 40/40 , f 20/20
            flechas = partesNick[2]
            flechasAtual = partesNick[2].split('/')[0]
            flechasTotal = partesNick[2].split('/')[1]
        else:
            # Maugrin Maugrin , 40/40 , 500/500
            mana = partesNick[2]
            manaAtual = partesNick[2].split('/')[0]
            manaTotal = partesNick[2].split('/')[1]

    elif len(partesNick) == 4:
        # Maugrin Maugrin , 40/40 , 500/500 , f 20/20

        mana = partesNick[2] + '|'
        manaAtual = partesNick[2].split('/')[0]
        manaTotal = partesNick[2].split('/')[1]
        flechas = partesNick[3]
        flechasAtual = partesNick[3].split('/')[0]
        flechasTotal = partesNick[3].split('/')[1]

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(f"nome: {nome}")
    print(f"hp: {hp}")
    print(f"hpAtual: {hpAtual}")
    print(f"hpTotal: {hpTotal}")
    print(f"flechas: {flechas}")
    print(f"flechasAtual: {flechasAtual}")
    print(f"flechasTotal: {flechasTotal}")
    print(f"manaTotal: {manaTotal}")
    print(f"manaAtual: {manaAtual}")
    print(f"mana: {mana}")
    print(f"nickFinal: {nickFinal}")

    if achar == 'nome':
        return nome
    elif achar == 'hp':
        return hp
    elif achar == 'hpAtual':
        return hpAtual
    elif achar == 'hpTotal':
        return hpTotal
    elif achar == 'mana':
        return mana
    elif achar == 'manaTotal':
        return manaTotal
    elif achar == 'manaAtual':
        return manaAtual
    elif achar == 'flechas':
        return flechas
    elif achar == 'flechasAtual':
        return flechasAtual
    elif achar == 'flechasTotal':
        return flechasTotal
    elif achar == 'nickFinal':
        return nickFinal
    else:
        return int('aaa')

    print('--FIM------------------------FIM--------------------FIM---------------FIM-----')


def rolagemAtributo(ctx, token, atributo, pericia):
    # tenta abrir a ficha, se não exiter o persongme, masnda a mesmagem de erro
    if token == None:
        try: token = idPersonagem(ctx.author.id)
        except IndexError:
            return ctx.send('Nenhum personagem selecionado para esse player. Selecione um personagem com o `.select <@player> <personagem>`')

    try:
        if val_personagem_existe(token) != True:
            return ctx.send('O personagem selecionado não existe')
    except mysql.connector.errors.OperationalError:
        return ctx.send('A conecção com o servidor PC batata de Maugrin foi perdida')

    try:
        url = data_base.get_link(token)
    except IndexError:
        return ctx.send('Essa ficha ainda não foi adicinado ao bot. Para adicioná-la utilize o comando `.ficha <nome do personagem> <link da palilha>` e compartilhe a planilha com este email elixiraccount@bot-elixir.iam.gserviceaccount.com')


    # trasforma o docs em lista e coloca o atributo no upper só pra confirmar
    atb = atributo_gs(atributo, token=token, get_mod=True, get_atb=True)
    modificador = atb[1]
    valorAtributo = atb[0]

    print(f'pericia: {pericia}')

    if pericia == '':
        tabelaSistema = 'tabela sistema d20.txt'
        arq = open(tabelaSistema, 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')

        rolarDado = rolagem(ctx, f'1d20{modificador}')
        dado = rolarDado[1]
        dadoNatural = rolarDado[3]

        # define o normal bom e extremo baseado na linha
        normal = tabelaAtributo[0]
        bom = tabelaAtributo[1]
        extremo = tabelaAtributo[2]

        if dadoNatural == ['**1**']:
            resultado = '**Desastre**'
        elif dadoNatural == ['**20**']:
            resultado = '__**Crítico**__'
        elif dado >= int(normal) and dado < int(bom):
            resultado = '`Sucesso Normal`'
        elif dado >= int(bom) and dado < int(extremo):
            resultado = '`**Sucesso Bom**`'
        elif dado >= int(extremo):
            resultado = '**Extremo**'
        elif dado < int(normal):
            resultado = 'Fracasso'
        else:
            resultado = 'uékkkkkk analise'

        final = ctx.reply(
            f'{token.title()}: Teste de {atributo.title()} = {valorAtributo}{modificador} \n{resultado} | {rolarDado[2]} ',
            mention_author=False)

    else:
        pl = pericia.split(' ')
        new_pericia = list()
        bonus_sum = 0
        bonus_dice = 0

        for p in pl:
            try:
                p.split('d')[1]
                int(p.split('d')[0])
            except (ValueError, IndexError):
                print(f'Deu ruim 1: {p} não é um dado')
                try: int(p)
                except ValueError:
                    print(f'Deu ruim 2: {p} não é numero, {p} é pericia msm')
                    new_pericia.append(p)
                else:
                    print(f'Deu bom 2: {p} é um numero')
                    bonus_sum = p
            else:
                print(f'Deu bom 1: {p} é dado')
                bonus_dice = int(p.split('d')[0])

        pericia = ' '.join(new_pericia)

        print(f'pericia: {pericia}')
        print(f'bonus_dice: {bonus_dice}')
        print(f'bonus_sum: {bonus_sum}')

        if check_per(atributo, pericia) == False:
            return ctx.send(f'{pericia.title()} não é uma perícia de {atributo.title()}')


        desv = False
        ctxDePericia = f" com {pericia.title()}"

        ctxModTruePericia = pericia_gs(pericia, token, get_mod=True)
        mod_per = int(ctxModTruePericia) + bonus_dice

        if mod_per < 0:
            ctxModPericia = mod_per - 1
            mod_per = mod_per * -1
            desv = True
        else:
            ctxModPericia = mod_per + 1

        mod_per = mod_per + 1
        if bonus_sum != 0: modificador = bonus_sum

        rolarDado = rolagemTag(f"{mod_per}#1d20{modificador}")
        dadosSeparados = rolarDado[0].split('\n')
        resultados = rolarDado[3]
        count = 0
        posi = ''

        if desv == False:
            maxN = 0

            print(len(resultados))
            while count < len(resultados):
                print(f"maxN: {maxN}")
                print(f"posi: {posi}")
                print(f"count: {count}")
                if maxN < resultados[count]:
                    print(f'entrou 1: {maxN} era menor que {resultados[count]}')
                    maxN = resultados[count]
                    posi = count
                else:
                    print(f'não entrou 1: {maxN} não é maior que {resultados[count]}')
                count = count + 1
        else:
            maxN = 99

            while count < len(resultados):
                print(f"maxN: {maxN}")
                print(f"posi: {posi}")
                print(f"count: {count}")
                if maxN > resultados[count]:
                    print(f'entrou 1: {maxN} era maior que {resultados[count]}')
                    maxN = resultados[count]
                    posi = count
                else:
                    print(f'nao entrou 1: {maxN} não era maior que {resultados[count]}')
                count = count + 1

        print(f"maxN: {maxN}")
        print(f"posi: {posi}")

        print(f"dadosSeparados: {dadosSeparados}")
        print(f"resultados: {resultados}")

        if posi != '' and mod_per != 1:
            dadosSeparados[posi] = f"**{dadosSeparados[posi].replace('*', '')}**"

        final = ctx.reply(
            f'{token.title()}: {atributo.title()} ({modificador}){ctxDePericia} ({ctxModTruePericia}) = {ctxModPericia}d20{modificador}\n' + '\n'.join(dadosSeparados),
            mention_author=False)


    return final

def check_per(atributo, pericia):
    atb_per = {'FORÇA': ['Lutar', 'Lut', 'Atletismo', 'Atle', 'Uso De Armas', 'Uso'],
               'DESTREZA': ['Arremesso', 'Arreme', 'Acrobacia', 'Acro', 'Furtividade', 'Furti', 'Mãos Leves', 'Maos Leves', 'Maos', 'Pilotar', 'Pilo', 'Uso De Armas', 'Uso'],
               'SABEDORIA': ['Percepção', 'Percepcao', 'Percep', 'Artes', 'Arte', 'Natureza', 'Natu'],
               'CARISMA': ['Lábia', 'Labia', 'Lab', 'Domesticar', 'Dome', 'Convencer', 'Conv'],
               'INTELIGENCIA': ['Primeiros Socorros', 'Prime', 'Medicina', 'Medi', 'Psicologia', 'Psi', 'Arcanismo', 'Arc', 'Estudos', 'Est', 'Crafting', 'Craf']}

    if pericia.title() in atb_per[atributo.upper()]:
        return True
    else:
        return False

def idPersonagem(nick: int):
    '''
    Retorna o nome do personagem a partir do id no discord
    '''
    try:
        name = data_base.return_fetchall(f"select nome from personagem where iddiscord = '{nick}'")[0][0]
    except IndexError:
        return IndexError ('Nenhum personagem selecionado para esse player. Selecione um personagem com o `.select <@player> <personagem>`', 0)
    else:
        return name

def idPeloPersonagem(personagem):
    try:
        id_ = id_name_db(name=personagem)
        name = data_base.return_fetchall(f"select iddisccord from personagem where idpersonagem = '{id_}'")[0][0]
    except IndexError:
        return 'Nenhum personagem selecionado para esse player. Selecione um personagem com o `.select <@player> <personagem>`'
    else:
        return name

def val_selection(ctx):
    try:
        token = idPersonagem(ctx.author.id)
        return token
    except IndexError:
        return ctx.send('Nenhum personagem selecionado para esse player. Selecione um personagem com o `.select <@player> <personagem>`')

def acharItemNaLista(item, lista):
    for i in lista:
        if item in i:
            return i
            break

def index_(item, list: list):
    count = 0
    for i in list:
        if remover(item, ['all']).lower() in remover(i, ['all']).lower():
            return (i, count)
            break
        count += 1

def val_a_in_b(a, b):
    if a in b:
        c = a
        return c


async def fichaCompletaCodigo(ctx, fichaInteira):

    await ctx.send('-------------------------------- INICIANDO CÓDIGO ----------------------------------')

    ficha = fichaInteira.split('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n')
    dadosPessoais = ficha[1].split('\n')
    atributos = ficha[2].split('\n')[1:]
    pericias = ficha[3].split('\n')[1:]

    bag = ficha[6].split('\n')[2:]
    bag2 = []
    for i in bag:
        i2 = i.split('►')
        bag2.append(''.join(i2))
    else:
        bag = bag2

    arma = ficha[7].split('\n')[2:]
    arma2 = []
    for i in arma:
        i2 = i.split('►')
        arma2.append(''.join(i2))
    else:
        arma = arma2

    nome = dadosPessoais[0].replace(" ", '').replace('NOME:', '')

    print('-------- DADOS PESSOAIS -----------')
    print(dadosPessoais)
    print('NOME: ' + nome)
    print('-------- ATRIBUTOS -----------')
    print(atributos)
    print('-------- PERICIAS -----------')
    print(pericias)
    print('-------- BAG -----------')
    print(bag)
    print('-------- ARMA -----------')
    print(arma)

    cAtributos = {'Força': 'str', 'Destreza': 'dex', 'Constituição':'con', 'Inteligência' : 'inte',
                  'Sabedoria' : 'wis', 'Carisma' : 'cha', 'Poder' : 'pod'}

    cPericias = {'acrobacia(dex)' : 'acrobacia', 'arcanismo(int)' : 'arcanismo', 'arremesso(dex)' : 'arremesso',
                 'artes(wis)' : 'artes', 'atletismo(str)' : 'atletismo', 'convencer(cha)' : 'convencer',
                 'crafting(int)' : 'crafting', 'domesticar(cha)' : 'domesticar', 'estudo(int)' : 'estudo',
                 'furtividade(dex)' : 'furtividade', 'lábia(cha)' : 'lábia', 'medicina(int)' : 'medicina',
                 'natureza(wis)' : 'natureza', 'percepção(wis)' : 'percepção', 'pilotar(int)' : 'pilotar',
                 'primeirossocorros(int)' : 'primeirossocorros', 'psicologia(int)' : 'psicologia',
                 'trapaça(dex)' : 'trapaça', 'usodearmas(str)' : 'armasstr', 'usodearmas(dex)' : 'armasdex'}

    atbL = []
    atbLB = []
    valL = []
    modL = []

    perL = []
    perLB = []
    pValL = []

    for item in atributos:
        item = item.replace(' ', '').split(':')
        if item == ['']: pass
        else:
            atb = cAtributos[item[0]]
            val = item[1].split('(')[0]
            mod = item[1].split('(')[1].replace(")", '')

            atbL.append(atb)
            atbLB.append(item[0])
            valL.append(val)
            modL.append(mod)

    for item in pericias:
        item = item.replace(' ', '').replace('►', '').replace('{', '').replace('}', '').replace('/', '').split(';')
        print("item pericias")
        print(item) # ['lutarbriga', '10']
        if item == ['']: pass
        else:
            per = cPericias[str(item[0])]
            val = item[1]
            if '[' in val:
                val = val.split("[")[0]
                print(f'val: {val}')

            perL.append(per)
            perLB.append(item[0])
            pValL.append(val)

    character_exist = False

    db = data_base.cursor.execute("""select a.idatributos, a.personagematributos
                                from atributos as a""", True)
    print(f"db: {db}")

    for tpl in db:
        print(f"Tupla: {tpl}")
        print(f"Nome: {tpl[1].lower()}")
        print(f"Igual: {nome.lower()}")
        if nome.lower() == tpl[1].lower():
            print(f'Foi\nidtable: {tpl[0]}')
            character_exist = True
            idtable = tpl[0]

            break

    character_per_exist = False

    db = data_base.cursor.execute("""select p.idpericias, p.personagempericias
                                    from pericias as p""", True)
    print(f"db: {db}")

    for tpl in db:
        print(f"Tupla: {tpl}")
        print(f"Nome: {tpl[1].lower()}")
        print(f"Igual: {nome.lower()}")
        if nome.lower() == tpl[1].lower():
            print(f'Foi\nidtable: {tpl[0]}')
            character_per_exist = True
            idtable_per = tpl[0]

            break
    if character_exist == True:
        for i in range(0, len(atbL)):
            try:
                data_base.script_sql(f"""UPDATE atributos SET {atbL[i]} = '{valL[i]}' WHERE idatributos = '{idtable}' """)
                data_base.script_sql(f"""UPDATE atributos SET mod{atbL[i]} = '{modL[i]}' WHERE idatributos = '{idtable}' """)
            except mysql.connector.errors.ProgrammingError:
                await ctx.send(f"Houve um erro ao modificar o atributo {atbLB[i].title()} para {valL[i]}")
            else:
                await ctx.send(f"{atbLB[i].title()} modificado para {valL[i]}")
    else:
        try:
            data_base.script_sql(f"""INSERT INTO atributos (personagematributos, {atbL[0]}, {atbL[1]}, {atbL[2]}, {atbL[3]},
                        {atbL[4]}, {atbL[5]}, {atbL[6]}, mod{atbL[0]}, mod{atbL[1]}, mod{atbL[2]}, mod{atbL[3]},
                        mod{atbL[4]}, mod{atbL[5]}, mod{atbL[6]}) VALUES ('{nome}', '{valL[0]}', '{valL[1]}',
                        '{valL[2]}', '{valL[3]}', '{valL[4]}', '{valL[5]}', '{valL[6]}', '{modL[0]}', '{modL[1]}', '{modL[2]}',
                        '{modL[3]}', '{modL[4]}', '{modL[5]}', '{modL[6]}')""")
        except mysql.connector.errors.ProgrammingError:
            await ctx.send(f"""Houve um erro ao adicinar algum de seus atributos, confira se todos estão digitados corretamentes
                      ou se o <@!675407695729131527> esqueceu de corrigir esse erro no bot""")
        else:
            await ctx.send(f"Todos seus atributos foram adicionados com sucesso")


    await ctx.send('--------------------------------------------------------------------------------------------')

    if character_per_exist == True:
        for i in range(0, len(perL)):
            try:
               data_base.script_sql(f"""UPDATE pericias SET {perL[i]} = '{pValL[i]}' WHERE idpericias = '{idtable}' """)
            except mysql.connector.errors.ProgrammingError:
                await  ctx.send(f"Houve um erro ao modificar a perícia {perLB[i].title()} para {perValL[i]}")
            else:
               await  ctx.send(f"{perLB[i].title()} modificado para {pValL[i]}")
    else:
        try:
            data_base.script_sql(f"""INSERT INTO pericias (personagempericias, {perL[0]}, {perL[1]}, {perL[2]}, {perL[3]},
                        {perL[4]}, {perL[5]}, {perL[6]}, {perL[7]}, {perL[8]}, {perL[9]}, {perL[10]}, {perL[11]}, {perL[12]}, 
                        {perL[13]}, {perL[14]}, {perL[15]}, {perL[16]}, {perL[17]}, {perL[18]}, {perL[19]}) 
                        VALUES ('{nome}', '{pValL[0]}', '{pValL[1]}', '{pValL[2]}', '{pValL[3]}',
                       '{pValL[4]}', '{pValL[5]}', '{pValL[6]}', '{pValL[7]}', '{pValL[8]}', '{pValL[9]}', '{pValL[10]}', 
                       '{pValL[11]}', '{pValL[12]}', '{pValL[13]}', '{pValL[14]}', '{pValL[15]}', '{pValL[16]}', '{pValL[17]}', 
                       '{pValL[18]}', '{pValL[19]}')""")
        except mysql.connector.errors.ProgrammingError:
            await ctx.send(f"""Houve um erro ao adicinar alguma de suas perícias, confira se todas estão digitadas corretamentes
                      ou se o <@!675407695729131527> esqueceu de corrigir esse erro no bot""")
        else:
            await ctx.send(f"Todas suas perícias foram adicinadas com sucesso")

    db = data_base.return_fetchall(f"""select pr.idpericias
                                        from pericias as pr 
                                        where pr.personagempericias = '{nome}'""")
    print(f'db per: {db[0][0]}')
    idtable_per = db[0][0]

    db = data_base.return_fetchall(f"""select a.idatributos
                                            from atributos as a 
                                            where a.personagematributos = '{nome}'""")
    print(f'db atb: {db[0][0]}')
    idtable_atb = db[0][0]

    data_base.script_sql(f"""INSERT INTO personagem (nome, atributostable, períciastable) 
                            VALUES ('{nome}', '{idtable_atb}', '{idtable_per}')""")

    await ctx.send('-----------------------------------Transferindos Itens------------------------------------')

    for item in bag:
        if item == '':
            print('passado')
            pass
        else:
            print(f"inventario({ctx}, {nome}, {item})")
            await bot_commands.inventario(ctx, nome, item=item)

    await ctx.send('-----------------------------------Transferindos Armas---------------------------------')

    for item in arma:
        if item == '':
            print('passado')
            pass
        else:
            print(f"nova_arma({ctx}, {nome}, {item})")
            await bot_commands.nova_arma(ctx, nome, arma=item)

    await ctx.send('--------------------------------------------------------------------------------------------')
    await ctx.send(f"Ficha de {nome} foi transferida para o bot com sucesso")

"""

    count = 0
    print(ficha)
    posicaoNome = item_lista(ficha, 'NOME')

    posicaoForça = item_lista(ficha, 'Força')
    posicaoDestreza = item_lista(ficha, 'Destreza')
    posicaoConstituição = item_lista(ficha, 'Constituição')
    posicaoCarisma = item_lista(ficha, 'Carisma')
    posicaoSabedoria = item_lista(ficha, 'Sabedoria')
    posicaoInteligencia = item_lista(ficha, 'Inteligência')

    posicaoArroba = item_lista(ficha, 'JOGADOR')

    if posicaoNome == IndexError: await ctx.send('Não consegui reconhecer seu nome')
    if posicaoForça == IndexError: await ctx.send('Não consegui reconhecer sua força ')
    if posicaoDestreza == IndexError: await ctx.send('Não consegui reconhecer sua destreza ')
    if posicaoConstituição == IndexError: await ctx.send('Não consegui reconhecer sua constituição')
    if posicaoCarisma == IndexError: await ctx.send('Não consegui reconhecer seu carisma')
    if posicaoSabedoria == IndexError: await ctx.send('Não consegui reconhecer sua sabedoria')
    if posicaoInteligencia == IndexError: await ctx.send('Não consegui reconhecer sua inteligencia')
    if posicaoArroba == IndexError: await ctx.send('Não consegui reconhecer seu @')

    token = ficha[posicaoNome].split('NOME')[1]
    arroba = ficha[posicaoArroba].split('JOGADOR:')[1]
    print(f'token antes {token}')
    if token.startswith(':  '):
        token = token[3:]
        print(f'token com dois espços na frente, agora ta assim{token}')
    elif token.startswith(': '):
        token = token[2:]
        print(f'token tava com 1 espaço só, agora ta asism{token}')
    elif token.startswith(':'):
        token = token[1:]
        print(f'sem espaço nenhum, tava certo{token}')
    else:
        await ctx.send("Não consegui reconhecer seu nome")

    token = token.split(' ')[0]
    Força = ficha[posicaoForça]
    Destreza = ficha[posicaoDestreza]
    Constituição = ficha[posicaoConstituição]
    Carisma = ficha[posicaoCarisma]
    Sabedoria = ficha[posicaoSabedoria]
    Inteligencia = ficha[posicaoInteligencia]

    try:
        modificadorHabilidade = ficha[item_lista(ficha, 'uso magico:')].split(':')[1].replace(' ', '')
    except TypeError:
        try:
            modificadorHabilidade = ficha[item_lista(ficha, 'uso de armas:')].split(':')[1].replace(' ', '')
        except TypeError:
            try:
                modificadorHabilidade = ficha[item_lista(ficha, 'poder')].split(':')[1].replace(' ', '')
            except TypeError:
                await ctx.send('Não consegui reconhecer seu poder')

    try:
        modificadorForça = Força.split('(')[0].split(':')[1].replace(' ', '')
        períciasForça = Força.split('(')[1].replace(')', '')
    except IndexError:
        modificadorForça = Força.split(':')[1].replace(' ', '')
        períciasForça = ''

    try:
        modificadorDestreza = Destreza.split('(')[0].split(':')[1].replace(' ', '')
        períciasDestreza = Destreza.split('(')[1].replace(')', '')
    except IndexError:
        modificadorDestreza = Destreza.split(':')[1].replace(' ', '')
        períciasDestreza = ''

    try:
        modificadorConstituição = Constituição.split(':')[1].replace(' ', '')
        períciasConstituição = Constituição.split('(')[1].replace(')', '')
    except IndexError:
        modificadorConstituição = Constituição.split(':')[1].replace(' ', '')
        períciasConstituição = ''

    try:
        modificadorCarisma = Carisma.split('(')[0].split(':')[1].replace(' ', '')
        períciasCarisma = Carisma.split('(')[1].replace(')', '')
    except IndexError:
        modificadorCarisma = Carisma.split(':')[1].replace(' ', '')
        períciasCarisma = ''

    try:
        modificadorSabedoria = Sabedoria.split('(')[0].split(':')[1].replace(' ', '')
        períciasSabedoria = Sabedoria.split('(')[1].replace(')', '')
    except IndexError:
        modificadorSabedoria = Sabedoria.split(':')[1].replace(' ', '')
        períciasSabedoria = ''

    try:
        modificadorInteligencia = Inteligencia.split('(')[0].split(':')[1].replace(' ', '')
        períciasInteligencia = Inteligencia.split('(')[1].replace(')', '')
    except IndexError:
        modificadorInteligencia = Inteligencia.split(':')[1].replace(' ', '')
        períciasInteligencia = ''

    força = f'STR={modificadorForça}'
    destreza = f'DEX={modificadorDestreza}'
    inteligencia = f'INT={modificadorInteligencia}'
    sabedoria = f'WIS={modificadorSabedoria}'
    carisma = f'CHA={modificadorCarisma}'
    constituicao = f'CON={modificadorConstituição}'
    habilidade = f'HAB={modificadorHabilidade}'

    print(modificadorDestreza)
    print(modificadorInteligencia)
    print(modificadorSabedoria)
    print(modificadorCarisma)
    print(modificadorConstituição)

    atributos = [força, destreza, inteligencia, sabedoria, carisma, constituicao, habilidade]

    print(token)
    print(type(token))
    open(f'ficha {token}.txt', 'a')
    if nova == True and editar == False:
        count = 0
        while count < 7:
            await novo_atributo(ctx, token, atributos[count])
            count = count + 1
        await xp(ctx, token, modificadorXp, '!')
        await select(ctx, arroba, token)
        await ctx.send('Nova ficha adicionada com sucesso\nUse o `.verF <personagem>` para ver sua ficha')
    elif nova == False and editar == True:
        count = 0
        while count < 7:
            await editar_atributo(ctx, token, atributos[count])
            count = count + 1
        await xp(ctx, token, modificadorXp)
        await ctx.send('Ficha editada com sucesso\nUse o `.verF <personagem>` para ver sua ficha')
"""


def atributosModi(atb, token):
    cAtributos = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'HAB', 'POD']
    nomeAtributo = atb
    valorAtributo = atributo_db(atb, token=token, get_atb=True)
    modificadorAtributo = atributo_db(atb, token=token, get_mod=True)
    validaçãoD100 = ['ptolomeu', 'maugrin']
    # validaçãoD60 = ['alissa', 'mario']
    validaçãoD60 = [' ']
    d100 = False

    if token.lower() in validaçãoD100:
        arq = open('tabela sistema d100.txt', 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
        d100 = True
    elif token.lower() in validaçãoD60:
        arq = open('tabela sistema d60.txt', 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
    else:
        arq = open('tabela sistema d20.txt', 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')

    normal = str(tabelaAtributo[0])
    bom = tabelaAtributo[1]
    extremo = tabelaAtributo[2]
    muitoBom = ''
    otimo = ''
    if d100 == True:
        muitoBom = tabelaAtributo[2]
        otimo = tabelaAtributo[3]
        extremo = tabelaAtributo[4]

    cEmoji = [':punch:', ':scales:', ':shield:', ':brain:', ':zany_face:', ':bow_and_arrow:', ':medal:']
    emoji = ''
    nomeAtributo = atb
    if 'STR' in nomeAtributo:
        emoji = cEmoji[0]
    elif 'DEX' in nomeAtributo:
        emoji = cEmoji[5]
    elif 'CON' in nomeAtributo:
        emoji = cEmoji[2]
    elif 'WIS' in nomeAtributo:
        emoji = cEmoji[1]
    elif 'CHA' in nomeAtributo:
        emoji = cEmoji[4]
    elif 'HAB' in nomeAtributo or 'POD' in nomeAtributo:
        nomeAtributo = 'PODER'
        emoji = cEmoji[6]
    elif 'INT' in nomeAtributo:
        emoji = cEmoji[3]

    sinal = qual_sinal_db(valorAtributo)

    return (nomeAtributo, valorAtributo, modificadorAtributo, sinal, normal, bom, extremo, emoji, muitoBom, otimo)

def remover(txt: str, char: list = ['all']):
    charList = ['!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '_', '-', ',', '.', '<', '>',
                '[', ']', '{', '}', '\'', ";", ":", '/', '?', 'º', '"', "'", '|', ' ']

    if char[0] == 'all': charUse = charList
    else: charUse = char

    for i in charUse: txt = txt.replace(i, '')
    else: return txt

def secao1(ctx):
    embedFicha = discord.Embed(
        title=f'Elixir Comandos\nSeção {1}/{5}:',
        description='',
        color=6950317
    )

    icon = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=icon)
    embedFicha.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    embedFicha.add_field(name='.planilha', value='Manda o link da ficha planilha',
                         inline=False)
    embedFicha.add_field(name='.ficha <personagem> <link>', value='Adiciona a ficha de um personagem ao bot',
                         inline=False)
    embedFicha.add_field(name='.[fichaCompleta|compF] <ficha>',
                         value='Adiciona a ficha de um personagme ao bot', inline=False)
    embedFicha.add_field(name='.[ver_Ficha|verFicha|verF] <personagem>',
                         value='Mostra a ficha do personagem', inline=False)
    embedFicha.add_field(name='.editarFicha <personagem> <cor> <url da imagem>',
                         value='Subistitui a cor e a imagem padrão da ficha pelas novas', inline=False)
    embedFicha.add_field(name='.[deleteFicha|dltF] <personagem>', value='Deleta a ficha de um personagem',
                         inline=False)
    embedFicha.add_field(name='.select <@player> <personagem>', value='Selciona um personagem para o player',
                         inline=False)
    embedFicha.add_field(name='.desselect <personagem>',
                         value='Desseleciona o personagem para o player ', inline=False)
    embedFicha.add_field(name='.selectAtual <@player>', value='Mostra o personagem selecionado pare o player',
                         inline=False)
    embedFicha.add_field(name='.[atack|atc|a] <arma>', value='Rola o ataque da arma', inline=False)
    embedFicha.add_field(name='.[iniciativa|ini] <personagens>',
                         value='Rola um teste de destreza dos personagens, caso a ficha esteja adicionada ao bot ou um d20 normal caso contrário, e organiza a ordem de iniciativa. Você pode colocar um "-" do lado para adicionar mais de um personagem/inimigo. Exemplo: .iniciativa player 1, player 2, player 3, inimigo -4',
                         inline=False)
    embedFicha.add_field(name='.[addIniciativa|addIni] <personagem>',
                         value='Adiciona o personagem no final da ordem de iniciativa. Você pode escrever "aleatorio:sim" ao final do comando para adicionar o personagem em uma poscição aleatória',
                         inline=False)
    embedFicha.add_field(name='.[remIniciativa|remIni] <personagem>',
                         value='Remove o personagem da ordem de iniciativa', inline=False)
    embedFicha.add_field(name='.next', value='Mostra o próximo na ordem de iniciativa', inline=False)
    embedFicha.add_field(name='.end', value='Encerra a iniciativa', inline=False)
    embedFicha.add_field(name='.view', value='Mostra a ordem de iniciativa', inline=False)

    return embedFicha

def secao2(ctx):
    embedFicha = discord.Embed(
        title=f'Elixir Comandos\nSeção {2}/{5}:',
        description='',
        color=6950317
    )

    icon = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=icon)
    embedFicha.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    embedFicha.add_field(name='.[cura|c] <dado> <@player>',
                         value='Rola um dado de cura e altera no nick', inline=False)
    embedFicha.add_field(name='.hp <valor> <@player(opicional)>',
                         value='Altera a hp no seu nick ou no nick de outro player', inline=False)
    embedFicha.add_field(name='.[dano|d] <dado> <@player>',
                         value='Rola um dado de dano e altera no nick', inline=False)
    embedFicha.add_field(name='.[flecha|f] <quantidade>',
                         value='Altera o seu nick adicionando ou removendo a quantidade', inline=False)
    embedFicha.add_field(name='.[magiaLeve|ml]',
                         value='Rola 2d10 de magia, tira a mana de seu nick e mostra o dado de dano que deu',
                         inline=False)
    embedFicha.add_field(name='.[magiaModerada|mm]',
                         value='Rola 2d30 de magia, tira a mana de seu nick e mostra o dado de dano que deu',
                         inline=False)
    embedFicha.add_field(name='.[magiaExtrema|me]',
                         value='Rola 2d50 de magia, tira a mana de seu nick e mostra o dado de dano que deu',
                         inline=False)
    embedFicha.add_field(name='.full <@player>', value='Coloca a vida e a mana(se tiver) no máximo',
                         inline=False)

    return embedFicha

def secao3(ctx):
    embedFicha = discord.Embed(
        title=f'Elixir Comandos\nSeção {3}/{5}:',
        description='',
        color=6950317
    )

    icon = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=icon)
    embedFicha.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    embedFicha.add_field(name='.[str|dex|con|int|wis|cha|pod] <pericia(opcional)>', value='Rola um teste de pericia um ou teste de atributo do personagem selecionado ao player que rodou o comando', inline=False)
    embedFicha.add_field(name='.[forçar_rolagem|fr] <personagem> <atributo> <pericia(opcional)>',
                         value='Rola um teste de pericia ou um teste de atributo do personagem citado no comando e não do personagem selecionado', inline=False)
    embedFicha.add_field(name='.[roll|r] <dado>', value='Rola um dado', inline=False)
    embedFicha.add_field(name='.[sorte|s]', value='Faz um teste de sorte', inline=False)

    return embedFicha

def secao4(ctx):
    embedFicha = discord.Embed(
        title=f'Elixir Comandos\nSeção {4}/{5}:',
        description='',
        color=6950317
    )

    icon = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=icon)
    embedFicha.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    embedFicha.add_field(name='.icon_server', value='Mostra o icone do servidor', inline=False)
    embedFicha.add_field(name='.icon_user <@membro>', value='Mostra a foto de perfil do membro marcado',
                         inline=False)
    embedFicha.add_field(
        name='.novaMesa nome:<nome da campanha>, player:<quantidade de players>, posicao:<numero>',
        value='Cria uma categoria em uma determinada posição no server do discord com o nome da campanha e adiciona canais de texto igual a quantidade de players com uma ficha e um link da plainha em cada um dos canais. Exemplo: .novaMesa nome:Nova Campanha, player:5, posicao:3',
        inline=False)
    embedFicha.add_field(name='.[petição|peticao] <frase>', value='Cria uma petição', inline=False)
    embedFicha.add_field(name='.calc <conta>', value='Realiza uma conta', inline=False)
    embedFicha.add_field(name='.[conversor|conv] <numero>',
                         value='Converte o numero de feet para metro e de metro para feet', inline=False)
    embedFicha.add_field(name='.mute <@membro>', value='Desativa o microfone de um membro em uma call',
                         inline=False)
    embedFicha.add_field(name='.muteAll',
                         value='Desativa o microfone de todos os membros em uma call que você esteja conectado também',
                         inline=False)
    embedFicha.add_field(name='.unmute <@membro>', value='Reativa o microfone de um membro em uma call',
                         inline=False)
    embedFicha.add_field(name='.[unmuteAll|desmuteall]',
                         value='Reativa o microfone de todos os membros em uma call que você esteja conectado também',
                         inline=False)
    return embedFicha

def secao5(ctx):
    embedFicha = discord.Embed(
        title=f'Elixir Comandos\nSeção {5}/{5}:',
        description='',
        color=6950317
    )

    icon = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=icon)
    embedFicha.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    embedFicha.add_field(name='.analise', value='Faz uma analise apurada da situação', inline=False)
    embedFicha.add_field(name='.eéaqui', value='Acaba com a seção e infarta os players', inline=False)
    embedFicha.add_field(name='.count <numero de vezes> <mensagem>',
                         value='Este comando repete uma mesma messagem',
                         inline=False)
    embedFicha.add_field(name='.xingar <@membro>', value='Xinga o membro marcado', inline=False)
    embedFicha.add_field(name='.hm', value='HUMMMMMMMMMMMMMMMMM', inline=False)
    embedFicha.add_field(name='.paror', value='para com tudo', inline=False)
    embedFicha.add_field(name='.reliquias', value='Confirma se ele disse reliquias', inline=False)
    return embedFicha
