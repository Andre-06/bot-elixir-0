from functions import *
from data_base import *


@client.command(aliases=['str', 'for', 'força'], pass_context=True)
async def stre(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'FORÇA', pericia)
    return ret


@client.command(aliases=['des', 'destreza'])
async def dex(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'DESTREZA', pericia)
    return ret


@client.command(aliases=['carisma', 'car'])
async def cha(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'CARISMA', pericia)
    return ret


@client.command(aliases=['sab', 'sabedoria'])
async def wis(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'SABEDORIA', pericia)
    return ret


@client.command(aliases=['int', 'inteligencia'])
async def inte(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'INTELIGENCIA', pericia)
    return ret


@client.command(aliases=['habilidade', 'poder', 'pod'])
async def hab(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'PODER', pericia)
    return ret


@client.command(aliases=['constituição', 'cons'])
async def con(ctx, *, pericia='', token=None):
    ret = await rolagemAtributo(ctx, token, 'CONSTITUIÇÃO', pericia)
    return ret


@client.command(aliases=['fr'])
async def forçar_rolagem(ctx, personagem, atributo, *, pericia=''):
    convertAtb = {'FORÇA': ['stre', 'str', 'for', 'força'], 'DESTREZA': ['dex', 'des', 'destreza'],
                  'SABEDORIA': ['wis', 'sab', 'sabedoria'], 'CARISMA': ['cha', 'carisma', 'car'],
                  'CONSTITUIÇÃO': ['con', 'cons', 'constituição'], 'INTELIGENCIA': ['inte', 'int', 'inteligencia'],
                  'PODER': ['hab', 'habilidade', 'poder', 'pod']}
    for i in convertAtb:
        if atributo in convertAtb[i]:
            atb = i
            break
    else:
        await ctx.send('Não reconheci o atributo selecionado')
        return

    await rolagemAtributo(ctx, personagem, atb, pericia)
