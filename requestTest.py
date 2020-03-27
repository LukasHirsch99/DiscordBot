import requests
from lxml import html
import lxml

source = requests.get("https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html").text
tree = lxml.html.fromstring(source)
cases = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[3]')[0].text_content()
deaths = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[4]')[0].text_content()

allInfo1 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[2]')[0].text_content()
allInfo2 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[3]')[0].text_content()
allInfo3 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[4]')[0].text_content()
allInfo4 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[5]')[0].text_content()
allInfo5 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[6]')[0].text_content()
allInfo = f'{allInfo1}\n{allInfo2}\n{allInfo3}\n{allInfo4}\n{allInfo5}'

cases = cases.split(', nach Bundesländern: ')
allCases = cases[0]
stateCases = cases[1]
stateCases = stateCases.split(', ')
stateCaseDict = {}

deaths = deaths.split(', nach Bundesländern: ')
allDeaths = deaths[0]
stateDeaths = deaths[1]
stateDeaths = stateDeaths.replace('\xa0', ' ')
stateDeaths = stateDeaths.split(', ')
stateDeathDict = {}



for i in range(len(stateCases)):
    stateCaseDict[i] = stateCases[i].split(' ')
for stateCase in stateCases:
    stateCaseDict[stateCase[0]] = stateCase[1][1:-1]

for i in range(len(stateDeaths)):
    stateDeaths[i] = stateDeaths[i].split(' ')
for stateDeath in stateDeaths:
    stateDeathDict[stateDeath[0]] = stateDeath[1][1:-1]

print (stateDeathDict)