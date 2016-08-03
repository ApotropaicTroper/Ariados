import math
'''
Use the info for the mons.
Ideas for functions:
- Damage calc
- IV calc (incorporate multiple levels)
- Moveset calc
- Coverage calc
- Hidden Power calc (incorporate formula into IV calc?)

'''
stats_str = (' HP','Atk','Def','SpA','SpD','Spe')
types_dict = {-1:'???',0:'Normal',1:'Fighting',2:'Flying',3:'Poison',4:'Ground',
              5:'Rock',6:'Bug',7:'Ghost',8:'Steel',9:'Fire',10:'Water',11:'Grass',
              12:'Electric',13:'Psychic',14:'Ice',15:'Dragon',16:'Dark',17:'Fairy'}
inv_dict = {value:key for key,value in types_dict.iteritems()}
type_battle = (( 1 , 1 , 1 , 1 , 1 ,0.5, 1 , 0 ,0.5, 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ),
               ( 2 , 1 ,0.5,0.5, 1 , 2 ,0.5, 0 , 2 , 1 , 1 , 1 , 1 ,0.5, 2 , 1 , 2 ,0.5),
               ( 1 , 2 , 1 , 1 , 1 ,0.5, 2 , 1 ,0.5, 1 , 1 , 2 ,0.5, 1 , 1 , 1 , 1 , 1 ),
               ( 1 , 1 , 1 ,0.5,0.5,0.5, 1 ,0.5, 0 , 1 , 1 , 2 , 1 , 1 , 1 , 1 , 1 , 2 ),
               ( 1 , 1 , 0 , 2 , 1 , 2 ,0.5, 1 , 2 , 2 , 1 ,0.5, 2 , 1 , 1 , 1 , 1 , 1 ),
               ( 1 ,0.5, 2 , 1 ,0.5, 1 , 2 , 1 ,0.5, 2 , 1 , 1 , 1 , 1 , 2 , 1 , 1 , 1 ),
               ( 1 ,0.5,0.5,0.5, 1 , 1 , 1 ,0.5,0.5,0.5, 1 , 2 , 1 , 2 , 1 , 1 , 2 ,0.5),
               ( 0 , 1 , 1 , 1 , 1 , 1 , 1 , 2 , 1 , 1 , 1 , 1 , 1 , 2 , 1 , 1 ,0.5, 1 ),
               ( 1 , 1 , 1 , 1 , 1 , 2 , 1 , 1 ,0.5,0.5,0.5, 1 ,0.5, 1 , 2 , 1 , 1 , 2 ),
               ( 1 , 1 , 1 , 1 , 1 ,0.5, 2 , 1 , 2 ,0.5,0.5, 2 , 1 , 1 , 2 ,0.5, 1 , 1 ),
               ( 1 , 1 , 1 , 1 , 2 , 2 , 1 , 1 , 1 , 2 ,0.5,0.5, 1 , 1 , 1 ,0.5, 1 , 1 ),
               ( 1 , 1 ,0.5,0.5, 2 , 2 ,0.5, 1 ,0.5,0.5, 2 ,0.5, 1 , 1 , 1 ,0.5, 1 , 1 ),
               ( 1 , 1 , 2 , 1 , 0 , 1 , 1 , 1 , 1 , 1 , 2 ,0.5,0.5, 1 , 1 ,0.5, 1 , 1 ),
               ( 1 , 2 , 1 , 2 , 1 , 1 , 1 , 1 ,0.5, 1 , 1 , 1 , 1 ,0.5, 1 , 1 , 0 , 1 ),
               ( 1 , 1 , 2 , 1 , 2 , 1 , 1 , 1 ,0.5,0.5,0.5, 2 , 1 , 1 ,0.5, 2 , 1 , 1 ),
               ( 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ,0.5, 1 , 1 , 1 , 1 , 1 , 1 , 2 , 1 , 0 ),
               ( 1 ,0.5, 1 , 1 , 1 , 1 , 1 , 2 , 1 , 1 , 1 , 1 , 1 , 2 , 1 , 1 ,0.5,0.5),
               ( 1 , 2 , 1 ,0.5, 1 , 1 , 1 , 1 ,0.5,0.5, 1 , 1 , 1 , 1 , 1 , 2 , 2 , 1 ))
