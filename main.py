from keep_alive import keep_alive
import os
import requests
import json
import datetime
from random import randint
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file

import discord

bot = discord.Bot()

"""
weather_token = os.environ['WEATHER_API_KEY']
"""
    
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")
  await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='BobBot | /help | /Bob')
    )  #Bot status, change this to anything you like
  print("Bot online")  #will print "bot online" in the console when the bot is online


#Send message "pong" when user sends /ping
@bot.slash_command(name="bob", description="BobBot is here!")
async def bob(ctx):
    await ctx.respond(content="Hi! I'm still here")

@bot.slash_command(name="ping", description=":-)")
async def Bob(ctx):
    await ctx.respond(content="pong!")

# Space given text by user
@bot.slash_command(name="fact", description="Make me say a cool fact")
async def fact(ctx):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    facttoken = os.getenv('ninjatoken')
    response = requests.get(api_url, headers={'X-Api-Key': facttoken})
    if response.status_code == requests.codes.ok:
        original = response.text
        parsed = original.replace('''[{"fact": "''', "")
        original = parsed
        parsed = original.replace('''"}]''', "")
        embed = discord.Embed(title="Your cool fact",
                              color=0xebb907,
                              timestamp=datetime.datetime.now(),
                              description=parsed)
        embed.set_author(
            name="BobBot's FACTS",
            icon_url=
            '''https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L'''
        )
        embed.set_footer(text="That was cool, right???")
        await ctx.respond(embed=embed)
        chance = randint(1, 4)
        if chance == 2:
            await ctx.respond("*What???*")
    else:
        await ctx.respond("Error:", response.status_code, response.text)


@bot.slash_command(name="joke", description="Gimme a joke man")
async def joke(ctx):
    facttoken = os.getenv('ninjatoken')
    response = requests.get('https://api.api-ninjas.com/v1/jokes?limit=1',
                            headers={'X-Api-Key': facttoken})
    original = response.text
    parsed = original.replace('''[{"joke": "''', " ")
    original = parsed
    parsed = original.replace('''"}]''', "")
    original = parsed.replace("\n\n", "")
    embed = discord.Embed(title="Your joke",
                          color=0xebb907,
                          timestamp=datetime.datetime.now(),
                          description=original)
    embed.set_author(
        name="BobBot's jokes",
        icon_url=
        "https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L"
    )
    embed.set_footer(text="😬 You cringed, right?")
    await ctx.respond(embed=embed)


@bot.slash_command(name="quote", description="A cool Zen quote")
async def quote(ctx):
    response = requests.get("https://zenquotes.io/api/random/")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    author = json_data[0]['a']
    embed = discord.Embed(title="Your quote.",
                          color=0xebb907,
                          timestamp=datetime.datetime.now())
    embed.set_author(
        name="BobBot's Zen Quotes",
        icon_url=
        '''https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L'''
    )
    embed.add_field(name=f"**'{quote}'**", value=f"- {author}", inline=False)
    embed.set_footer(text="Hey, like a good quote!")
    await ctx.respond(embed=embed)


@bot.slash_command(name="help", description="When all else fails")
async def help(ctx):
    embed = discord.Embed(title="Help:",
                          description='Stop it, get some help',
                          timestamp=datetime.datetime.now(),
                          color=0xebb907)
    embed.set_author(
        name="BobBot Help",
        icon_url=
        "https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L"
    )
    embed.add_field(name="/help",
                    value="Displays this help menu.",
                    inline=False)
    embed.add_field(name="/Bob", value="Tests BobBot.", inline=False)
    embed.add_field(name="/quote", value="Gives you a quote.", inline=False)
    embed.add_field(name="/fact",
                    value="Gives out a very cool fact.",
                    inline=False)
    embed.add_field(name="/joke",
                    value="Gives out a very lame joke.",
                    inline=False)
    chance = randint(1, 4)
    if chance == 1:
        text = "🤔 What is the meaning of life?"
    elif chance == 2:
        text = "plz help me...i need help plzz 😭"
    else:
        text = "Stop it, get some help"
    embed.set_footer(text=text)
    await ctx.respond(embed=embed)


"""
@bot.slash_command(name="weather", description="Find the weather in a certain place")
async def weather(ctx, place: discord.Option(str)):
  response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/london?unitGroup=metric&include=days&key=52ZZPYY6U92CNSYCA5PFC7872&contentType=json")
  jsonData = response.json()
  address = jsonData["resolvedAddress"]
  desc = jsonData["days"][0]["description"]
  title = f"Weather in {address}"
  temp = jsonData["days"][0]["temp"]
  tempmax = jsonData["days"][0]["tempmax"]
  tempmin = jsonData["days"][0]["tempmin"]
  feelslike = jsonData["days"][0]["feelslike"]
  percip = jsonData["days"][0]["precipprob"]
  cond = jsonData["days"][0]["conditions"]
  sunset = jsonData["days"][0]["sunset"]
  sunrise = jsonData["days"][0]["sunrise"]
  embed = discord.Embed(title=title,
                             description=desc,
                          timestamp=datetime.datetime.now(),
                          color=0xebb907)
  embed.set_author(
        name="BobBot Weather",
        icon_url=
        "https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L"
  )
  if response.status_code!=200:
    embed.add_field(name="Error:",
                    value=f"Unexpected response: {response.status_code}", inline = False)
  else:
    embed.add_field(name="Today:",
                    value=f"Weather today: {cond} with a {percip}% chance of rain. Highs at {tempmax} degrees Celcius with a low of {tempmin} degrees with an average of {temp}. Feels like {feelslike} degrees. Sunset at {sunset} and sunrise at {sunrise}.", inline = False)
  
"""

#Run our webserver, this is what we will ping

keep_alive()

#Run our bot

token = os.getenv("discordtoken")
bot.run(token)
