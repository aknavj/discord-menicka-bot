# Simple test of discord lunch bot using menicka.cz as source feed

from lxml import html
import requests
import pprint
import datetime

import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

BOT_VERSION = 'v1.1'
BOT_REPOSITORY = 'https://github.com/aknavj/discord-menicka-bot'

SOURCE_URL = 'https://www.menicka.cz/tisk.php?'
pp = pprint.PrettyPrinter(indent=4)

#populate it by favorites
restaurant_list = {
    'Pizzerie u Tomase' : 5899,
    'Slezska krcma' : 5854,
    'Pochutnej si! Bistro' : 7792,
}

# parse html output
def populateRestaurant(id_restaurace):
    params = { 'restaurace' : id_restaurace }
    page = requests.post(SOURCE_URL, params=params)
    page.encoding = 'utf-8'

    days_list = []
    soup_list = []
    maindish_list = []
    prices_list = []
    if page is not None:
        data = html.fromstring(page.content)
        for t in data.xpath('//div[@class="content"]'):
            
            day = t.xpath('.//h2/text()')
            days_list.append(day)

            soup = t.xpath('.//tr[@class="soup"]//td[@class="food"]/text()')
            soup_list.append(soup)

            maindish = t.xpath('.//tr[@class="main"]//td[@class="food"]/text()')
            maindish_list.append(maindish)

            prices = t.xpath('.//td[@class="prize"]/text()')
            prices_list.append(prices)
        
        return days_list, soup_list, maindish_list, prices_list
    return None

# populate buffer with lunch information
def restaurantLunchMenu(restaurant, name, weekday):
    buf = []
    d = weekday
    dl, sl, mdl, pl = populateRestaurant(restaurant)
    if dl is not None:
        buf.append(name)
        buf.append(dl[d])
            
        # printout soups
        it = 1
        buf.append("Polevky.... {0}".format(len(sl[d])))
        for soup in sl[d]:
            buf.append("    {0}. {1}".format(it, soup))
            it = it + 1
                
        buf.append("Hlavni jidlo... {0}".format(len(mdl[d])))
        it = 1
        for meal in mdl[d]:
            buf.append("    {0}. {1}".format(it, meal))
            it = it + 1
    else:
        buf.append("Restaurace nema zadane menu!")

    return buf
 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    pass

@bot.command(name='version', help='sources & bot version')
async def get_version(ctx):
    await ctx.send("version: {0}\nsource: {1}\nrepo: {2}\n". format(BOT_VERSION, SOURCE_URL, BOT_REPOSITORY))

@bot.command(name='dice', help='Your lunch destiny is fullfiled by me!')
async def dice_lunch(ctx):
    buf = ""

    # pick random restaurant

    # pick random meal from restaurant

    await ctx.send('Dnes si das.... {0}, {1}'.format(buf, 0))

@bot.command(name='restaurant', help='List our favorite restaurants in Trinec!')
async def get_restaurant(ctx):
    msg = [*restaurant_list]

    buf = ""
    for item in msg:
        buf += item + ", "

    await ctx.send(buf)

@bot.command(name='lunch', help='Where to?')
async def get_lunch(ctx):
    weekday = datetime.datetime.today().weekday()

    rIt = 0
    restaurants = [*restaurant_list]
    for res in restaurant_list.values():
        data = restaurantLunchMenu(res, restaurants[rIt], weekday)
        rIt = rIt + 1

        msg = ""
        for d in data:
            msg += str('{0}\n'.format(d))

        await ctx.send(msg)

bot.run(TOKEN)