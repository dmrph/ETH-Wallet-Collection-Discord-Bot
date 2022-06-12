#!/usr/bin/env python

""" Discord Wallet Extraction Bot

extract users entered ethereum wallet address along wtih discord user name from specified channel intcsv

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Kevin Hoffman", "David Murphy"]
__contact__ = "kehoffman@ursinus.edu, djm7566@psu.edu"
__copyright__ = "Copyright $2022, $Murphy-Hoffman Inc."
__date__ = "06/05/2022"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"

import discord
from discord.ext import commands
import os
from replit import db
import pandas as pd
import re

bot = commands.Bot(command_prefix="\\", description="Wallet Collection")

time_to_delete = 5

#function to verify validity of address input into the bot
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

#command to add wallet address into database
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

#list all wallets function with corresponding discord IDs
@bot.command()
async def list(ctx):
  await ctx.message.delete()
  embed = discord.Embed(title='WL Addresses', color=0xFF4533,timestamp=ctx.message.created_at)
  if db.keys():
    keys = db.keys()
    ##iterate through all the keys
    
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

#command to clear the database, reports back to console when complete
@bot.command()
async def __clear_db(ctx):
  await ctx.message.delete()
  for key in db:
    del db[key]
  print('Deleted!')
  print(db)

#command to export data users have input into a CSV file, takes "wl" name paramater
@bot.command()
async def __csv(ctx, wl):
  await ctx.message.delete()
  keys = db.keys()
  ## TODO: iterate through all the keys
  
  usernames = [username for username in keys]
  wallets = [db[username] for username in usernames]
  
  df = pd.DataFrame({'Username': usernames, 'Wallets': wallets})
  df.to_csv(wl + ".csv")

#command to allow users to check if/what address they have stored in the DB
@bot.command()
async def check(ctx):
  await ctx.message.delete()
  keys = db.keys()
  username = ctx.author
  usernames = [username for username in keys]
  wallet = [db[username] for username in usernames]

  if str(username) in db.keys():
      print(username)
      await ctx.send(f'I have {ctx.author} with address {wallet}',delete_after=time_to_delete)
  else:
    await ctx.send(f'I do not have an address for {ctx.author}')

#tell users how to enter eth address into bot  
@bot.command()
async def __how(ctx):
  await ctx.message.delete()
  await ctx.send('Use "\\\wallet [ADDRESS]" to enter your ETH address. Ex: \\\wallet 0xAd5b1dC1F4fb668F476b22E8525c4583bc499F30')
  

token = os.environ['secret_token']
bot.run(token)