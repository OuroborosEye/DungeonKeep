import random
import re
from enum import Enum

repetion_match = r'[\s]*[0-9]+[\s]+(?![\+\-])'
setting_match = r'![\w\s]+'


class rollCommand():
    def __init__(self):
        self.guild_aliases = {}

    def runCommand(self, message):
        command = message.content.lower().replace('!roll ', '').strip()

        guild_id = message.guild.id

        if guild_id not in self.guild_aliases:
            self.guild_aliases[guild_id] = {}

        output = ''
        if '#' in command:
            if command.startswith('#'):
                output += 'Jogando Apelido %s (%s)\n' % (command[1:], self.guild_aliases[guild_id][command[1:]])
                command = self.guild_aliases[guild_id][command[1:]]
            else:
                alias = command[command.index('#')+1:]
                command = command[:command.index('#')]
                self.guild_aliases[guild_id][alias] = command
                output += 'Apelido Salvo %s\n' % alias

        output += '%s Jogou %s\n e o Resutado foi:' % (message.author.display_name, command)
        roll = Roll(command)
        output += roll.printResult()
        return output
        output += roll.printResult()
        return output


class Roll():
    def __init__(self, command):
        self.repetition = 1
        self.verbosity = Verbosity.Normal
        command = command.lower()

        match = re.match(repetion_match, command)
        if match:
            self.repetition = int(match.group())
            command = command.replace(match.group(), '', 1)

        for m in re.findall(setting_match, command):
            command = command.replace(m, '', 1)
            if m in ['!verbose', '!v']:
                self.verbosity = Verbosity.Verbose
            elif m in ['!quiet', '!q']:
                self.verbosity = Verbosity.Quiet

        command = command.replace(' ', '')

        self.throw = command
        self.dice = [Die(die) for die in re.split(r'[-\+]', command) if 'd' in die]

    def getResult(self):
        return [[die.rollDie() for die in self.dice] for _ in range(self.repetition)]

    def printResult(self):
        output = ''
        for throw in self.getResult():
            flat_list = []
            format_throw = self.throw
            for dieResult in throw:
                flat_list.append(dieResult.output)
                format_throw = format_throw.replace(dieResult.throw, str(sum(dieResult.output)), 1)

            if self.verbosity == Verbosity.Verbose:
                output += '`%s` %s  **Result: %i**\n' % (str(flat_list)[1:-1].replace(', [', '['), format_throw, eval(format_throw))
            elif self.verbosity == Verbosity.Quiet:
                output += '**Result: %i**\n' % (eval(format_throw))
            else:
                output += '%s  **Result: %i**\n' % (format_throw, eval(format_throw))
        return output


class Verbosity(Enum):
    Verbose = 1
    Normal = 2
    Quiet = 3


class RollResult():
    def __init__(self):
        self.throw = ''
        self.output = []


class Die():
    def __init__(self, die):
        self.die = die
        idx = self.die.index('d')
        self.num_times = int(self.die[:idx]) if idx > 0 else 1
        self.faces = int(self.die[idx+1:])

    def rollDie(self):
        result = RollResult()
        result.throw = self.die
        result.output = [random.randint(1, self.faces) for _ in range(self.num_times)]
        return result
