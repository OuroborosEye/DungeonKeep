import random
import re

repetion_match = r'([0-9])(?![\s]*[\+]+)'
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

        self.dice = [Die(die) for die in re.split(r'[-\+]',command)]


    def getResult(self):
        results = []
        for _ in range(self.repetition):
            currResult = []
            for die in self.dice:
                currResult.append(die.rollDie())
            results.append(currResult)
        return results


class Die():
    def __init__(self,die):
        self.die = die
        if 'd' in self.die: 
            idx = self.die.index('d')
            self.num_times = int(self.die[:idx])
            self.die_type = int(self.die[idx+1:])
            self.isFixed = False
        else:
            self.num_times = 1
            self.die_type = 1
            self.isFixed = True

    def rollDie(self):
        if self.isFixed:
            return [int(self.die)]
        return [random.randint(1,self.die_type) for _ in range(self.num_times)]
    
