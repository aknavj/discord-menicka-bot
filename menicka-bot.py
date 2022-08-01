# Simple test of discord lunch bot using menicka.cz as source feed

from lxml import html
import requests
import pprint
import datetime

import os
import discord
from dotenv import load_dotenv

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
def lunchMenus(restaurant_list, weekday):

    if restaurant_list is None:
        return "No restaurants present!"

    buf = []
    d = weekday

    rIt = 0
    restaurants = [*restaurant_list]
    for res in restaurant_list.values():
        dl, sl, mdl, pl = populateRestaurant(res)
        if dl is not None:
            buf.append(restaurants[rIt])
            rIt = rIt + 1

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

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    pass

@client.event
async def on_message(message):
    if message.content == 'restaurants!':
        header = [*restaurant_list]
        for r in header:
            await message.channel.send(r)

    if message.content == 'lunch!':
        weekday = datetime.datetime.today().weekday()
        response = lunchMenus(restaurant_list, weekday)
        for r in response:
            await message.channel.send(r)

client.run(TOKEN)

#if __name__ == '__main__':    
#    pp.pprint(buf)          