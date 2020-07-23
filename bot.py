import discord
import random
from rollClasses import Roll

client = discord.Client()
servers = {}

basic_help_message = '```Dungeon Keep Help:\n\n\t- Purge all bot-related messages: !purge\n\t- Roll dices: !roll\n\n- For details on more complex commands, type !help command (eg. !help roll)```'
roll_help_message = '```Dungeon Keep Roll Command Help:\n\n\tRepetition:!roll 2 2d6 + 3d10 repeats two times a roll of two six-sided dice and three ten-sided dice. If there is no number the default is one repetition Aliases: !roll 1d20 #alias_name creates an alias. Afterwards, !roll #alias_name will roll 1d20\n\tTHIS FEATURE IS IN DEVELOPMENT! OH NOES! COME BACK LATER :D```'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    if message.content.startswith('!roll '):
        await process_roll(message)
    elif message.content.startswith('!purge'):
        await purge_messages(message)
    elif message.content.startswith('!help'):
        await show_help(message)        

def is_bot_message(message):
    if message.author == client.user:
        return True
    if message.content.startswith('!roll '):
        return True
    if message.content.startswith('!purge'):
        return True
    if message.content.startswith('!help'):
        return True
    return False

async def show_help(message):
    if 'roll' in message.content:
        await message.channel.send(roll_help_message)
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
        if message.guild.id not in servers:
            servers[message.guild.id] = {}
        
        if command.index('#') == 0:
            if command[1:] not in servers[message.guild.id]:
                await message.channel.send('Could not find alias %s' % command[1:])
                return
            else:
                await message.channel.send('Rolling %s (%s)' % (command[1:], servers[message.guild.id][command[1:]])) 
                command = servers[message.guild.id][command[1:]]
        else:   
            [command,alias] = [seg.strip() for seg in command.split('#')]
            servers[message.guild.id][alias] = command
            await message.channel.send('Saved alias %s: %s' % (command,alias))
    

    cmd = Roll(command)
    result = cmd.getResult()
    await message.channel.send('%s rolled %s:' % (message.author.display_name,command))
    for arr in result:
        flattened = [item for sublist in arr for item in sublist]
        await message.channel.send('%s: %s' % (flattened,sum(flattened)))

client.run('')