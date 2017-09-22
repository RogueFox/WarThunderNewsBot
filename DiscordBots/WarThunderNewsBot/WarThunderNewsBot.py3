import discord
from discord.ext import commands
from lxml import html
import requests
import asyncio

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

async def backgroundCheckNews():
    await client.wait_until_ready()
    while(not client.is_closed):
        await asyncio.sleep(3600)
        await postNewsBackground()

@client.event
async def on_ready():
    client.move_member(client,"war_thunder_news")
    await postNewsBackground()
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")

@client.command()
async def shutdown():
    await client.say("Disconnecting...")
    await client.close()

@client.command()
async def test():
    await client.say("Connected!")

@client.command()
async def postNews():
    await postNewsBackground()

async def postNewsBackground():
    id = '356111716792139787' #bots
    #id = '352496881454153729' #war-thunder-news
    await client.send_message(discord.Object(id),("Obtaining latest news from War Thunder..."))
    page = requests.get('https://warthunder.com/en/news')
    tree = html.fromstring(page.content)

    articleNames = tree.xpath('//div[contains(@class, "news-item__anons")]/a[@href]')

    webLinks = []
    for href in articleNames:
        webLinks.append(href.attrib['href'])
    print(webLinks)

    try:
        postedArticles = open('posted_articles.txt', 'r+')
    except FileNotFoundError:
        postedArticles = open('posted_articles.txt', 'w')
        postedArticles.close()
        postedArticles = open('posted_articles.txt', 'r+')
    linkList = postedArticles.read().splitlines()
    print(linkList)

    postedList = []

    madeAPost = False
    for link in webLinks:
        doNotPrint = False
        for post in linkList:
            if (link == post):
                doNotPrint = True
                break
        if (not doNotPrint):
            # post code here
            madeAPost = True
            print("https://warthunder.com" + link)
            await client.send_message(discord.Object(id),("https://warthunder.com" + link))
            # add to posted list
            postedList.append(link)

    if(not madeAPost):
        await client.send_message(discord.Object(id),"No new posts.")

    toBeSaved = ""

    for link in postedList:
        toBeSaved += (link + "\n")

    postedArticles.write(postedArticles.read() + toBeSaved)
    postedArticles.close()

input("Press ENTER to start...")
client.loop.create_task(backgroundCheckNews())
client.run("MzUyOTI5NTg0MzY4NDUxNTg1.DJCCSg.E3JTWtKNCSsIZldR229KY5IIN2M")
input("Press ENTER to exit...")