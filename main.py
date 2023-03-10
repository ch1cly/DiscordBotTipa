local = True #change if not on False

if not local:
    import os
    from dotenv import load_dotenv
    load_dotenv()
# This example requires the 'message_content' intent.

import discord
from bs4 import BeautifulSoup
import requests
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def anekdot(message):

    def formString(var):
        svar = ''
        if var > 0 and var < 10:
            svar = '0'+str(var)
        else:
            svar = str(var)
        return svar

    def parse(page):
        try:
            if page.status_code != 200:
                raise Exception("Can not reach site")
            soup = BeautifulSoup(page.text, "html.parser")
            allNews = soup.findAll('div', class_='anekdot')
            anek = allNews[number].text
        except:
            if year < 2006:
                anek = 'За данный год нет анекдотов'
            elif month < 0 or month > 12:
                anek = 'Неверный месяц'
            elif number < 0 or number > 14:
                anek = 'Нет анекдота по данному индексу'
            else:
                anek = 'none'
        return anek
    if len(message.content.split(' ')) != 4:
        return 'Неверный запрос!'
    number = int(message.content.split(' ')[3])
    year = int(message.content.split(' ')[1])
    month = int(message.content.split(' ')[2])
    syear = str(year)
    smonth = formString(month)

    url = 'http://anekdotov.net/anekdot/month/{}-{}.html'.format(syear,smonth)
    page = requests.get(url)
    anek = parse(page)

    return anek


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!привет'):
        name =''
        if message.author.nick == None:
            name = message.author.display_name
        else:
            name = message.author.nick

        roles = ''
        for r in message.author.roles:
            if r.name != '@everyone':
                if roles != '':
                    roles += ', '
                roles += r.name

        if roles == '':
            roles = 'по жизни никто'
        await message.channel.send('{}, здарова, заебал!\n'
                                   'Ты оказывается у наc еще {}'.format(name,roles))

    if message.content.startswith('!анекдот'):
        await message.channel.send(anekdot(message))

    if message.content.startswith('!лучший'):
        await message.channel.send(anekdot(message))

    if message.content.startswith('!рандом'):
        a = 1
        b = 100
        if len(message.content.split(' ')) == 3:
            a = int(message.content.split(' ')[1])
            b = int(message.content.split(' ')[2])
        await message.channel.send(random.randint(a,b))

    if message.content.startswith('!помощь'):
        ansv = 'Я могу:\n' \
               '!привет |Поприветствовать тебя\n' \
               '!анекдот [год] [месяц(цифра)] [номер(1-12)]  |Найти анекдот \n' \
               '!рандом [n1] [n2] | Случайное число от числе n1 до n2 включительно'
        await message.channel.send(ansv)

if not local:
    TOKEN = os.environ['TOKEN']
else:
    f = open("loacltoken.txt", "r")
    TOKEN = f.read()

client.run(TOKEN)
