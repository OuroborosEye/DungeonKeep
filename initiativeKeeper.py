
class initiativeKeeper():
    def __init__(self):
        self.guild_initiatives = {}
        self.init_index = 0

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
        elif command.startswith('next'):
            return self.nextInitiative(guild_id)
        else:
            return 'Invalid command'

    def addInitiative(self,guild_id,command):
        try:
            char,init = command.split(' ')
            self.guild_initiatives[guild_id][char] = init
            self.init_index = 0
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
    
    def nextInitiative(self,guild_id):
        output = 'Next turn is for: %s' % (sorted(self.guild_initiatives[guild_id].items(), reverse=True, key=lambda x: int(x[1]))[self.init_index][0])
        self.init_index += 1
        if self.init_index == len(self.guild_initiatives[guild_id]):
            self.init_index = 0
        return output