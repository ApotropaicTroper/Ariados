# -*- coding: UTF-8 -*-
import sys
import requests
import urllib
from bs4 import BeautifulSoup
import codecs
'''
Idea: web spider to scan bulbapedia to get data on all 721 pokemon
HP: FF5959
Atk:F5AC78
Def:FAE078
SpA:9DB7F5
SpD:A7DB8D
Spe:FA92B2
BST:    varies (primary type, sum of all other base stats)
'''
stats_str = (' HP','Atk','Def','SpA','SpD','Spe')
def formatNum(num,maxDigits):
    out = ''
    while len(str(num) + out) <= maxDigits:
        out += ' '
    return (out + str(num))#pad length at beginning with space until length equals maxDigits+1

PIthon = 'C:\\Users\\Jethro\\Desktop\\PIthon\\'
pedia = 'http://bulbapedia.bulbagarden.net'

# ~~~~~~~~~~ Type (s), Abilities, & Weight ~~~~~~~~~~
def get_types(td):
    out = ['','']
    path = td.find('tr').findAll('td')
    out[0] = str(path[0].span.string)
    if 'display: none' in str(path[1].get('style')):
        out[1] = '???'
    else:
        out[1] = str(path[1].span.string)
    return out

def get_stats(table,spec,form):
    tr = table.findAll('tr',recursive = False)
    types = ['','']
    abilities = ['','','',]
    weight = -1
    if len(tr) == 13: #Multiple abilities/typesets/forms, or ordinary
        #~~~~~~~~~~ Types ~~~~~~~~~~
        path = tr[1].find('table').findAll('tr',recursive=False)
        types_td = path[0].findAll('td',recursive = False)
        if len(path) > 1:
            types_td.extend(path[1].findAll('td',recursive = False))
        index = 0
        while index < len(types_td):
            if 'display: none;' in str(types_td[index].get('style')):
                types_td.remove(types_td[index])
                continue
            index += 1
        for td in types_td:
            if form == spec or len(types_td) == 1:
                types = get_types(td)
                break
            else:
                type_small = str(td.small.string)
                if form in type_small or type_small in form:
                    types = get_types(td)
                if '  ' in type_small:
                    type_small = type_small.replace('  ',' ')
                if form in str(type_small):
                    types = get_types(td)
        #~~~~~~~~~~ Abilities ~~~~~~~~~~
        path = tr[2].find('table').findAll('tr')
        ables_td = path[0].findAll('td',recursive = False)
        if len(path) > 1:
            ables_td.extend(path[1].findAll('td'))
        index = 0
        while index < len(ables_td):
            if 'display:none;' in str(ables_td[index].get('style')):
                ables_td.remove(ables_td[index])
                continue
            index += 1
        for td in ables_td:
            if form == spec:
                if abilities[0] == '':
                    abilities[0] = str(td.span.string)
                    if len(td.findAll('a')) > 1:
                        abilities[1] = str(td.findAll('a')[1].span.string)
            else:
                try:
                    if form in str(td.small.string) or str(td.small.string) in form:
                        abilities[0] = str(td.span.string)
                except AttributeError:
                    abilities[0] = str(td.span.string)
            if 'Hidden' in str(td.small) and 'Mega' not in form:
                    abilities[2] = str(td.span.string)
        #~~~~~~~~~~ Weights ~~~~~~~~~~
        if form == spec:
            weight = tr[5].findAll('td',recursive=False)[1].find('table').find('tr').findAll('td')[1].string
        else:
            weights_tr = tr[5].findAll('td',recursive=False)[1].find('table').findAll('tr',recursive=False)
            while 'display:none' in str(weights_tr[-1].get('style')):
                weights_tr.remove(weights_tr[-1])
            if len(weights_tr) == 1:
                weight = weights_tr[0].findAll('td')[1].string
            for index in range(0,len(weights_tr)/2):
                weightID = str(weights_tr[index*2+1].td.small.string)
                if form.split(' ')[0] in weightID or form.split(' ')[1] in weightID:
                    weight = weights_tr[index*2].findAll('td')[1].string
                    break                
    else: #Only one form/typeset/ability
        path = tr[1].findAll('td',recursive=False)
        types = get_types(path[0].find('table').find('tr').find('td'))
        abilities[0] = str(path[1].find('tr').find('td').span.string)
        weight = tr[4].findAll('td',recursive=False)[1].find('table').find('tr').findAll('td')[1].string
    weight = str(weight.split(' ')[1])

    return [types,abilities,weight]

