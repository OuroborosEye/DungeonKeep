import discord
import os
import random
from rollCommand import rollCommand
from initiativeKeeper import initiativeKeeper

client = discord.Client()
servers = {}

init_keep = initiativeKeeper()
roll_cmd = rollCommand()

basic_help_message = '```Dungeon Keep Help:\n\n\t- Purge all bot-related messages: !purge\n\t- Roll dices: !roll\n\t- Initiative Keeping: !init\n\nFor details on more complex commands, type !help command (eg. !help roll)```'
roll_help_message = '```Dungeon Keep Roll Command Help:\n\n\tRepetition:!roll 2 2d6 + 3d10 repeats two times a roll of two six-sided dice and three ten-sided dice. If there is no number the default is one repetition Aliases: !roll 1d20 #alias_name creates an alias. Afterwards, !roll #alias_name will roll 1d20\n\tTHIS FEATURE IS IN DEVELOPMENT! OH NOES! COME BACK LATER :D```'
init_help_message = '```Dungeon Keep Initiative Command Help:\n\n\tshow: Shows all commands currently saved\n\tadd char init: Adds char to the initiative list with initiative init\n\tnext: Shows next char in the list\n\tclear: Empties the initiatives list```'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    if message.content.startswith('!roll '):
        await message.channel.send(roll_cmd.runCommand(message.content))
    elif message.content.startswith('!purge'):
        await purge_messages(message)
    elif message.content.startswith('!help'):
        await show_help(message)
    elif message.content.startswith('!init '):
        await message.channel.send(init_keep.runCommand(message.content))

def is_bot_message(message):
    if message.author == client.user:
        return True
    if message.content.startswith('!roll '):
        return True
    if message.content.startswith('!purge'):
        return True
    if message.content.startswith('!help'):
        return True
    if message.content.startswith('!init'):
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
        if is_bot_message(message):
            to_delete.append(message)
    await message.channel.delete_messages(to_delete)

async def process_roll(message):
    command = message.content.replace('!roll ','').strip()
    if '#' in command:
    

    cmd = Roll(command)
    result = cmd.getResult()
    await message.channel.send('%s rolled %s:' % (message.author.display_name,command))
    for arr in result:
        flattened = [item for sublist in arr for item in sublist]
        await message.channel.send('%s: %s' % (flattened,sum(flattened)))

async def process_init(message):
    command = message.content.replace('!init ','')
    args = command.split(' ')

    guild_id = message.guild.id
    if guild_id not in servers:
        servers[guild_id] = {}
        servers[guild_id]['initiatives'] = []
        servers[guild_id]['initiatives_idx'] = 0

    if args[0] == 'show':
        msg = '```Current initiatives list:\n\n'
        for init in servers[guild_id]['initiatives']:
            msg += '\t\t%s with %s as initiative\n' % (init['name'], init['initiative'])
        msg += '```'

        await message.channel.send(msg)
    elif args[0] == 'add':
        servers[guild_id]['initiatives'].append({'name':args[1], 'initiative':int(args[2])})
        servers[guild_id]['initiatives'].sort(key=lambda k:k['initiative'],reverse=True)
        await message.channel.send('Initiative Added!')
    elif args[0] == 'next': 
        await message.channel.send('Next turn is for: %s' % servers[guild_id]['initiatives'][servers[guild_id]['initiatives_idx']]['name'])

        servers[guild_id]['initiatives_idx'] += 1
        if servers[guild_id]['initiatives_idx'] == len(servers[guild_id]['initiatives']):
            servers[guild_id]['initiatives_idx'] = 0
    elif args[0] == 'clear':
        servers[guild_id]['initiatives'] = []
        servers[guild_id]['initiatives_idx'] = 0

        await message.channel.send('Initiatives reset')


client.run(os.environ['botToken'])