import random
import re

repetion_match = r'([0-9])(?![\s]*[\+]+)'
class rollCommand():
    def __init__(self):
        self.guild_aliases = {}

    def runCommand(self,message):
        command = message.content.lower().replace('!roll ', '').strip()
        
        guild_id = message.guild.id
    
        if guild_id not in self.guild_aliases:
            self.guild_aliases[guild_id] = {} 
        
        output = ''
        if '#' in command:
            if command.startswith('#'):
                command = self.guild_aliases[guild_id][command[1:]]
                output += 'Throwing alias %s (%s)\n' % ([command[1:]],command)
            else:
                alias = command[command.indexOf('#'):]
                self.guild_aliases[guild_id][alias]
                output += 'Saved Alias %s\n' % alias
        
        roll = Roll(command)
        output += roll.printResult()
        return output


class Roll():
    def __init__(self, command):
        self.repetition = 1
        command = command.lower()
        
        match = re.match(repetion_match,command)
        if match:
            print(match.group())
            self.repetition = int(match.group())
            command = command.replace(match.group(),'',1)        
        
        command = command.replace(' ','')

        self.throw = command
        self.dice = [Die(die) for die in re.split(r'[-\+]',command)]

    def getResult(self):
        return [ [ die.rollDie() for die in self.dice ] for _ in range(self.repetition)]

    def printResult(self):
        output = 'X threw %i %s\n' % (self.repetition,self.throw)
        for throw in self.getResult():
            flat_list = []
            format_throw = self.throw
            for dieResult in throw:
                flat_list.extend(dieResult.output)
                format_throw = format_throw.replace(dieResult.throw,str(sum(dieResult.output)),1)
            output += '%s %s: %i\n' % (flat_list,format_throw,eval(format_throw))
        return output

class RollResult():
    def __init__(self):
        self.throw = ''
        self.output = []

class Die():
    def __init__(self,die):
        self.die = die
        if self.die.isnumeric():
            self.isFixed = True
        else:
            idx = self.die.index('d')
            self.num_times = int(self.die[:idx])
            self.faces = int(self.die[idx+1:])
            self.isFixed = False

    def rollDie(self):
        result = RollResult()
        result.throw = self.die
        result.output = [int(self.die)] if self.isFixed else [random.randint(1,self.faces) for _ in range(self.num_times)]
        return result
    