natures = (('Bashful','Lonely','Adamant','Naughty','Brave'  ),
           ('Bold'   ,'Docile','Impish' ,'Lax'    ,'Relaxed'),
           ('Modest' ,'Mild'  ,'Hardy'  ,'Rash'   ,'Quiet'  ),
           ('Calm'   ,'Gentle','Careful','Quirky' ,'Sassy'  ),
           ('Timid'  ,'Hasty' ,'Jolly'  ,'Naive'  ,'Serious'))
def formatNum(num,maxDigits):
    out = ''
    while len(str(num) + out) <= maxDigits:
        out += ' '
    return (out + str(num))#pad length at beginning with space until length equals maxDigits+1
class dexMon():
    species = ''
    base_stats = [5,5,5,5,5,5]  #1-255
    dext = ''
    form = ''
    weight = -1
    abilities = [] #possible abilities given form identifier
    types = []       #one or two types

    def __init__(self,species):
        self.species = species
        fr = open('Mons.txt','r')
        for line in fr:             #build string from file
            if species in line or species in self.dext:
                if '~~~~~~~~~~' not in line:
                    self.dext += line
                else:
                    break
        fr.close()
        count = 0
        found = -1
        for line in self.dext.split('\n')[1:]:
            count += 1
            if 'Forms:' in self.dext and found == -1 and self.form == '':#if multiple forms, ask which form
                for line2 in self.dext.split('\n')[1:]:
                    if 'Ability' not in line2 and ',' not in line2:
                        if species in line2 and ('Mega' in self.dext or 'Primal' in self.dext):# and count > 1:
                            print('-' + line2)
                        elif 'Mega' in line2 or 'Primal' in line2 or 'Forme' in line2 or 'Size' in line2:
                            print('-' + line2)
                        elif 'Form' in line2 and ':' not in line2 or 'Cloak' in line2 or 'Mode' in line2:
                            print('-' + line2)
                        elif ' Rotom' in line2 or ' Kyurem' in line2 or 'Hoopa ' in line2:
                            print('-' + line2)
                print('Which form?')
                self.form = 'Mega'
                print(' ' + self.form)
            elif self.form == '':
                found = 1
            if self.form in line and found == -1 and self.form != '' and 'Ability' not in line:
                found = count
                continue
        if found != -1:
            self.weight = self.dext.split('\n')[found+1]
            temp = self.dext.split('\n')[found+2].split(' / ')
            for item in temp:
                self.types.append(inv_dict[item])
            for index in range(6):
                self.base_stats[index] = int(self.dext.split('\n')[found+3+index])
            if len(self.types) == 1:
                self.types.append(-1)
        for string in self.dext.split('\n')[1].split(', '):
            self.abilities.append(string)
            if 'Hidden' in string:
                break
        if len(self.abilities) == 1:#sole ability, such as Rotom's Levitate
            pass
            #print('Only ability is ' + self.abilities[0])
        else:
            for string in self.abilities: # if form identifier in one of the abilities, must have ability
                if self.form in string and self.form != '' and self.form not in species:
                    #print('Ability must be ' + string)
                    self.abilities = [string]
                    break
        print(self.weight)
    def IV_calc(self):
        print('Which nature?')
        nature = 'Quirky'
        print(nature)
        boost = -1
        drop = -1
        for index in range(0,5):
            if nature in natures[index]:
                boost = index
                drop = natures[index].index(nature)
        IV_list = [range(0,32),range(0,32),range(0,32),range(0,32),range(0,32),range(0,32)]

        print('Hidden Power type? (optional)')
        HPtype = 'Fire'
        if HPtype in types_dict.values():
            HPtype = inv_dict[HPtype]-1
        else:
            HPtype = -1
        HPmod = [[],[],[],[],[],[]] #Odd or even? can it be both?
        for count in range(0,64):
            bi = bin(count)[2:]
            while len(bi) < 6:
                bi = '0' + bi
            num = math.floor(int(bi[4]+bi[3]+bi[5]+bi[2]+bi[1]+bi[0],2)*15.0/63)
            if num == HPtype:
                for index in range(0,6):
                    if bi[index] not in HPmod[index]:
                        HPmod[index].append(bi[index])
        for index in range(0,6):
            if len(HPmod[index]) == 2:
                continue
            newList = []
            if '0' in HPmod[index]:
                for IV in IV_list[index]:
                    if IV % 2 == 0:
                        newList.append(IV)
            if '1' in HPmod[index]:
                for IV in IV_list[index]:
                    if IV % 2 == 1:
                        newList.append(IV)
            IV_list[index] = newList
        while True:
            level = 50
            out = ''
            while level < 1 or level > 100:     #get level
                print('What level? 1-100')
                level = 100
                if level < 1 or level > 100:
                    print('Out of range! 1-100')
            #user proof max/min stats
            minStat = [int((2*self.base_stats[0])*level/100 + level + 10),
                       int(int((2*self.base_stats[1])*level/100 + 5)*0.9),
                       int(int((2*self.base_stats[2])*level/100 + 5)*0.9),
                       int(int((2*self.base_stats[3])*level/100 + 5)*0.9),
                       int(int((2*self.base_stats[4])*level/100 + 5)*0.9),
                       int(int((2*self.base_stats[5])*level/100 + 5)*0.9)]
            maxStat = [int((94.0 + 2*self.base_stats[0])*level/100 + level + 10),
                       int(int((94.0 + 2*self.base_stats[1])*level/100 + 5)*1.1),
                       int(int((94.0 + 2*self.base_stats[2])*level/100 + 5)*1.1),
                       int(int((94.0 + 2*self.base_stats[3])*level/100 + 5)*1.1),
                       int(int((94.0 + 2*self.base_stats[4])*level/100 + 5)*1.1),
                       int(int((94.0 + 2*self.base_stats[5])*level/100 + 5)*1.1)]
            while True:
                print('Stats?')             #get stats
                stats = [160,105,105,105,105,105]
                print(stats)
                for index in range(0,6):
                    if stats[index] < minStat[index]:
                        print(stats_str[index] + ' is too low! Min = ' + str(minStat[index]))
                        stats[index] = -1
                        break
                    if stats[index] > maxStat[index]:
                        print(stats_str[index] + ' is too high! Max = ' + str(maxStat[index]))
                        stats[index] = -1
                        break
                if -1 not in stats:
                    break
            print('EVs?')               #get EVs
            EVs = [0,0,0,0,0,0]
            print(EVs)
            out = 'At level ' + str(level) + ':\nStats:'
            for stat in stats:
                out += formatNum(stat,3)
            out += '\n  EVs:'
            for stat in EVs:
                out += formatNum(stat,3)
            newList = []
            for IV in IV_list[0]:
                guess = int((IV+2*self.base_stats[0]+EVs[0]/4.0)*level/100 + level + 10)
                if guess == stats[0]:
                    newList.append(IV)
                IV_list[0] = newList
            out += '\nPossible IV\'s:\n' + stats_str[0] + ': ' + str(IV_list[0])
            for index in range(1,6):
                newList = []
                for IV in IV_list[index]:
                    guess = math.floor((IV+2*self.base_stats[index]+EVs[index]/4.0)*level/100+5)
                    if boost != drop:
                        if index == boost:
                            guess *= 1.1
                        elif index == drop:
                            guess *= 0.9
                    guess = int(math.floor(guess))
                    if guess == stats[index]:
                        newList.append(IV)
                IV_list[index] = IV_list[index] and newList
                out += '\n' + stats_str[index] + ': ' + str(IV_list[index])
            break
        print(out)
