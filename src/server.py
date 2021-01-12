import json
from plaid import Client
from plaid.errors import APIError, ItemError
import discord
from discord.ext import commands



f = open("/keys/keys.json")
keys=json.load(f)
print(keys)
bot = commands.Bot(command_prefix='$')

@bot.command()
async def balance(ctx):
    #await ctx.channel.send("pong")
    #await ctx.channel.send(get_balance())
    client = Client(client_id=keys['PLAID-CLIENT-ID'],secret=keys['PLAID-SECRET'],environment='development')
    try:
        await ctx.channel.send('Looking that up..')
        response = client.Accounts.balance.get(keys['PLAID-ACCESS-TOKEN'])
        acc = response['accounts']
        print(acc)
        await ctx.channel.send("The balance of our %d accounts is"%(len(acc)))
        for a in acc:
            await ctx.channel.send("%s: %s"%( a['name'],str(a['balances']['available'])))
    except ItemError as e:
        await ctx.channel.send( "Error, Response: %s"%(e.code))
    except APIError as e:
        await ctx.channel.send( "API Error, Rssponse: %s"%(e.code))
    except requests.Timeout:
        await ctx.channel.send( "Timeout when connecting to Plaid API")


bot.run(keys['DISCORD-BOT-TOKEN'])
