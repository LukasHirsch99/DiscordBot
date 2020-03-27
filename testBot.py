import discord
from discord.ext import commands, tasks

import requests
from lxml import html
import lxml

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

class news():
    def __init__(self):
        self.allInfo = ''
        self.stateCaseDict = {}
        self.stateDeathDict = {}

    def getCurInfo(self):
        source = requests.get("https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html").text
        tree = lxml.html.fromstring(source)
        allInfo1 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[2]')[0].text_content()
        allInfo2 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[3]')[0].text_content()
        allInfo3 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[4]')[0].text_content()
        allInfo4 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[5]')[0].text_content()
        allInfo5 = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[6]')[0].text_content()
        self.allInfo = f'{allInfo1}\n{allInfo2}\n{allInfo3}\n{allInfo4}\n{allInfo5}'

        cases = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[3]')[0].text_content()
        deaths = tree.xpath('/html/body/div[3]/div/div/div/div[2]/main/p[4]')[0].text_content()

        cases = cases.split(', nach Bundesländern: ')
        self.allCases = cases[0]
        stateCases = cases[1]
        stateCases = stateCases.replace('\xa0', ' ')
        stateCases = stateCases.split(', ')
        self.stateCaseDict = {}

        deaths = deaths.split(', nach Bundesländern: ')
        self.allDeaths = deaths[0]
        stateDeaths = deaths[1]
        stateDeaths = stateDeaths.replace('\xa0', ' ')
        stateDeaths = stateDeaths.split(', ')
        self.stateDeathDict = {}

        for i in range(len(stateCases)):
            stateCases[i] = stateCases[i].split(' ')
        for stateCase in stateCases:
            self.stateCaseDict[stateCase[0]] = stateCase[1][1:stateCase[1].index(')')]

        for i in range(len(stateDeaths)):
            stateDeaths[i] = stateDeaths[i].split(' ')
        for stateDeath in stateDeaths:
            self.stateDeathDict[stateDeath[0]] = stateDeath[1][1:stateDeath[1].index(')')]

lastInfo = news()
channelIds = []

@tasks.loop(hours = 1)
async def update():
    global lastInfo, channelIds
    currNews = news()
    currNews.getCurInfo()

    if currNews.allInfo == lastInfo.allInfo:
        return

    lastInfo.allInfo = currNews.allInfo
    for channel in channelIds:
        await channel.send(currNews.allInfo)
        print(f"Update done for channel: '{channel.name}'")


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.event
async def on_ready():
    update.start()
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = '.help'))
    print("Bot is ready")


@client.command()
async def info(ctx, args1, args2):
    currNews = news()
    currNews.getCurInfo()
    print("getting Info")
    if args1 == 'all' and args2 == 'all':
        await ctx.send(currNews.allInfo)
    elif args1 == 'tote':
        if args2 == 'all':
            for key,val in currNews.stateDeathDict.items():
                await ctx.send(f'{key}: {val}')
        else:
            await ctx.send(currNews.stateDeathDict[args2])
    elif args1 == 'fälle':
        if args2 == 'all':
            for key,val in currNews.stateCaseDict.items():
                await ctx.send(f'{key}: {val}')
        else:
            await ctx.send(currNews.stateCaseDict[args2])
    else:
        await ctx.send('Wrong Syntax')

@client.command()
async def testChannels(ctx):
    global channelIds
    for channel in channelIds:
        await channel.send(channel.name)
        print(f"Update done for channel: '{channel.name}'")

@client.command()
async def stop(ctx):
    await ctx.send("Bot is going to sleep")
    print("Bot shuttingdown")
    await client.close()

@client.command()
async def addChannel(ctx):
    global channelIds
    currNews = news()
    currNews.getCurInfo()
    channel = client.get_channel(ctx.channel.id)
    if channel not in channelIds:
        channelIds.append(channel)
        print(f"added channel: '{ctx.channel.name}' to update list")
        await ctx.send(currNews.allInfo)
    else:
        print(f"channel '{channel.name}' already added")
        await ctx.send("Channel already added")

@client.command()
async def removeChannel(ctx):
    global channelIds
    if client.get_channel(ctx.channel.id) in channelIds:
        channelIds.remove(client.get_channel(ctx.channel.id))
        await ctx.send('Removed your Channel')
        print(f"removed channel '{ctx.channel.name}' from update list")
    else:
        await ctx.send('Channel is not added')


@client.command(pass_context = True)
async def help(ctx):
    await ctx.send('.ping: returns ping from bot to server\n.info + (all/tote/fälle) + (all/eg. Burgenland): get current corona news\n.addChannel: add current channel to frequently cornona updates\n.removeChannel: reomovs channel from updates\n.help: shows this')
    
client.run("NjkwNjgwODgzMDUyODA2MjA1.XnU8uA.qL3SlcWQ5iixjVYVncVfPJRtHkw")