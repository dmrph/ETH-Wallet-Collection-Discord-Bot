'''
extract users text and discord user name from specified channel into txt or csv

wallet collection
'''
import discord
from discord.ext import commands
import os
from replit import db
import pandas as pd
import re

bot = commands.Bot(command_prefix="\\", description="Wallet Collection")

time_to_delete = 5

def is_valid_address(address):
  """
  Identifies if the inputted address matches 
  the properties of an Ethereum wallet address

  Parameters
  ----------
  address (str): contains the proposed address

  Return
  ------
  True if the address matches the properties.
  False, otherwise.
  """
  res = False
  reg = r'0x[a-fA-F0-9]{40}$'
  if re.match(reg, address):
    res = True
  return res

@bot.event
async def on_ready():
  print("Ready!")

@bot.command(pass_context = True)
async def wallet(ctx, *arg):
  # Check is valid input
  error_msg = f'Hello {ctx.author}! Please send a correct ETH address. Ex: 0xAd5b1dC1F4fb668F476b22E8525c4583bc499F35'
  if len(arg) == 1:
    if is_valid_address(arg[0]):
      username = ctx.author
      if str(username) in db.keys():
        await ctx.send(f'Sneaky beaky, I got {ctx.author} trying to enter multiple addresses. Previous address overwritten 😈',  delete_after = time_to_delete)
      else: 
        await ctx.send(f'Thank you, {ctx.author}. Wallet accepted! Welcome to the WL 😊', delete_after = time_to_delete)
      wallet = arg[0]
      db[username] = wallet 
    else:
      await ctx.send(error_msg, delete_after=time_to_delete)
      
  # Return error message
  else:
    await ctx.send(error_msg, delete_after=time_to_delete)
  await ctx.message.delete()

## TODO: make list all wallets function
@bot.command()
async def list(ctx):
  embed = discord.Embed(title='WL Addresses', color=0xFF4533,timestamp=ctx.message.created_at)
  if db.keys():
    keys = db.keys()
    ## TODO: iterate through all the keys
    
    usernames = [username for username in keys]
    wallets = [db[username] for username in usernames]
    
    usernames = '\n'.join(usernames)
    wallets = '\n'.join(wallets)
    
    embed.add_field(name='Disc ID', value=usernames)
    embed.add_field(name='Address', value=wallets)
  
    print(pd.DataFrame(db))
  
    await ctx.send(embed=embed)
  else:
    await ctx.send('Database empty.', delete_after=time_to_delete)

@bot.command()
async def __clear_db(ctx):
  await ctx.message.delete()
  for key in db:
    del db[key]
  print('Deleted!')
  print(db)

@bot.command()
async def __csv(ctx):
  await ctx.message.delete()
  keys = db.keys()
  ## TODO: iterate through all the keys
  
  usernames = [username for username in keys]
  wallets = [db[username] for username in usernames]
  
  df = pd.DataFrame({'Username': usernames, 'Wallets': wallets})
  df.to_csv('wl.csv')

#tell users how to enter eth address into bot  
@bot.command()
async def __how(ctx):
  await ctx.message.delete()
  await ctx.send('Use \\\wallet + [Address] to enter your ETH address.')

  
token = os.environ['secret_token']
bot.run(token)