def mon_spider(first = 'Bulbasaur',num = 1):
    url = 'http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VI-present)'
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    start = False
    startNum = -1

    if first == 'Nidoran(F)':
        first = u'\u2640'
    elif first == 'Nidoran(M)':
        first = u'\u2642'
    elif first == 'Flabebe':
        first = u'\u00e9'
    
    for tr in soup.findAll('tr',{'style':'background:#FFFFFF'}):
    #~~~~~~~~~~ Beginning/Ending logic ~~~~~~~~~~
        if not start:
            if first not in str(tr):
                continue
            else:
                startNum = tr.find('td',{'align':'right'}).b.string[0:3]
                start = True
        dexNum = tr.find('td',{'align':'right'}).b.string[0:3]
        if int(dexNum) - int(startNum) >= num:
            break
    #~~~~~~~~~~ Set up variables ~~~~~~~~~~
        out = ''
        ID = tr.find('td',{'align':'left'})
        spec = ID.a.string
        if '<small>' in str(ID):
            form = str(ID.small.string[1:-1])
        else:
            form = spec
        if spec == 'Castform':
            form = 'Normal'
    # ~~~~~~~~~~ Data not provided on main page ~~~~~~~~~~
        nurl = pedia + ID.a.get('href')
        subsoup = BeautifulSoup(requests.get(nurl).text,'lxml')
        table = subsoup.find('table',{'class':'roundy'})
        misc = get_stats(table,spec,form)
        print(dexNum + ' ' + form)
    #~~~~~~~~~~ Download icons, initiate file writer ~~~~~~~~~~
        fw = -1
        imgSRC = str(tr.findAll('td')[1].a.img.get('src'))
        if form == spec:
            urllib.urlretrieve(imgSRC, PIthon + 'Icons\\' + spec + '.png')
            fw = codecs.open(PIthon + 'Mons\\' + dexNum + ' ' + spec + '.txt','w','utf-8')
        else:
            urllib.urlretrieve(imgSRC, PIthon + 'Icons\\' + spec + ' (' + form + ')' + '.png')
            fw = codecs.open(PIthon + 'Mons\\' + dexNum + ' ' + spec + ' (' + form + ')' + '.txt','w','utf-8')
    #~~~~~~~~~~ Statistics ~~~~~~~~~~
        stats = []
        for index in range(0,6):
            stats.append(str(tr.findAll('td')[index+3].string[1:-1]))
        #~~~~~~~~~~ Write stuff ~~~~~~~~~~
        if spec not in form:
            fw.write(spec + '\n')
        fw.write(form + '\n')
        #~ Types
        fw.write(misc[0][0])
        if misc[0][1] != '???':
            fw.write(' / ' + misc[0][1] + '\n')
        #~ Abilities
        fw.write(misc[1][0])
        for item in misc[1][1:]:
            if str(item) != '':
                fw.write(', ' + str(item))
        fw.write('\n')
        #~ Stats
        for index in range(0,6):
            fw.write(formatNum(stats[index],2) + '\n')
        fw.write(formatNum(misc[2],4) + ' kg')
        fw.close()

#mon_spider(num = 721) #721 mons






#problem: 'All pokemon' sections
def learnlist(soup,name):
    if name == 'Struggle':
        return ['-1']
    if 'event-exclusive' in str(soup):
        return ['Event move']
    learn_tr = []
    learnset = set()
    #~~~~~~~~~~ Some moves can be learned by almost all mons ~~~~~~~~~~
    if 'mon who can learn' in str(soup):
        table = soup.findAll('table',{'width':'500px'})[-1]
        if '--' not in str(table.findAll('tr')[1].findAll('th')[-1].small.string):
            learnset.add('-1')
            for a in table.findAll('tr')[2].findAll('a'):
                learnset.add(str(a.string))
            return learnset
    learn_tr = soup.findAll('tr',{'style':'background:#fff; text-align:center'})
    learn_tr.extend(soup.findAll('tr',{'style':'background:#fff'}))
    for tr in learn_tr:
        if 'href' not in str(tr):
            continue
        td = tr.findAll('td',recursive=False)
        th = tr.findAll('th',recursive=False)
        if len(td) != 0 and 'FFFFFF' not in td[-1].get('style'):
            learnset.add(td[2].a.string)
        elif len(th) != 0 and 'FFFFFF' not in th[-1].get('style'):
            learnset.add(td[2].a.string)
    #~~~~~~~~~~ Smeargle can learn any move except Chatter (via Sketch) ~~~~~~~~~~
    if 'Smeargle' not in learnset: 
        if name != 'Chatter' and '-1' not in learnset:
            learnset.add(u'Smeargle') 
    return learnset


def move_spider(first = 'Pound',num = 1):
    url = 'http://bulbapedia.bulbagarden.net/wiki/List_of_moves'
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    start = False
    startNum = -1
    for tr in soup.findAll('table',{'border':'1'})[0].findAll('tr')[1:]:
        #~~~~~~~~~~ Beginning/Ending logic ~~~~~~~~~~
        if not start:
            if first not in str(tr.findAll('td')[1]):
                continue
            else:
                startNum = int(tr.td.string)
                start = True
        dexNum = int(tr.td.string)
        if dexNum - startNum >= num:
            break
        #~~~~~~~~~~ All stats except learnsets ~~~~~~~~~~
        move_td = tr.findAll('td')
        name = move_td[1].a.string
        typ = move_td[2].a.string
        cat = move_td[3].a.string
        PP = -1; acc = -1; power = -1
        if '\"' in str(move_td[5]):
            for string in move_td[5].strings:
                PP = string.strip()
                break
        else:
            PP = move_td[5].string.strip()
        if '\"' in str(move_td[6]):
            for string in move_td[6].strings:
                power = string.strip()
                break
        else:
            power = move_td[6].string.strip()
        if '\"' in str(move_td[7]):
            for string in move_td[7].strings:
                acc = string.strip()
                break
        else:
            acc = move_td[7].string.strip()
        print(name)
        #~~~~~~~~~~ Learnset ~~~~~~~~~~
        nurl = pedia + move_td[1].a.get('href')
        subsoup = BeautifulSoup(requests.get(nurl).text,'lxml')
        learnset = learnlist(subsoup,name)
        #~~~~~~~~~~ Write stuff ~~~~~~~~~~
        fw = codecs.open(PIthon + 'Moves\\' + name + '.txt','w','utf-8')
        fw.write(name+'\n' + typ+' / '+cat+'\n' + power+'\n' + acc+'\n' + PP+' PP'+'\n')
        if '-1' in learnset:
            fw.write('All except:\n')
        for mon in learnset:
            if mon != '-1':
                fw.write(mon + '\n')
        fw.close()
move_spider(num = 621)#621 moves