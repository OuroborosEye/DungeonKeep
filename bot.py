import discord
import random

client = discord.Client()
servers = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!roll '):
        await process_roll(message)
    elif message.content.startswith('!purge'):
        await purge_messages(message)

def is_bot_message(message):
    if message.author == client.user:
        return True
    if message.content.startswith('!roll '):
        return True
    if message.content.startswith('!purge'):
        return True
    return False

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
                await message.channel.send('Rolling %s: %s' % (command[1:], servers[message.guild.id][command[1:]])) 
        else:   
            [command,alias] = [seg.strip() for seg in command.split('#')]
            servers[message.guild.id][alias] = command
            await message.channel.send('Saved alias %s: %s' % (command,alias))

client.run('')