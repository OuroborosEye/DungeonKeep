import discord
import os
import random
from rollCommand import rollCommand
from initiativeKeeper import initiativeKeeper
from datetime import datetime

client = discord.Client()
servers = {}

init_keep = initiativeKeeper()
roll_cmd = rollCommand()

basic_help_message = '```Em Que Posso Ajudar Milord(ady) ?:\n\n\t- Apagar Todas as Minhas Mensagens: !purge\n\t- Rolar Dados: !roll\n\t- Lista de Iniciativa: !init\n\nPara Mais Detalhes ou Comandos Mais Complexos, Digite !help command (ex. !help roll)```'
roll_help_message = '``Aqui Está Mais Detalhes da Lista de Comando de Rolagem,Milord(ady): \n\n\tRepetition:Ex:!roll 2 2d6 + 3d10: Repete 2x a Rolagem do Dado 2d6 + 3d10. Se Não Tiver Um Número Antes, o Padrão é 1. \n\tAliase: !roll 1d20 #aliase_name, Cria Um Apelido, Depois, !roll #alias_name Irá Rolar 1d20 \n\tESSA FUNÇÃO ESTÁ EM DESENVOLVIMENTO! VOLTE DEPOIS :D```'
init_help_message = '```Aqui Está Mais Detalhes da Lista de Comando de Iniciativa, Milord(ady): \n\tshow: Mostra Todos As Iniciativas Salvas na Lista\n\tadd char init: Adiciona Personagem na Lista de Iniciativa\n\tnext: Mostra o Próximo Personagem Da Lista\n\tclear: Limpa a Lista de Iniciativa```'


@client.event
async def on_ready():
    print('Estamos Logados Em {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    if message.content.startswith('!roll '):
        await message.channel.send(roll_cmd.runCommand(message))
    elif message.content.startswith('!purge'):
        await purge_messages(message)
    elif message.content.startswith('!help'):
        await show_help(message)
    elif message.content.startswith('!init '):
        await message.channel.send(init_keep.runCommand(message))

def is_bot_message(message):
    if message.author == client.user:
        return True
    if message.content.lower().startswith('!roll '):
        return True
    if message.content.lower().startswith('!purge'):
        return True
    if message.content.lower().startswith('!help'):
        return True
    if message.content.lower().startswith('!init'):
        return True
    return False


async def show_help(message):
    if 'roll' in message.content:
        await message.channel.send(roll_help_message)
    elif 'init' in message.content:
        await message.channel.send(init_help_message)
    else:
        await message.channel.send(basic_help_message)


async def purge_messages(message):
    to_delete = []
    async for message in message.channel.history(limit=200):
        if is_bot_message(message) and (datetime.now() - message.created_at).days < 14:
            to_delete.append(message)
    await message.channel.delete_messages(to_delete)

client.run('Token Aqui')
