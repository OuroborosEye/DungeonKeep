
class initiativeKeeper():
    def __init__(self):
        self.guild_initiatives = {}

    def runCommand(self,message):
        command = message.content.lower().replace('!init ', '')
        
        guild_id = message.guild.id
    
        if guild_id not in self.guild_initiatives:
            self.guild_initiatives[guild_id] = {} 

        if command.startswith('clear'):
            return  self.clearInitiatives(guild_id)
        elif command.startswith('show'):
            return self.printInitiatives(guild_id,message.guild.name)
        elif command.startswith('add'):
            return self.addInitiative(guild_id, command.replace('add ',''))
        else:
            return 'Invalid command'

    def addInitiative(self,guild_id,command):
        try:
            char,init = command.split(' ')
            self.guild_initiatives[guild_id][char] = init
            return 'Initiative Added'
        except:
            return 'Invalid initiatives to add'

    def clearInitiatives(self,guild_id):
        self.guild_initiatives[guild_id] = {}
        return 'Initiatives cleared'

    def printInitiatives(self,guild_id,guild_name):
        if len(self.guild_initiatives[guild_id]) == 0:
            return 'No initiatives saved'

        output = '```Initiatives for %s\n' % guild_name
        for row in sorted(self.guild_initiatives[guild_id].items(),key=lambda k:k[1],reverse=True):
            output += '%s: %s\n' % (row[0],row[1])
        output += '```'
        return output