#mon = dexMon('Celebi')
#mon.IV_calc()

#Stat modifiers:
# if accuracy or evasion
#  if stage > 1 then (3+stage)/3
#  if stage < 1 then 3/(3+stage)
# else
#  if stage > 1 then (2+stage)/2
#  if stage < 1 then 2/(2+stage)
#Damage:
# If secret sword, psyshock, or psystrike, then use SpA and Def.
# If physical, use Atk and Def. If special, use SpA and SpD.
# ((2*Lv + 10)/250 * Atk/Def * BasePower + 2) * Modifier
#  Modifier = STAB * Type * Critical * rand[0.85,1.00] * other
#   other depends on item, ability, field effects, number of targets
# reduced by 25% if multiple targets

class Mon(dexMon):
    stats = [1,1,1,1,1,1]
    IV = [0,0,0,0,0,0]    #0-31
    EV = [0,0,0,0,0,0]          #0-252
    nature = ' '          #boost one stat, drop another; or no change at all
    ability = ''                #one ability
    level = 50

    def __init__(self,species, innature = ' ', inability = ''):
        dexMon.__init__(self,species)
        for list in natures:        #natures
            if innature in list:
                self.nature = innature
        if self.nature == ' ':
            self.askNature()
        boost = 0; drop = -1
        for list in natures:
            boost += 1
            try:
                drop = list.index(self.nature) + 1
                break
            except:
                continue

        if 'Shedinja' in self.species:  #current stats
            self.stats[0] = 1
        else:
            self.stats[0] = int((self.IV[0] + 2*self.base_stats[0] + self.EV[0]/4.0)*self.level/100) + self.level + 10
        for index in range(1,6):
            self.stats[index] = int((self.IV[index] + 2*self.base_stats[index] + self.EV[index]/4.0)*self.level/100) + 5
            if boost != drop:
                if boost == index:
                    self.stats[index] = self.stats[index] * 1.1
                elif drop == index:
                    self.stats[index] = self.stats[index] * 0.9
            self.stats[index] = int(self.stats[index])

        if inability in self.abilities: #ability
            self.ability = inability
        else:
            self.askAbility()
    def getHPType(self):
        HPtype = bin(self.IV[4])[-1]+bin(self.IV[3])[-1]+bin(self.IV[5])[-1]
        HPtype += bin(self.IV[2])[-1]+bin(self.IV[1])[-1]+bin(self.IV[0])[-1]
        out = int(HPtype,2)*15/63 + 1
        return types_dict[out]
    def askAbility(self):
        if len(self.abilities) == 1:
            self.ability = self.abilities[0]
            print('You can only have ' + self.ability)
        else:
            for index in range(len(self.abilities)):
                print(str(index) + '. ' + self.abilities[index])
            print('Which ability?')
            self.ability = self.abilities[1]
            print(' ' + self.ability)
    def askIV(self):
        while True:
            for index in self.IV:
                self.IV[0] = 31 #int(input('HP IV?'))
            if max(self.IV) > 31 or min(self.IV) < 0:
                print('Something is out of range! 0-31')
            else:
                break
    def askEV(self):
        while True:
            for index in self.EV:
                self.EV[index] = 0 #int(input('HP EV?'))
            if max(self.EV) > 252 or min(self.EV) < 0:
                print('Something is out of range! 0-252')
            elif sum(self.EV) > 510:
                print('EV sum is out of range! At most 510 total')
            else:
                break
    def askLvl(self):
        while True:
            self.level = 50 #int(input('Level?'))
            if self.level > 100 or self.level < 1:
                print('That\'s out of range! Level must be 1-100')
                continue
            break
    def askNature(self):
        while True:
            try:
                print('Raise which stat?\n1.Atk\n2.Def\n3.SpA\n4.SpD\n5.Spe')
                boost = 3 #int(input('Raise which stat? 1.Atk\n2.Def\n3.SpA\n4.SpD\n5.Spe'))
                print('Lower which stat?\n1.Atk\n2.Def\n3.SpA\n4.SpD\n5.Spe')
                drop =  3 #int(input('Lower which stat? 1.Atk\n2.Def\n3.SpA\n4.SpD\n5.Spe'))
            except:
                print('That\'s not a number!')
                continue
            if boost < 0 or boost > 5:
                if 'y' in input('No change? y/n'):
                    self.nature = 'Quirky'
                else:
                    print('Then pick a stat!')
            self.nature = natures[boost][drop]
            break
    def toString(self):
        out = self.species + '\n' + types_dict[self.types[0]]
        if self.types[1] != -1:
            out += ' / ' + types_dict[self.types[1]] + '\nAbility: '+self.ability
        out += '\n' + self.weight + ' kg\nLv.'+str(self.level) + '\n' + self.nature+' nature'
        out += '\nCurrent stats:'
        for stat in self.stats:
            out += formatNum(stat,3)
        out += '\n   Base stats:'
        for stat in self.base_stats:
            out += formatNum(stat,3)
        out += '\n          IVs:'
        for stat in self.IV:
            out += formatNum(stat,3)
        out += '\n          EVs:'
        for stat in self.EV:
            out += formatNum(stat,3)
        return out
mon = Mon('Charizard')
print(mon.toString())
#print(mon.getHPType())



