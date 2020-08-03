
class initiativeKeeper():
    def __init__(self):
        self.guild_initiatives = {}   

    def runCommand(self, message):
        command = message.content.lower().replace('!init ', '')

        guild_id = message.guild.id
<<<<<<< HEAD

        if guild_id not in self.guild_initiatives:
            self.guild_initiatives[guild_id] = {'Initiatives': {}, 'Init_Index': -1}
=======
    
        if guild_id not in self.guild_initiatives:
            self.guild_initiatives[guild_id] = {'Initiatives':{}, 'Init_Index':-1} 
>>>>>>> master
        if command.startswith('clear'):
            return self.clearInitiatives(guild_id)
        elif command.startswith('show'):
            return self.printInitiatives(guild_id, message.guild.name)
        elif command.startswith('add'):
<<<<<<< HEAD
            return self.addInitiative(guild_id, command.replace('add ', ''))
=======
            return self.addInitiative(guild_id, command.replace('add ',''))
>>>>>>> master
        elif command.startswith('next'):
            return self.nextInitiative(guild_id)
        else:
            return 'Invalid command'

    def addInitiative(self, guild_id, command):
        try:
<<<<<<< HEAD
            char, init = command.split(' ')
=======
            char,init = command.split(' ')
>>>>>>> master
            self.guild_initiatives[guild_id]['Initiatives'][char] = init
            self.guild_initiatives[guild_id]['Init_Index'] = 0
            return 'Initiative Added'
        except:
            return 'Invalid initiatives to add'

    def clearInitiatives(self, guild_id):
        self.guild_initiatives[guild_id] = {'Initiatives': {}, 'Init_Index': -1}
        return 'Initiatives cleared'

    def printInitiatives(self, guild_id, guild_name):
        if len(self.guild_initiatives[guild_id]['Initiatives']) == 0:
            return 'No initiatives saved'

        output = '```Initiatives for %s\n' % guild_name
        for row in sorted(self.guild_initiatives[guild_id]['Initiatives'].items(), reverse=True, key=lambda k: int(k[1])):
            output += '%s: %s\n' % (row[0], row[1])
        output += '```'
        return output

    def nextInitiative(self, guild_id):
        idx = self.guild_initiatives[guild_id]['Init_Index']
        if len(self.guild_initiatives[guild_id]['Initiatives']) == 0:
            return 'No initiatives saved'
        output = '```Next turn is for: %s```' % (sorted(self.guild_initiatives[guild_id]['Initiatives'].items(), reverse=True, key=lambda k: int(k[1]))[idx][0])
        idx += 1
        if idx == len(self.guild_initiatives[guild_id]['Initiatives']):
            idx = 0
        self.guild_initiatives[guild_id]['Init_Index'] = idx
        return output
